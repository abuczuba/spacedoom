"""Pager tests never contact ntfy; lifecycle fixtures are explicitly synthetic."""
from email.header import decode_header, make_header
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from cdev_harness import CdevHarness
from activity_harness import dispatch, enable_driver

REPO = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pager = load('pager', REPO / 'configs/tmux/pager.py')
dashboard = load('dashboard_pager_test', REPO / 'configs/tmux/agent-dashboard.py')


class PagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='df-pager-', dir='/private/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.config = self.root / 'pager.json'
        self.config.write_text(json.dumps({'url': 'https://ntfy.invalid/fixture-only', 'token': 'fixture-token'}))
        self.config.chmod(0o600)
        self.project = self.root / 'project-one'
        self.project.mkdir()
        subprocess.run(['git', 'init', '-q', str(self.project)], check=True, capture_output=True)
        self.publisher = pager.Publisher(self.root / 'state', '/private/tmp/owned-test.sock', self.config)
        self.publisher.observe([], now=100, spawn=False)

    def pane(self, state='working', revision=1, turn='turn-one', stamp=101, agent='one'):
        return dict(track_id=hashlib.sha256(agent.encode()).hexdigest(), state=state, revision=revision,
                    turn=turn, stamp=stamp, project_dir=str(self.project))

    def ledger(self):
        return pager.private_json(self.publisher.path)

    def queue(self, state='done'):
        pane = self.pane(state)
        self.publisher.observe([pane], now=102, spawn=False)
        return pane

    def test_priorities_privacy_and_nonblocking_delivery_boundary(self):
        with patch.object(pager, 'build_opener') as opener:
            opener.return_value.open.return_value.__enter__.return_value.read.return_value = b'private-response'
            for state, priority, label in [('waiting', '4', 'Approval required'), ('done', '3', 'Review needed')]:
                self.assertEqual(pager.Ntfy(pager.configuration(self.config)).publish('project-one', state), ('sent', False))
                request = opener.return_value.open.call_args.args[0]
                self.assertEqual(request.headers['Priority'], priority)
                self.assertEqual(str(make_header(decode_header(request.headers['Title']))), 'Codex · project-one — ' + label)
                self.assertNotIn('\n', request.headers['Title'])
                self.assertNotIn(str(self.root).encode(), request.data)
                self.assertNotIn(b'success', request.data)
                self.assertEqual(opener.return_value.open.call_args.kwargs['timeout'], 3)
        with patch.object(pager.Ntfy, 'publish', side_effect=AssertionError('HTTP reached refresh')), patch.object(pager, 'project_label', return_value='project-one'), patch.object(pager.subprocess, 'Popen') as child:
            self.publisher.observe([self.pane('done')], now=102)
            child.assert_called_once()
            self.assertTrue(child.call_args.kwargs['start_new_session'])
            self.assertNotIn('fixture-token', str(child.call_args))
            self.assertNotIn('https://', str(child.call_args))

    def test_working_idle_unknown_silent_and_attention_deduplicated(self):
        for state in ('working', 'idle', 'unknown'):
            self.publisher.observe([self.pane(state)], now=102, spawn=False)
        self.assertEqual(self.ledger()['alerts'], {})
        waiting = self.pane('waiting', revision=2)
        self.publisher.observe([waiting], now=102, spawn=False)
        self.publisher.observe([waiting | {'revision': 3}], now=103, spawn=False)
        self.assertEqual(len(self.ledger()['alerts']), 1)
        self.publisher.observe([self.pane('done', revision=4)], now=104, spawn=False)
        alerts = list(self.ledger()['alerts'].values())
        self.assertEqual([a['status'] for a in alerts], ['expired', 'pending'])

    def test_concurrent_agents_keep_independent_identity_and_queue(self):
        panes = [self.pane('done', agent='a'), self.pane('waiting', agent='b')]
        self.publisher.observe(panes, now=102, spawn=False)
        transport = Mock()
        transport.publish.return_value = ('sent', False)
        self.publisher.drain(snapshot=lambda: panes, transport=transport, now=lambda: 103)
        self.assertEqual(transport.publish.call_count, 2)
        self.assertEqual({a['agent'] for a in self.ledger()['alerts'].values()}, {p['track_id'] for p in panes})
        self.assertEqual({a['status'] for a in self.ledger()['alerts'].values()}, {'sent'})

    def test_initial_stopped_snapshot_and_worker_restart_never_replay_history(self):
        self.publisher.path.unlink()
        pane = self.pane('done', stamp=101)
        self.publisher.observe([pane], now=102, spawn=False)
        self.assertEqual(self.ledger()['alerts'], {})
        restarted = pager.Publisher(self.root / 'state', self.publisher.socket, self.config)
        restarted.observe([pane | {'revision': 9}], now=103, spawn=False)
        self.assertEqual(self.ledger()['alerts'], {})
        restarted.observe([self.pane('working', turn='new', stamp=104)], now=104, spawn=False)
        stopped = self.pane('done', turn='new', revision=11, stamp=105)
        restarted.observe([stopped], now=105, spawn=False)
        transport = Mock(); transport.publish.return_value = ('sent', False)
        restarted.drain(snapshot=lambda: [stopped], transport=transport, now=lambda: 106)
        restarted.observe([stopped], now=107, spawn=False)
        restarted.drain(snapshot=lambda: [stopped], transport=transport, now=lambda: 107)
        self.assertEqual(transport.publish.call_count, 1)

    def test_rejections_retry_bounded_but_uncertain_delivery_does_not(self):
        pane = self.queue()
        transport = Mock(); transport.publish.side_effect = [('rejected', True), ('sent', False)]
        sleep = Mock()
        self.publisher.drain(snapshot=lambda: [pane], transport=transport, sleep=sleep, now=lambda: 103)
        self.assertEqual(transport.publish.call_count, 2)
        self.assertEqual(next(iter(self.ledger()['alerts'].values()))['attempts'], 2)
        newer = self.pane('done', turn='new', revision=3, stamp=104)
        self.publisher.observe([newer], now=105, spawn=False)
        transport.publish.side_effect = None; transport.publish.return_value = ('uncertain', False)
        self.publisher.drain(snapshot=lambda: [newer], transport=transport, now=lambda: 106)
        self.assertEqual(transport.publish.call_count, 3)
        self.publisher.drain(snapshot=lambda: [newer], transport=transport, now=lambda: 106)
        self.assertEqual(transport.publish.call_count, 3)

    def test_interrupted_worker_does_not_republish_an_inflight_request(self):
        self.queue()
        ledger = self.ledger()
        next(iter(ledger['alerts'].values()))['status'] = 'inflight'
        pager.save(self.publisher.path, ledger)
        transport = Mock()
        self.publisher.drain(snapshot=lambda: [], transport=transport, now=lambda: 103)
        transport.publish.assert_not_called()
        self.assertEqual(next(iter(self.ledger()['alerts'].values()))['status'], 'uncertain')

    def test_terminated_or_stale_agents_expire_without_network(self):
        self.queue()
        transport = Mock()
        self.publisher.drain(snapshot=lambda: [], transport=transport, now=lambda: 103)
        transport.publish.assert_not_called()
        self.assertEqual(next(iter(self.ledger()['alerts'].values()))['status'], 'expired')
        self.publisher.observe([self.pane('waiting', turn='old', stamp=1)], now=500, spawn=False)
        self.assertEqual(len(self.ledger()['alerts']), 1)

    def test_unsafe_or_disabled_configuration_never_spawns(self):
        self.config.chmod(0o644)
        with self.assertRaises(ValueError):
            self.publisher.observe([self.pane('done')], now=102)
        self.config.chmod(0o600)
        self.config.write_text(json.dumps({'enabled': False}))
        with patch.object(pager.subprocess, 'Popen') as child:
            self.publisher.observe([self.pane('done')], now=102)
            child.assert_not_called()
        self.config.unlink()
        self.config.symlink_to(self.publisher.path)
        with self.assertRaises(OSError):
            pager.configuration(self.config)

    def test_network_failures_and_redirects_do_not_leak_credentials(self):
        config = pager.configuration(self.config)
        transport = pager.Ntfy(config)
        with patch.object(pager, 'build_opener') as opener:
            opener.return_value.open.side_effect = URLError(ConnectionRefusedError())
            self.assertEqual(transport.publish('project-one', 'done'), ('unavailable', True))
            opener.return_value.open.side_effect = TimeoutError()
            self.assertEqual(transport.publish('project-one', 'done'), ('uncertain', False))
            opener.return_value.open.side_effect = HTTPError(config['url'], 302, 'redirect', {}, None)
            self.assertEqual(transport.publish('project-one', 'done'), ('rejected', False))
        self.assertIsNone(pager.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://elsewhere.invalid'))
        with self.assertRaises(ValueError):
            transport.publish('/absolute/private/path', 'done')

    def test_disable_preserves_private_destination_and_does_not_call_transport(self):
        before = pager.private_json(self.config)
        with patch('sys.argv', ['pager.py', 'disable', '--config', str(self.config), '--approve']), patch('sys.stdout', new_callable=io.StringIO), patch.object(pager.Ntfy, 'publish') as transport:
            self.assertEqual(pager.main(), 0)
        self.assertEqual(pager.private_json(self.config), before | {'enabled': False})
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o600)
        transport.assert_not_called()


@unittest.skipUnless(os.environ.get('DOTFILES_INTEGRATION') == '1', 'Private tmux + synthetic lifecycle fixture')
class PagerIntegration(unittest.TestCase):
    def test_ordinary_cdev_source_reuse_moves_and_termination(self):
        h = CdevHarness(); self.addCleanup(h.close)
        enable_driver(h)
        config = h.root / 'pager.json'
        config.write_text(json.dumps({'url': 'https://ntfy.invalid/fixture-only'})); config.chmod(0o600)
        roots = [h.repo('pager-a'), h.repo('pager-b')]
        panes = []
        for index, root in enumerate(roots):
            h.saved(root)
            result = h.cdev(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            pane = h.tm('list-panes', '-t', h.window(root), '-F', '#{pane_id}').splitlines()[1]
            panes.append(pane)
            dispatch(h, pane, event='UserPromptSubmit', session='session-' + str(index))
        view = dashboard.Dashboard(h.socket, state=h.env['XDG_STATE_HOME'])
        publisher = pager.Publisher(h.env['XDG_STATE_HOME'], h.socket, config)
        publisher.observe([], now=int(time.time()) - 2, spawn=False)
        self.assertEqual(len(view.snapshot()), 2)
        publisher.observe(view.snapshot(), spawn=False)
        for index, pane in enumerate(panes):
            dispatch(h, pane, event='Stop', session='session-' + str(index))
        observed = view.snapshot()
        publisher.observe(observed, spawn=False)
        ids = {p['pane']: p['track_id'] for p in observed}
        h.tm('swap-window', '-s', h.window(roots[0]), '-t', h.window(roots[1]))
        h.tm('rename-window', '-t', h.window(roots[0]), 'changed-title')
        self.assertEqual({p['pane']: p['track_id'] for p in view.snapshot()}, ids)
        publisher.observe(view.snapshot(), spawn=False)
        self.assertEqual(len(pager.private_json(publisher.path)['alerts']), 2)
        previous = h.snapshot(), h.log()
        self.assertEqual(h.cdev(roots[0]).returncode, 0)
        self.assertEqual((h.snapshot(), h.log()), previous)
        transport = Mock(); transport.publish.return_value = ('sent', False)
        publisher.drain(snapshot=view.snapshot, transport=transport)
        self.assertEqual({call.args[0] for call in transport.publish.call_args_list}, {'pager-a', 'pager-b'})
        for root in roots:
            h.tm('kill-window', '-t', h.window(root))
        self.assertEqual(view.snapshot(), [])
