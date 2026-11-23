"""Normal Doom startup from the complete public source in disposable terminals."""
import os
import time
import unittest

from doom_harness import DoomHarness


@unittest.skipUnless(os.environ.get('DOTFILES_INTEGRATION') == '1', 'owned full-config Doom instances')
class PersonalDoomTests(unittest.TestCase):
    def verify(self, h):
        data = h.data("""(list :theme doom-theme
          :clipboard (symbol-name (lookup-key doom-leader-map (kbd "y")))
          :org-root org-directory :theme-org spacemacs-theme-org-highlight
          :agenda (mapcar #'expand-file-name org-agenda-files)
          :faces (fboundp 'dotfiles-dashboard-background-h)
          :identity user-mail-address)""")
        self.assertEqual(data['theme'], 'spacemacs-dark')
        self.assertEqual(data['clipboard'], 'dotfiles/copy-visual-to-clipboard')
        self.assertTrue(data['faces'])
        self.assertFalse(data['theme-org'])
        self.assertTrue(all(path.startswith(str(h.home) + '/') for path in (data['agenda'] or [])))
        self.assertFalse((h.home / 'org').exists())  # No private Org documents were loaded.
        self.assertEqual(data['identity'], 'fixture@example.org')

    def harness(self):
        h = DoomHarness(personal_config=True)
        self.addCleanup(h.close)
        (h.home / '.config/doom/identity.el').write_text('(setq user-mail-address "fixture@example.org")\n')
        return h

    def test_complete_config_with_terminal_clients(self):
        h = self.harness()
        h.start()
        for name in ['project-one', 'project-two']:
            root = h.root / name
            root.mkdir()
            h.connect(root)
        self.verify(h)
        self.assertTrue(h.data("(featurep 'dotfiles-cdev)"))

    def test_complete_config_with_standalone_terminal(self):
        h = self.harness()
        h.start_standalone(h.root)
        self.verify(h)

    def test_kj_exits_insert_mode_without_inserting_the_chord(self):
        h = self.harness()
        h.start()
        root = h.root / 'escape-project'
        root.mkdir()
        _, terminal = h.connect(root)
        h.frame(root, '(progn (fundamental-mode) (erase-buffer) (evil-normal-state) t)')

        def wait_for(state):
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if h.frame(root, '(symbol-name evil-state)') == state:
                    return
                time.sleep(.05)
            self.fail('Expected Evil state: ' + state)

        os.write(terminal, b'i')
        wait_for('insert')
        os.write(terminal, b'kj')
        wait_for('normal')
        self.assertEqual(h.frame(root, '(buffer-string)'), '')
        self.assertEqual(h.frame(root, 'evil-escape-key-sequence'), 'kj')

        # A k not followed promptly by j remains ordinary text.
        os.write(terminal, b'i')
        wait_for('insert')
        os.write(terminal, b'k')
        time.sleep(.3)
        os.write(terminal, b'j')
        deadline = time.monotonic() + 5
        while h.frame(root, '(buffer-string)') != 'kj' and time.monotonic() < deadline:
            time.sleep(.05)
        self.assertEqual(h.frame(root, '(symbol-name evil-state)'), 'insert')
        self.assertEqual(h.frame(root, '(buffer-string)'), 'kj')
