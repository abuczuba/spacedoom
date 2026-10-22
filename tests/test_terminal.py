from __future__ import annotations

import errno
import json
import os
from pathlib import Path
import pty
import re
import select
import shlex
import signal
import stat
import struct
import subprocess
import tempfile
import termios
import time
import unittest
import fcntl
from unittest.mock import patch

from deploy import Deployment
from validation import private_tmux, syntax_checks, ValidationError


REPO = Path(__file__).resolve().parents[1]
INTEGRATION = os.environ.get("DOTFILES_INTEGRATION") == "1"


@unittest.skipUnless(INTEGRATION, "Use scripts/test.py --integration for private tmux/PTY tests")
class TmuxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dotfiles-binding-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name).resolve()
        self.server = private_tmux()
        self.tmux = self.server.__enter__()
        self.addCleanup(lambda: self.server.__exit__(None, None, None))
        self.tmux("set-option", "-g", "base-index", "1")
        self.tmux("move-window", "-r")
        self.tmux("set-option", "-g", "renumber-windows", "on")
        defaults = self.tmux("list-keys", "-T", "prefix")
        for key in ("M-h", "M-l"):
            self.assertFalse(any(shlex.split(line)[3] == key for line in defaults.splitlines()),
                             f"Reordering key {key} conflicts with an installed default")
        self.assertIn("switch-client -l", self.tmux("list-keys", "-T", "prefix", "L"))
        source = (REPO / "configs/tmux/czuba-navigation.conf").read_text()
        overlay = self.directory / "navigation.conf"
        overlay.write_text(source.replace("@RELEASE@", str(self.directory)))
        self.tmux("source-file", str(overlay))

    def windows(self):
        output = self.tmux("list-windows", "-F", "#{window_id}|#{window_index}|#{window_name}|#{window_active}")
        return [line.split("|") for line in output.splitlines()]

    def press(self, key):
        # Execute exactly the command read back from the installed test binding.
        binding = self.tmux("list-keys", "-T", "prefix", key).strip()
        body = re.split(r"\s+", binding, maxsplit=4)[4]
        command_file = self.directory / "keypress.conf"
        command_file.write_text(body + "\n")
        try:
            self.tmux("source-file", str(command_file))
        except ValidationError as exc:
            self.fail(f"Private test binding failed: {exc.diagnostics}")

    def three(self):
        self.tmux("new-window", "-d", "-n", "two", "/bin/sleep 120")
        self.tmux("new-window", "-d", "-n", "three", "/bin/sleep 120")
        windows = self.windows()
        self.tmux("select-window", "-t", windows[1][0])
        return {window[2]: window[0] for window in windows}

    def assert_order(self, names, active):
        windows = self.windows()
        self.assertEqual([window[2] for window in windows], names)
        self.assertEqual([int(window[1]) for window in windows], list(range(1, len(names) + 1)))
        self.assertEqual([window[0] for window in windows if window[3] == "1"], [active])

    def test_adjacent_moves_preserve_focus_and_number_selection(self):
        ids = self.three()
        self.press("M-h")
        self.assert_order(["two", "one", "three"], ids["two"])
        self.press("M-l")
        self.assert_order(["one", "two", "three"], ids["two"])
        self.press("M-l")
        self.assert_order(["one", "three", "two"], ids["two"])
        self.press("2")
        self.assert_order(["one", "three", "two"], ids["three"])
        self.assertIn("switch-client -l", self.tmux("list-keys", "-T", "prefix", "L"))

    def test_first_last_and_single_window_do_not_wrap(self):
        only = self.windows()[0][0]
        for key in ("M-h", "M-l"):
            self.press(key)
            self.assert_order(["one"], only)
        ids = self.three()
        self.tmux("select-window", "-t", ids["one"])
        self.press("M-h")
        self.assert_order(["one", "two", "three"], ids["one"])
        self.tmux("select-window", "-t", ids["three"])
        self.press("M-l")
        self.assert_order(["one", "two", "three"], ids["three"])

    def test_gaps_are_renumbered_and_marked_window_is_not_moved(self):
        ids = self.three()
        self.tmux("set-option", "-g", "renumber-windows", "off")
        self.tmux("move-window", "-s", ids["two"], "-t", ":5")
        self.tmux("move-window", "-s", ids["three"], "-t", ":9")
        self.tmux("select-pane", "-m", "-t", ids["one"])
        self.tmux("select-window", "-t", ids["two"])
        self.press("M-l")
        self.assert_order(["one", "three", "two"], ids["two"])

    def test_popup_binding_has_local_styles_and_preserved_invocation(self):
        binding = self.tmux("list-keys", "-T", "prefix", "?")
        for color in ("#20242b", "#f3e8d2", "#264f78"):
            self.assertIn(color, binding)
        config = (REPO / "configs/ghostty/config.ghostty").read_text()
        self.assertIn(r"keybind = super+shift+p=text:\x06?", config)


@unittest.skipUnless(INTEGRATION, "Use scripts/test.py --integration for private tmux/PTY tests")
class ParserTests(unittest.TestCase):
    def test_complete_release_migration_and_restore_with_actual_templates(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-full-release-") as folder:
            directory = Path(folder).resolve()
            home = directory / "home"
            home.mkdir()
            originals = {
                ".tmux.conf": (b"# original fixture\n", 0o640),
                ".config/tmux/czuba-navigation.conf": (b"# original navigation\n", 0o600),
                ".config/tmux/cheatsheet.txt": (b"original shortcuts\n", 0o644),
            }
            helpers = (".config/tmux/show-shortcuts.sh", ".config/tmux/shortcuts.lesskey")
            for name, (data, mode) in originals.items():
                path = home / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                path.chmod(mode)
            for name in ("tmux-dotbar/dotbar.tmux", "tpm/tpm"):
                path = home / ".tmux/plugins" / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("#!/bin/sh\nexit 99\n")
                path.chmod(0o755)
            deployment = Deployment(REPO, home, directory / "active release")
            with deployment.locked():
                release = deployment.stage()
                backup = deployment.migrate(release, "tmux")
                self.assertEqual(deployment.current(), release)
                journal = json.loads((deployment.root / "backups" / backup / "backup.json").read_text())
                self.assertIsNone(journal["current_before"])
                self.assertEqual(len(journal["entries"]), 5)
                self.assertEqual(sum(item["existed"] for item in journal["entries"]), 3)
                for item in journal["entries"]:
                    path = home / item["target"]
                    self.assertEqual(os.readlink(path), deployment.link_target(item))
                    self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o444)
                for name, (data, mode) in originals.items():
                    saved = deployment.root / "backups" / backup / "files" / name
                    self.assertEqual(saved.read_bytes(), data)
                    self.assertEqual(stat.S_IMODE(saved.stat().st_mode), mode)
                self.assertIn("Ctrl+F -> Alt+h/l", (home / ".config/tmux/cheatsheet.txt").read_text())
                self.assertFalse((home / ".config/ghostty/config.ghostty").exists())
                deployment.restore(backup)
                deployment.restore(backup)
            for name, (data, mode) in originals.items():
                path = home / name
                self.assertFalse(path.is_symlink())
                self.assertEqual(path.read_bytes(), data)
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), mode)
            for name in helpers:
                self.assertFalse(os.path.lexists(home / name))
            self.assertFalse(os.path.lexists(deployment.root / "current"))
            deployment.receipt(release, parse=False)

    def test_complete_rendered_configuration_parses_without_loading_plugins(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-parse-") as folder:
            directory = Path(folder).resolve()
            deployment = Deployment(REPO, directory / "home", directory / "state")
            manifest = deployment.manifest()
            deployment.materialize(directory / "candidate", directory / "candidate", manifest)
            deployment.layout_check(directory / "candidate", manifest, directory / "candidate")
            results = syntax_checks(directory / "candidate", manifest)
            self.assertEqual(len(results), 5)
            self.assertFalse((directory / "state").exists())

    def test_ghostty_validator_rejects_invalid_syntax(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-invalid-") as folder:
            directory = Path(folder)
            (directory / "invalid.ghostty").write_text("font-size = invalid\n")
            with self.assertRaises(ValidationError):
                syntax_checks(directory, {"files": [{"path": "invalid.ghostty", "syntax": "ghostty"}]})

    def test_explicit_ghostty_validation_ignores_default_files(self):
        with tempfile.TemporaryDirectory(prefix="dotfiles-ghostty-defaults-") as folder:
            directory = Path(folder)
            (directory / "defaults/ghostty").mkdir(parents=True)
            for name in ("config", "config.ghostty"):
                (directory / "defaults/ghostty" / name).write_text("font-size = invalid\n")
            (directory / "good.ghostty").write_text("font-size = 12\n")
            with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(directory / "defaults")}):
                syntax_checks(directory, {"files": [{"path": "good.ghostty", "syntax": "ghostty"}]})


@unittest.skipUnless(INTEGRATION, "Use scripts/test.py --integration for private tmux/PTY tests")
class PopupTests(unittest.TestCase):
    def test_renderer_preserves_plaintext_and_uses_accessible_palette(self):
        script = REPO / "configs/tmux/show-shortcuts.sh"
        rendered = subprocess.check_output(["sh", str(script), "--render"])
        original = (script.parent / "cheatsheet.txt").read_bytes()
        stripped = re.sub(rb"\x1b\[[0-9;]*m", b"", rendered)
        self.assertEqual(stripped, original)
        self.assertTrue(original.isascii())
        self.assertNotRegex(original.decode(), r"\bPrefix\b")
        self.assertIn(b"38;2;38;79;120m", rendered)
        self.assertIn(b"38;2;139;58;47m", rendered)

    def test_pager_section_jumps_search_and_quit_in_a_real_pty(self):
        script = REPO / "configs/tmux/show-shortcuts.sh"
        pid, fd = pty.fork()
        if pid == 0:
            env = os.environ.copy()
            env["TERM"] = "xterm-256color"
            os.execve("/bin/sh", ["sh", str(script)], env)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 24, 100, 0, 0))

        def read_until(text):
            output = b""
            until = time.monotonic() + 5
            while time.monotonic() < until:
                ready, _, _ = select.select([fd], [], [], 0.1)
                if ready:
                    try:
                        output += os.read(fd, 65536)
                    except OSError as exc:
                        if exc.errno == errno.EIO:
                            break
                        raise
                    if text.encode() in re.sub(rb"\x1b\[[0-?]*[ -/]*[@-~]", b"", output):
                        return output
            clean = re.sub(rb"\x1b\[[0-?]*[ -/]*[@-~]", b"", output)
            self.fail(f"Pager did not reach {text}; tail: {clean[-750:]!r}")

        reaped = False
        try:
            read_until("SHORTCUTS / TERMINAL + EDITOR")
            for key, title in [(b"2", "@tmux / 2"), (b"8", "@desktop / 8"),
                               (b"4", "@fish / 4"), (b"1", "@daily / 1")]:
                os.write(fd, key)
                read_until(title)
            os.write(fd, b"/literal\n")
            read_until("Send a literal Ctrl+F")
            os.write(fd, b"q")
            until = time.monotonic() + 5
            while time.monotonic() < until:
                # Keep draining the terminal: otherwise a final redraw can fill
                # its output buffer and prevent less from processing q.
                ready, _, _ = select.select([fd], [], [], 0.02)
                if ready:
                    try:
                        os.read(fd, 65536)
                    except OSError as exc:
                        if exc.errno != errno.EIO:
                            raise
                child, status = os.waitpid(pid, os.WNOHANG)
                if child:
                    reaped = True
                    self.assertEqual(os.waitstatus_to_exitcode(status), 0)
                    break
                time.sleep(0.02)
            self.assertTrue(reaped, "Pager did not exit after q")
        finally:
            os.close(fd)
            if not reaped:
                try:
                    os.killpg(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                os.waitpid(pid, 0)
