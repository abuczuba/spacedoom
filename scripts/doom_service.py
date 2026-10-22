#!/usr/bin/env python3
"""Explicit launchd management. Default plan is read-only; never installs files.

bootstrap/kickstart/bootout each require separate user approval, not merely the
--approve accident guard. kickstart never uses -k (never replaces a live job).
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import plistlib
import shlex
import stat
import subprocess
import sys

from deploy import Deployment, DeployError

LABEL = "local.dotfiles.doom"


def verified_plist(home, repo):
    root = home / ".local/share/dotfiles-active"
    deployment = Deployment(repo, home, root)
    release = deployment.current()
    if release is None:
        raise DeployError("No current deployment")
    deployment.receipt(release, parse=False)
    target = home / "Library/LaunchAgents" / (LABEL + ".plist")
    expected = root / "current/launchd" / target.name
    if not target.is_symlink() or os.readlink(target) != str(expected):
        raise DeployError("LaunchAgent must first be individually migrated to its approved managed link")
    value = plistlib.loads(target.read_bytes())
    if value.get("Label") != LABEL or value.get("KeepAlive") is not False:
        raise DeployError("Unexpected LaunchAgent lifecycle definition")
    if value.get("ProgramArguments") != ["/usr/bin/python3", "-B", str(deployment.release_dir(release) / "cdev/doom-server.py"), "serve"]:
        raise DeployError("LaunchAgent command does not pin the verified current release")
    return target


def prepare_logs(home):
    directory = home / ".local/state/cdev-emacs"
    for ancestor in [directory, *directory.parents]:
        if ancestor.is_symlink():
            raise DeployError("Runtime directory ancestry cannot contain symlinks")
    if directory.exists():
        info = directory.stat()
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise DeployError("Existing runtime directory must be owned by you, mode 700")
    else:
        directory.mkdir(mode=0o700, parents=True)
    log = directory / "server.log"
    if log.exists() or log.is_symlink():
        info = log.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise DeployError("Existing server log must be a private regular file")
    else:
        with log.open("x"):
            log.chmod(0o600)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["plan", "status", "bootstrap", "kickstart", "bootout"], nargs="?", default="plan")
    parser.add_argument("--approve", action="store_true")
    args = parser.parse_args(argv)
    domain = "gui/" + str(os.getuid())
    target = domain + "/" + LABEL
    home = Path.home()
    plist = home / "Library/LaunchAgents" / (LABEL + ".plist")
    commands = {"status": ["/bin/launchctl", "print", target],
                "bootstrap": ["/bin/launchctl", "bootstrap", domain, str(plist)],
                "kickstart": ["/bin/launchctl", "kickstart", target],
                "bootout": ["/bin/launchctl", "bootout", target]}
    if args.action == "plan":
        print(json.dumps({key: shlex.join(value) for key, value in commands.items()}, indent=2))
        return 0
    if args.action != "status" and not args.approve:
        parser.error("This operation requires specific user approval and --approve")
    try:
        if args.action != "status":
            verified_plist(home, Path(__file__).resolve().parents[1])
        if args.action == "bootstrap":
            prepare_logs(home)  # launchd must be able to open its logs before exec.
            directory = home / ".local/state/cdev-emacs"
            socket = directory / "server"
            if socket.exists() or socket.is_symlink():
                raise DeployError("Named socket already exists; inspect the current manager before bootstrap")
            fd = os.open(directory / "server.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, "a") as lock:
                try:
                    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as error:
                    raise DeployError("Manual manager is active; do not bootstrap a duplicate") from error
        if args.action == "bootout":
            expression = ("(list (length (cl-remove-if-not (lambda (f) (frame-parameter f 'client)) (frame-list))) "
                          "(length (cl-remove-if-not (lambda (b) (with-current-buffer b (buffer-modified-p))) (buffer-list))))")
            result = subprocess.run(["/opt/homebrew/bin/emacsclient", "-s", str(home / ".local/state/cdev-emacs/server"),
                                     "-a", "/usr/bin/false", "-e", expression], capture_output=True, text=True, timeout=5,
                                    env={k: v for k, v in os.environ.items() if k not in {"EMACS_SERVER_FILE", "EMACS_SOCKET_NAME", "ALTERNATE_EDITOR"}})
            if result.returncode == 0 and result.stdout.strip() != "(0 0)":
                raise DeployError("Clients or modified buffers remain; save/close them before approved shutdown")
            if result.returncode:
                raise DeployError("Cannot establish safe shutdown state; inspect the named service manually")
        return subprocess.run(commands[args.action], check=False).returncode
    except (DeployError, OSError, ValueError, subprocess.TimeoutExpired) as error:
        print("doom-service: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
