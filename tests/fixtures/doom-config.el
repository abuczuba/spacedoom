;;; doom-config.el --- Sanitized inspected terminal preferences -*- lexical-binding: t; -*-
;; No identity, private Org/custom files, clipboard data, templates or credentials.
(setq doom-theme 'spacemacs-dark
      doom-font (font-spec :family "Source Code Pro" :size 15)
      doom-variable-pitch-font (font-spec :family "Source Code Pro" :size 15))
(setq-default display-line-numbers-type 'relative
              display-line-numbers-current-absolute t)
;; The live config has this public frame-focus hook. Exercise it with two TTYs.
(add-hook 'after-make-frame-functions
          (lambda (frame) (select-frame-set-input-focus frame)))

;; Normal Doom initialization owns clipboard behavior for every launch method.
(load! "clipboard")
