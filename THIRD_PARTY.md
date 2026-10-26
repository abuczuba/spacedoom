# Attribution and licenses

My original configuration, Python tools, tests and documentation use the
[MIT license](LICENSE). This is a collection of separate programs and configs;
the following upstream portions keep their existing terms.

| Files | Origin | License |
|---|---|---|
| Doom template text in `configs/doom/{init,config,packages}.el` and `tests/fixtures/doom-*.el` | [Doom Emacs](https://github.com/doomemacs/core), Henrik Lissner, 2014–2026 | [MIT](LICENSES/Doom-MIT.txt) |
| `configs/doom/simpleclip.el` | [simpleclip](https://github.com/rolandwalker/simpleclip), Roland Walker, 2012–2020 | BSD-2-Clause; full notice retained in the file |
| `configs/fish/config.fish` and `configs/fish/functions/fish_prompt.fish` | Adapted Fish default prompt, Lily Ballard and fish-shell contributors | [GPL-2.0-only](LICENSES/GPL-2.0-only.txt), including my adaptations in those files |
| `configs/fish/conf.d/fzf.fish`, `configs/fish/functions/__fzf*.fish` | [jethrokuan/fzf](https://github.com/jethrokuan/fzf), Jethro Kuan, 2016 | [MIT](LICENSES/fzf-MIT.txt) |

The ten fzf files are an unchanged, small source snapshot of upstream commit
`479fa67d7439b23095e01b64987ae79a91a4e283`, verified against the installed files.
Their hashes are recorded in [deploy/provenance.json](deploy/provenance.json).
`fish_plugins` records the original plugin choice; updating a managed plugin means
updating its source snapshot here, not letting Fisher overwrite release files.

The Org configuration retains its original acknowledgement to Andy; the snippets
and personal settings came from my existing configuration. Spacemacs-inspired
terminal colors are configuration values; the actual Spacemacs theme, Doom,
Evil, Dirvish and other packages are installed externally, not vendored here.
The local simpleclip source is retained for completeness; `packages.el` also
declares the normal Doom-managed package.

tmux uses external [TPM](https://github.com/tmux-plugins/tpm),
[tmux-dotbar](https://github.com/vaaleyard/tmux-dotbar) and
[Rose Pine](https://github.com/rose-pine/tmux). Fonts, applications, language
servers and their licenses are supplied by their respective distributions.
No upstream Doom tree, package cache, font binary or Collie source is included.
