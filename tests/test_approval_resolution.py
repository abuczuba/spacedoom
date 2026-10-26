"""Native approval IDs refine the existing hook state; never decide permissions."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('approval_activity',
    Path(__file__).resolve().parents[1] / 'configs/cdev/activity.py')
activity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(activity)


class ApprovalResolutionTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(token='launch-one', remote_session='session-one', session=None,
                           turn=None, state='idle', ended=False, sequence=0, stamp=0,
                           approval_stream=True)
        self.hook('UserPromptSubmit')

    def hook(self, event, **extra):
        result = activity.transition(self.record, dict(hook_event_name=event,
            session_id='session-one', turn_id='turn-one', tool_name='Bash') | extra, 1000)
        if result is not None:
            self.record = result
        return result

    def receive(self, method='item/commandExecution/requestApproval', identity=0, **extra):
        message = dict(method=method, params={'threadId':'session-one'} | extra)
        if method == 'serverRequest/resolved':
            message['params']['requestId'] = identity
        else:
            message['id'] = identity
            message['params'] = {'turnId':'turn-one', 'itemId':'exec-one'} | message['params']
        result = activity.approval_transition(self.record, message, 1001)
        if result is not None:
            self.record = result
        return result

    def test_real_0164_sequence_resolves_before_a_tool_result(self):
        # Sanitized shape/order observed from genuine Codex 0.164.0. The hook
        # has no tool_use_id; request/resolved supply the exact native RPC ID.
        self.hook('PreToolUse', tool_use_id='exec-one')
        self.hook('PermissionRequest')
        self.assertEqual(self.record['state'], 'working')
        self.receive()
        self.assertEqual(self.record['state'], 'waiting')
        self.receive('serverRequest/resolved')
        self.assertEqual(self.record['state'], 'working')
        self.assertEqual(self.record['pending'], [])
        self.hook('PermissionRequest')  # A delayed/duplicate hook cannot revive it.
        self.assertEqual(self.record['state'], 'working')
        self.hook('PostToolUse', tool_use_id='exec-one')
        self.hook('Stop')
        self.assertEqual(self.record['state'], 'done')

    def test_resolution_requires_no_tool_result_or_invented_decision(self):
        for method in sorted(activity.APPROVAL_REQUESTS):
            with self.subTest(method=method):
                self.setUp()
                self.receive(method)
                self.receive('serverRequest/resolved')
                self.assertEqual(self.record['state'], 'working')
                self.assertNotIn('decision', json.dumps(self.record))
                self.hook('Interrupt')
                self.assertEqual(self.record['state'], 'idle')

    def test_concurrent_requests_are_not_matched_by_tool_name_or_item_alone(self):
        self.receive(identity=1)
        self.receive(identity=2)  # Multiple callbacks can share an item ID.
        self.receive(identity=3, itemId='exec-two')
        before = json.dumps(self.record, sort_keys=True)
        self.assertIsNone(self.receive(identity=1))
        self.assertEqual(json.dumps(self.record, sort_keys=True), before)
        self.hook('PostToolUse', tool_use_id='exec-one')
        self.assertEqual(len(self.record['pending']), 3)
        self.receive('serverRequest/resolved', identity=2)
        self.receive('serverRequest/resolved', identity=1)
        self.assertEqual(self.record['state'], 'waiting')
        self.receive('serverRequest/resolved', identity=3)
        self.assertEqual(self.record['state'], 'working')

    def test_out_of_order_and_duplicate_resolutions_are_tombstoned(self):
        self.receive('serverRequest/resolved', identity=7)
        self.assertIsNone(self.receive(identity=7))
        self.assertIsNone(self.receive('serverRequest/resolved', identity=7))
        self.assertEqual(self.record['state'], 'working')
        self.receive(identity=8)
        self.receive('serverRequest/resolved', identity=99)
        self.assertEqual(self.record['pending'], ['8'])
        self.assertEqual(self.record['state'], 'waiting')

    def test_retired_turn_and_foreign_session_cannot_clear_a_new_request(self):
        self.receive(identity=1)
        self.hook('UserPromptSubmit', turn_id='turn-two')
        self.receive(identity=2, turnId='turn-two')
        self.receive('serverRequest/resolved', identity=1)
        self.assertEqual(self.record['pending'], ['2'])
        for extra in [dict(threadId='other'), dict(turnId='turn-one')]:
            self.assertIsNone(self.receive(identity=3, **extra))
        self.assertEqual(self.record['pending'], ['2'])
        self.hook('Stop', turn_id='turn-two')
        self.assertIsNone(self.receive('serverRequest/resolved', identity=2))
        self.assertEqual(self.record['state'], 'done')

    def test_request_id_types_and_metadata_only_cache(self):
        self.receive(identity=0, command='PRIVATE TOOL DATA', reason='PRIVATE REASON')
        self.receive(identity='0', itemId='exec-two')
        self.receive('serverRequest/resolved', identity=0)
        self.assertEqual(self.record['pending'], ['"0"'])
        self.assertIsNone(self.receive(identity=False))
        self.assertNotIn('PRIVATE', json.dumps(self.record))

    def test_live_requests_survive_bounded_resolution_tombstones(self):
        for identity in range(70):
            self.receive(identity=identity, itemId='exec-'+str(identity))
        for identity in range(100, 200):
            self.receive('serverRequest/resolved', identity=identity)
        self.assertEqual(len(self.record['pending']), 70)
        self.assertEqual(sum(v.get('resolved',False) for v in self.record['approvals'].values()),64)
        for identity in range(70):
            self.receive('serverRequest/resolved', identity=identity)
        self.assertEqual(self.record['state'],'working')
        self.assertIsNone(self.receive(identity=69,itemId='exec-69'))

    def test_unrelated_stream_messages_do_not_read_state_or_spawn_processes(self):
        with tempfile.TemporaryDirectory(prefix='df-permission-fast-') as directory:
            launch=activity.Launch(Path(directory).resolve(),'/private/tmp/owned.sock','%9')
            with patch.object(activity,'private_record') as read, \
                 patch.object(activity,'process_identity') as process, patch.object(activity,'tmux') as tmux:
                for method in ['item/agentMessage/delta','thread/status/changed','turn/completed']:
                    launch.approval(dict(method=method,params={'text':'NOT LIFECYCLE EVIDENCE'}))
                read.assert_not_called()
                process.assert_not_called()
                tmux.assert_not_called()

    def test_callback_revalidates_launch_child_backend_and_pane_generations(self):
        with tempfile.TemporaryDirectory(prefix='df-permission-origin-') as directory:
            launch = activity.Launch(Path(directory).resolve(), '/private/tmp/owned.sock', '%9')
            launch.started = 'launcher-start'
            launch.remote_session, launch.backend, launch.backend_started = 'session-one', 77, 'backend-start'
            original = self.record | dict(token=launch.token, pid=os.getpid(), started=launch.started,
                child=88, child_started='child-start', backend=77, backend_started='backend-start', boot='boot')
            identities = {os.getpid():dict(started=launch.started),
                88:dict(parent=os.getpid(),started='child-start',command='codex'),
                77:dict(started='backend-start',command='codex')}
            message = dict(method='item/commandExecution/requestApproval',id=0,
                params=dict(threadId='session-one',turnId='turn-one',itemId='exec-one'))
            for drift in ['none','token','launcher','child','child-parent','backend','pane','ended','terminated']:
                with self.subTest(drift=drift):
                    activity.save(launch.path, original)
                    changed = {k:dict(v) for k,v in identities.items()}
                    if drift in {'launcher','child','backend'}:
                        changed[{'launcher':os.getpid(),'child':88,'backend':77}[drift]]['started']='reused PID'
                    if drift=='child-parent':changed[88]['parent']=999
                    if drift=='terminated':del changed[88]
                    if drift=='token':activity.save(launch.path, original | dict(token='new-launch'))
                    if drift=='ended':activity.save(launch.path, original | dict(ended=True))
                    before=launch.path.read_bytes()
                    pane='wrong boot|123' if drift=='pane' else 'boot|'+str(os.getpid())
                    def identify(pid):
                        if pid not in changed:raise ValueError('process exited')
                        return changed[pid]
                    with patch.object(activity,'process_identity',side_effect=identify), \
                         patch.object(activity,'tmux',return_value=pane), patch.object(activity,'mark') as mark:
                        launch.approval(message)
                    if drift=='none':
                        self.assertEqual(activity.private_record(launch.path)['state'],'waiting')
                        mark.assert_called_once()
                    else:
                        self.assertEqual(launch.path.read_bytes(),before)
                        mark.assert_not_called()


if __name__=='__main__':
    unittest.main()
