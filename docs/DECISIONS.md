# Architectural decisions

## D-001 — Canonical development, stable deployment, live paths

**Adopted by the user, 2026-10-21.** `~/dev/dotfiles` is the Git source of truth.
Stable copied releases live under `~/.local/share/dotfiles-active/`. Live files
may link through that deployment tree only after individually approved migration.
A live/deployment symlink into the checkout is forbidden. Uncommitted edits,
branch switches and commits never change the workstation.

This supersedes the starter's statement that the repository is only a proposed
staging area. Existing live settings still describe currently loaded behavior
until migration, approved reload and acceptance are recorded.

## D-002 — Repository autonomy, operation-specific external approval

**Adopted by the user, 2026-10-21.** Agents may inspect relevant config, maintain
development copies, refactor, test, update docs and make reviewed local commits.
M1's initial audit/import approval gate has been satisfied and superseded for
ordinary repository work.

Staging outside the checkout, backup/migration, external symlink changes,
activation, rollback/restore, reload/restart, package/system changes, destructive
operations and remote pushes each require explicit authorization. A tool flag
does not supply consent; written rules do not replace the actual sandbox.

## D-003 — Preserve the established workstation

Ghostty → Fish → tmux main → Doom/Codex remains the workflow. Preserve Ctrl+F,
Command shortcuts, no-wrap pane movement, theme and user processes. Fish, Doom,
workmux and AeroSpace remain outside configuration-editing scope. Their exact
config was inspected only to reconcile the reference. Unrelated repositories,
including Tailscale, remain out of scope.

## D-004 — Minimal copied-release tool, no Stow

**Adopted for this milestone.** Use Python 3.9+ standard-library tooling, a small
explicit manifest, versioned complete releases and a single atomic current
pointer. Stow could link a copied tree, but does not replace release copying,
preflight, backups, history or failure handling. Adding it provides no benefit
for this small managed set and would add a package dependency.

Release files are independent copies with hashes and read-only modes. The tool
does not edit an installed release in place. Tmux includes and popup launchers
pin immutable absolute release paths; old loaded bindings remain internally
consistent until an explicit reload. Old releases must remain available.

## D-005 — Atomic pointer, explicit partial-migration recovery

A single current-pointer replacement is atomic on one local filesystem.
Replacing several original live files with managed links is not jointly atomic.
Back up every exact target before the first replacement; retain a migration
journal. Failures stop with evidence and block activation until explicitly
authorized recovery. There is no implicit compensation operation.

Rollback of later activation is another validated pointer switch. Initial
restoration uses original-file backups and preserves their POSIX modes. Neither
operation reloads applications. A standalone Terminal.app procedure covers
broken tooling and failed startup.

## D-006 — Window reordering preserves existing defaults

User preference: Ctrl+F then Shift+H/L if free. Installed tmux 3.8 binds L to
switch-client -l. It also binds < and > to window/pane menus. Preserve all three.

Use Ctrl+F then Alt+h/l (Option on this Mac); both are unbound in installed
defaults and the inspected custom files. Native tmux commands capture session/
window IDs before swapping, explicitly reselect that same window and renumber
from base-index 1. First/last/single-window boundaries are no-ops. Marked windows
must not redirect the move. Tests cover these cases; live plugin overrides and
physical Option-key delivery await acceptance.

## D-007 — Readable reference with explicit evidence

The popup alone uses #f3e8d2 background, #20242b body text, #264f78 headings and
#8b3a2f keys. The surrounding Ghostty/tmux theme remains intact. A plain ASCII
source is colored at display time with sh/awk and viewed in system less, using
an uncompiled lesskey source for section jumps. No new runtime package is needed.

Use Ctrl+F -> key consistently. Distinguish configured bindings, installed
defaults and unverified runtime references. Remove stale task narratives and
obsolete project/Linux alias inventories. Correct Escape in tmux copy mode:
it clears the selection; q exits.


## D-008 — Advisory activity evidence, native cached title animation

2026-10-22, approved for repository implementation. Workmux commands support plain
panes, but current cdev panes had no valid records. Keep global hooks/settings
untouched; add invocation-local, pane/socket/nonce-pinned advisory hooks for
future cdev launches. Preserve all policies, notifications and hook trust. Do not
attach an observer to existing conversations. Unknown evidence stays idle.

Dotbar remains the title-format owner. A workmux-aware title slot prevents its
format auto-installer competing with Dotbar. Native 1Hz format monitors launch
short refresh jobs only on changed signatures. Cached arithmetic animates a
readable steel title/crimson band without per-tick processes or a polling
daemon. n cycles attention, c creates, Shift+N selects the next ordinary window.
The installer refuses binding, local-format and hook-slot conflicts.
The final approved aesthetic is one connected three-cell wave, moving right
at 1Hz and leaving the right edge before reentering on the left. Dark-crimson
and blood-red glow under steel reflections; a red-lit leading letter uses
black for contrast. All working palette pairs exceed 4.5:1; no random color
phases or flashing. This refines 17c6f99 without changing lifecycle detection.
Ghostty's old Cmd+Shift+N forwards n, so the candidate changes that single line
to c. Keep legacy n creation until separate companion adoption/reload and an
explicit second tmux reload. Background monitoring never changes bindings.

Stop indicates a stopped turn/review or reply, not task success. PermissionRequest
is separate evidence; arbitrary conversational waiting and a fully ordered
approval-resolution stream are unavailable. These boundaries, real-CLI trust
acceptance and the old-session fallback are explicit in ACTIVITY.md.

## D-009 — Named Doom daemon, native frame workspaces, explicit recovery

2026-10-22, approved for repository implementation and disposable validation.
Use the installed Doom/Emacs with one named foreground daemon and terminal
emacsclient frames. No replacement init/config/Org files or parallel workspace
system. Frame parameters bind project identity; native Doom perspectives persist
across client closure. Only SPC f f delegates from the associated project root;
ordinary local directory semantics and explicit outside-project navigation stay
available. Existing project windows/processes are reused as-is.

A user LaunchAgent owns login startup and job tracking. KeepAlive=false avoids
unattended failure loops; recovery is explicit, with logs and singleton locking.
No auto-start from cdev, empty alternate editor, default server, package install,
GUI repair or unsafe legacy toggle. Persistent service installation/start remains
unapproved. CDEV_EDITOR_MODE=standalone is an independent launch fallback.

## D-010 — Preserve the existing deployment transaction

The 15-file complete release extends schema-1 manifests with Fish/Python/Elisp/
plist validation and @HOME@ rendering. No framework/dependency replacement.
Only exact Fish functions, one companion Ghostty file and one plist need
additional adoption; other helpers can stay payload-only through pinned includes.
New component backups must be
restored before rolling back the shared pointer to an older release without
those mappings. This is tested using the established journals/restore methods.
Commit-keyed, idempotent/exclusive staging remains a separate follow-up.
