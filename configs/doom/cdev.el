;;; cdev.el --- Frame-local project clients for the named Doom server -*- lexical-binding: t; -*-

;; Loaded explicitly by doom-server.py AFTER the user's normal Doom startup.
;; No replacement init.el/config.el, global default-directory, or timer.
(require 'cl-lib)

(defconst dotfiles-cdev-dashboard-if-new t
  "This frame integration supports emax's dashboard-on-first-open request.")

(defun dotfiles-cdev-workspace-name (root)
  "Return a stable, collision-resistant native Doom workspace name for ROOT."
  (concat "cdev:" (file-name-nondirectory (directory-file-name root)) ":"
          (substring (secure-hash 'sha256 root) 0 12)))

(defun dotfiles-cdev-associate-frame (&optional frame)
  "Associate only a cdev client FRAME with its project and native workspace."
  (let* ((frame (or frame (selected-frame)))
         (root (frame-parameter frame 'cdev-project-root)))
    (when root
      (unless (and (stringp root) (file-name-absolute-p root)
                   (file-directory-p root) (not (file-remote-p root)))
        (error "cdev: invalid local project directory"))
      (with-selected-frame frame
        (require 'persp-mode)
        (unless (and (bound-and-true-p persp-mode) (fboundp '+workspace-switch))
          (error "cdev: Doom's :ui workspaces module must be enabled"))
        (let* ((root (file-name-as-directory (file-truename root)))
               (name (dotfiles-cdev-workspace-name root))
               (exists (+workspace-exists-p name)))
          (+workspace-switch name t)
          (set-persp-parameter '+workspace-project root (get-current-persp))
          (set-frame-parameter frame 'cdev-project-root root)
          (set-frame-parameter frame 'cdev-workspace name)
          ;; Doom deletes auto-associated frame workspaces on client close.
          ;; A cdev project is deliberately retained for terminal reconnection.
          (set-frame-parameter frame 'workspace nil)
          (unless exists
            (if (frame-parameter frame 'cdev-dashboard-if-new)
                ;; The dashboard is shared: keep its default-directory untouched.
                ;; SPC f f already uses this frame's project-root parameter.
                (switch-to-buffer (doom-fallback-buffer))
              (let ((buffer (get-buffer-create (concat "*" name "*"))))
                (with-current-buffer buffer
                  (setq-local default-directory root))
                (persp-add-buffer buffer (get-current-persp) nil nil)
                (switch-to-buffer buffer)))))))))

(defun dotfiles/cdev-find-file ()
  "Use this frame's cdev root for SPC f f; preserve other file navigation.
Outside cdev frames, delegate with the current buffer's usual directory.
Absolute paths and explicit parent-directory navigation remain available."
  (interactive)
  (let ((default-directory (or (frame-parameter nil 'cdev-project-root)
                               default-directory)))
    (call-interactively (or (command-remapping #'find-file) #'find-file))))

(add-hook 'server-after-make-frame-hook #'dotfiles-cdev-associate-frame t)
(map! :leader :desc "Find file from this project's root"
      "f f" #'dotfiles/cdev-find-file)

(provide 'dotfiles-cdev)
;;; cdev.el ends here
