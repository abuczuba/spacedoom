# Current state and next action

**As of 2026-10-21, 22:46 EDT (2026-10-22 UTC). Agent-observed.**
The deployment tooling's pointer-restoration repair passed the complete 47-test
suite. The original migration stopped in preflight; its exact-state restoration
blocker is now resolved in isolated tests. The staged ec518f0 release is unchanged.
**No live files were migrated, current is absent, and no application was reloaded.**

| Milestone | Status | Evidence |
|---|---|---|
| Targeted Ghostty/tmux audit | Complete | Exact sources/includes inspected; privacy-screened; original hashes in INVENTORY.md |
| Approved development imports | Complete | Four regular copies; unused Ghostty profile and empty macOS override not adopted |
| Popup and window reordering | Implemented in repo | Config templates, renderer, pager keys and reconciled ASCII reference; private-server/PTY tests pass |
| Three-layer architecture/tooling | Implemented in repo | Complete copied releases, pinned references, checks, backups, journals, activation, rollback and restore |
| Agent governance | Updated | Repo edits/tests/docs/reviewed local commits authorized; external actions remain separately gated |
| Final staged review | Complete | 28-file preflight, staged whitespace, preservation review and documentation links passed |
| Local version control | Committed as ec518f0 | Implementation snapshot; no remote publication; this status update is not part of that release |
| Production staging | Complete; inactive | Commit-keyed release verified against committed blobs; independent regular copies, mode 444; current absent |
| Pointer-restoration repair | Implemented and verified; this revision | Backup journal schema 2, pointer/drift/dependency guards and resumable restoration; 47 tests pass |
| Initial tmux migration | Awaiting renewed approval | Prior preflight stopped; restoration blocker fixed without changing the staged release; no production backup or migration performed |
| Application reload | NOT AUTHORIZED / NOT PERFORMED | Existing live configuration and running application settings were not changed |
| Manual loaded UX acceptance | NOT PERFORMED | Required after separately approved migration/reload |

## Authorization recorded

The user explicitly approved importing relevant Ghostty/tmux sources, improving
the popup, adding nonconflicting window reordering, implementing deployment/
rollback tooling in temporary fixtures, updating governance/docs and making local
commits. Future repository development and reviewed local commits are standing
permissions. This supersedes the starter's M1-only write/commit gates.

The user subsequently approved inactive staging of ec518f0, which completed
without changing live files or current. Initial tmux-only migration was then
approved subject to all preflight conditions passing, with instructions to stop
on any failure. The exact-state restore condition was not met, so migration was
not attempted. The next task explicitly authorized a bounded repository repair,
isolated tests, recovery/status documentation and a local commit. It explicitly
withheld live migration, production pointer changes, application reload and
replacement of the staged release. Reload, Ghostty adoption, unrelated
repositories and AeroSpace changes remain outside this approval.

## Repository changes

- Imported configs/ghostty/config.ghostty unchanged from its inspected source.
- Imported configs/tmux/tmux.conf, changing only its hardcoded navigation include
  to @RELEASE@/tmux/czuba-navigation.conf. Existing plugins/startup remain intact.
- Imported and updated configs/tmux/czuba-navigation.conf and cheatsheet.txt.
- Added configs/tmux/show-shortcuts.sh and shortcuts.lesskey.
- Added deploy/manifest.json, scripts/deploy.py, validation.py, test.py, and two
  test modules. Test artifacts use owned temporary directories, not live paths.
- Updated AGENTS.md, README, workflow, decisions, inventory and continuation
  prompt. Added validation evidence and independent Terminal.app recovery docs.
- Starter local controls and historical ENVIRONMENT.md remain in the repository;
  no live Codex configuration or other application repository was accessed.

## Behavior in the candidate

Cmd+Shift+P still sends Ctrl+F then ?. The popup has #f3e8d2 background,
#20242b text, #264f78 headings and #8b3a2f keys. Plain ASCII columns fit within
73 columns; section keys 1–8, tags, search, paging and a persistent prompt improve
navigation. Ctrl+F sequences are explicit. Copy-mode Escape is corrected; stale
task commentary and irrelevant legacy alias inventories were removed. Doom,
workmux and AeroSpace limitations are stated rather than presented as verified.

Window movement uses Ctrl+F, release, then Alt+h/l (Option on this Mac).
The preferred Shift+L conflicts with tmux's previous-client binding; < and >
also have existing menus. Those bindings are preserved. Candidate Alt+h/l is
unbound in installed defaults and inspected custom files. Movement uses captured
session/window IDs, retains focus, ignores marked windows, renumbers from 1 and
stops at first/last boundaries. Numeric tmux selection is tested; physical
Command/Option delivery awaits live acceptance.

## Original milestone commands and observed validation

- sh scripts/audit.sh: targeted path/availability/Git inventory completed.
- tmux -V: 3.8; ghostty +version: 1.3.1; /usr/bin/less --version: 668;
  Python used for tests: 3.12.15.
- sh -n configs/tmux/show-shortcuts.sh: passed.
- python3 scripts/test.py: 22 unit tests passed, 10 integration tests explicitly
  skipped without --integration.
- python3 scripts/test.py --integration: **32 tests passed**, final run 1.320s.
  Covers parsers, PTY navigation, full actual-template staging/migration/restore
  in a fake home, activation/rollback, backup permissions, interrupted migration
  and post-pointer journal recovery, drift, corrupt releases, bad references,
  symlinks/traversal, writer lock and Terminal-only emergency pointer replacement.
- Actual dependency/override preflight method: passed read-only executable/file
  availability and empty/absent Ghostty override guards. No plugins were run.
- Original source SHA-256/mode checks: all four live imports still match their
  original hashes and remain regular files, mode 644; reconfirmed during the
  migration preflight below.
- Computed text contrast: body 12.8:1; blue 7.0:1; rust 6.3:1 on the light panel.
- python3 scripts/preflight.py: all 28 staged files passed the heuristic scan.
- git diff --cached --check: passed. Complete staged diff reviewed; all staged
  blobs matched reviewed regular development files. Preservation comparisons
  confirmed Ghostty is unchanged, main tmux only normalizes its include and all
  pre-popup navigation bindings are identical. Relative Markdown links resolve.

See VALIDATION.md for proof boundaries. Earlier development failures were fixed;
sandbox-denied private sockets were not misreported as successful tests.

## Inactive release and stopped migration preflight (before repair)

The approved inactive staging created this release, with no preexisting
deployment root encountered at staging time:

```text
/Users/czuba/.local/share/dotfiles-active/releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16
```

Staging used a temporary commit-keyed guard because the checked-in stage command
does not yet provide idempotent release IDs or exclusive publication. The guard
verified repeated staging reuses the identical release without writes and that
collisions are refused. Staging parser/dependency checks passed. The permanent
release.json and the temporary staging-result.json record that operation.

The stopped pre-repair preflight verified:

- All six payload files match the exact committed blobs after release-path
  rendering; the manifest matches the commit. Payloads and release.json remain
  regular mode-444 files. Payloads have independent inodes, one hard link and no
  symlinks into the checkout. Dependencies and release-local references pass.
- The five tmux destinations match the staging baseline: ~/.tmux.conf,
  ~/.config/tmux/czuba-navigation.conf and ~/.config/tmux/cheatsheet.txt are
  regular mode-644 files with their original SHA-256 values. show-shortcuts.sh
  and shortcuts.lesskey under ~/.config/tmux remain absent. Existing parents
  are ordinary directories; no target or parent symlink was adopted.
- The configured popup command explicitly invokes sh with the staged helper
  path. That exact shell command passed a PTY invocation at mode 444, including
  section jumps, search and quit. Plain/render modes preserve the reference
  text. Executable permission on the helper is unnecessary. This did not open
  a popup or load bindings in the live server.
- A temporary-home rehearsal used copies of the three existing originals,
  the actual manifest and the real migration/restore methods. It verified all
  three backups' bytes and POSIX modes and both absent-path records, restored
  all three regular files exactly, and removed both newly created live helper
  links. Parser calls were isolated from this filesystem rehearsal; no fresh
  tmux parser/server test was needed after the stop condition was established.
- **Failed condition:** the same rehearsal starts with current absent but
  restore leaves current -> releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16.
  The journal does not record the previous pointer state. This matches the
  documented retention behavior but falls short of exact pre-migration state.
  No restore-tool or staged-payload repair was attempted.

Only temporary fixtures and this repository status record were written during
this preflight. Production current remains absent; backups and history remain
empty. No production backup ID or rollback operation exists. No active tmux or
Ghostty process was accessed, reloaded, restarted or terminated; active session
and pane continuity was not queried because migration did not proceed. Ghostty's
live regular file remains byte-identical, mode 644. No process-related success
claim is inferred from the isolated helper test.

Temporary evidence for this preflight (not a permanent dependency):

```text
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/dotfiles-migrate-preflight-d2jawzi2/
```

baseline.json, helper-result.json and restore-result.json contain the measured
manifest, invocation result and before/after restore difference. The backup ID
inside restore-result.json belongs only to the temporary fixture.

## Verified pointer-restoration repair

Repository changes are limited to scripts/deploy.py, the two existing test
modules, and STATUS/WORKFLOW/RECOVERY/VALIDATION documentation. Config templates,
deploy/manifest.json and the published release were not changed.

New backup journals use schema 2 and record the exact current_before link text
(null for absence), current_after and all declared targets. Restoration validates
the pointer/files first, restores originals and removes new helper links, then
restores the pointer state. It refuses pointer drift and removal while any
declared live configuration still depends on it, including another component's
links, skipped managed paths, relative links and aliases. The existing rule
against migration silently switching releases remains in force: the older
current-release case is tested with a newer inactive release present.

Failures retain a restoring journal and block new migration/activation. Retries
skip validated completed work, including after pointer removal. Successful
repeats validate recovered state without new writes; later user changes are
refused. Legacy schema-1 backup journals lack pointer evidence and require
reviewed manual recovery. Release receipts and payload manifests remain schema 1.

Observed repair validation:

- python3 -B scripts/test.py --integration: **47 tests passed in 1.642s**
  (37 unit tests and all 10 integration tests). The initial sandbox run blocked
  private sockets; the permitted complete suite used isolated homes, private
  sockets, empty startup configs and inert test panes only.
- Real-template integration now checks all five tmux links and mode-444 release
  targets, all three backups' bytes/modes, restoration of all three originals,
  absence of both new helpers, and current's original absence, including repeat
  restoration. CLI failure injection returns nonzero without a success message.
- Recovery interruptions during migration/file restoration, pointer removal, pointer
  directory fsync and final journal publication are covered. Pointer drift before
  restoration and during file/dependency checks is refused safely.
- Read-only production fingerprints before/after testing matched: contents,
  permissions, symlink/absence states, inodes, mtimes, ctimes and deployment
  directory members. Current remains absent; backups/history remain empty.
- The staged release matches ec518f0's committed manifest and rendered blobs.
  Its schema-1 receipt and every payload remain unchanged and compatible with
  the repaired tool. No replacement release or new staging operation is needed.
- python3 -B scripts/preflight.py: all seven staged repair files passed the
  heuristic scan. git diff --cached --check passed; staged files matched the
  reviewed regular working files. The Terminal-only pointer removal example
  was also exercised in a temporary directory without altering its release.

The original five-file migration plan and preflight requirements can be reused
unchanged with the repaired repository tool: the failing exact-state restore
check now passes in isolation. This is not a fresh live migration acceptance;
recheck drift, dependencies, helper invocation and process/reload effects before
any newly approved live operation. No live session/pane query was performed.

## Separate staging-tool follow-up

- Integrate the tested commit-keyed, idempotent staging guard into the checked-in
  deployment tooling. Render exact commit blobs, verify and reuse an identical
  existing release, reject mismatches/collisions without overwrite, and publish
  with an exclusive atomic rename. Test in temporary directories and preserve
  the separation between staging, activation and reload. This documentation
  follow-up does not change any payload, stage a release or trigger deployment.

## Unknowns and retained risks

The live tmux socket read was denied; no unsandboxed live retry occurred. Plugins
may affect loaded bindings. Workmux help attempted to initialize a real log and
failed in the sandbox; no retry against real account state occurred. Doom was
not initialized/evaluated and private Org/iCloud content was not read.
AeroSpace configuration was inspected only and its enabled state remains unknown.

Ghostty's installed CLI documents explicit reload but does not establish watcher
behavior across symlink pointer changes. No GUI watcher or visual contrast test
was authorized. Ghostty migration must address that uncertainty separately.
Syntax checks do not prove physical key delivery or running application behavior.

## Next single action

Obtain renewed authorization for the original tmux-only migration to the existing
staged ec518f0 release, subject to a fresh unchanged preflight. This repair task
does not authorize that operation. A subsequent tmux reload requires separate
authorization. Physical acceptance must explicitly test Ctrl+F, release, then
Option+h/l (without Shift): automated
tests do not prove Ghostty delivers those physical key combinations. Ghostty
adoption remains separate.
