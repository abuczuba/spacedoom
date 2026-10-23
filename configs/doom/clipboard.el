;;; clipboard.el --- Terminal-safe visual copying -*- lexical-binding: t; -*-

;; Ghostty owns Cmd+C for terminal selections. Keep that behavior in shell and
;; Codex panes; use the native Doom leader for editor selections instead.
(require 'evil)
(require 'simpleclip)
(require 'rect)

(evil-define-command dotfiles/copy-visual-to-clipboard ()
  "Copy Evil's complete visual selection without changing the kill ring.
Character, line and block selections use Evil's expanded range. Leave the
selection, buffer and ordinary Evil yank bindings unchanged."
  :keep-visual t
  :repeat nil
  (interactive)
  (unless (evil-visual-state-p)
    (user-error "Select text in Evil visual mode first"))
  (let* ((range (evil-visual-range))
         (beg (nth 0 range))
         (end (nth 1 range))
         (text (if (eq (nth 2 range) 'block)
                   (mapconcat #'identity (extract-rectangle beg end) "\n")
                 (buffer-substring-no-properties beg end))))
    (simpleclip-set-contents text)
    (message "Copied visual selection to macOS clipboard")))

(defvar dotfiles-clipboard--installed nil)
(defvar dotfiles-clipboard--previous-binding nil)

(defun dotfiles-clipboard-install ()
  "Install the copy binding, refusing to replace an unrelated leader key."
  (unless (boundp 'doom-leader-map)
    (error "Doom's leader map is unavailable"))
  (let ((current (lookup-key doom-leader-map (kbd "y"))))
    (unless (or (null current) (eq current #'dotfiles/copy-visual-to-clipboard))
      (error "Doom SPC y is already bound; review the clipboard conflict"))
    (unless dotfiles-clipboard--installed
      (setq dotfiles-clipboard--previous-binding current))
    (define-key doom-leader-map (kbd "y") #'dotfiles/copy-visual-to-clipboard)
    (setq dotfiles-clipboard--installed t)))

(defun dotfiles-clipboard-uninstall ()
  "Remove only our binding; never replace a subsequent user binding."
  (interactive)
  (when (eq (lookup-key doom-leader-map (kbd "y")) #'dotfiles/copy-visual-to-clipboard)
    (define-key doom-leader-map (kbd "y") dotfiles-clipboard--previous-binding))
  (setq dotfiles-clipboard--installed nil))

(dotfiles-clipboard-install)
(provide 'dotfiles-clipboard)
;;; clipboard.el ends here
