;; Dashboard text uses the buffer background, including Solaire's remapping.
(custom-set-faces!
  `((+dashboard-banner +dashboard-loaded)
    :inherit nil
    :background unspecified
    :foreground ,(face-foreground 'font-lock-comment-face nil t)))
