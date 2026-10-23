"""Local cdev metadata/launcher; standard library only, no credentials/message reads."""
import argparse
import base64
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import socket
import stat
import struct
import subprocess
import sys
import tempfile
import time
import uuid


class CdevError(Exception):
    pass


def project_root(directory):
    result = subprocess.run(['git', '-C', str(directory), 'rev-parse', '--show-toplevel'],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if result.returncode or not result.stdout.strip():
        raise CdevError('not a Git working tree: ' + str(directory))
    root = Path(result.stdout.rstrip('\n')).resolve()
    if any(c in str(root) for c in '\r\n\t'):
        raise CdevError('project paths containing tabs/newlines are unsupported')
    return root


def session_uuid(value):
    try:
        parsed = str(uuid.UUID(value))
    except (ValueError, AttributeError):
        raise CdevError('pin must be a session UUID')
    if value.lower() != parsed:
        raise CdevError('pin must use the full hyphenated session UUID')
    return parsed


def codex_home():
    return Path(os.environ.get('CODEX_HOME') or str(Path.home() / '.codex')).expanduser().resolve()


def state_dir():
    parent = Path(os.environ.get('XDG_STATE_HOME') or str(Path.home() / '.local/state')).expanduser()
    if not parent.is_absolute():
        raise CdevError('XDG_STATE_HOME must be absolute')
    directory = parent / 'cdev'
    probe = directory
    while not probe.exists():
        probe = probe.parent
    check = subprocess.run(['git', '-C', str(probe), 'rev-parse', '--is-inside-work-tree'],
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    if check.returncode == 0 and check.stdout.strip() == 'true':
        raise CdevError('pin metadata must be outside Git working trees; choose a different XDG_STATE_HOME')
    return directory


def read_pins():
    path = state_dir() / 'pins.json'
    if path.is_symlink():
        raise CdevError('refusing symlinked pin metadata')
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if data.get('version') != 1 or not isinstance(data.get('pins'), dict):
            raise ValueError('unsupported metadata format')
        pins = data['pins']
        for root, value in pins.items():
            if not isinstance(root, str) or not Path(root).is_absolute():
                raise ValueError('invalid project path')
            session_uuid(value)
        return pins
    except (ValueError, TypeError, AttributeError, CdevError) as error:
        raise CdevError('cannot read pin metadata; refusing a fresh fallback: ' + str(error))


def header(path):
    # Only the metadata line is read; no conversation messages or auth files.
    with path.open() as stream:
        line = stream.readline(1024 * 1024 + 1)
    if not line:  # An empty, unsaved rollout placeholder is not resumable history.
        return None
    if len(line) > 1024 * 1024:
        raise CdevError('session metadata is too large: ' + path.name)
    try:
        row = json.loads(line)
        payload = row['payload']
        if row.get('type') != 'session_meta' or not isinstance(payload, dict):
            raise ValueError('missing session_meta header')
        identity = session_uuid(payload['id'])
        cwd = payload['cwd']
        if not isinstance(cwd, str) or not Path(cwd).is_absolute():
            raise ValueError('missing absolute session directory')
        return {'id': identity, 'cwd': Path(cwd).resolve(), 'source': payload.get('source')}
    except (ValueError, KeyError, TypeError) as error:
        raise CdevError('cannot verify session metadata: ' + path.name + ' (' + str(error) + ')')


def verify_pin(root, identity):
    identity = session_uuid(identity)
    candidates = []
    # An explicit archived pin may be attempted, but any CLI failure stays a failure.
    for directory in ['sessions', 'archived_sessions']:
        folder = codex_home() / directory
        if folder.is_dir():
            candidates.extend(folder.rglob('*' + identity + '*.jsonl'))
    verified = []
    for path in candidates:
        if path.is_symlink():
            raise CdevError('refusing symlinked session metadata')
        data = header(path)
        if data is None:
            continue
        if data['id'] != identity:
            raise CdevError('session filename/UUID disagreement; refusing resume')
        if project_root(data['cwd']) != root:
            raise CdevError('pinned session belongs to another repository; refusing resume')
        verified.append(data)
    if not verified:
        raise CdevError('pinned session ' + identity + ' is missing or unverifiable; no fresh session started')
    if len(verified) != 1:
        raise CdevError('multiple saved copies of session ' + identity + '; refusing ambiguous resume')
    return identity


def plan(root):
    # Selection and persistence share a lock: two callers cannot choose different
    # defaults. No timestamp heuristic and no second selection by Codex --last.
    with pin_lock():
        pins = read_pins()
        pin = pins.get(str(root))
        if pin:
            return {'mode': 'pinned', 'session': verify_pin(root, pin)}
        folder = codex_home() / 'sessions'
        matches = set()
        if folder.is_dir():
            for path in sorted(folder.rglob('*.jsonl')):
                data = header(path)
                if data is None or data['source'] not in ('cli', 'vscode'):
                    continue
                try:
                    if project_root(data['cwd']) == root:
                        matches.add(data['id'])
                except CdevError:
                    pass  # A deleted unrelated working directory cannot match this root.
        if len(matches) > 1:
            raise CdevError('ambiguous project history; use cdev-pin UUID PROJECT to choose the exact conversation')
        if matches:
            identity = verify_pin(root, matches.pop())
            pins[str(root)] = identity
            write_pins(pins)
            return {'mode': 'pinned', 'session': identity}
        return {'mode': 'fresh', 'session': None}


@contextlib.contextmanager
def pin_lock():
    directory = state_dir()
    if directory.is_symlink():
        raise CdevError('refusing symlinked cdev state directory')
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(str(directory / 'pins.lock'), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def update_pin(root, value):
    with pin_lock():
        pins = read_pins()
        if value is None:
            pins.pop(str(root), None)
        else:
            pins[str(root)] = verify_pin(root, value)
        write_pins(pins)


def write_pins(pins):
    """Caller holds pin_lock; never store conversation text or credentials."""
    directory = state_dir()
    fd, temporary = tempfile.mkstemp(prefix='.pins-', dir=str(directory))
    try:
        with os.fdopen(fd, 'w') as stream:
            json.dump({'version': 1, 'pins': pins}, stream, indent=2, sort_keys=True)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, directory / 'pins.json')
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def writer_busy(identity):
    path = codex_home() / 'thread-writer-locks' / (identity + '.lock')
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    except FileNotFoundError:
        return False
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o022:
            raise CdevError('unexpected session writer-lock ownership or permissions')
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        fcntl.flock(stream, fcntl.LOCK_UN)
    return False


def shared_endpoint():
    path = codex_home() / 'app-server-control/app-server-control.sock'
    if not os.path.lexists(path):
        return None
    # Codex itself uses a symlink into a private /tmp directory. Permit that
    # rendezvous, but never an endpoint writable/owned by another account.
    target = path.resolve(strict=True)
    if path.lstat().st_uid != os.getuid():
        raise CdevError('unexpected shared app-server socket owner')
    for item in (path.parent, target.parent, target):
        info = item.stat()
        if info.st_uid != os.getuid() or info.st_mode & 0o022:
            raise CdevError('unsafe shared app-server socket permissions')
    if not stat.S_ISSOCK(target.stat().st_mode):
        raise CdevError('shared app-server endpoint is not a socket')
    return path


@contextlib.contextmanager
def server_connection(endpoint):
    """Bounded local WebSocket; callers choose explicit metadata/config RPCs."""
    deadline = time.monotonic() + 5
    with socket.socket(socket.AF_UNIX) as connection:
        connection.settimeout(5)
        connection.connect(str(endpoint))
        with connection.makefile('rb') as stream:
            def exact(size):
                connection.settimeout(max(.001, deadline - time.monotonic()))
                value = stream.read(size)
                if len(value) != size:
                    raise CdevError('shared app-server closed its metadata connection')
                return value

            key = base64.b64encode(os.urandom(16)).decode()
            connection.sendall(('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\n'
                                'Connection: Upgrade\r\nSec-WebSocket-Version: 13\r\n'
                                'Sec-WebSocket-Key: ' + key + '\r\n\r\n').encode())
            status = stream.readline(8193)
            headers = {}
            for _ in range(64):
                line = stream.readline(8193)
                if line == b'\r\n':
                    break
                if not line or len(line) > 8192 or b':' not in line:
                    raise CdevError('invalid shared app-server handshake')
                name, value = line.decode('ascii').split(':', 1)
                headers[name.lower()] = value.strip()
            else:
                raise CdevError('oversized shared app-server handshake')
            expected = base64.b64encode(hashlib.sha1((key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
            if not status.startswith(b'HTTP/1.1 101 ') or headers.get('sec-websocket-accept') != expected:
                raise CdevError('shared app-server refused its metadata connection')

            def send(value, opcode=1):
                body = json.dumps(value).encode() if opcode == 1 else value
                mask = os.urandom(4)
                length = bytes([len(body)]) if len(body) < 126 else b'\x7e' + struct.pack('!H', len(body))
                connection.sendall(bytes([0x80 | opcode, length[0] | 0x80]) + length[1:] + mask +
                                   bytes(c ^ mask[i % 4] for i, c in enumerate(body)))

            def request(identity, method, params):
                send({'id': identity, 'method': method, 'params': params})
                for _ in range(1000):
                    first, second = exact(2)
                    if first & 0xf0 != 0x80 or second & 0x80:
                        raise CdevError('unsupported shared app-server frame')
                    size = second & 0x7f
                    if size in (126, 127):
                        size = int.from_bytes(exact(2 if size == 126 else 8), 'big')
                    if size > 1024 * 1024:
                        raise CdevError('oversized shared app-server metadata')
                    body = exact(size)
                    opcode = first & 15
                    if opcode == 9:
                        send(body, 10)
                        continue
                    if opcode == 10:
                        continue
                    if opcode != 1:
                        raise CdevError('shared app-server ended its metadata connection')
                    row = json.loads(body)
                    if row.get('id') == identity:
                        if 'error' in row or not isinstance(row.get('result'), dict):
                            raise CdevError('shared app-server rejected ' + method)
                        return row['result']
                raise CdevError('shared app-server metadata response missing')

            request(1, 'initialize', {'clientInfo': {'name': 'cdev_recovery', 'version': '1'}})
            send({'method': 'initialized', 'params': {}})
            yield request, connection


def loaded_threads(endpoint):
    """Read-only discovery; never start, resume, or read a conversation."""
    with server_connection(endpoint) as (request, _):
        loaded, cursor = set(), None
        for page in range(100):
            result = request(page + 2, 'thread/loaded/list', {'cursor': cursor})
            data = result.get('data')
            if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
                raise CdevError('invalid shared app-server thread identities')
            loaded.update(data)
            cursor = result.get('nextCursor')
            if not cursor:
                return loaded
            if not isinstance(cursor, str):
                break
        raise CdevError('shared app-server thread pagination is invalid or too large')


def configure_remote_activity(endpoint, identity, root, observer, adapter):
    # The 0.163 remote TUI drops -c hooks.* from thread/resume.config. Send
    # only those same definitions through the supported per-thread API first.
    # No global config/trust writes, policies, prompts, or history hydration.
    with server_connection(endpoint) as (request, connection):
        if sys.platform != 'darwin':
            raise CdevError('remote hook attribution requires macOS Unix peer credentials')
        backend = connection.getsockopt(0, 2)  # SOL_LOCAL / LOCAL_PEERPID
        observer.remote(identity, backend)
        request(2, 'thread/resume', {'threadId': identity, 'cwd': str(root),
                                   'excludeTurns': True,
                                   'config': observer.definition_config(adapter)})


def resume_transport(identity):
    busy = writer_busy(identity)
    endpoint = shared_endpoint()
    if endpoint is None:
        if busy:
            raise CdevError('session is owned by another process without a verified shared app-server; close its client or investigate ownership')
        return []
    try:
        loaded = loaded_threads(endpoint)
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise CdevError('cannot verify shared app-server; no local fallback: ' + str(error))
    if busy and identity not in loaded:
        raise CdevError('session writer is not owned by the verified shared app-server; refusing duplicate resume')
    return ['--remote', 'unix://' + str(endpoint)]


def report_launch_error(message):
    print('cdev: ' + message, file=sys.stderr, flush=True)
    pane = os.environ.get('TMUX_PANE')
    if pane and os.environ.get('TMUX'):
        subprocess.run(['tmux', 'set-option', '-p', '-t', pane, '@cdev_resume_error', message],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def launch(root, agent):
    selection = plan(root)  # Revalidate immediately before the child is started.
    if selection['mode'] == 'pinned':
        command = [agent, 'resume', selection['session'], '--cd', str(root)] + resume_transport(selection['session'])
        label = 'pinned session ' + selection['session']
    else:
        command = [agent, '--cd', str(root)]
        label = 'fresh session for ' + str(root)
    print('cdev: launching ' + label, flush=True)
    observer = None
    child_env = os.environ.copy()
    # Never leak an enclosing launch's registration to an untracked CLI.
    child_env.pop('CDEV_ACTIVITY_CONTEXT', None)
    if os.environ.get('CDEV_DASHBOARD', '1') != '0' and os.environ.get('TMUX') and os.environ.get('TMUX_PANE'):
        try:
            sys.dont_write_bytecode = True  # An immutable release is never an import cache.
            from activity import Launch
            # Query this launcher only. Stable hooks receive separate runtime
            # context and verify that the actual child/launcher are ancestors.
            socket = subprocess.check_output(['tmux', 'display-message', '-p', '#{socket_path}'], text=True, timeout=3).strip()
            state = os.environ.get('XDG_STATE_HOME') or str(Path.home() / '.local/state')
            observer = Launch(state, socket, os.environ['TMUX_PANE'])
            observer.register()
            # Python resolves sys.path through a symlinked main script, so the
            # imported module's __file__ may name a versioned release. The main
            # script retains its lexical installed path; use that stable sibling.
            adapter = Path(__file__).absolute().with_name('activity.py')
            hook_args = observer.config_args(adapter=adapter)
            if '--remote' in command:
                endpoint = command[command.index('--remote') + 1].removeprefix('unix://')
                configure_remote_activity(Path(endpoint), selection['session'], root, observer, adapter)
            child_env.update(observer.environment())
            command += hook_args
        except (ImportError, CdevError, OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.SubprocessError):
            if observer is not None:
                try:
                    observer.finish()
                except (OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.SubprocessError):
                    pass
            observer = None
            print('cdev: activity tracking unavailable; Codex launch policies unchanged', file=sys.stderr)
    # No --all, approval/sandbox overrides, prompts, credential reads, or retries.
    try:
        child = subprocess.Popen(command, cwd=str(root), env=child_env)
        if observer is not None:
            try:
                observer.attach(child.pid)
            except (OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.SubprocessError):
                # Early hooks may race registration; they are skipped. Later
                # events can bind a session, but never without child identity.
                print('cdev: activity child identity unavailable; Codex continues', file=sys.stderr)
        code = child.wait()
    except KeyboardInterrupt:
        return 130
    except OSError as error:
        report_launch_error('could not launch ' + label + ': ' + str(error) + '; no fallback started')
        return 1
    finally:
        if observer is not None:
            try:
                observer.finish()
            except (OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.SubprocessError):
                pass  # Pane/boot/age checks still reject abandoned evidence.
    if code:
        report_launch_error(label + ' failed (exit ' + str(code) + '); no fallback session started')
    return code if code >= 0 else 128 - code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'launch', 'pin', 'unpin', 'show', 'verify'])
    parser.add_argument('--root', required=True)
    parser.add_argument('--session')
    parser.add_argument('--codex')
    args = parser.parse_args()
    try:
        root = project_root(args.root)
        if args.action == 'plan':
            print(plan(root)['mode'])
        elif args.action == 'launch':
            if not args.codex:
                raise CdevError('missing Codex executable')
            return launch(root, args.codex)
        elif args.action == 'pin':
            if not args.session:
                raise CdevError('missing session UUID')
            update_pin(root, args.session)
            print('cdev: pinned ' + str(root) + ' to ' + session_uuid(args.session))
        elif args.action == 'unpin':
            update_pin(root, None)
            print('cdev: removed pin for ' + str(root) + '; future launches require unique verified project history or an explicit pin')
        elif args.action == 'show':
            print(read_pins().get(str(root), '(no pin)'))
        elif args.action == 'verify':
            if not args.session:
                raise CdevError('missing session UUID')
            print(verify_pin(root, args.session))
        return 0
    except (CdevError, OSError) as error:
        message = str(error)
        if args.action == 'launch':
            report_launch_error(message + '; no fallback session started')
        else:
            print('cdev: ' + message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
