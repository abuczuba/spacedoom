#!/usr/bin/env python3
"""Optional transports for validated dashboard transitions; never a lifecycle detector."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from email.header import Header
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import socket
import stat
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

MAX_AGE = 120
PRIORITIES = {"waiting": 4, "done": 3}
LABELS = {"waiting": "Approval required", "done": "Review needed"}


def config_path():
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "cdev/pager.json"


def private_json(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd) as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_mode & 0o077 or info.st_nlink != 1 or info.st_size > 1024 * 1024):
            raise ValueError("pager files must be private regular files")
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError("invalid pager data")
    return value


def configuration(path):
    value = private_json(path)
    if value.get("enabled", True) is not True:
        return None
    parts = urlsplit(value.get("url", ""))
    if (parts.scheme != "https" or not parts.hostname or parts.username or parts.password
            or parts.query or parts.fragment or not re.fullmatch(r"/[A-Za-z0-9_/-]+", parts.path)
            or parts.path.endswith("/")):
        raise ValueError("pager requires an HTTPS topic URL without query credentials")
    token = value.get("token", "")
    if not isinstance(token, str) or any(c in token for c in "\r\n"):
        raise ValueError("invalid pager credentials")
    return value


def save(path, value):
    fd, temporary = tempfile.mkstemp(prefix=".pager-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def project_label(directory):
    # Project identity comes from the existing launch/workmux metadata, never a
    # window title, prompt or terminal scrape. Only its Git basename leaves Mac.
    result = subprocess.run(["git", "-C", directory, "rev-parse", "--show-toplevel"],
                            capture_output=True, text=True, timeout=2)
    if result.returncode:
        return None
    label = Path(result.stdout.rstrip("\n")).name
    return label if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_. -]{0,63}", label) else None


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward a private topic/token to another endpoint.


class Ntfy:
    """Small transport boundary; a future adapter can implement publish()."""
    def __init__(self, config):
        self.config = config

    def publish(self, project, state, test=False):
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_. -]{0,63}", project) or state not in PRIORITIES:
            raise ValueError("invalid notification")
        label = "Pager test" if test else LABELS[state]
        title = "Codex · " + project + " — " + label
        body = ("Pager delivery test." if test else
                "Approval is needed." if state == "waiting" else "Turn stopped; review may be needed.")
        headers = {"Title": Header(title, "utf-8", maxlinelen=1000).encode(), "Priority": str(PRIORITIES[state]),
                   "Content-Type": "text/plain; charset=utf-8", "User-Agent": "dotfiles-pager/1"}
        if self.config.get("token"):
            headers["Authorization"] = "Bearer " + self.config["token"]
        request = Request(self.config["url"], data=body.encode(), headers=headers, method="POST")
        try:
            with build_opener(NoRedirect()).open(request, timeout=3) as response:
                response.read(4096)  # Never log the response (it contains the topic).
            return "sent", False
        except HTTPError as error:
            error.close()
            return "rejected", error.code == 429 or 500 <= error.code < 600
        except URLError as error:
            return ("unavailable", True) if isinstance(error.reason, (socket.gaierror, ConnectionRefusedError)) else ("uncertain", False)
        except (OSError, ValueError):
            return "uncertain", False


def dashboard_snapshot(sock, state):
    spec = importlib.util.spec_from_file_location("pager_dashboard", Path(__file__).with_name("agent-dashboard.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Dashboard(sock, state=state).snapshot()


class Publisher:
    def __init__(self, state, sock, config=None):
        self.state, self.socket = Path(state), sock
        if not self.state.is_absolute() or not Path(sock).is_absolute():
            raise ValueError("explicit absolute pager state/socket required")
        self.config = Path(config or config_path())
        self.directory = self.state / "dotfiles-pager"
        self.key = hashlib.sha256(sock.encode()).hexdigest()
        self.path = self.directory / (self.key + ".json")

    def prepare(self):
        if any(p.is_symlink() for p in (self.directory, *self.directory.parents)):
            raise ValueError("symlinked pager state")
        self.directory.mkdir(parents=True, mode=0o700, exist_ok=True)
        info = self.directory.stat()
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("pager state must be private")

    @contextmanager
    def locked(self, worker=False):
        self.prepare()
        path = self.directory / (self.key + (".worker" if worker else ".lock"))
        fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "a") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077 or info.st_nlink != 1:
                raise ValueError("unsafe pager lock")
            deadline = time.monotonic() + (30 if worker else 1)
            while True:
                try:
                    fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("pager busy")
                    time.sleep(.02)
            yield

    def observe(self, panes, now=None, spawn=True):
        """Called only by dashboard refresh. Local bookkeeping, never HTTP."""
        config = configuration(self.config)
        if config is None:
            return
        now = int(time.time()) if now is None else now
        with self.locked():
            initial = not self.path.exists()
            ledger = private_json(self.path) if not initial else dict(started=now, seen={}, alerts={})
            for pane in panes:
                identity, state = pane.get("track_id"), pane["state"]
                if not isinstance(identity, str) or not re.fullmatch(r"[0-9a-f]{64}", identity):
                    continue
                current = {k: pane.get(k) for k in ("state", "turn", "revision", "stamp")}
                previous = ledger["seen"].get(identity)
                ledger["seen"][identity] = current | {"last": now}
                for alert in ledger["alerts"].values():
                    if (alert["agent"] == identity and alert["status"] == "pending"
                            and (alert["state"], alert.get("turn")) != (state, pane.get("turn"))):
                        alert["status"] = "expired"
                if (initial or state not in PRIORITIES or pane["stamp"] <= ledger["started"]
                        or now - pane["stamp"] > MAX_AGE or pane["stamp"] > now
                        or previous and previous["state"] == state and previous.get("turn") == pane.get("turn")):
                    continue
                project = project_label(pane.get("project_dir") or "")
                if not project:
                    continue  # Unverified project metadata is not a notification.
                event = hashlib.sha256(json.dumps([identity, state, pane.get("turn"), pane.get("revision")]).encode()).hexdigest()
                ledger["alerts"].setdefault(event, dict(agent=identity, project=project, state=state,
                    turn=pane.get("turn"), revision=pane.get("revision"), created=now,
                    status="pending", attempts=0))
            for key in ("seen", "alerts"):
                if len(ledger[key]) > 512:
                    order = sorted(ledger[key], key=lambda k: ledger[key][k].get("last", ledger[key][k].get("created", 0)))
                    ledger[key] = {k: ledger[key][k] for k in order[-512:]}
            save(self.path, ledger)
            pending = any(a["status"] == "pending" for a in ledger["alerts"].values())
        if pending and spawn:
            # A separate worker may wait on another publisher; Codex and its
            # hooks never wait for the worker or perform network operations.
            subprocess.Popen([sys.executable, "-B", str(Path(__file__).absolute()), "drain",
                              "--state", str(self.state), "--socket", self.socket, "--config", str(self.config)],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True, close_fds=True)

    def drain(self, snapshot=None, transport=None, sleep=time.sleep, now=time.time):
        config = configuration(self.config)
        if config is None:
            return
        snapshot = snapshot or (lambda: dashboard_snapshot(self.socket, self.state))
        deadline = time.monotonic() + 30
        with self.locked(worker=True):
            while time.monotonic() < deadline:
                with self.locked():
                    if not self.path.exists():
                        return
                    ledger = private_json(self.path)
                    # An interrupted request may already have delivered. Never
                    # replay it after a crash merely to obtain an acknowledgement.
                    for alert in ledger["alerts"].values():
                        if alert["status"] == "inflight":
                            alert["status"] = "uncertain"
                    pending = [(k, a) for k, a in ledger["alerts"].items() if a["status"] == "pending"]
                    if not pending:
                        save(self.path, ledger)
                        return
                    key, alert = pending[0]
                    alert["status"] = "inflight"
                    alert["attempts"] += 1
                    save(self.path, ledger)
                current = {p.get("track_id"): p for p in snapshot()}
                pane = current.get(alert["agent"])
                if (int(now()) - alert["created"] > MAX_AGE or not pane or
                        any(pane.get(k) != alert.get(k) for k in ("state", "turn"))):
                    outcome, retry = "expired", False
                else:
                    # Claim is durable before HTTP. No status/queue lock spans it.
                    current_config = configuration(self.config)
                    if current_config is None:
                        outcome, retry = "disabled", False
                    else:
                        outcome, retry = (transport or Ntfy(current_config)).publish(alert["project"], alert["state"])
                with self.locked():
                    ledger = private_json(self.path)
                    ledger["alerts"][key]["status"] = "pending" if retry and alert["attempts"] < 3 else outcome
                    save(self.path, ledger)
                if retry and alert["attempts"] < 3:
                    sleep(alert["attempts"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["drain", "status", "test", "disable"])
    parser.add_argument("--state", default=str(Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")))
    parser.add_argument("--socket")
    parser.add_argument("--config", type=Path, default=config_path())
    parser.add_argument("--project", default="dotfiles")
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args()
    try:
        if args.action == "disable":
            if not args.approve:
                raise ValueError("disabling requires approval")
            value = private_json(args.config)
            save(args.config, value | {"enabled": False})
            print("Pager disabled; credentials preserved privately. No service or application restarted.")
            return 0
        config = configuration(args.config)
        if args.action == "test":
            if not args.approve or config is None:
                raise ValueError("test requires approval and enabled private configuration")
            outcome, _ = Ntfy(config).publish(args.project, "done", test=True)
            print("Pager delivery test: " + outcome)
            return 0 if outcome == "sent" else 1
        publisher = Publisher(args.state, args.socket or "", args.config)
        if args.action == "drain":
            publisher.drain()
        else:
            counts = {}
            if publisher.path.exists():
                for alert in private_json(publisher.path)["alerts"].values():
                    counts[alert["status"]] = counts.get(alert["status"], 0) + 1
            print(json.dumps({"enabled": bool(config), "notifications": counts}))
        return 0
    except (OSError, ValueError, TypeError, KeyError, RuntimeError, subprocess.SubprocessError):
        print("Pager unavailable; check private configuration or status. No topic or credentials logged.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
