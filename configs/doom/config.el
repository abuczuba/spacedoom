;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!

;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets. It is optional.
(setq user-full-name "Matthew Czuba"
      user-mail-address "188480365+abuczuba@users.noreply.github.com")

;; Personal mail identity stays outside Git; absence uses the public address.
(load (expand-file-name "identity.el" doom-user-dir) t t)



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; abucz doom/emacs UX tweaks ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; Leave insert mode by typing kj in quick succession.
(after! evil-escape
  (setq evil-escape-key-sequence "kj"))

;; focus new frames
(add-hook 'after-make-frame-functions
          (lambda (frame)
            (select-frame-set-input-focus frame)))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; abucz doom/emacs org-mode configuration ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
(load! "org")
(setq org-directory "~/org/")
;; remove emphasis markers for WYSIWYG org-ing.
(setq org-hide-emphasis-markers t
      spacemacs-theme-org-highlight nil)
;; auto-insert for templates e.g. .org boilerplate snippets
(setq auto-insert-alist nil)  ;; prevent legacy template conflicts
(add-hook 'find-file-hook #'auto-insert)
(auto-insert-mode 1)
(setq auto-insert-directory "~/.config/doom/templates/")
(define-auto-insert
  '("\\.org\\'" . "Org default boilerplate")
  "new.org")
;; Custom org file creator
(defun abucz/new-org-file ()
  "Prompt for a new Org file in `org-directory`, with boilerplate triggered."
  (interactive)
  (let ((filename (read-file-name "New Org file: " org-directory nil nil nil
                                  (lambda (f) (string-suffix-p ".org" f)))))
    (find-file filename)))
;; custom binding for new org files
(map! :leader
      :desc "New .org file!"
      "f o" #'abucz/new-org-file)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; abucz doom/emacs theme configuration ;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'spacemacs-dark) ; 'doom-one), 'tango-dark), 'tsdh-dark)

(load! "dashboard-faces")
(setq evil-normal-state-cursor '(box "DarkGoldenrod2")) ;'(box "SkyBlue2"))
(setq evil-insert-state-cursor '(bar "chartreuse3"))
(setq evil-emacs-state-cursor '(box "SkyBlue2"))
(setq evil-visual-state-cursor '(box "LightGoldenrod3")) ;'(hbar "gray"))
(setq evil-replace-state-cursor '(box "chocolate"))
(setq evil-operator-state-cursor '((hbar . 2) "chartreuse3"))
;;(setq evil-motion-state-cursor '())
;;
;; Fonts
(setq doom-font (font-spec :family "Source Code Pro" :size 15)
      doom-variable-pitch-font (font-spec :family "Source Code Pro" :size 15))
;; (setq doom-font (font-spec :family "Hasklug Nerd Font" :size 15)
;;       doom-variable-pitch-font (font-spec :family "Hasklug Nerd Font" :size 15))`
;;
;; i don't remember why i had these here
;;
;;(("normal" "DarkGoldenrod2" box)
;;("insert" "chartreuse3" (bar . 2))
;;("emacs" "SkyBlue2" box)
;;("hybrid" "SkyBlue2" (bar . 2))
;;("replace" "chocolate" (hbar . 2))
;;("evilified" "LightGoldenrod3" box)
;;("visual" "gray" (hbar . 2))
;;("motion" "plum3" box)
;;("lisp" "HotPink1" box)
;;("iedit" "firebrick1" box)
;;("iedit-insert" "firebrick1" (bar . 2)))


;; Title Bar Customization
;;
;; - Remove the title bar
;;(add-to-list 'default-frame-alist '(undecorated . t))
;; - Customize the title bar on macOS
;;(setq ns-use-proxy-icon nil
;;      frame-title-format nil
;;      ns-transparent-titlebar t
;;      ns-appearance 'dark) ;; or 'light


;; Doom exposes five (optional) variables for controlling fonts in Doom:
;;
;; - `doom-font' -- the primary font to use
;; - `doom-variable-pitch-font' -- a non-monospace font (where applicable)
;; - `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;; - `doom-unicode-font' -- for unicode glyphs
;; - `doom-serif-font' -- for the `fixed-pitch-serif' face
;;
;; See 'C-h v doom-font' for documentation and more examples of what they
;; accept. For example:
;;
;;(setq doom-font (font-spec :family "Fira Code" :size 12 :weight 'semi-light)
;;      doom-variable-pitch-font (font-spec :family "Fira Sans" :size 13))
;;
;; If you or Emacs can't find your font, use 'M-x describe-font' to look them
;; up, `M-x eval-region' to execute elisp code, and 'M-x doom/reload-font' to
;; refresh your font settings. If Emacs still can't find your font, it likely
;; wasn't installed correctly. Font issues are rarely Doom issues!


;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq-default display-line-numbers-type 'relative
              display-line-numbers-current-absolute t
              display-line-numbers-width 4
              display-line-numbers-widen t)
(add-hook 'text-mode-hook #'display-line-numbers-mode)
(add-hook 'prog-mode-hook #'display-line-numbers-mode)

;; system clipboard made easy!
(load! "clipboard")

;; word wrapping by default
(global-visual-line-mode t)

;; packages for abucz!
(after! dired
  (use-package! dirvish
    :init
    (dirvish-override-dired-mode)))

;; melange-specific python exceptions
;;; ~/repos and ~/repos/parsing currently have a .dir-locals.el with:
;;;;     ((python-mode
;;;;       (python-shell-interpreter . "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12")
;;;;       (lsp-python-ms-python-executable-cmd . "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12")))
;;; the following is to set the default python interpreter for LSP to 3.13
;;; currently toggled off to see if it does that by default, because otherwise,
;;; when 3.14 comes along, i'll have to manually update this:
                                        ;    (after! lsp-python-ms
                                        ;      (setq lsp-python-ms-python-executable-cmd "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13"))

;; Whenever you reconfigure a package, make sure to wrap your config in an
;; `after!' block, otherwise Doom's defaults may override your settings. E.g.
;;
;;   (after! PACKAGE
;;     (setq x y))
;;
;; The exceptions to this rule:
;;
;;   - Setting file/directory variables (like `org-directory')
;;   - Setting variables which explicitly tell you to set them before their
;;     package is loaded (see 'C-h v VARIABLE' to look up their documentation).
;;   - Setting doom variables (which start with 'doom-' or '+').
;;
;; Here are some additional functions/macros that will help you configure Doom.
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;; Alternatively, use `C-h o' to look up a symbol (functions, variables, faces,
;; etc).
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented. Adding a goodbye from Czuba!
