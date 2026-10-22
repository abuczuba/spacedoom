#!/usr/bin/env python3
"""Stable, advisory Codex hooks with a verified per-launch runtime handoff.

No trust writes, transcript reads, shell input or shared-server identity guesses.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import time
import uuid

EVENTS = ("SessionStart", "UserPromptSubmit", "PreToolUse", "PermissionRequest",
          "PostToolUse", "Stop", "Interrupt", "SessionEnd")
CONTEXT_ENV = "CDEV_ACTIVITY_CONTEXT"


def process_identity(pid):
    """Read only this process's ownership/parent/start identity, never its env."""
    result = subprocess.run(["/bin/ps", "-p", str(pid), "-o", "uid=,ppid=,lstart=,comm="],
                            env=os.environ.copy() | {"LC_ALL": "C"},
                            capture_output=True, text=True, timeout=1)
    fields = result.stdout.strip().split(None, 7)
    if result.returncode or len(fields) != 8 or int(fields[0]) != os.getuid():
        raise ValueError("activity process identity unavailable")
    return {"parent": int(fields[1]), "started": " ".join(fields[2:7]),
            "command": Path(fields[7]).name}


def runtime_context():
    raw = os.environ.get(CONTEXT_ENV, "")
    if not raw:  # A bare/uninstrumented CLI is deliberately unlabelled.
        return None
    if len(raw) > 4096:
        raise ValueError("oversized activity context")
    data = json.loads(raw)
    if (not isinstance(data, dict) or data.get("version") != 1
            or type(data.get("pid")) is not int or data["pid"] <= 1
            or not isinstance(data.get("started"), str)
            or not isinstance(data.get("token"), str)
            or not re.fullmatch(r"[0-9a-f]{32}", data["token"])
            or not all(isinstance(data.get(k), str) for k in ("state", "socket", "pane"))):
        raise ValueError("invalid activity context")
    return data


def verified_origin(context, record):
    """Fail closed if a shared server inherited another terminal's context.

Both the registered Codex child and its cdev launcher must be live ancestors
with unchanged start identities. TMUX, cwd and payload text are never selectors.
"""
    if (record.get("pid") != context["pid"] or record.get("started") != context["started"]
            or record.get("socket") != context["socket"] or record.get("pane") != context["pane"]
            or record.get("token") != context["token"] or record.get("ended")
            or type(record.get("child")) is not int or not record.get("child_started")):
        return False
    child_seen = False
    pid = os.getppid()
    visited = set()
    for _ in range(32):
        if pid <= 1 or pid in visited:
            return False
        visited.add(pid)
        identity = process_identity(pid)
        if pid == context["pid"]:
            return child_seen and identity["started"] == context["started"]
        if pid == record["child"]:
            if identity["started"] != record["child_started"]:
                return False
            child_seen = True
        elif identity["command"] in {"codex", "codex-cli"} and not child_seen:
            return False  # A nested or unrelated Codex is not the registered CLI.
        pid = identity["parent"]
    return False


def tmux(socket, *args):
    env = os.environ.copy()
    env.pop("TMUX", None)
    env.pop("TMUX_PANE", None)
    result = subprocess.run(["tmux", "-N", "-S", socket, *args], env=env,
                            capture_output=True, text=True, timeout=3)
    if result.returncode:
        raise RuntimeError("activity bridge could not reach its explicit tmux target")
    return result.stdout.removesuffix("\n")


def mark(socket, pane, token, value):
    # A delayed hook/finalizer from an old launch cannot replace a new marker.
    tmux(socket, "if-shell", "-t", pane, "-F", "#{m:" + token + ":*,#{@dotfiles-agent-evidence}}",
         "set-option -p -t " + pane + " @dotfiles-agent-evidence " + shlex.quote(value))


def folder(state):
    path = Path(state) / "dotfiles-dashboard"
    if not path.is_absolute() or any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("invalid activity state directory")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("activity state directory must be private")
    return path


def private_record(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd) as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_mode & 0o077 or info.st_nlink != 1 or info.st_size > 65536):
            raise ValueError("untrusted activity record")
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("activity record must be an object")
    return value


def record_path(state, socket, pane):
    if not Path(socket).is_absolute() or not re.fullmatch(r"%\d+", pane):
        raise ValueError("explicit socket and stable pane ID required")
    return folder(state) / (hashlib.sha256(socket.encode()).hexdigest() + "-" + pane[1:] + ".json")


@contextmanager
def lock(state, socket):
    path = folder(state) / (hashlib.sha256(socket.encode()).hexdigest() + ".lock")
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a") as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_mode & 0o077 or info.st_nlink != 1):
            raise ValueError("untrusted activity lock")
        deadline = time.monotonic() + 1
        while True:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise RuntimeError("activity cache is busy; observer update skipped")
                time.sleep(.02)
        yield


def save(path, data):
    fd, name = tempfile.mkstemp(prefix=".event-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(data, stream)
            stream.flush()
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def transition(record, payload, now):
    """Pure state machine: reject previous launch/session/turn and late events."""
    record = record.copy()
    event = payload.get("hook_event_name")
    session = payload.get("session_id")
    turn = payload.get("turn_id")
    if (event not in EVENTS or not isinstance(session, str) or not 0 < len(session) <= 256
            or record.get("ended")):
        return None
    if record.get("session") not in (None, session):
        return None
    record["session"] = session
    if event == "SessionStart":
        return record
    if event == "SessionEnd":
        record.update(state="idle", ended=True, stamp=now)
        return record
    if not isinstance(turn, str) or not 0 < len(turn) <= 256 or turn in record.get("retired", []):
        return None
    old_turn = record.get("turn")
    if event == "UserPromptSubmit" and turn == old_turn:
        return None
    if event == "UserPromptSubmit" or (event == "PreToolUse" and old_turn is None):
        if old_turn and old_turn != turn:
            record["retired"] = (record.get("retired", []) + [old_turn])[-64:]
        record.update(turn=turn, state="working", settled=False, pending=[])
    elif turn != old_turn or record.get("settled"):
        return None
    elif event in {"PreToolUse", "PostToolUse"}:
        pending = list(record.get("pending", []))
        name = payload.get("tool_name")
        name = name if isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", name) else "<unknown>"
        if event == "PostToolUse" and name in pending:
            pending.remove(name)
        record.update(state="waiting" if pending else "working", pending=pending)
    elif event == "PermissionRequest":
        record["state"] = "waiting"
        name = payload.get("tool_name")
        name = name if isinstance(name, str) and re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", name) else "<unknown>"
        record["pending"] = (list(record.get("pending", [])) + [name])[-64:]
    elif event in {"Stop", "Interrupt"}:
        record.update(state="done" if event == "Stop" else "idle", settled=True, pending=[])
    record.update(stamp=now, sequence=record.get("sequence", 0) + 1)
    return record


class Launch:
    def __init__(self, state, socket, pane):
        self.state, self.socket, self.pane = str(state), socket, pane
        self.token = uuid.uuid4().hex
        self.path = record_path(state, socket, pane)

    def register(self):
        identity = tmux(self.socket, "display-message", "-p", "-t", self.pane,
                        "#{start_time}:#{pid}|#{pane_pid}")
        boot, pid = identity.split("|")
        # A cdev launcher is the pane's root process, not an arbitrary descendant.
        if int(pid) != os.getpid():
            raise ValueError("activity launcher does not own this pane")
        self.started = process_identity(int(pid))["started"]
        with lock(self.state, self.socket):
            save(self.path, dict(socket=self.socket, pane=self.pane, boot=boot,
                                 pid=int(pid), started=self.started, token=self.token, session=None, turn=None,
                                 state="idle", stamp=int(time.time()), sequence=0, ended=False))
        tmux(self.socket, "set-option", "-p", "-t", self.pane, "@dotfiles-agent-evidence", self.token + ":0")

    def config_args(self, adapter=None):
        # Keep the installed lexical path: resolving a managed symlink would
        # embed the release ID. Ordinary launches must have identical hashes.
        # cdev already requires macOS's /usr/bin/python3. Its sys.executable may
        # expose a versioned CommandLineTools path; keep that out of the hash.
        command = shlex.join(["/usr/bin/python3", "-B", str(Path(adapter or __file__).absolute()), "event"])
        # TOML inline tables, passed as argv data. Codex merges hooks from
        # separate layers. No trust/approval/sandbox/notification override.
        value = '[{hooks=[{type="command",command=' + json.dumps(command) + ',timeout=2}]}]'
        return [item for event in EVENTS for item in ["-c", "hooks." + event + "=" + value]]

    def environment(self):
        context = dict(version=1, state=self.state, socket=self.socket, pane=self.pane,
                       token=self.token, pid=os.getpid(), started=self.started)
        return {CONTEXT_ENV: json.dumps(context, separators=(",", ":"))}

    def attach(self, child):
        identity = process_identity(child)
        if identity["parent"] != os.getpid():
            raise ValueError("activity child is not owned by this launcher")
        with lock(self.state, self.socket):
            data = private_record(self.path)
            if data.get("token") != self.token or data.get("ended"):
                raise ValueError("activity launch was superseded")
            data.update(child=child, child_started=identity["started"])
            save(self.path, data)

    def finish(self):
        with lock(self.state, self.socket):
            if self.path.is_symlink():
                return
            data = private_record(self.path)
            if data.get("token") != self.token:
                return
            data.update(ended=True, state="idle", stamp=int(time.time()), sequence=data["sequence"] + 1)
            save(self.path, data)
        mark(self.socket, self.pane, self.token, "")


def event(context, payload):
    state, socket, pane, token = (context[k] for k in ("state", "socket", "pane", "token"))
    path = record_path(state, socket, pane)
    with lock(state, socket):
        if path.is_symlink():
            return
        record = private_record(path)
        if not isinstance(payload, dict) or not verified_origin(context, record):
            return
        identity = tmux(socket, "display-message", "-p", "-t", pane,
                        "#{start_time}:#{pid}|#{pane_pid}")
        if identity != record.get("boot", "") + "|" + str(record.get("pid")):
            return
        result = transition(record, payload, int(time.time()))
        if result is None:
            return
        # Most tools run while already working. Keep those hooks cheap and do
        # not trigger another renderer. Refresh the lease at most every 30s.
        significant = lambda value: {k: v for k, v in value.items() if k not in {"stamp", "sequence"}}
        if significant(result) == significant(record) and result.get("stamp", 0) - record.get("stamp", 0) < 30:
            return
        save(path, result)
    # No payload, prompts, tool inputs or transcript text enters tmux or disk.
    mark(socket, pane, token, token + ":" + str(result["sequence"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["event"])
    parser.parse_args()
    try:
        context = runtime_context()
        if context is None:
            return 0
        data = sys.stdin.buffer.read(1024 * 1024 + 1)
        if len(data) <= 1024 * 1024:
            payload = json.loads(data)
            if isinstance(payload, dict):
                event(context, payload)
    except (OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.TimeoutExpired):
        # Advisory observer only: a dashboard failure must never control Codex.
        print("cdev activity evidence unavailable; continuing without a status update", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
