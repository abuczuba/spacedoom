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
