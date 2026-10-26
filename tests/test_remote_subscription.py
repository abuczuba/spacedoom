"""Remote hook ownership and transport cleanup; no live server or Codex process."""
import base64
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import struct
import sys
import tempfile
import threading
import types
import unittest
from unittest.mock import Mock, patch


SPEC = importlib.util.spec_from_file_location(
    'subscription_cdev', Path(__file__).resolve().parents[1] / 'configs/cdev/codex_session.py')
cdev = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cdev)


class RemoteSubscriptionTests(unittest.TestCase):
    def test_setup_subscription_outlives_child_and_closes_after_finalization(self):
        for outcome in ('normal', 'spawn-error', 'interrupt', 'setup-error'):
            with self.subTest(outcome=outcome):
                events, live = [], []
                observer = Mock()
                observer.environment.return_value = {}
                observer.config_args.return_value = []
                observer.definition_config.return_value = {'hooks.Stop': []}
                observer.finish.side_effect = lambda: events.append('finish')
                connection = Mock()
                connection.getsockopt.return_value = 77

                def rpc(*args):
                    events.append('setup')
                    if outcome == 'setup-error':
                        raise cdev.CdevError('unavailable')

                @contextlib.contextmanager
                def server(*args, **kwargs):
                    live.append(True)
                    events.append('open')
                    try:
                        yield rpc, connection
                    finally:
                        live.pop()
                        events.append('close')

                def spawn(*args, **kwargs):
                    # Reproduces 0.164: a closed prewarm loses invocation hooks
                    # before the new TUI subscribes, even with a live registration.
                    self.assertEqual(bool(live), outcome != 'setup-error')
                    events.append('spawn')
                    if outcome == 'spawn-error':
                        raise OSError('owned fixture could not start')
                    child = Mock(pid=34)
                    def wait():
                        self.assertEqual(bool(live), outcome != 'setup-error')
                        events.append('wait')
                        if outcome == 'interrupt':
                            raise KeyboardInterrupt
                        return 0
                    child.wait.side_effect = wait
                    return child

                with patch.dict(os.environ, CDEV_DASHBOARD='1', TMUX='private,1,0', TMUX_PANE='%1'), \
                        patch.dict(sys.modules, activity=types.SimpleNamespace(Launch=Mock(return_value=observer))), \
                        patch.object(cdev, 'plan', return_value={'mode': 'pinned', 'session': 'exact-uuid'}), \
                        patch.object(cdev, 'resume_transport', return_value=['--remote', 'unix:///private/tmp/owned.sock']), \
                        patch.object(cdev, 'server_connection', side_effect=server) as connect, \
                        patch.object(cdev.subprocess, 'check_output', return_value='/private/tmp/owned-tmux.sock\n'), \
                        patch.object(cdev.subprocess, 'Popen', side_effect=spawn), \
                        patch.object(cdev, 'report_launch_error'), \
                        patch.object(cdev.sys, 'platform', 'darwin'):
                    self.assertEqual(cdev.launch(Path('/private/tmp/project'), '/owned/codex'),
                                     {'spawn-error': 1, 'interrupt': 130}.get(outcome, 0))
                self.assertFalse(live)
                self.assertEqual(events.count('close'), 1)
                connect.assert_called_once_with(Path('/private/tmp/owned.sock'), retain=True, on_message=observer.approval)
                if outcome != 'setup-error':
                    self.assertGreater(events.index('close'), events.index('finish'))
                    if outcome != 'spawn-error':
                        observer.attach.assert_called_once()
                    else:
                        observer.attach.assert_not_called()

    def test_fresh_launch_does_not_open_a_remote_subscription(self):
        with patch.dict(os.environ, CDEV_DASHBOARD='0'), \
                patch.object(cdev, 'plan', return_value={'mode': 'fresh', 'session': None}), \
                patch.object(cdev, 'server_connection') as connect, \
                patch.object(cdev.subprocess, 'Popen') as spawn:
            spawn.return_value.wait.return_value = 0
            self.assertEqual(cdev.launch(Path('/private/tmp/project'), '/owned/codex'), 0)
        connect.assert_not_called()
        self.assertEqual(spawn.call_args.args[0], ['/owned/codex', '--cd', '/private/tmp/project'])

    def websocket_case(self, close_from_peer, stalled=False, callback=None):
        before_fds = set(os.listdir('/dev/fd'))
        with tempfile.TemporaryDirectory(prefix='df-remote-subscription-', dir='/private/tmp') as temp:
            endpoint = Path(temp) / 'peer.sock'
            heartbeat, closed, errors = threading.Event(), threading.Event(), []
            def frame(opcode, body, final=True):
                length = len(body)
                size = bytes([length]) if length < 126 else b'\x7f' + struct.pack('!Q', length)
                return bytes([opcode | (0x80 if final else 0)]) + size + body

            def serve(listener):
                try:
                    client, _ = listener.accept()
                    with client, client.makefile('rb') as stream:
                        client.settimeout(3)
                        headers = {}
                        self.assertEqual(stream.readline(), b'GET / HTTP/1.1\r\n')
                        while True:
                            line = stream.readline()
                            if line == b'\r\n':
                                break
                            key, value = line.decode().split(':', 1)
                            headers[key.lower()] = value.strip()
                        accept = base64.b64encode(hashlib.sha1((headers['sec-websocket-key'] +
                            '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
                        client.sendall(('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n'
                                        'Connection: Upgrade\r\nSec-WebSocket-Accept: ' + accept + '\r\n\r\n').encode())
                        def receive():
                            header = stream.read(2)
                            if not header:
                                return None
                            first, second = header
                            length = second & 127
                            if length in (126, 127):
                                length = int.from_bytes(stream.read(2 if length == 126 else 8), 'big')
                            mask, body = stream.read(4), stream.read(length)
                            return first & 15, bytes(c ^ mask[i % 4] for i, c in enumerate(body))
                        for method in ('initialize', 'initialized', 'thread/resume'):
                            _, body = receive()
                            row = json.loads(body)
                            self.assertEqual(row['method'], method)
                            if 'id' in row:
                                client.sendall(frame(1, json.dumps({'id': row['id'], 'result': {}}).encode()))
                        if stalled:
                            # Exit must unblock a reader waiting for the rest of
                            # a frame, rather than leave a thread/socket alive.
                            client.sendall(b'\x81\x7f' + struct.pack('!Q', 1048576) + b'x')
                            heartbeat.set()
                            self.assertIsNone(receive())
                        else:
                            if callback is not None:
                                for identity in (1, 2):
                                    body = json.dumps({'method':'serverRequest/resolved',
                                        'params':{'threadId':'fixture','requestId':identity}}).encode()
                                    client.sendall(frame(1, body[:12], final=False))
                                    client.sendall(frame(0, body[12:]))
                            # Data is discarded, never decoded as lifecycle text.
                            client.sendall(frame(1, b'not-json' * 140000, final=False))
                            client.sendall(frame(0, b'ignored fragment'))
                            client.sendall(frame(9, b'ping'))
                            self.assertEqual(receive(), (10, b'ping'))
                            heartbeat.set()
                            if close_from_peer:
                                client.sendall(frame(8, b''))
                            else:
                                self.assertIsNone(receive())
                except BaseException as error:
                    errors.append(error)
                finally:
                    closed.set()

            before = {t.ident for t in threading.enumerate() if t.name == 'cdev-hook-subscription'}
            with socket.socket(socket.AF_UNIX) as listener:
                listener.bind(str(endpoint))
                listener.listen(1)
                peer = threading.Thread(target=serve, args=(listener,), daemon=True)
                peer.start()
                try:
                    with cdev.server_connection(endpoint, retain=True, on_message=callback) as (request, _):
                        request(2, 'thread/resume', {'threadId': 'fixture', 'excludeTurns': True})
                        self.assertTrue(heartbeat.wait(3), errors)
                        if close_from_peer:
                            self.assertTrue(closed.wait(3))
                        with self.assertRaisesRegex(cdev.CdevError, 'cannot issue further RPCs'):
                            request(3, 'thread/resume', {})
                finally:
                    peer.join(timeout=4)
                self.assertFalse(peer.is_alive())
            self.assertEqual(errors, [])
            self.assertTrue(closed.is_set())
            self.assertEqual({t.ident for t in threading.enumerate() if t.name == 'cdev-hook-subscription'}, before)
        self.assertEqual(set(os.listdir('/dev/fd')), before_fds)

    def test_retained_transport_drains_without_parsing_and_closes_cleanly(self):
        self.websocket_case(close_from_peer=False)

    def test_backend_eof_is_advisory_and_does_not_leak_a_reader(self):
        self.websocket_case(close_from_peer=True)

    def test_exit_unblocks_partial_frame_without_socket_or_reader_leaks(self):
        self.websocket_case(close_from_peer=False, stalled=True)

    def test_fragmented_approval_messages_and_callback_failure_preserve_transport(self):
        observed=[]
        def callback(row):
            observed.append(row)
            if row['params']['requestId']==1:
                raise RuntimeError('advisory callback unavailable')
        self.websocket_case(close_from_peer=False, callback=callback)
        self.assertEqual([r['params']['requestId'] for r in observed],[1,2])


if __name__ == '__main__':
    unittest.main()
