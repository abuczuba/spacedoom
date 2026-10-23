"""Real terminal Doom dashboards; no production frames or font changes."""
import os
import unittest

from doom_harness import DoomHarness


@unittest.skipUnless(os.environ.get('DOTFILES_INTEGRATION') == '1', 'disposable Doom terminals')
class DashboardFacesTests(unittest.TestCase):
    def verify_dashboard(self, h, evaluate):
        evaluate("(progn (switch-to-buffer (doom-fallback-buffer)) (+dashboard-reload t) t)")
        state = evaluate("""(list
          :mode major-mode :solaire solaire-mode
          :default-background (face-attribute 'default :background nil t)
          :buffer-default (cdr (assq 'default face-remapping-alist))
          :comment-background (face-attribute 'font-lock-comment-face :background nil t)
          :banner (list (face-attribute '+dashboard-banner :inherit nil nil)
                        (face-attribute '+dashboard-banner :background nil nil)
                        (face-attribute '+dashboard-banner :foreground nil t))
          :loaded (list (face-attribute '+dashboard-loaded :inherit nil nil)
                        (face-attribute '+dashboard-loaded :background nil nil)
                        (face-attribute '+dashboard-loaded :foreground nil t))
          :comment-foreground (face-attribute 'font-lock-comment-face :foreground nil t))""")
        values = state if isinstance(state, dict) else dict(zip(state[::2], state[1::2]))
        self.assertEqual(values['mode'], '+dashboard-mode')
        self.assertTrue(values['solaire'])
        self.assertIn('solaire-default-face', values['buffer-default'])
        for key in ['banner', 'loaded']:
            self.assertEqual(values[key], [None, 'unspecified', values['comment-foreground']])
        # The comment face keeps its original explicit background. Only the two
        # dashboard faces lose it, letting the remapped buffer default show.
        self.assertNotEqual(values['comment-background'], 'unspecified')
        self.assertEqual(evaluate("(get-text-property (string-match \"=\" (+dashboard-draw-ascii-banner-fn)) 'face (+dashboard-draw-ascii-banner-fn))"),
                         '+dashboard-banner')
        before = evaluate("(list (buffer-string) +dashboard-functions face-remapping-alist)")
        # A theme customization refresh must preserve text/layout and global
        # theme/comment/background properties as well as the fixed faces.
        h.request("(run-hooks 'doom-customize-theme-hook)")
        self.assertEqual(evaluate("(list (buffer-string) +dashboard-functions face-remapping-alist)"), before)
        self.assertEqual(evaluate("(face-attribute 'default :background nil t)"), values['default-background'])
        self.assertEqual(evaluate("(face-attribute 'font-lock-comment-face :background nil t)"), values['comment-background'])
        self.assertEqual(evaluate("(symbol-name (lookup-key doom-leader-map (kbd \"y\")))"), 'dotfiles/copy-visual-to-clipboard')
        # Independent runtime rollback removes only these user face specs.
        h.request("""(let ((callback (cl-find-if
          (lambda (fn) (and (symbolp fn) (fboundp fn)
            (string-match-p (regexp-quote "+dashboard-banner") (prin1-to-string (symbol-function fn)))))
          doom-customize-theme-hook)))
          (unless callback (error "expected cosmetic callback"))
          (remove-hook 'doom-customize-theme-hook callback)
          (custom-theme-reset-faces 'user '(+dashboard-banner nil) '(+dashboard-loaded nil))
          (dolist (frame (frame-list))
            (face-spec-recalc '+dashboard-banner frame)
            (face-spec-recalc '+dashboard-loaded frame)))""")
        self.assertEqual(evaluate("(face-attribute '+dashboard-banner :inherit nil nil)"), 'font-lock-comment-face')
        self.assertEqual(evaluate("(face-attribute '+dashboard-loaded :inherit nil nil)"), 'font-lock-comment-face')

    def test_standalone_terminal_dashboard(self):
        h = DoomHarness(dashboard_faces=True)
        self.addCleanup(h.close)
        h.start_standalone(h.root)
        self.verify_dashboard(h, lambda body: h.data('(with-selected-window (frame-selected-window) '+body+')'))
        h.request('(kill-emacs)', check=False)

    def test_new_terminal_emacsclient_dashboard(self):
        h = DoomHarness(dashboard_faces=True)
        self.addCleanup(h.close)
        h.start()
        root = h.root/'project'
        root.mkdir()
        h.connect(root)
        self.verify_dashboard(h, lambda body: h.frame(root, body))
