"""Disposable installed-Doom fixture. Never load the user's config or state.

Installed libraries/packages are read-only dependencies. Generated startup files
are COPIES with home references rebased, and the captured environment loader is
omitted. All caches, workspace state, HOME, sockets and project files are private.
"""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import pty
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import select
import time

REPO = Path(__file__).resolve().parents[1]


class DoomHarness:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory(prefix="df-doom-", dir="/private/tmp")
        self.root = Path(self.temp.name).resolve()
        self.home = self.root / "home"
        self.emacs_dir = self.home / ".config/emacs"
        self.emacs_dir.mkdir(parents=True)
        source = Path.home() / ".config/emacs"
        audited = json.loads((REPO / "tests/fixtures/doom-runtime.json").read_text())["files"]
        actual = [source / "early-init.el", *sorted((source / ".local/etc/@").rglob("*.el"))]
        fingerprints = {str(file.relative_to(source)): hashlib.sha256(file.read_bytes()).hexdigest()
                        for file in actual if "env.load" not in file.name}
        if fingerprints != audited:
            raise AssertionError("Doom generated startup changed since the audit; inspect it before refreshing the fixture")
        self.emacs_dir.joinpath("early-init.el").write_text(
            ";;; -*- lexical-binding: t; -*-\n(setq native-comp-jit-compilation nil)\n"
            + (source / "early-init.el").read_text())
        for name in ["lisp", "modules", "sources"]:
            (self.emacs_dir / name).symlink_to(source / name, target_is_directory=True)
        (self.emacs_dir / ".local/straight").mkdir(parents=True)
        for name in ["repos", "build-31.1"]:
            (self.emacs_dir / ".local/straight" / name).symlink_to(source / ".local/straight" / name,
                                                                target_is_directory=True)
        for file in (source / ".local/etc/@").rglob("*.el"):
            target = self.emacs_dir / file.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("" if "env.load" in file.name else file.read_text().replace(str(Path.home()), str(self.home)))
        private = self.home / ".config/doom"
        private.mkdir(parents=True)
        # The installed, inspected module selection has no private data.
        private.joinpath("init.el").write_bytes((REPO / "tests/fixtures/doom-init.el").read_bytes())
        private.joinpath("config.el").write_bytes((REPO / "tests/fixtures/doom-config.el").read_bytes())
        self.env = os.environ.copy()
        for key in ["TMUX", "TMUX_PANE", "DOOMPROFILE", "DOOMPROFILELOADFILE", "EMACSDIR",
                    "EMACS_SERVER_FILE", "EMACS_SOCKET_NAME", "ALTERNATE_EDITOR", "EMACSNATIVELOADPATH", "EMACSLOADPATH"]:
            self.env.pop(key, None)
        self.env.update(HOME=str(self.home), XDG_CONFIG_HOME=str(self.home / ".config"),
                        XDG_CACHE_HOME=str(self.home / ".cache"), XDG_DATA_HOME=str(self.home / ".local/share"),
                        XDG_STATE_HOME=str(self.home / ".local/state"), DOOMDIR=str(private),
                        DOOMLOCALDIR=str(self.emacs_dir / ".local"), MACOSX_DEPLOYMENT_TARGET="27.0",
                        TERM="xterm-256color")
        directory = self.home / ".local/state/cdev-emacs"
        directory.mkdir(mode=0o700, parents=True)
        self.socket = directory / "server"
        self.log = (self.root / "daemon.log").open("w")
        self.process = None
        self.clients = []
        self.frame_clients = {}
        self.stop = threading.Event()

    def start(self):
        self.process = subprocess.Popen([sys.executable, "-B", str(REPO / "configs/cdev/doom-server.py"),
                                         "serve", "--socket", str(self.socket), "--emacs-dir", str(self.emacs_dir)],
                                        env=self.env, cwd=self.root, stdout=self.log, stderr=self.log)
        until = time.monotonic() + 35
        while time.monotonic() < until and self.process.poll() is None:
            if self.socket.exists():
                result = self.request("(and (featurep 'dotfiles-cdev) (bound-and-true-p persp-mode) t)", check=False)
                if result.returncode == 0 and result.stdout.strip() == "t":
                    return
            time.sleep(0.1)
        raise AssertionError("Disposable Doom failed: " + (self.root / "daemon.log").read_text()[-3500:])

    def request(self, expression, check=True):
        result = subprocess.run(["/opt/homebrew/bin/emacsclient", "-s", str(self.socket),
                                 "-a", "/usr/bin/false", "-e", expression],
                                env=self.env, text=True, capture_output=True, timeout=10)
        if check and result.returncode:
            raise AssertionError(result.stderr + result.stdout)
        return result

    def data(self, expression):
        return json.loads(json.loads(self.request("(json-encode " + expression + ")").stdout))

    def terminal(self, root, command):
        child, fd = pty.fork()
        if child == 0:
            os.chdir(root)
            os.execve(command[0], command, self.env)
        self.clients.append((child, fd))
        def drain():
            while not self.stop.is_set():
                try:
                    if select.select([fd], [], [], 0.1)[0]:
                        data = os.read(fd, 65536)
                        if not data:
                            return
                        if b'\x1b[6n' in data:
                            os.write(fd, b'\x1b[1;1R')
                        if b'\x1b[c' in data or b'\x1b[0c' in data:
                            os.write(fd, b'\x1b[?1;2c')
                        if b'\x1b[>c' in data:
                            os.write(fd, b'\x1b[>0;1;0c')
                except OSError:
                    return
        threading.Thread(target=drain, daemon=True).start()
        return child, fd

    def start_standalone(self, root):
        # Same sanitized Doom startup, but a real -nw process rather than a
        # daemon/client. The private server is only an observation/control path.
        expression = "(progn (require 'server) (setq server-name " + json.dumps(str(self.socket)) + ") (server-start))"
        child, fd = self.terminal(root, ["/opt/homebrew/bin/emacs", "--init-directory", str(self.emacs_dir),
                                       "-nw", "--load", str(REPO / "configs/doom/clipboard.el"),
                                       "--eval", expression])
        until = time.monotonic() + 35
        while time.monotonic() < until:
            if self.socket.exists():
                result = self.request("(featurep 'dotfiles-clipboard)", check=False)
                if result.returncode == 0 and result.stdout.strip() == "t":
                    return child, fd
            time.sleep(.1)
        raise AssertionError("disposable standalone Doom did not initialize")

    def connect(self, root):
        parameters = "((cdev-project-root . " + json.dumps(str(root)) + "))"
        child, fd = self.terminal(root, ["/opt/homebrew/bin/emacsclient", "-s", str(self.socket), "-a", "/usr/bin/false",
                                       "-t", "--frame-parameters=" + parameters])
        self.frame_clients[str(root)] = (child, fd)
        until = time.monotonic() + 10
        while time.monotonic() < until:
            if self.data("(length (cl-remove-if-not (lambda (f) (equal (frame-parameter f 'cdev-project-root) "
                         + json.dumps(str(root) + "/") + ")) (frame-list)))") == 1:
                return child, fd
            time.sleep(0.1)
        raise AssertionError("terminal client frame did not initialize")

    def frame(self, root, body):
        return self.data("(with-selected-frame (cl-find " + json.dumps(str(root) + "/")
                         + " (frame-list) :key (lambda (f) (frame-parameter f 'cdev-project-root)) :test #'equal) "
                         + "(with-selected-window (frame-selected-window) " + body + "))")

    def picker(self, root, keys=b" ff"):
        # Execute the real leader keys on the frame's own terminal. An eval
        # client cannot legally enter another terminal's locked minibuffer.
        self.request("""(defun dotfiles-test-picker-probe ()
          (set-frame-parameter nil 'cdev-picker-probe
            (list default-directory (bound-and-true-p ivy--directory)))
          (remove-hook 'minibuffer-setup-hook #'dotfiles-test-picker-probe)
          (abort-recursive-edit))""")
        self.frame(root, """(progn (set-frame-parameter nil 'cdev-picker-probe nil)
          (evil-normal-state)
          (add-hook 'minibuffer-setup-hook #'dotfiles-test-picker-probe) t)""")
        os.write(self.frame_clients[str(root)][1], keys)
        until = time.monotonic() + 5
        while time.monotonic() < until:
            result = self.frame(root, "(frame-parameter nil 'cdev-picker-probe)")
            if result:
                return result
            time.sleep(0.1)
        raise AssertionError("SPC f f did not enter the file picker")

    def close(self):
        try:
            if self.socket.exists() and self.process is not None and self.process.poll() is None:
                self.request("(kill-emacs)", check=False)  # only our unique private socket
        except (OSError, subprocess.TimeoutExpired):
            pass
        self.stop.set()
        for pid, fd in self.clients:
            try:
                os.close(fd)
            except OSError:
                pass
            try:
                done, _ = os.waitpid(pid, os.WNOHANG)
                if done == 0:
                    os.kill(pid, signal.SIGTERM)
                    os.waitpid(pid, 0)
            except ChildProcessError:
                pass
        if self.process is not None:
            if self.process.poll() is None:
                self.process.terminate()  # only our own manager, never a discovered PID
            self.process.wait(timeout=10)
        self.log.close()
        self.temp.cleanup()
