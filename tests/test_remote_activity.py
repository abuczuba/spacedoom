"""Focused shared-server registration tests; real CLI acceptance is separate."""
import contextlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
import uuid
import sys


ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


activity = module('remote_activity', 'configs/cdev/activity.py')
cdev = module('remote_cdev', 'configs/cdev/codex_session.py')


class RemoteActivityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='df-remote-registration-', dir='/private/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.registry = patch.object(activity, 'REMOTE_DIRECTORY', self.root / 'registry')
        self.registry.start()
        self.addCleanup(self.registry.stop)

    def launch(self, pane, pid, session):
        launch = activity.Launch(self.root / 'state', '/private/tmp/fixture.sock', pane)
        launch.started = 'launcher-' + str(pid)
        record = dict(pid=pid, started=launch.started, token=launch.token,
                      socket=launch.socket, pane=pane, boot='1:22', child=pid + 1,
                      child_started='child-' + str(pid + 1), state='idle', session=None,
                      turn=None, ended=False, stamp=0, sequence=0)
        activity.save(launch.path, record)
        # environment() describes the actual launcher PID. Override it only in
        # this unit fixture so different mock launchers have distinct identities.
        launch.environment = lambda: {activity.CONTEXT_ENV: json.dumps({
            'version': 1, 'pid': pid, 'started': launch.started, 'token': launch.token,
            'state': launch.state, 'socket': launch.socket, 'pane': pane})}
        with patch.object(activity, 'process_identity', return_value={
                'parent': 1, 'started': 'backend', 'command': 'codex'}):
            launch.remote(session, 77)
        return launch

    def test_stable_native_definitions_are_the_only_remote_overrides(self):
        launch = activity.Launch(self.root, '/private/tmp/test.sock', '%1')
        adapter = self.root / 'activity.py'
        config = launch.definition_config(adapter)
        self.assertEqual(set(config), {'hooks.' + event for event in activity.EVENTS})
        for value in config.values():
            handler = value[0]['hooks'][0]
            self.assertEqual(handler['timeout'], 2)
            self.assertIn(json.dumps(handler['command']), launch.config_args(adapter)[1])
            self.assertNotIn(launch.token, handler['command'])
        request, connection, observer = Mock(), Mock(), Mock()
        connection.getsockopt.return_value = 77
        observer.definition_config.return_value = config
        with patch.object(cdev, 'server_connection', return_value=contextlib.nullcontext((request, connection))), \
                patch.object(cdev.sys, 'platform', 'darwin'):
            cdev.configure_remote_activity(Path('/private/tmp/test.sock'), 'uuid', self.root, observer, adapter)
        connection.getsockopt.assert_called_once_with(0, 2)
        observer.remote.assert_called_once_with('uuid', 77)
        request.assert_called_once_with(2, 'thread/resume', {
            'threadId': 'uuid', 'cwd': str(self.root), 'excludeTurns': True, 'config': config})

    def test_remote_origin_requires_peer_birth_live_frontend_and_launcher(self):
        session = str(uuid.uuid4())
        launch = self.launch('%1', 33, session)
        record = activity.private_record(launch.path)
        context = json.loads(launch.environment()[activity.CONTEXT_ENV])
        identities = {
            33: {'started': 'launcher-33', 'parent': 1, 'command': 'Python'},
            34: {'started': 'child-34', 'parent': 33, 'command': 'codex'},
            55: {'started': 'hook-shell', 'parent': 77, 'command': 'sh'},
            77: {'started': 'backend', 'parent': 1, 'command': 'codex'},
        }
        with patch.object(activity.os, 'getppid', return_value=55), \
                patch.object(activity, 'process_identity', side_effect=identities.__getitem__):
            self.assertTrue(activity.verified_origin(context, record))
            for pid, field, wrong in [(33, 'started', 'reused'), (34, 'started', 'reused'),
                                      (34, 'parent', 99), (77, 'started', 'reused'),
                                      (55, 'command', 'codex')]:
                old = identities[pid][field]
                identities[pid][field] = wrong
                self.assertFalse(activity.verified_origin(context, record))
                identities[pid][field] = old

    def test_concurrent_sessions_use_uuid_and_pane_not_cwd_titles_or_numbers(self):
        sessions = [str(uuid.uuid4()), str(uuid.uuid4())]
        launches = [self.launch('%1', 33, sessions[0]), self.launch('%9', 66, sessions[1])]
        contexts = [activity.remote_context({'session_id': sid}) for sid in sessions]
        self.assertNotEqual(contexts[0]['token'], contexts[1]['token'])
        for index, launch in enumerate(launches):
            with patch.object(activity, 'verified_origin', return_value=True), \
                    patch.object(activity, 'tmux', return_value='1:22|' + str([33, 66][index])), \
                    patch.object(activity, 'mark'):
                payload = {'session_id': sessions[index], 'turn_id': 'turn-' + str(index),
                           'hook_event_name': 'UserPromptSubmit'}
                activity.event(contexts[index], payload)
                payload['hook_event_name'] = 'Stop'
                activity.event(contexts[index], payload)
                before = launch.path.read_bytes()
                activity.event(contexts[index], payload | {'session_id': sessions[1-index]})
                self.assertEqual(launch.path.read_bytes(), before)
            self.assertEqual(activity.private_record(launch.path)['state'], 'done')
            self.assertEqual(launch.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(activity.REMOTE_DIRECTORY.stat().st_mode & 0o777, 0o700)

    def test_duplicate_registration_stale_turns_exit_and_repeat_finish(self):
        session = str(uuid.uuid4())
        first = self.launch('%1', 33, session)
        context = activity.remote_context({'session_id': session})
        with patch.object(activity, 'verified_origin', return_value=True), \
                patch.object(activity, 'tmux', return_value='1:22|33'), patch.object(activity, 'mark'):
            for name in ['UserPromptSubmit', 'Stop']:
                activity.event(context, {'session_id': session, 'turn_id': 'old-turn', 'hook_event_name': name})
            first.finish()
            first.finish()
        self.assertIsNone(activity.remote_context({'session_id': session}))
        second = self.launch('%99', 66, session)
        row = activity.private_record(second.path)
        self.assertIn('old-turn', row['retired'])
        self.assertIsNone(activity.transition(row, {
            'session_id': session, 'turn_id': 'old-turn', 'hook_event_name': 'UserPromptSubmit'}, 100))
        with patch.object(activity, 'process_identity', side_effect=lambda pid: {
                'started': 'launcher-66' if pid == 66 else 'backend', 'command': 'codex', 'parent': 1}):
            with self.assertRaisesRegex(ValueError, 'already has a live'):
                second.remote(session, 77)
        # A delayed finalizer cannot remove or end the new registration.
        with patch.object(activity, 'mark'):
            first.finish()
        self.assertEqual(activity.remote_context({'session_id': session})['token'], second.token)
        with patch.object(activity, 'process_identity', side_effect=ValueError('exited')):
            with self.assertRaises(ValueError):
                activity.verified_origin(activity.remote_context({'session_id': session}), row)

    def test_registry_rejects_paths_symlinks_and_nonprivate_permissions(self):
        for session in ['../../escape', 'not-a-uuid', None]:
            self.assertIsNone(activity.remote_context({'session_id': session}))
        session = str(uuid.uuid4())
        self.launch('%1', 33, session)
        path = activity.remote_path(session)
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        path.chmod(0o644)
        self.assertIsNone(activity.remote_context({'session_id': session}))
        path.unlink()
        path.symlink_to(self.root / 'unrelated')
        with self.assertRaises(OSError):
            activity.remote_context({'session_id': session})

    def test_remote_bridge_failure_leaves_one_usable_unlabelled_cli(self):
        observer = Mock()
        observer.config_args.return_value = ['-c', 'hooks.Stop=[]']
        selection = {'mode': 'pinned', 'session': str(uuid.uuid4())}
        transport = ['--remote', 'unix:///private/tmp/owned.sock']
        with patch.object(cdev, 'plan', return_value=selection), \
                patch.object(cdev, 'resume_transport', return_value=transport), \
                patch.object(cdev, 'configure_remote_activity', side_effect=cdev.CdevError('unavailable')), \
                patch.dict(sys.modules, {'activity': Mock(Launch=Mock(return_value=observer))}), \
                patch.dict(os.environ, {'TMUX': '/private/tmp/owned.sock,1,0', 'TMUX_PANE': '%1',
                                        'CDEV_DASHBOARD': '1', activity.CONTEXT_ENV: 'inherited'}), \
                patch.object(cdev.subprocess, 'check_output', return_value='/private/tmp/owned.sock\n'), \
                patch.object(cdev.subprocess, 'Popen') as child:
            child.return_value.wait.return_value = 0
            self.assertEqual(cdev.launch(self.root, '/owned/codex'), 0)
            self.assertEqual(child.call_args.args[0], [
                '/owned/codex', 'resume', selection['session'], '--cd', str(self.root), *transport])
            self.assertNotIn(activity.CONTEXT_ENV, child.call_args.kwargs['env'])
            observer.finish.assert_called_once()
            observer.attach.assert_not_called()


if __name__ == '__main__':
    unittest.main()
