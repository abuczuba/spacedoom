;; Extend the original ASCII/banner charcoal across the dashboard only.
(require 'face-remap)
(defvar-local dotfiles-dashboard-background-remaps nil)

(defun dotfiles-dashboard-background-h ()
  (when (eq major-mode '+dashboard-mode)
    (let ((background (face-background 'font-lock-comment-face nil t)))
      (mapc #'face-remap-remove-relative dotfiles-dashboard-background-remaps)
      (setq dotfiles-dashboard-background-remaps
            (mapcar (lambda (face)
                      (face-remap-add-relative face `(:background ,background)))
                    '(default fringe))))))

(defun dotfiles-dashboard-background-refresh-h ()
  (dolist (buffer (buffer-list))
    (with-current-buffer buffer
      (dotfiles-dashboard-background-h))))

(add-hook '+dashboard-mode-hook #'dotfiles-dashboard-background-h t)
;; Run after Solaire remaps its faces, so its darker default cannot cover ours.
(add-hook 'solaire-mode-hook #'dotfiles-dashboard-background-h t)
(add-hook 'doom-load-theme-hook #'dotfiles-dashboard-background-refresh-h 100)
(dotfiles-dashboard-background-refresh-h)
