"""Focused recovery tests: private metadata, owned locks and a local fake server."""
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import uuid


SPEC = importlib.util.spec_from_file_location(
    'codex_session', Path(__file__).resolve().parents[1] / 'configs/cdev/codex_session.py')
cdev = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cdev)


class CdevRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='df-cdev-recovery-', dir='/private/tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / 'codex'
        self.home.mkdir(mode=0o700)
        self.env = patch.dict(os.environ, CODEX_HOME=str(self.home), XDG_STATE_HOME=str(self.root / 'state'),
                              CDEV_DASHBOARD='0', TMUX='', TMUX_PANE='')
        self.env.start()
        self.addCleanup(self.env.stop)
        self.project = self.repo('one')
        self.other = self.repo('two')

    def repo(self, name):
        path = self.root / name
        path.mkdir()
        subprocess.run(['git', 'init', '-q', str(path)], check=True, capture_output=True)
        return path

    def saved(self, root, identity=None):
        identity = identity or str(uuid.uuid4())
        path = self.home / 'sessions' / (identity + '.jsonl')
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({'type': 'session_meta', 'payload': {
            'id': identity, 'cwd': str(root), 'source': 'cli'}}) + '\nNOT JSON: NEVER READ MESSAGES\n')
        return identity, path

    def test_unique_project_uuid_is_persisted_and_newer_history_cannot_replace_it(self):
        identity, _ = self.saved(self.project)
        self.saved(self.other)
        self.assertEqual(cdev.plan(self.project), {'mode': 'pinned', 'session': identity})
        self.saved(self.project)
        self.assertEqual(cdev.plan(self.project)['session'], identity)
        pins = cdev.state_dir() / 'pins.json'
        self.assertEqual(pins.stat().st_mode & 0o777, 0o600)
        self.assertEqual(cdev.state_dir().stat().st_mode & 0o777, 0o700)
        self.assertNotIn('NEVER READ', pins.read_text())

    def test_ambiguity_missing_pin_and_wrong_repository_fail_without_fallback(self):
        identity, path = self.saved(self.project)
        self.saved(self.project)
        with self.assertRaisesRegex(cdev.CdevError, 'ambiguous project history'):
            cdev.plan(self.project)
        self.assertEqual(cdev.read_pins(), {})
        cdev.update_pin(self.project, identity)
        with self.assertRaisesRegex(cdev.CdevError, 'another repository'):
            cdev.update_pin(self.other, identity)
        path.unlink()
        with self.assertRaisesRegex(cdev.CdevError, 'missing or unverifiable'):
            cdev.plan(self.project)
        self.assertEqual(cdev.read_pins()[str(self.project)], identity)

    def test_nested_git_root_empty_history_and_duplicate_metadata(self):
        self.assertEqual(cdev.plan(self.project), {'mode': 'fresh', 'session': None})
        nested = self.project / 'nested'
        nested.mkdir()
        identity, path = self.saved(nested)
        self.assertEqual(cdev.plan(self.project)['session'], identity)
        archived = self.home / 'archived_sessions'
        archived.mkdir()
        (archived / path.name).write_bytes(path.read_bytes())
        with self.assertRaisesRegex(cdev.CdevError, 'multiple saved copies'):
            cdev.plan(self.project)

    def test_filename_mismatch_and_malformed_headers_are_rejected(self):
        identity, path = self.saved(self.project)
        path.rename(path.with_name(str(uuid.uuid4()) + '.jsonl'))
        with self.assertRaisesRegex(cdev.CdevError, 'missing or unverifiable'):
            cdev.plan(self.project)
        path.write_text('{broken\n')
        with self.assertRaisesRegex(cdev.CdevError, 'cannot verify session metadata'):
            cdev.plan(self.project)

    def test_remote_selection_rejects_unexpected_owner_and_never_retries_local(self):
        identity = str(uuid.uuid4())
        endpoint = self.home / 'control.sock'
        with patch.object(cdev, 'writer_busy', return_value=True), patch.object(cdev, 'shared_endpoint', return_value=None):
            with self.assertRaisesRegex(cdev.CdevError, 'owned by another process'):
                cdev.resume_transport(identity)
        with patch.object(cdev, 'writer_busy', return_value=False), patch.object(cdev, 'shared_endpoint', return_value=None):
            self.assertEqual(cdev.resume_transport(identity), [])
        with patch.object(cdev, 'writer_busy', return_value=True), patch.object(cdev, 'shared_endpoint', return_value=endpoint):
            with patch.object(cdev, 'loaded_threads', return_value={identity}):
                self.assertEqual(cdev.resume_transport(identity), ['--remote', 'unix://' + str(endpoint)])
            with patch.object(cdev, 'loaded_threads', return_value=set()):
                with self.assertRaisesRegex(cdev.CdevError, 'refusing duplicate resume'):
                    cdev.resume_transport(identity)
            with patch.object(cdev, 'loaded_threads', side_effect=TimeoutError('offline')):
                with self.assertRaisesRegex(cdev.CdevError, 'no local fallback'):
                    cdev.resume_transport(identity)

    def test_exact_uuid_and_remote_arguments_reach_one_child(self):
        identity, _ = self.saved(self.project)
        transport = ['--remote', 'unix:///private/tmp/owned.sock']
        selection = cdev.plan(self.project)
        with patch.object(cdev, 'plan', return_value=selection), patch.object(cdev, 'resume_transport', return_value=transport), patch.object(cdev.subprocess, 'Popen') as child:
            child.return_value.wait.return_value = 17
            self.assertEqual(cdev.launch(self.project, '/owned/codex'), 17)
            child.assert_called_once()
            self.assertEqual(child.call_args.args[0], ['/owned/codex', 'resume', identity, '--cd', str(self.project), *transport])
            self.assertEqual(child.call_args.kwargs['cwd'], str(self.project))

    def test_writer_lock_checks_real_contention_without_modifying_file(self):
        identity = str(uuid.uuid4())
        folder = self.home / 'thread-writer-locks'
        folder.mkdir()
        lock = folder / (identity + '.lock')
        lock.write_bytes(b'')
        child = subprocess.Popen([sys.executable, '-c',
            'import fcntl,sys; f=open(sys.argv[1],"rb"); fcntl.flock(f,fcntl.LOCK_EX); '
            'print("ready",flush=True); sys.stdin.read()', str(lock)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            self.assertEqual(child.stdout.readline().strip(), 'ready')
            self.assertTrue(cdev.writer_busy(identity))
        finally:
            child.stdin.close()
            child.wait(timeout=3)
            child.stdout.close()
        self.assertFalse(cdev.writer_busy(identity))
        self.assertEqual(lock.read_bytes(), b'')
        lock.unlink()
        lock.symlink_to(self.root / 'unrelated')
        with self.assertRaises(OSError):
            cdev.writer_busy(identity)

    def test_control_socket_symlink_permissions_and_stale_target(self):
        folder = self.home / 'app-server-control'
        folder.mkdir(mode=0o700)
        path = folder / 'app-server-control.sock'
        target = self.root / 'real.sock'
        with socket.socket(socket.AF_UNIX) as server:
            server.bind(str(target))
            target.chmod(0o600)
            path.symlink_to(target)
            self.assertEqual(cdev.shared_endpoint(), path)
            target.chmod(0o666)
            with self.assertRaisesRegex(cdev.CdevError, 'unsafe shared'):
                cdev.shared_endpoint()
        target.unlink()
        with self.assertRaises(FileNotFoundError):
            cdev.shared_endpoint()

    def test_actual_local_websocket_protocol_only_uses_read_only_methods(self):
        identity = str(uuid.uuid4())
        endpoint = self.root / 'mock.sock'
        calls, errors = [], []

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
                    for _ in range(4):
                        first, second = stream.read(2)
                        self.assertEqual(first, 0x81)
                        self.assertTrue(second & 0x80)
                        length = second & 127
                        if length == 126:
                            length = struct.unpack('!H', stream.read(2))[0]
                        mask = stream.read(4)
                        body = stream.read(length)
                        row = json.loads(bytes(c ^ mask[i % 4] for i, c in enumerate(body)))
                        calls.append(row['method'])
                        if row['method'] == 'initialized':
                            continue
                        result = {} if row['method'] == 'initialize' else {
                            'data': [identity], 'nextCursor': 'page-two' if len(calls) == 3 else None}
                        response = json.dumps({'id': row['id'], 'result': result}).encode()
                        client.sendall(b'\x81' + bytes([len(response)]) + response)
            except BaseException as error:
                errors.append(error)

        with socket.socket(socket.AF_UNIX) as listener:
            listener.bind(str(endpoint))
            listener.listen(1)
            listener.settimeout(3)
            thread = threading.Thread(target=serve, args=(listener,), daemon=True)
            thread.start()
            self.assertEqual(cdev.loaded_threads(endpoint), {identity})
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
        if errors:
            raise errors[0]
        self.assertEqual(calls, ['initialize', 'initialized', 'thread/loaded/list', 'thread/loaded/list'])
