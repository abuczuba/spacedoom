#!/usr/bin/env python3
"""Session-scoped, advisory Codex hook bridge. No transcript/prompt persistence.

The hook COMMAND pins socket, pane and launch nonce rather than inheriting the
shared Codex app-server's terminal environment. Existing global hooks still run.
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
import subprocess
import sys
import tempfile
import time
import uuid

EVENTS = ("SessionStart", "UserPromptSubmit", "PreToolUse", "PermissionRequest",
          "PostToolUse", "Stop", "Interrupt", "SessionEnd")


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
    if not path.is_absolute() or path.is_symlink():
        raise ValueError("invalid activity state directory")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("activity state directory must be private")
    return path


def record_path(state, socket, pane):
    if not Path(socket).is_absolute() or not re.fullmatch(r"%\d+", pane):
        raise ValueError("explicit socket and stable pane ID required")
    return folder(state) / (hashlib.sha256(socket.encode()).hexdigest() + "-" + pane[1:] + ".json")


@contextmanager
def lock(state, socket):
    path = folder(state) / (hashlib.sha256(socket.encode()).hexdigest() + ".lock")
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a") as stream:
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
        with lock(self.state, self.socket):
            save(self.path, dict(socket=self.socket, pane=self.pane, boot=boot,
                                 pid=int(pid), token=self.token, session=None, turn=None,
                                 state="idle", stamp=int(time.time()), sequence=0, ended=False))
        tmux(self.socket, "set-option", "-p", "-t", self.pane, "@dotfiles-agent-evidence", self.token + ":0")

    def config_args(self):
        command = shlex.join([sys.executable, "-B", str(Path(__file__).resolve()), "event",
                              "--state", self.state, "--socket", self.socket,
                              "--pane", self.pane, "--token", self.token])
        # TOML inline tables, passed as argv data. Codex merges hooks from
        # separate layers. No trust/approval/sandbox/notification override.
        value = '[{hooks=[{type="command",command=' + json.dumps(command) + ',timeout=2}]}]'
        return [item for event in EVENTS for item in ["-c", "hooks." + event + "=" + value]]

    def finish(self):
        with lock(self.state, self.socket):
            if self.path.is_symlink():
                return
            data = json.loads(self.path.read_text())
            if not isinstance(data, dict):
                return
            if data.get("token") != self.token:
                return
            data.update(ended=True, state="idle", stamp=int(time.time()), sequence=data["sequence"] + 1)
            save(self.path, data)
        mark(self.socket, self.pane, self.token, "")


def event(state, socket, pane, token, payload):
    path = record_path(state, socket, pane)
    with lock(state, socket):
        if path.is_symlink():
            return
        record = json.loads(path.read_text())
        if not isinstance(record, dict) or not isinstance(payload, dict):
            return
        if record.get("token") != token:
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
    parser.add_argument("--state", required=True)
    parser.add_argument("--socket", required=True)
    parser.add_argument("--pane", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()
    try:
        data = sys.stdin.buffer.read(1024 * 1024 + 1)
        if len(data) <= 1024 * 1024:
            payload = json.loads(data)
            if isinstance(payload, dict):
                event(args.state, args.socket, args.pane, args.token, payload)
    except (OSError, ValueError, RuntimeError, TypeError, KeyError, subprocess.TimeoutExpired):
        # Advisory observer only: a dashboard failure must never control Codex.
        print("cdev activity evidence unavailable; continuing without a status update", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
