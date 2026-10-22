"""Local cdev metadata/launcher; standard library only, no credentials/history reads."""
import argparse
import contextlib
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
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
    return identity


def plan(root):
    pin = read_pins().get(str(root))
    if pin:
        return {'mode': 'pinned', 'session': verify_pin(root, pin)}
    folder = codex_home() / 'sessions'
    exact_match = False
    subdirectory_history = False
    if folder.is_dir():
        # Validate all eligible metadata, fail closed on malformed nonempty headers.
        for path in sorted(folder.rglob('*.jsonl')):
            data = header(path)
            if data is None or data['source'] not in ('cli', 'vscode'):
                continue
            if data['cwd'] == root:
                exact_match = True
            else:
                try:
                    if project_root(data['cwd']) == root:
                        subdirectory_history = True
                except CdevError:
                    pass  # A deleted unrelated working directory cannot match this root.
    if exact_match:
        return {'mode': 'last', 'session': None}
    if subdirectory_history:
        raise CdevError('saved project sessions use a different subdirectory; pin their UUID explicitly instead of starting fresh')
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


def report_launch_error(message):
    print('cdev: ' + message, file=sys.stderr, flush=True)
    pane = os.environ.get('TMUX_PANE')
    if pane and os.environ.get('TMUX'):
        subprocess.run(['tmux', 'set-option', '-p', '-t', pane, '@cdev_resume_error', message],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def launch(root, agent):
    selection = plan(root)  # Revalidate immediately before the child is started.
    if selection['mode'] == 'pinned':
        command = [agent, 'resume', selection['session'], '--cd', str(root)]
        label = 'pinned session ' + selection['session']
    elif selection['mode'] == 'last':
        command = [agent, 'resume', '--last', '--cd', str(root)]
        label = 'most recent session for ' + str(root)
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
            hook_args = observer.config_args(adapter=Path(__file__).absolute().with_name('activity.py'))
            child_env.update(observer.environment())
            command += hook_args
        except (ImportError, OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.SubprocessError):
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
            print('cdev: removed pin for ' + str(root) + '; future new workspaces use project-scoped --last or fresh')
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
