# Inspected sources and managed mapping

**Agent-observed on 2026-10-21.** Sources are regular files, not symlinks. A
targeted heuristic screen found no secret signatures in approved imports; it is
not a proof of absence. No live files were replaced, linked or reloaded.

| Live source | Development copy | Release-relative file |
|---|---|---|
| ~/.tmux.conf | configs/tmux/tmux.conf | tmux/tmux.conf |
| ~/.config/tmux/czuba-navigation.conf | configs/tmux/czuba-navigation.conf | tmux/czuba-navigation.conf |
| ~/.config/tmux/cheatsheet.txt | configs/tmux/cheatsheet.txt | tmux/cheatsheet.txt |
| new helper, not live | configs/tmux/show-shortcuts.sh | tmux/show-shortcuts.sh |
| new pager keys, not live | configs/tmux/shortcuts.lesskey | tmux/shortcuts.lesskey |
| ~/.config/ghostty/config.ghostty | configs/ghostty/config.ghostty | ghostty/config.ghostty |

After approved migration, exact live paths link to the corresponding file under
`~/.local/share/dotfiles-active/current/`. No whole-directory links. The manifest
is `deploy/manifest.json`; a component migration affects only its enumerated files.
The first proposed migration is tmux only (five files), not Ghostty.

## Include graph and precedence

- Ghostty primary: XDG config.ghostty, 81 lines; no config-file directives.
  The macOS Application Support config.ghostty is empty; both legacy config
  paths are absent. Preflight guards against new nonempty unmanaged overrides.
- The preserved spacemacs-dark.ghostty profile exists but is not included;
  it was screened but not imported or modified.
- Main tmux config: 76 source lines. It runs the existing tmux-dotbar and TPM
  scripts, then sources czuba-navigation.conf. Imported template changes only
  that hardcoded home include to a release-pinned reference. Original redundant
  renumber-windows on settings are preserved.
- Navigation overlay: 44 source lines, including the original ? popup. Its
  release-pinned popup and new reordering bindings are development changes.
- Ctrl+F is configured as prefix, base-index is 1, mode-keys is vi, and
  renumber-windows is on. Command-driven bindings send Ctrl+F plus the action.
- Existing plugins remain external dependencies under ~/.tmux/plugins; their
  caches/code were not imported or executed by validation.

## Original source hashes (SHA-256)

These identify the inspected originals, not the modified development copies.

| Source | Hash |
|---|---|
| Ghostty primary | ce68f75b1a5da571a934a196eac1c116e70ad885450b13632217ab33c196cbf2 |
| Main tmux | 66798d000a7d8d226c55eb38bd3accd3bdba5af8969908b8747329d3dd0523d1 |
| Navigation | 0c3d9913351dce09ad4d2a511f0b92bcab6329e06310850e2a5b78f2d61753d1 |
| Shortcuts text | 29bcf8f66ec4de60558982bd86f611b345dabad4826b0fbcce84e08cadb563bd |

The imported Ghostty primary remains byte-identical. No machine-specific private
paths were retained in the redesigned reference. The original navigation include
in main tmux was normalized into the release template.

## Adjacent sources inspected, not imported or changed

- Fish config.fish (346 lines), conf.d/fzf.fish (63), and functions/cdev.fish
  (130). No fish_user_key_bindings.fish is present. fzf's legacy bindings are a
  configured default controlled by universal variables; the running shell was
  not queried or restarted. No universal-variable dump was read.
- Workmux config.yaml (161 lines): configured pane layout and Codex agent.
  --help tried to initialize a log and failed inside the sandbox; it was not
  retried against the real account outside the sandbox. CLI subcommands and
  last-agent remain references, not verified functionality.
- Doom config.el (183) and init.el (222): custom key declaration and enabled
  modules only. No Org/iCloud content or live Emacs evaluation was accessed.
  Conventional Doom bindings remain explicitly unverified.
- AeroSpace aerospace.toml (21): key/action declarations only. Enabled state
  was not queried; no enable/reload/edit was performed.

## Unverified runtime state

The sandbox denied access to the existing default tmux socket. No unsandboxed
live-socket retry occurred. Installed-default conflicts and candidate behavior
were tested on separately approved private servers instead. Actual loaded
plugins/bindings, display contrast in Ghostty and GUI watcher behavior await
separately authorized activation and acceptance.

No application repository, credential store, unrelated directory, Fish/Doom
configuration deployment or macOS setting is part of this milestone.
