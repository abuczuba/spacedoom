"""Offline acceptance-fixture preflight, using real cdev and private tmux panes.

No native Codex, editor, authentication, HTTP publisher or production socket is
started. The same per-pane environment wrapper must be kept for real acceptance.
"""
from __future__ import annotations

import json
import importlib.util
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import time


REPO = Path(__file__).resolve().parents[1]
PROBE = REPO / "tests/fixtures/acceptance_probe.py"
UTF8_LOCALE = "en_US.UTF-8"


def verify_utf8(env):
    result = subprocess.run(["/usr/bin/locale", "charmap"], env=env, capture_output=True, text=True, timeout=5)
    if result.returncode or result.stdout.strip().replace("-", "").lower() != "utf8":
        raise RuntimeError("acceptance fixture requires a verified UTF-8 locale")


class AcceptanceHarness:
    def __init__(self, *, source=None, propagate=True, locale_name=UTF8_LOCALE):
        self.temp = tempfile.TemporaryDirectory(prefix="df-accept-", dir="/private/tmp")
        self.root = Path(self.temp.name).resolve()
        self.source = Path(source or os.environ.get("DOTFILES_ACCEPTANCE_SOURCE", REPO)).resolve()
        self.tmux = shutil.which("tmux")
        self.fish = shutil.which("fish")
        if not self.tmux or not self.fish:
            self.temp.cleanup()
            raise RuntimeError("acceptance preflight requires the existing tmux and Fish")
        self.socket = self.root / "tmux.sock"
        self.server_home = self.root / "server-home"
        self.home = self.root / "home"
        self.project = self.root / "project"
        self.config = self.root / "fixture.json"
        self.backend = None
        self.started = False
        for name in ("server-home", "home", "bin", "config/cdev", "state", "cache", "data",
                     "runtime", "tmp", "codex", "proofs", "payload/cdev", "payload/fish"):
            (self.root / name).mkdir(mode=0o700, parents=True, exist_ok=True)
        # Build an environment, rather than copying the agent's credentials,
        # app-server addresses, inherited hook context or developer settings.
        self.env = {
            "HOME": str(self.home), "XDG_CONFIG_HOME": str(self.root / "config"),
            "XDG_STATE_HOME": str(self.root / "state"), "XDG_CACHE_HOME": str(self.root / "cache"),
            "XDG_DATA_HOME": str(self.root / "data"), "XDG_RUNTIME_DIR": str(self.root / "runtime"),
            "CODEX_HOME": str(self.root / "codex"), "TMPDIR": str(self.root / "tmp"),
            "TMP": str(self.root / "tmp"), "TEMP": str(self.root / "tmp"),
            "TMUX_TMPDIR": str(self.root / "runtime"),
            "PATH": str(self.root / "bin") + ":/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            "CDEV_EDITOR_MODE": "standalone", "CDEV_DASHBOARD": "1",
            "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1", "LC_ALL": locale_name, "LANG": locale_name, "TERM": "xterm-256color",
        }
        self.server_env = {"HOME": str(self.server_home), "PATH": "/opt/homebrew/bin:/usr/bin:/bin",
                           "TMPDIR": str(self.root / "tmp"), "TERM": "xterm-256color",
                           "LC_ALL": locale_name, "LANG": locale_name}
        verify_utf8(self.env)
        verify_utf8(self.server_env)
        for name in ("codex_session.py", "activity.py"):
            shutil.copyfile(self.source / "configs/cdev" / name, self.root / "payload/cdev" / name)
        fish = (self.source / "configs/fish/functions/cdev.fish").read_text()
        (self.root / "payload/fish/cdev.fish").write_text(fish.replace("@RELEASE@", str(self.root / "payload")))
        shutil.copyfile(PROBE, self.root / "probe.py")
        (self.root / "codex/config.toml").write_text('cli_auth_credentials_store = "file"\n')
        self.spec = dict(root=str(self.root), env=self.env, tmux=self.tmux, socket=str(self.socket),
                         project=str(self.project),
                         propagate_commands=["new-window", "split-window"] if propagate else [])
        self.config.write_text(json.dumps(self.spec))
        self.config.chmod(0o600)
        for target, role in [("bin/tmux", "tmux"), ("bin/emacs", "editor"), ("bin/codex", "agent"),
                             ("config/cdev/codex_session.py", "helper"), ("config/cdev/activity.py", "event")]:
            path = self.root / target
            path.write_text("#!/bin/sh\nexec /usr/bin/python3 -B " + shlex.quote(str(self.root / "probe.py"))
                            + " " + role + ' "$@"\n')
            # cdev invokes helper.py with Python, not via its shebang.
            if target.endswith(".py"):
                path.write_text("import os, sys\nos.execv('/usr/bin/python3', ['/usr/bin/python3', '-B', "
                                + repr(str(self.root / "probe.py")) + ", " + repr(role) + "] + sys.argv[1:])\n")
            path.chmod(0o700)
        subprocess.run(["git", "init", "-q", "--template=", str(self.project)], env=self.env, check=True)
        try:
            subprocess.run([self.tmux, "-S", str(self.socket), "-f", "/dev/null", "new-session", "-d",
                            "-s", "acceptance", "-x", "160", "-y", "48", "-n", "guard", "/bin/sleep", "120"],
                           env=self.server_env, check=True, capture_output=True, timeout=10)
            self.started = True
            self.tm("set-option", "-g", "default-shell", "/bin/sh")
            self.tm("set-option", "-g", "update-environment", "")
            self.server_before = self.server_markers()
        except BaseException:
            self.close()
            raise

    def tm(self, *args):
        result = subprocess.run([self.tmux, "-N", "-S", str(self.socket), *args], env=self.server_env,
                                text=True, capture_output=True, timeout=10)
        if result.returncode:
            raise RuntimeError("private tmux command failed: " + args[0])
        return result.stdout.rstrip("\n")

    def server_markers(self):
        result = {}
        for key in ("HOME", "XDG_CONFIG_HOME", "XDG_STATE_HOME", "CODEX_HOME", "PATH", "LC_ALL", "LANG"):
            child = subprocess.run([self.tmux, "-N", "-S", str(self.socket), "show-environment", "-g", key],
                                   env=self.server_env, text=True, capture_output=True, timeout=5)
            result[key] = child.stdout.strip() if child.returncode == 0 else None
        return result

    def open(self):
        code = ("/usr/bin/python3 -B " + shlex.quote(str(self.root / "probe.py")) + " control; or exit 91\n"
                "source " + shlex.quote(str(self.root / "payload/fish/cdev.fish")) + "\n"
                "cdev " + shlex.quote(str(self.project)) + "\n"
                "printf '%s\\n' $status > " + shlex.quote(str(self.root / "open-status")) + "\n")
        script = self.root / "open.fish"
        script.write_text(code)
        # The server itself started with a clean allowlist. Keep only its
        # tmux-generated TMUX/TMUX_PANE while replacing the fixture variables.
        command = ["/usr/bin/env", *(key + "=" + value for key, value in self.env.items()),
                   self.fish, "--no-config", str(script)]
        self.tm("new-window", "-d", "-n", "control", "-c", str(self.root), *command)

    def proofs(self, role=None):
        rows = [json.loads(p.read_text()) for p in (self.root / "proofs").glob("*.json")]
        return [row for row in rows if role is None or row["role"] == role]

    def wait(self, condition, timeout=8):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            result = condition()
            if result:
                return result
            time.sleep(.04)
        raise AssertionError("private acceptance fixture did not meet its preflight condition")

    def allow_launcher(self):
        for role in ("control", "plan", "editor", "launcher"):
            assert any(row["ok"] for row in self.proofs(role)), "unverified " + role
        assert not self.proofs("agent")
        assert not (self.root / "state/cdev/pins.json").exists()
        assert self.server_markers() == self.server_before
        (self.root / "allow-launcher").touch(mode=0o600)

    def run_probe(self, role, *args, env=None, input=None):
        return subprocess.run(["/usr/bin/python3", "-B", str(self.root / "probe.py"), role, *args],
                              env=self.env if env is None else env, input=input,
                              text=True, capture_output=True, timeout=10)

    def start_backend_probe(self):
        self.backend = subprocess.Popen(["/usr/bin/python3", "-B", str(self.root / "probe.py"), "backend"],
                                        env=self.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.wait(lambda: any(row["ok"] for row in self.proofs("backend")))

    def install_renderer_callback(self):
        """Install the unchanged renderer through a test-only metadata auditor."""
        source = self.root / "payload/agent-dashboard.py"
        shutil.copyfile(self.source / "configs/tmux/agent-dashboard.py", source)
        shim = self.root / "callback/agent-dashboard.py"
        shim.parent.mkdir(mode=0o700)
        shutil.copyfile(REPO / "tests/fixtures/renderer_callback.py", shim)
        ghostty = self.root / "config/ghostty/config.ghostty"
        ghostty.parent.mkdir(mode=0o700)
        shutil.copyfile(self.source / "configs/ghostty/config.ghostty", ghostty)
        spec = importlib.util.spec_from_file_location("acceptance_renderer", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.__file__ = str(shim)  # Only the installed callback path is rebased.
        view = module.Dashboard(str(self.socket), state=self.root / "state", ghostty_config=ghostty)
        # Reproduce the prior UTF-8 installer / C callback mismatch in the
        # negative test. The corrected fixture uses UTF-8 at BOTH boundaries.
        view.env = self.env | {"LC_ALL": UTF8_LOCALE, "LANG": UTF8_LOCALE}
        for option in ("window-status-format", "window-status-current-format"):
            self.tm("set-option", "-gw", option, " #I" + module.TITLE_SLOT)
        for option, value in (("@tmux-dotbar-fg", "#85868c"), ("@tmux-dotbar-fg-current", "#ffffff"),
                              ("@tmux-dotbar-bg", "#1f1d2e")):
            self.tm("set-option", "-g", option, value)
        view.install()

    def callback_audits(self):
        path = self.root / "callback.jsonl"
        return [json.loads(line) for line in path.read_text().splitlines() if line] if path.exists() else []

    def close(self):
        (self.root / "stop").touch(exist_ok=True)
        if self.backend is not None:
            self.backend.wait(timeout=5)
        if self.started:
            # Only the private socket/session created above, even after assertion failure.
            subprocess.run([self.tmux, "-N", "-S", str(self.socket), "kill-session", "-t", "=acceptance"],
                           env=self.server_env, capture_output=True, timeout=10)
        self.temp.cleanup()
