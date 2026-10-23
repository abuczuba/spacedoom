"""Real terminal dashboards and non-dashboard buffers in owned Doom instances."""
import json
import os
import unittest

from doom_harness import DoomHarness


@unittest.skipUnless(os.environ.get('DOTFILES_INTEGRATION') == '1', 'disposable Doom terminals')
class DashboardFacesTests(unittest.TestCase):
    def verify_dashboard(self, h, evaluate):
        evaluate("(progn (switch-to-buffer (doom-fallback-buffer)) (+dashboard-reload t) t)")
        appearance = """(list
          :body (plist-get (cadr (assq 'default face-remapping-alist)) :background)
          :fringe (plist-get (cadr (assq 'fringe face-remapping-alist)) :background)
          :original (face-background 'font-lock-comment-face nil t)
          :solaire-background (face-background 'solaire-default-face nil t)
          :remaps (length dotfiles-dashboard-background-remaps)
          :banner (list (face-attribute '+dashboard-banner :inherit nil nil)
                        (face-background '+dashboard-banner nil t)
                        (face-foreground '+dashboard-banner nil t))
          :loaded (list (face-attribute '+dashboard-loaded :inherit nil nil)
                        (face-background '+dashboard-loaded nil t)
                        (face-foreground '+dashboard-loaded nil t))
          :cyan (face-foreground 'font-lock-comment-face nil t))"""
        state = evaluate(appearance)
        self.assertEqual(state['body'], state['original'])
        self.assertEqual(state['fringe'], state['original'])
        self.assertNotEqual(state['body'], state['solaire-background'])
        self.assertEqual(state['remaps'], 2)
        for key in ['banner', 'loaded']:
            self.assertEqual(state[key], ['font-lock-comment-face', state['original'], state['cyan']])
        global_faces = evaluate("(mapcar #'face-all-attributes '(default font-lock-comment-face solaire-default-face +dashboard-menu-title +dashboard-menu-desc))")
        before = evaluate("(list (buffer-string) +dashboard-functions)")
        # Both reactivation and theme refresh must retain the lighter full-buffer
        # default, with exactly two local cookies and no text/layout changes.
        evaluate("(progn (solaire-mode -1) (solaire-mode 1) t)")
        h.request("(dotfiles-dashboard-background-refresh-h)")
        self.assertEqual(evaluate(appearance), state)
        self.assertEqual(evaluate("(list (buffer-string) +dashboard-functions)"), before)
        self.assertEqual(evaluate("(mapcar #'face-all-attributes '(default font-lock-comment-face solaire-default-face +dashboard-menu-title +dashboard-menu-desc))"), global_faces)
        self.assertEqual(evaluate("(symbol-name (lookup-key doom-leader-map (kbd \"y\")))"), 'dotfiles/copy-visual-to-clipboard')

    def test_standalone_terminal_dashboard(self):
        h = DoomHarness(dashboard_faces=True)
        self.addCleanup(h.close)
        h.start_standalone(h.root)
        self.verify_dashboard(h, lambda body: h.data('(with-selected-window (frame-selected-window) '+body+')'))
        h.request('(kill-emacs)', check=False)

    def test_new_client_dashboard_preserves_file_org_vterm_and_other_frame(self):
        h = DoomHarness(dashboard_faces=True)
        self.addCleanup(h.close)
        h.start()
        roots = [h.root/'project-a', h.root/'project-b']
        for root in roots:
            root.mkdir()
            h.connect(root)
        plain, org = roots[1]/'plain.txt', roots[1]/'note.org'
        plain.write_text('ordinary file\n'); org.write_text('* ordinary heading\n')
        for path in [plain, org]:
            h.frame(roots[1], '(progn (find-file '+json.dumps(str(path))+') t)')
        # The installed native module is required first: never offer to build it.
        h.frame(roots[1], """(progn (require 'vterm-module) (require 'vterm)
          (switch-to-buffer (get-buffer-create "*scope-vterm*"))
          (let ((vterm-shell "/bin/sh") (process-environment (cons "ENV=/dev/null" process-environment)))
            (vterm-mode))
          (set-process-query-on-exit-flag (get-buffer-process (current-buffer)) nil) t)""")
        snapshot = """(mapcar (lambda (name) (json-encode (with-current-buffer name
          (list :mode major-mode :solaire solaire-mode :faces face-remapping-alist
                :local (local-variable-p 'dotfiles-dashboard-background-remaps)))))
          '("plain.txt" "note.org" "*scope-vterm*"))"""
        before = h.frame(roots[1], snapshot)
        decoded = [json.loads(entry) for entry in before]
        self.assertEqual([entry['mode'] for entry in decoded], ['text-mode', 'org-mode', 'vterm-mode'])
        self.assertTrue(all(not entry['local'] for entry in decoded))
        frame_before = h.frame(roots[1], "(list (buffer-name) (face-all-attributes 'default))")
        self.verify_dashboard(h, lambda body: h.frame(roots[0], body))
        self.assertEqual(h.frame(roots[1], snapshot), before)
        self.assertEqual(h.frame(roots[1], "(list (buffer-name) (face-all-attributes 'default))"), frame_before)
