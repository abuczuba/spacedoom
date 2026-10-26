# Live sources and deliberate exclusions

Inspected on 2026-10-26. The manifest lists exact files, not whole directories.
`docs/STATUS.md` records the active release and completed adoptions. Repository
sources are authoritative; private runtime state and upstream dependencies are not
copied into Git. A new task must check for intervening manual edits before work.

## Exact release mappings

| Live path | Authoritative source | Component |
|---|---|---|
| `~/.tmux.conf` | `configs/tmux/tmux.conf` | `tmux` |
| `~/.config/tmux/czuba-navigation.conf` | `configs/tmux/czuba-navigation.conf` | `tmux` |
| `~/.config/tmux/cheatsheet.txt` | `configs/tmux/cheatsheet.txt` | `tmux` |
| `~/.config/tmux/show-shortcuts.sh` | `configs/tmux/show-shortcuts.sh` | `tmux` |
| `~/.config/tmux/shortcuts.lesskey` | `configs/tmux/shortcuts.lesskey` | `tmux` |
| `~/.config/ghostty/config.ghostty` | `configs/ghostty/config.ghostty` | `ghostty` |
| `~/.config/tmux/agent-dashboard.conf` | `configs/tmux/agent-dashboard.conf` | `tmux-dashboard` |
| `~/.config/tmux/agent-dashboard.py` | `configs/tmux/agent-dashboard.py` | `tmux-dashboard` |
| `~/.config/cdev/codex_session.py` | `configs/cdev/codex_session.py` | `cdev` |
| `~/.config/cdev/activity.py` | `configs/cdev/activity.py` | `cdev` |
| `~/.codex/AGENTS.md` | `configs/codex/AGENTS.md` | `codex-instructions` |
| `~/.config/fish/functions/cnew.fish` | `configs/fish/functions/cnew.fish` | `fish-cnew` |
| `~/.config/fish/functions/cdev.fish` | `configs/fish/functions/cdev.fish` | `fish-cdev` |
| `~/.config/fish/functions/cdev-pin.fish` | `configs/fish/functions/cdev-pin.fish` | `fish-cdev` |
| `~/.config/cdev/doom-server.py` | `configs/cdev/doom-server.py` | `doom-client` |
| `~/.config/doom/cdev.el` | `configs/doom/cdev.el` | `doom-client` |
| `~/.config/doom/clipboard.el` | `configs/doom/clipboard.el` | `doom-clipboard` |
| `~/Library/LaunchAgents/local.dotfiles.doom.plist` | `configs/launchd/local.dotfiles.doom.plist` | `doom-service` |
| `~/.config/doom/dashboard-faces.el` | `configs/doom/dashboard-faces.el` | `doom-config` |
| `~/.config/doom/init.el` | `configs/doom/init.el` | `doom-config` |
| `~/.config/doom/org.el` | `configs/doom/org.el` | `doom-config` |
| `~/.config/doom/packages.el` | `configs/doom/packages.el` | `doom-config` |
| `~/.config/doom/simpleclip.el` | `configs/doom/simpleclip.el` | `doom-config` |
| `~/.config/doom/snippets/org-mode/org-latex-block` | `configs/doom/snippets/org-mode/org-latex-block` | `doom-config` |
| `~/.config/doom/snippets/org-mode/org-source-block` | `configs/doom/snippets/org-mode/org-source-block` | `doom-config` |
| `~/.config/doom/snippets/org-mode/phonemic` | `configs/doom/snippets/org-mode/phonemic` | `doom-config` |
| `~/.config/doom/templates/new.org` | `configs/doom/templates/new.org` | `doom-config` |
| `~/.config/fish/conf.d/fzf.fish` | `configs/fish/conf.d/fzf.fish` | `fish-config` |
| `~/.config/fish/config.fish` | `configs/fish/config.fish` | `fish-config` |
| `~/.config/fish/fish_plugins` | `configs/fish/fish_plugins` | `fish-config` |
| `~/.config/fish/functions/__fzf_cd.fish` | `configs/fish/functions/__fzf_cd.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_complete.fish` | `configs/fish/functions/__fzf_complete.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_complete_preview.fish` | `configs/fish/functions/__fzf_complete_preview.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_find_file.fish` | `configs/fish/functions/__fzf_find_file.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_get_dir.fish` | `configs/fish/functions/__fzf_get_dir.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_open.fish` | `configs/fish/functions/__fzf_open.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_parse_commandline.fish` | `configs/fish/functions/__fzf_parse_commandline.fish` | `fish-config` |
| `~/.config/fish/functions/__fzf_reverse_isearch.fish` | `configs/fish/functions/__fzf_reverse_isearch.fish` | `fish-config` |
| `~/.config/fish/functions/__fzfcmd.fish` | `configs/fish/functions/__fzfcmd.fish` | `fish-config` |
| `~/.config/fish/functions/fish_greeting.fish` | `configs/fish/functions/fish_greeting.fish` | `fish-config` |
| `~/.config/fish/functions/fish_import_bash_aliases.fish` | `configs/fish/functions/fish_import_bash_aliases.fish` | `fish-config` |
| `~/.config/fish/functions/fish_prompt.fish` | `configs/fish/functions/fish_prompt.fish` | `fish-config` |
| `~/.config/fish/functions/fp.fish` | `configs/fish/functions/fp.fish` | `fish-config` |
| `~/.config/fish/functions/la.fish` | `configs/fish/functions/la.fish` | `fish-config` |
| `~/.config/fish/functions/ll.fish` | `configs/fish/functions/ll.fish` | `fish-config` |
| `~/.config/aerospace/aerospace.toml` | `configs/aerospace/aerospace.toml` | `aerospace` |
| `~/.gitconfig` | `configs/git/gitconfig` | `git-config` |
| `~/.zprofile` | `configs/shell/zprofile` | `shell` |
| `~/.config/gh/config.yml` | `configs/gh/config.yml` | `gh` |
| `~/.config/fish/conf.d/colors.fish` | `configs/fish/conf.d/colors.fish` | `fish-config` |
| `~/.config/doom/config.el` | `configs/doom/config.el` | `doom-config` |

There are 51 payload files. The two `tmux-dashboard` helper aliases are optional
and remain absent on this machine; tmux uses release-pinned helpers. All other
targets are individually adopted after verified original-file backups.

## Additional maintained source and defaults

| Live location | Source / disposition |
|---|---|
| `~/.config/workmux/config.yaml` | `configs/workmux/config.yaml`; exact reviewed reference, external live file; no workmux setup or settings migration |
| `~/.codex/hooks.json` | `configs/codex/hooks.json`; seven unchanged workmux definitions, external live file; no global hook installation or trust changes |
| `~/.codex/config.toml` | Only the maintained public hook-enable preference is in `configs/codex/config.example.toml`; mutable project/hook trust, UI state, plugins and private endpoints stay local |
| `~/.config/ghostty/profiles/*.ghostty` | Both personal alternate profiles are tracked under `configs/ghostty/profiles/`; inactive and not included by the active primary config |
| `~/.config/starship.toml` | Absent; Starship built-in defaults, initialized by Fish; see `configs/starship/README.md` |
| `~/.config/fish/fish_variables` | Generated state remains external. The 27 portable color choices are captured in `configs/fish/conf.d/colors.fish`; fzf defaults are in its included integration |
| Fish abbreviations / completions | No personal abbreviation definitions or completion files were found; application and Fish completions remain upstream |
| `~/.config/doom/custom.el` | Generated writable Custom file stays external. Its only settings, hidden Org emphasis and disabled Spacemacs Org highlighting, are captured in `config.el` |
| `~/.config/doom/identity.el` | Optional private mail identity, mode 600, deliberately excluded. `identity.example.el` documents the format; public defaults use the GitHub noreply address |

## Doom coverage

`init.el`, `config.el`, `packages.el`, Org configuration, clipboard commands,
dashboard faces, project-frame/workspace Lisp, the local simpleclip library,
all three personal Org snippets and the auto-insert template are included. No
custom module directory was present. `config.el` loads Org, clipboard and the
dashboard helper normally; there is one implementation of each helper. The
named-server launcher loads `cdev.el`; standalone Doom needs no extra `--load`
for clipboard or appearance. `custom.el` remains writable for future local Custom
and safe-local-variable choices, rather than becoming an immutable release file.

## Kept external

- Upstream `~/.config/emacs`, installed modules/packages, generated profiles,
  native compilation, environment captures, caches and workspace state. Their
  presence/version is validated where required; source/package caches are not dotfiles.
- Org/iCloud/Dropbox documents and symlinks, shell histories, old Doom/Fish/Ghostty
  backups, browser/application data, Codex conversations, pins, runtime registrations,
  auth files, trust decisions, Keychain material, SSH/GPG keys and rclone credentials.
- `~/.config/cdev/collie.json`, `~/.config/collie/`, Collie binaries/service/pairing/push
  state, Tailscale and its Serve configuration: independent installation, untouched.
  The cdev handoff code is tracked; no phone transport is installed by dotfiles.
- `~/.config/gh/hosts.yml`: authentication; only the nonsecret config/alias file is managed.
- Vendor Riot LaunchAgent: application-managed. The only personal LaunchAgent is
  the tracked Doom server; Collie has its own separately maintained agent.
- `~/.local/bin` contains external Collie/Tailscale/Python symlinks. No personal
  `~/bin` or `~/scripts` directory exists. Legacy aliases to older scripts are
  retained as personal references, not evidence those programs are installed.
- `~/.config/opencode` is empty. `doom-original` and dated Doom backups are
  historical copies, not authoritative sources. No other shell startup files,
  Vim/skhd/yabai configuration or global Git ignore file were found.

The tracked `fish_plugins` file records the installed fzf choice. Its ten source
files exactly match the revision in `deploy/provenance.json`; update those through
Git/release staging. Do not let a plugin manager mutate copied releases.
