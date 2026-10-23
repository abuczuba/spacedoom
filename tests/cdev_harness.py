"""Private tmux, synthetic Git/session metadata and native inert Codex stand-in."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import socket
import subprocess
import tempfile
import uuid

from deploy import Deployment
from validation import private_tmux

REPO = Path(__file__).resolve().parents[1]


class CdevHarness:
    def __init__(self, doom=None):
        self.temp = tempfile.TemporaryDirectory(prefix="df-cdev-", dir="/private/tmp")
        self.root = Path(self.temp.name).resolve()
        self.home = doom.home if doom else self.root / "home"
        self.home.mkdir(exist_ok=True)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.server = private_tmux()
        self.tm = self.server.__enter__()
        self.socket = self.tm("display-message", "-p", "#{socket_path}").strip()
        self.env = (doom.env if doom else os.environ).copy()
        self.env.update(HOME=str(self.home), XDG_CONFIG_HOME=str(self.home / ".config"),
                        XDG_STATE_HOME=str(self.home / ".local/state"), XDG_CACHE_HOME=str(self.home / ".cache"),
                        CODEX_HOME=str(self.root / "codex"), CDEV_TEST_LOG=str(self.root / "agent.log"),
                        CDEV_TEST_EDITOR_LOG=str(self.root / "editor.log"),
                        PATH=str(self.bin) + ":/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
                        TMUX=self.socket + ",0,0", TMUX_PANE=self.tm("display-message", "-p", "#{pane_id}").strip())
        Path(self.env["CODEX_HOME"]).mkdir()
        self.release = self.root / "release"
        deploy = Deployment(REPO, self.home, self.root / "inactive")
        deploy.materialize(self.release, self.release, deploy.manifest())
        installed = self.home / ".config/cdev"
        installed.mkdir(parents=True, exist_ok=True)
        for name in ("codex_session.py", "activity.py"):
            (installed / name).symlink_to(self.release / "cdev" / name)
        ghostty = self.home / ".config/ghostty/config.ghostty"
        ghostty.parent.mkdir(parents=True, exist_ok=True)
        ghostty.write_bytes((self.release / "ghostty/config.ghostty").read_bytes())
        self.bin.joinpath("tmux").write_text("#!/bin/sh\nexec /opt/homebrew/bin/tmux -N -S " + shlex.quote(self.socket) + ' "$@"\n')
        self.dummy = None
        if doom is None:
            directory = Path(self.env["XDG_STATE_HOME"]) / "cdev-emacs"
            directory.mkdir(mode=0o700, parents=True)
            self.dummy = socket.socket(socket.AF_UNIX)
            self.dummy.bind(str(directory / "server"))
            self.bin.joinpath("emacsclient").write_text('''#!/bin/sh
case "$*" in *--eval*)
    test "${CDEV_TEST_FAIL:-}" = unavailable && exit 1
    printf 't\\n'; exit 0;;
esac
printf '%s|%s\\n' "$PWD" "$*" >> "$CDEV_TEST_EDITOR_LOG"
test "${CDEV_TEST_FAIL:-}" = emacs && exit 29
exec /bin/sleep 120
''')
        self.bin.joinpath("emacs").write_text('''#!/bin/sh
printf '%s|%s|%s\\n' "$PWD" "$MACOSX_DEPLOYMENT_TARGET" "$*" >> "$CDEV_TEST_EDITOR_LOG"
exec /bin/sleep 120
''')
        for file in self.bin.iterdir():
            file.chmod(0o755)
        subprocess.run(["/usr/bin/cc", str(REPO / "tests/fixtures/mock_codex.c"), "-o", str(self.bin / "codex")],
                       check=True, capture_output=True)
        for key in ["HOME", "XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME", "CODEX_HOME", "PATH",
                    "CDEV_TEST_LOG", "CDEV_TEST_EDITOR_LOG"]:
            self.tm("set-environment", "-g", key, self.env[key])

    def fish(self, code, inside=True, env=None, cwd=None):
        command = "source " + shlex.quote(str(self.release / "fish/functions/cdev.fish")) + "; source "
        command += shlex.quote(str(self.release / "fish/functions/cdev-pin.fish")) + "; " + code
        current = (env or self.env).copy()
        if not inside:
            current.pop("TMUX", None)
        return subprocess.run(["fish", "--no-config", "-c", command], env=current, cwd=cwd or self.root,
                              text=True, capture_output=True, timeout=15)

    def cdev(self, root=None, **kwargs):
        return self.fish("cdev" + (" " + shlex.quote(str(root)) if root is not None else ""), **kwargs)

    def repo(self, name):
        root = self.root / "projects" / name
        root.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
        return root

    def saved(self, root, cwd=None):
        identity = str(uuid.uuid4())
        path = Path(self.env["CODEX_HOME"]) / "sessions" / (identity + ".jsonl")
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(dict(type="session_meta", payload=dict(id=identity, cwd=str(cwd or root), source="cli")))
                        + '\n{"PRIVATE SYNTHETIC CONTENT":"must never be read"}\n')
        return identity

    def log(self):
        path = Path(self.env["CDEV_TEST_LOG"])
        return [line.split("\t") for line in path.read_text().splitlines()] if path.exists() else []

    def window(self, root):
        for row in self.tm("list-windows", "-a", "-F", "#{window_id}\t#{@cdev_root}").splitlines():
            window, recorded = row.split("\t")
            if recorded == str(root):
                return window
        raise AssertionError("No fixture project window")

    def snapshot(self):
        return self.tm("list-panes", "-a", "-F", "#{window_id}:#{pane_id}:#{pane_pid}")

    def close(self):
        self.server.__exit__(None, None, None)
        if self.dummy:
            self.dummy.close()
        self.temp.cleanup()
