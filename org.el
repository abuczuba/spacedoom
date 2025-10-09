;;; $DOOMDIR/+org.el -*- lexical-binding: t; -*-

;; thanks andy
;; but what's going on here?
;; ~/dotfiles/doom-emacs/.config/doom/+org.el -*- lexical-binding: t; -*-

  ;; Setup org agenda
;    (custom-set-variables
;     '(org-directory my/org-directory)
;     '(org-agenda-files (list org-directory)))
     (setq org-agenda-files (directory-files-recursively "~/Dropbox/org" "org$"))

(after! org

  ;; Set org file associations
  (setq org-file-apps
      `((auto-mode . emacs)
        (,(rx ".pdf::" (group (one-or-more digit)) string-end) . "zathura %s -P %1")
        (,(rx ".pdf" string-end) . "zathura %s")
        (directory . emacs)))

  ;; org-appear always (and forever) --mncz
(require 'org-appear)
(add-hook 'org-mode-hook #'org-appear-mode)

  ;; browser needs to be set with a separate function
;    commented out, we'll do emacs browser configuration LATER --mncz
; (setq browse-url-browser-function 'browse-url-generic
;       browse-url-generic-program "qutebrowser")

  ;; Don't use blank lines between text and the following heading
;    commented out --mncz
; (setq org-blank-before-new-entry
;       '((heading . nil) (plain-list-item . nil)))

  ;; show 1 empty line between collapsed headings --mncz
; (setq org-cycle-separator-lines 0)
  (setq org-cycle-separator-lines 1)

  ;; Org todo keywords and colours
  (setq org-todo-keywords
        '((sequence "TODO(t)" "|" "DONE(d)")
          (sequence "NEXT(n)" "WAITING(w)" "LATER(l)" "|" "CANCELLED(c)")))

  ;; My custom faces for todo items. I'm reusing most from:
  ;; ~/.emacs.d/modules/lang/org/config.el
  (with-no-warnings
    (custom-declare-face '+org-todo-important '((t (:inherit (bold default)))) ""))

  (setq org-todo-keyword-faces
        '(("LATER"     +org-todo-onhold)
          ("NEXT"      +org-todo-important)
          ("WAITING"   +org-todo-onhold)
          ("CANCELLED" +org-todo-cancel)))

  ;; In the datetime prompt, if entering a time that has already
  ;; passed today, interpret it as a time for tomorrow.
  (setq org-read-date-prefer-future 'time)

  ;; org-books
;    commented out --mncz
; (after! f

;   (defvar org-books-file
;     (f-join org-directory "books.org")
;     "File to use with org-books mode")

    ;; Derive a separate mode for org-books-specific keybinds
;   (define-derived-mode org-books-mode org-mode "Org books mode")
    ;; Autostart this mode when opening the org-books file
;   (add-to-list 'auto-mode-alist `(,org-books-file . org-books-mode))
    ;; Add new books at the bottom of the chosen subtree
;   (setq org-books-add-to-top nil)
    ;; Allow adding books under level 3 headings
;   (setq org-books-file-depth 3))

  ;; org-agenda settings
  ;; Display one week, always starting from Monday.
;    commented out --mncz
; (setq org-agenda-span 'week)
; (setq org-agenda-start-on-weekday 1)
; (setq org-agenda-start-day ".")

  ) ; end of after! block
