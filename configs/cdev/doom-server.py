#!/usr/bin/env python3
"""Explicit named Doom server: check, terminal client, foreground serve, status.

No auto-start, default-server fallback, stale-socket deletion, install or reload.
launchd may own `serve`; the same command is the manual foreground fallback.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys


class ServerError(RuntimeError):
    pass


def client_environment():
    env = os.environ.copy()
    for key in ["EMACS_SERVER_FILE", "EMACS_SOCKET_NAME", "ALTERNATE_EDITOR"]:
        env.pop(key, None)
    return env


def paths():
    state = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    if not state.is_absolute():
        raise ServerError("XDG_STATE_HOME must be absolute")
    directory = state / "cdev-emacs"
    return directory, directory / "server"


def check_directory(directory, create=False):
    # All ancestors below HOME/state must be real directories. In particular,
    # never follow a replacement private socket directory to another user.
    for path in [directory, *directory.parents]:
        if path.is_symlink():
            # macOS aliases /var and /tmp are resolved by the caller first.
            raise ServerError("server directory ancestry must not contain symlinks")
    if create:
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if directory.exists():
        info = directory.stat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ServerError("server directory must be owned by you, mode 700")


def check(socket, client="/opt/homebrew/bin/emacsclient"):
    check_directory(socket.parent)
    if not socket.exists() or socket.is_symlink():
        raise ServerError("Doom server unavailable; start the named server explicitly (serve), then retry cdev")
    info = socket.stat()
    if not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.getuid():
        raise ServerError("unsafe server socket; no connection attempted")
    expression = "(and (daemonp) (featurep 'dotfiles-cdev) (bound-and-true-p persp-mode) t)"
    result = subprocess.run([client, "--socket-name=" + str(socket), "--alternate-editor=/usr/bin/false",
                             "--eval", expression], capture_output=True, text=True, timeout=5, env=client_environment())
    if result.returncode or result.stdout.strip() != "t":
        raise ServerError("named Doom server failed readiness checks; no fallback or pane replacement attempted")


def client_command(socket, root, client="/opt/homebrew/bin/emacsclient"):
    root = Path(root).resolve(strict=True)
    if not root.is_dir() or any(c in str(root) for c in "\r\n\t"):
        raise ServerError("invalid project directory")
    parameters = "((cdev-project-root . " + json.dumps(str(root), ensure_ascii=False) + "))"
    # Directory ownership/readiness were checked first. Do not use -a '' or -n:
    # those can start a different daemon or suppress the terminal client frame.
    return [client, "--socket-name=" + str(socket), "--alternate-editor=/usr/bin/false",
            "-t", "--frame-parameters=" + parameters]


def serve(socket, emacs, emacs_dir, integration):
    check_directory(socket.parent, create=True)
    lock = socket.parent / "server.lock"
    fd = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ServerError("named server already has a manager; no duplicate started") from error
        if socket.exists() or socket.is_symlink():
            raise ServerError("server socket already exists; inspect it before explicit recovery (never auto-delete)")
        if not emacs_dir.is_dir() or not (emacs_dir / "early-init.el").is_file() or not integration.is_file():
            raise ServerError("Doom startup or client integration is missing")
        env = client_environment()
        env.update(MACOSX_DEPLOYMENT_TARGET="27.0", PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin")
        env.pop("TMUX", None)
        env.pop("TMUX_PANE", None)
        command = [emacs, "--init-directory", str(emacs_dir), "--fg-daemon=" + str(socket), "--load", str(integration)]
        # This process holds the singleton lock and waits; it does not poll.
        child = subprocess.Popen(command, env=env)
        def forward(sig, _frame):
            if child.poll() is None:
                child.send_signal(sig)
        previous = {sig: signal.signal(sig, forward) for sig in (signal.SIGTERM, signal.SIGINT)}
        try:
            return child.wait()
        finally:
            for sig, handler in previous.items():
                signal.signal(sig, handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["check", "client", "serve", "status"])
    parser.add_argument("--project")
    parser.add_argument("--socket", type=Path)
    parser.add_argument("--emacs", default="/opt/homebrew/bin/emacs")
    parser.add_argument("--emacsclient", default="/opt/homebrew/bin/emacsclient")
    parser.add_argument("--emacs-dir", type=Path, default=Path.home() / ".config/emacs")
    parser.add_argument("--integration", type=Path, default=Path(__file__).resolve().parents[1] / "doom/cdev.el")
    args = parser.parse_args()
    try:
        directory, default_socket = paths()
        socket = args.socket or default_socket
        if not socket.is_absolute() or len(os.fsencode(socket)) > 100:
            raise ServerError("server socket must be an absolute path of at most 100 bytes")
        if args.action == "serve":
            return serve(socket, args.emacs, args.emacs_dir, args.integration)
        check(socket, args.emacsclient)
        if args.action == "client":
            if not args.project:
                raise ServerError("client requires --project")
            command = client_command(socket, args.project, args.emacsclient)
            os.chdir(Path(args.project).resolve())
            os.execve(command[0], command, client_environment())
        if args.action == "status":
            print("Named Doom server ready: " + str(socket))
        return 0
    except (OSError, ServerError, subprocess.TimeoutExpired) as error:
        print("cdev-emacs: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
