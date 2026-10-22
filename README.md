# Personal macOS dotfiles

The Git source of truth is `~/dev/dotfiles`. Work here does not change the
running workstation. The ec518f0 tmux deployment passed user-reported physical
acceptance. The activity dashboard and persistent Doom clients are **repository
candidates only**. See [status](docs/STATUS.md).

## Three layers

```text
~/dev/dotfiles/configs/                        development copies/templates
    |
    | explicit, validated COPY
    v
~/.local/share/dotfiles-active/releases/ID/    stable release files
~/.local/share/dotfiles-active/current        atomic release pointer
    ^
    | exact live file links, only after approved migration
~/.tmux.conf
~/.config/tmux/{czuba-navigation.conf,cheatsheet.txt,...}
~/.config/ghostty/config.ghostty               future, separately approved
```

Live configuration must never link into the checkout. Git branches, uncommitted
edits and commits cannot deploy or reload anything. New cdev Fish/Doom/service
files have exact optional manifest mappings, but none is migrated. Global Codex
hooks, workmux settings, unrelated Fish/Doom configuration and AeroSpace remain
separately managed and unchanged.

## Development

Requirements: Python 3.9+ standard library. Integration validation uses the
installed Ghostty 1.3.1, tmux 3.8+, Fish, Emacs/emacsclient 31.1 with the existing
Doom installation, workmux 0.1.276, system less 668+, sh and awk. No Stow or package
installation is required.

Run from this checkout; these commands work in Fish, Zsh and POSIX sh:

```sh
python3 scripts/test.py
python3 scripts/test.py --integration
python3 scripts/deploy.py check
python3 scripts/deploy.py plan
```

Unit tests use temporary homes. Integration tests create private tmux sockets
with empty startup configs and inert panes, parse copied settings without user
plugins, and exercise the pager through a pseudo-terminal. They do not connect
to the live tmux server. Doom tests use sanitized homes, copied/rebased startup
files, read-only installed libraries and unique owned sockets/terminal clients;
they exclude private Org/custom configuration. Codex tests use synthetic payloads,
local config parsing and inert stand-ins, not active conversations.
Codex's macOS sandbox may require narrow approval for
private test sockets. `check` additionally verifies actual external dependencies
and unmanaged override files; it does not create deployment state.

The tmux files contain `@RELEASE@` references. The release tool renders those to
immutable release paths. Do not source the development templates into a live
tmux server.

## Included changes

- A warm light shortcuts popup with charcoal text, blue headings, rust keys,
  ASCII columns, section keys 1–8, search and persistent navigation help.
- `Cmd+Shift+P` remains the invocation; tmux sequences spell out `Ctrl+F`.
- `Ctrl+F`, release, then `Opt+h/l` moves the selected window left/right.
  Focus follows the window, numbering becomes consecutive from 1, and ends
  do not wrap. Default `L` and `<`/`>` bindings are preserved.
- Complete copied releases, hash/reference/dependency checks, backup-first
  migration, explicit activation, rollback, and restoration of original files.
- An event-cached activity title overlay and Ctrl+F n attention cycling; window
  creation moves to c and ordinary next-window to Shift+N. Idle theme unchanged.
  The one-line candidate Ghostty Cmd+Shift+N remap to c preserves creation;
  attention stays gated in legacy mode until that companion is adopted/reloaded.
- One explicitly managed named Doom daemon, terminal client frames with native
  workspaces and stable project-root SPC f f, plus explicit standalone fallback.

The original popup/reordering changes are accepted in production. New dashboard,
Fish/Doom and LaunchAgent changes require separate staging/activation approvals.

## Navigation

- [AGENTS.md](AGENTS.md): standing agent permissions and approval boundaries
- [Workflow](docs/WORKFLOW.md): development, staged review and each release operation
- [Recovery](docs/RECOVERY.md): independent Terminal.app instructions
- [Validation](docs/VALIDATION.md): evidence, manual acceptance and limits
- [Inventory](docs/INVENTORY.md): inspected sources, target mapping and provenance
- [Decisions](docs/DECISIONS.md): copied releases rather than development symlinks/Stow
- [Activity evidence/design](docs/ACTIVITY.md) and [offline preview](docs/previews/dashboard.html)
- [Persistent Doom architecture](docs/DOOM-SERVER.md)
- [Proposed milestone deployment/rollback](docs/MILESTONE-DEPLOYMENT.md)
- [Historical handoff](docs/ENVIRONMENT.md): October 20–21 context, not a live inventory

## Local commits

Repository edits, tests, documentation and appropriately scoped local commits
are authorized. Stage only intended files, inspect the staged diff, run
`python3 scripts/preflight.py` and `git diff --cached --check`, then commit using
the existing Git identity/signing settings. The optional tracked pre-commit hook
also runs preflight; do not enable/change Git settings without permission.
The heuristic scan cannot guarantee absence of secrets.

Deployment, external symlinks, rollback, reload and remote pushes each require
their own explicit approval. Nothing in a Git hook, shell startup or test suite
performs those operations. See the workflow before running mutation commands.
