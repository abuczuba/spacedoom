"""Real disposable Doom terminals; replace only the clipboard transport.

Never inspect or change the user's macOS clipboard, private config or buffers.
"""
import json
import os
import time
import unittest

from doom_harness import DoomHarness, REPO


@unittest.skipUnless(os.environ.get("DOTFILES_INTEGRATION") == "1", "disposable Doom terminals")
class ClipboardTests(unittest.TestCase):
    def check_selection(self, harness, terminal, evaluate, text, beg, end, kind, expected, direction=1):
        evaluate("(progn (evil-normal-state) (switch-to-buffer (get-buffer-create \"*copy-fixture*\"))"
                 " (erase-buffer) (insert " + json.dumps(text) + ")"
                 " (setq dotfiles-test-copied nil kill-ring '(\"kept\") kill-ring-yank-pointer kill-ring)"
                 " (evil-visual-select " + f"{beg} {end} '{kind} {direction}" + ") t)")
        before = evaluate("(list (buffer-string) kill-ring (point) (mark) (symbol-name evil-state))")
        os.write(terminal[1], b" y")  # actual visual-mode Doom leader sequence
        until = time.monotonic() + 5
        while time.monotonic() < until:
            if evaluate("dotfiles-test-copied") is not None:
                break
            time.sleep(.05)
        self.assertEqual(evaluate("dotfiles-test-copied"), expected)
        self.assertEqual(evaluate("(list (buffer-string) kill-ring (point) (mark) (symbol-name evil-state))"), before)

    def stub_clipboard(self, harness):
        harness.request("(progn (defvar dotfiles-test-copied nil)"
                        " (fset 'simpleclip-set-contents (lambda (text) (setq dotfiles-test-copied text))) t)")

    def cases(self, harness, terminal, evaluate):
        self.stub_clipboard(harness)
        self.check_selection(harness, terminal, evaluate, "alpha beta\n", 1, 6, "inclusive", "alpha")
        self.check_selection(harness, terminal, evaluate, "alpha beta\n", 1, 6, "inclusive", "alpha", -1)
        self.check_selection(harness, terminal, evaluate, "alpha beta\nsecond\n", 1, 12, "line", "alpha beta\n")
        self.check_selection(harness, terminal, evaluate, "abcde\nfghij\n", 2, 11, "block", "bcd\nghi")
        evaluate("(progn (evil-normal-state) t)")
        self.assertEqual(evaluate("(symbol-name (key-binding (kbd \"y\")))"), "evil-yank")
        self.assertEqual(evaluate("(condition-case nil (dotfiles/copy-visual-to-clipboard) (user-error \"select first\"))"),
                         "select first")
        # Reload is idempotent; uninstall preserves any later unrelated binding.
        harness.request("(load " + json.dumps(str(REPO / "configs/doom/clipboard.el")) + " nil nil t)")
        self.assertEqual(evaluate("(symbol-name (lookup-key doom-leader-map (kbd \"y\")))"),
                         "dotfiles/copy-visual-to-clipboard")
        harness.request("(progn (dotfiles-clipboard-uninstall) t)")
        self.assertIsNone(evaluate("(lookup-key doom-leader-map (kbd \"y\"))"))
        harness.request("(progn (define-key doom-leader-map (kbd \"y\") 'ignore) t)")
        self.assertEqual(evaluate("(condition-case nil (dotfiles-clipboard-install) (error \"conflict\"))"), "conflict")
        self.assertEqual(evaluate("(symbol-name (lookup-key doom-leader-map (kbd \"y\")))"), "ignore")

    def test_persistent_client_visual_copy_and_other_frame_survives(self):
        h = DoomHarness()
        self.addCleanup(h.close)
        h.start()
        roots = [h.root / "a", h.root / "b"]
        for root in roots:
            root.mkdir()
            h.connect(root)
        other = h.frame(roots[1], "(list (+workspace-current-name) (buffer-name))")
        self.cases(h, h.frame_clients[str(roots[0])], lambda expr: h.frame(roots[0], expr))
        self.assertEqual(h.frame(roots[1], "(list (+workspace-current-name) (buffer-name))"), other)

    def test_standalone_terminal_doom_visual_copy(self):
        h = DoomHarness()
        self.addCleanup(h.close)
        terminal = h.start_standalone(h.root)
        self.assertIsNone(h.data("(daemonp)"))
        self.assertTrue(h.data("(featurep 'evil)"))
        self.cases(h, terminal, h.data)
        h.request("(kill-emacs)", check=False)  # only our own standalone process
