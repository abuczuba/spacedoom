# Machine and workflow handoff (dated snapshot, not a live audit)

**Compiled:** 2026-10-21. **Primary evidence:** user-supplied `MAC_DEVELOPMENT_ENVIRONMENT_HANDOFF_2026-10-20(2).md` (itself dated 2026-10-20), plus subsequent user-reported vterm/AeroSpace CLI output in the dotfiles chat. The original handoff focused on JobApply, but this distillation is **only about this machine and workstation configuration**. No original JobApply requirements or other project's files are copied here.

Legend: **UV** user-verified by output or direct report; **AR** agent-reported/previously configured; **U** not yet independently verified for this repo. Snapshots can become stale; rerun narrow checks before making changes.

## Environment

| Layer | Snapshot | Provenance and caveats |
|---|---|---|
| Hardware | Apple Silicon MBP, arm64, macOS 27.0 | UV 2026-10-20; often clamshell, one active G34WQC/Gigabyte ultrawide; do not assume two active displays |
| Ghostty | Homebrew cask, Spacemacs Dark-inspired theme; charcoal background `#292b2e`, custom padding/transparent macOS titlebar | UV that it runs; specific build U |
| Fish | 4.9.3, Starship 1.27.0; direnv/fnm/fzf integrations | UV/AR as documented 2026-10-20; shell account login shell may still be Zsh |
| tmux | 3.8; persistent primary session `main`; TPM/plugins | UV 2026-10-20; exact current sessions U |
| Emacs/Doom | GNU Emacs 31.1, Doom at `~/.config/emacs`, user config `~/.config/doom`; terminal `emacs -nw` works | UV 2026-10-20; graphical Source Code Pro font/daemon unresolved then |
| vterm | Module built successfully (`[100%] Built target vterm-module`) after `libtool` installation | UV output in later dotfiles chat; current loaded runtime U |
| Codex CLI | v0.163.0, logged in using ChatGPT | UV 2026-10-20; confirm current CLI flags with local `codex --help` if they differ |
| cdev | Fish function intended to launch/reuse left Doom + right Codex tmux window without worktrees | AR/mocked tests; true multi-project collision/reuse behavior not fully UV |
| workmux | v0.1.276 installed; optional Git-worktree parallel agents | UV disposable test, not required here |
| Git/GitHub | `gh` authenticated; SSH-signed commits configured globally | UV prior handoff; do not regenerate keys, expose auth material, or alter global signing |
| AeroSpace | v0.21.3 Beta, config at `~/.config/aerospace/aerospace.toml` | UV path/single monitor; AR said disabled later; **current enabled/disabled state U** and out of this milestone |
| Homebrew/CLI | Homebrew `/opt/homebrew`; Apple CLT; uv Python 3.12.15 | UV/AR prior handoff; no reason to re-provision workstation |

## Interaction model: do not conflate layers

- **Ghostty** owns GUI rendering, fonts, and macOS-level keybindings. It normally launches Fish and attaches to tmux `main`; do not add a duplicate auto-attach mechanism.
- **tmux** owns the window strip the user calls the **flywheel**, plus sessions/windows/panes. It is not Ghostty's tab bar, Doom workspace, or a native macOS Space.
- **Doom** runs primarily as a terminal UI within tmux. A vterm buffer is a terminal within Doom, not a second tmux session.
- **Codex** runs as a separate interactive process, often in the right tmux pane. A tmux window name is not a Codex session ID; `codex resume` exists for session continuation.
- **AeroSpace** handles GUI windows separately from tmux and macOS Mission Control Desktops; do not modify native Spaces as a side effect of terminal configuration.

## Keyboard/appearance invariants (recorded 2026-10-20)

| Binding | Intended current behavior |
|---|---|
| `Ctrl+F` | tmux prefix, NOT `Ctrl+B` |
| `⌘⇧H/J/K/L` | Move focus between tmux panes with **no wrap at edges** |
| `⌘1` through `⌘9` | Select tmux window by 1-based index |
| `⌘⇧V` / `⌘⇧S` | Split panes side-by-side / top-bottom |
| `⌘⇧N` / `⌘⇧Z` | New tmux window / zoom pane |
| `⌘⇧X` | Confirm before killing pane |
| `⌘⇧P` | Searchable tmux shortcut cheatsheet popup |
| `⌘⇧Y` | Copy tmux **retained scrollback**, not last command's output |
| `⌘⇧,` | Reload Ghostty configuration |
| `⌘⌃P` | Ghostty command palette |

Some bindings are previously configured rather than independently exercised after each subsequent change. Test them against the running setup before changing behavior.

## Known uncertainties and constraints

- Ghostty can load XDG configuration **and** macOS Application Support configuration, which may override earlier XDG values. Verify both locations and any `config-file` includes before declaring which settings are effective.
- `~/.tmux.conf` may source `~/.config/tmux/czuba-navigation.conf` or additional files. Inspect the actual include graph; do not assume every file mentioned in old backups is active.
- Graphical Doom font fix, daemon startup, and AeroSpace window-management refinements remain unrelated to the initial Ghostty/tmux task.
- `cdev` may refuse a naming collision with an existing tmux window: don't destroy windows to force it.
- The full June backup may contain outdated Linux aliases, secrets, or credentials; no bulk restore/import.
- Terminal tool invocations from Codex may use Zsh/sh even though the user's interactive shell is Fish.
