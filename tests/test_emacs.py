from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import time
import shlex
import unittest
from unittest.mock import patch

from doom_harness import DoomHarness, REPO
from cdev_harness import CdevHarness
from activity_harness import context, dispatch, enable_driver

SPEC = importlib.util.spec_from_file_location("doom_server", REPO / "configs/cdev/doom-server.py")
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)
INTEGRATION = os.environ.get("DOTFILES_INTEGRATION") == "1"


class EmacsManagerTests(unittest.TestCase):
    def test_unavailable_and_unsafe_socket_never_start_a_server(self):
        with tempfile.TemporaryDirectory(prefix="df-server-") as directory:
            path = Path(directory).resolve() / "server"
            with patch.object(server.subprocess, "Popen") as popen:
                with self.assertRaises(server.ServerError):
                    server.check(path)
                path.write_text("not a socket")
                with self.assertRaises(server.ServerError):
                    server.check(path)
                popen.assert_not_called()
            path.unlink()
            path.symlink_to("missing")
            with self.assertRaises(server.ServerError):
                server.check(path)

    def test_terminal_command_encodes_project_as_data_and_disables_fallback(self):
        with tempfile.TemporaryDirectory(prefix="df-project-") as directory:
            root = Path(directory).resolve() / 'a "quoted" project'
            root.mkdir()
            command = server.client_command(Path("/private/tmp/owned/server"), root)
            self.assertIn("-t", command)
            self.assertNotIn("-n", command)
            self.assertIn("--alternate-editor=/usr/bin/false", command)
            self.assertIn(json.dumps(str(root)), command[-1])


@unittest.skipUnless(INTEGRATION, "Use --integration for a disposable Doom daemon and terminal clients")
class DoomIntegration(unittest.TestCase):
    def test_two_terminal_frames_project_navigation_persistence_and_recovery(self):
        harness = DoomHarness()
        self.addCleanup(harness.close)
        harness.start()
        identity = harness.data("(list (emacs-pid) (daemonp) (featurep 'evil) (featurep 'persp-mode) (symbol-name doom-theme))")
        self.assertTrue(all(identity[1:4]), identity)
        self.assertEqual(identity[-1], "spacemacs-dark")
        roots = [harness.root / "project a", harness.root / "project b"]
        for root in roots:
            (root / "nested").mkdir(parents=True)
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            (root / "nested/example.txt").write_text(root.name)
            harness.connect(root)
        a, b = roots
        names = [harness.frame(root, "(+workspace-current-name)") for root in roots]
        self.assertNotEqual(*names)
        self.assertEqual(harness.frame(a, "(symbol-name (lookup-key doom-leader-map (kbd \"f f\")))"),
                         "dotfiles/cdev-find-file")
        for root in roots:
            # Actual Ivy remapping and minibuffer entry, not just a stubbed
            # directory function. A nested file retains its buffer directory.
            harness.frame(root, "(progn (find-file " + json.dumps(str(root / "nested/example.txt")) + ") t)")
            before = harness.frame(root, "default-directory")
            self.assertIn(str(root) + "/", harness.picker(root))
            self.assertEqual(harness.frame(root, "default-directory"), before)
            self.assertEqual(before, str(root / "nested") + "/")
            self.assertIn(str(root / "nested") + "/", harness.picker(root, b"\x18\x06"))
            self.assertEqual(harness.frame(root, "(symbol-name (command-remapping #'find-file))"), "counsel-find-file")
        # Switching A's native workspace leaves B's workspace and root alone.
        harness.frame(a, '(progn (+workspace-switch "extra-a" t) (switch-to-buffer (get-buffer-create "*scratch-a*")) t)')
        self.assertEqual(harness.frame(b, "(+workspace-current-name)"), names[1])
        # Explicit cross-project file navigation is allowed without reassociating
        # either frame, and the local finder still starts at that file's directory.
        harness.frame(a, "(progn (find-file " + json.dumps(str(b / "nested/example.txt")) + ") t)")
        self.assertIn(str(b / "nested") + "/", harness.picker(a, b"\x18\x06"))
        self.assertIn(str(a) + "/", harness.picker(a))
        self.assertEqual(harness.frame(b, "(+workspace-current-name)"), names[1])
        self.assertEqual(harness.frame(a, "(frame-parameter nil 'cdev-project-root)"), str(a) + "/")
        # File picker root is stable even in a scratch buffer/another workspace.
        self.assertIn(str(a) + "/", harness.picker(a))
        harness.frame(a, "(+workspace-switch " + json.dumps(names[0]) + ")")
        harness.frame(a, '(progn (switch-to-buffer (get-buffer-create "*persistent-a*")) (insert "persistent unsaved text") t)')
        harness.frame(a, "(progn (delete-frame nil t) t)")
        self.assertEqual(harness.data("(emacs-pid)"), identity[0])
        self.assertEqual(harness.frame(b, "(+workspace-current-name)"), names[1])
        self.assertEqual(harness.data('(with-current-buffer "*persistent-a*" (buffer-string))'), "persistent unsaved text")
        harness.connect(a)
        self.assertEqual(harness.frame(a, "(+workspace-current-name)"), names[0])
        self.assertIn(str(a) + "/", harness.picker(a))
        self.assertEqual(harness.data('(with-current-buffer "*persistent-a*" (buffer-string))'), "persistent unsaved text")
        server.check(harness.socket)
        # Duplicate management cannot create another Emacs instance.
        duplicate = subprocess.run(["python3", "-B", str(REPO / "configs/cdev/doom-server.py"), "serve",
                                     "--socket", str(harness.socket), "--emacs-dir", str(harness.emacs_dir)],
                                    env=harness.env, text=True, capture_output=True, timeout=5)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn("no duplicate", duplicate.stderr)
        self.assertEqual(harness.data("(emacs-pid)"), identity[0])

    def test_real_cdev_layout_dashboard_and_client_pane_close(self):
        doom = DoomHarness()
        self.addCleanup(doom.close)
        doom.start()
        h = CdevHarness(doom)
        self.addCleanup(h.close)
        enable_driver(h)  # Synthetic hook payloads, actual isolated Doom clients.
        h.tm("source-file", str(h.release / "tmux/agent-dashboard.conf"))
        # Dotbar's title slot contract, without executing any installed plugin.
        title_slot = h.tm("show-options", "-gqv", "@tmux-dotbar-window-status-format").strip()
        h.tm("set-option", "-g", "window-status-format", title_slot)
        h.tm("set-option", "-g", "window-status-current-format", title_slot)
        roots = [h.repo("combined-a"), h.repo("combined-b")]
        for root in roots:
            result = h.cdev(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        until = time.monotonic() + 8
        while time.monotonic() < until:
            if doom.data("(length (cl-remove-if-not (lambda (f) (frame-parameter f 'cdev-project-root)) (frame-list)))") == 2:
                break
            time.sleep(.1)
        for root in roots:
            self.assertEqual(doom.frame(root, "(frame-parameter nil 'cdev-project-root)"), str(root) + "/")
        snapshot = h.snapshot()
        self.assertEqual(h.cdev(roots[0]).returncode, 0)
        self.assertEqual(h.snapshot(), snapshot)
        self.assertEqual(len(h.log()), 2)
        first = h.window(roots[0])
        panes = h.tm("list-panes", "-t", first, "-F", "#{pane_id}").splitlines()
        context(h, panes[1])
        for event, expected in [("UserPromptSubmit", "#751b25"), ("PermissionRequest", "#a50021"), ("Stop", "●")]:
            result = dispatch(h, panes[1], event=event, session="combined-thread", turn="combined-turn")
            self.assertEqual(result["code"], 0, result["stderr"])
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if expected in h.tm("show-options", "-wqv", "-t", first, "@dotfiles-agent"):
                    break
                time.sleep(.1)
            self.assertIn(expected, h.tm("show-options", "-wqv", "-t", first, "@dotfiles-agent"))
        h.tm("select-window", "-t", "@0")
        binding = h.tm("list-keys", "-T", "prefix", "n")
        h.tm(*shlex.split(binding)[4:])
        self.assertEqual(h.tm("display-message", "-p", "#{pane_id}").strip(), panes[1])
        pid = doom.data("(emacs-pid)")
        doom.frame(roots[0], '(progn (switch-to-buffer (get-buffer-create "*pane-close-test*")) (insert "retained") t)')
        h.tm("kill-pane", "-t", panes[0])  # explicitly owned client pane only
        time.sleep(.2)
        self.assertEqual(doom.data("(emacs-pid)"), pid)
        self.assertEqual(doom.data('(with-current-buffer "*pane-close-test*" (buffer-string))'), "retained")
        self.assertTrue(doom.frame(roots[1], "(+workspace-current-name)"))
        # The right-hand Codex stand-in remains alive and cdev does not respawn it.
        self.assertEqual(h.tm("display-message", "-p", "-t", panes[1], "#{pane_dead}").strip(), "0")
        self.assertEqual(h.cdev(roots[0]).returncode, 0)
        self.assertEqual(len(h.log()), 2)

    def test_installed_native_compiler_with_terminal_macos_workaround(self):
        with tempfile.TemporaryDirectory(prefix="df-native-", dir="/private/tmp") as directory:
            root = Path(directory)
            source = root / "example.el"
            source.write_text(";;; -*- lexical-binding: t; -*-\n(defun dotfiles-native-test () 42)\n")
            expression = "(progn (require 'comp) (native-compile " + json.dumps(str(source)) + ") (princ \"native-ok\"))"
            env = os.environ.copy() | {"HOME": str(root), "XDG_CONFIG_HOME": str(root),
                "XDG_CACHE_HOME": str(root / "cache"), "XDG_STATE_HOME": str(root / "state"), "XDG_DATA_HOME": str(root / "data"),
                "MACOSX_DEPLOYMENT_TARGET": "27.0", "LIBRARY_PATH": ":".join(
                    "/Applications/Emacs.app/Contents/MacOS/lib-arm64-11/libgccjit/" + x
                    for x in ["", "apple-darwin", "sdk-libs"])}
            for key in ["EMACSNATIVELOADPATH", "EMACSLOADPATH", "EMACS_SERVER_FILE", "EMACS_SOCKET_NAME"]:
                env.pop(key, None)
            result = subprocess.run(["emacs", "-Q", "--batch", "--eval", expression],
                                    cwd=root, env=env, text=True, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("native-ok", result.stdout)
