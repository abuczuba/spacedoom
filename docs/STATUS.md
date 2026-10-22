# Hook-registration repair candidate — 2026-10-22

**Repository repair tested; actual Codex hook delivery remains a user-review
gate. No live changes are authorized or performed by this milestone.** See
[HOOK-REGISTRATION.md](HOOK-REGISTRATION.md) for evidence, the runtime protocol,
failure behavior and the exact one-time native review procedure. It supersedes
the older nonce-in-command bridge and rollout instructions below.

- Codex 0.163.0's own hooks/list API confirms that changing only the original
  launch nonce changes all eight definition hashes. The eight new entries are
  SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse,
  Stop, Interrupt and SessionEnd, from sessionFlags rather than the workmux file.
- Repaired definitions contain only a fixed /usr/bin/python3 invocation of the
  installed lexical activity.py path and event action. Distinct runtime nonces,
  panes, sockets and state locations now produce identical native currentHash
  values and source keys. Tests preserve all seven workmux keys/hashes. No
  trusted_hash is written, and all new native definitions remain untrusted.
- Private runtime JSON is passed in the child environment. The adapter verifies
  the registered Codex child and launcher as live same-user ancestors, process
  start identities, nonce, server boot and stable pane ID before binding the
  documented session/turn IDs. It does not select by cwd or inherited TMUX.
  Records/locks are 0600 under 0700 state; symlinks, unsafe permissions, stale
  identities and unrelated process origins fail closed. Missing/failed hooks
  leave the CLI usable and unlabelled; owned child termination clears evidence.
- **90/90 full regressions passed in 53.806s** with
  `python3 -B scripts/test.py --integration`. Native discovery/hash checks are
  real Codex RPC calls; event dispatch is explicitly synthetic, through actual
  owned process trees and private sockets. Tests cover two same-cwd agents,
  cross-pane context rejection, window movement, stale/ended sessions, cleanup,
  failure/lock contention, existing renderer/keys, workmux, standalone cdev
  reuse/compiler handling, isolated Doom clients and deployment recovery.
  `python3 -B scripts/deploy.py check` also passed. Two fixture assumptions found
  during the first full run were corrected: wait for the finalizer's marker
  write, and dispatch the Doom integration's synthetic events inside its agent
  ancestry. No production workaround or renderer change was needed.
- Actual hook-subprocess environment propagation, repeated native trust reuse,
  real working/stopped/approval delivery and shared-app-server behavior are not
  established by those tests. A shared server outside the registered ancestry
  is deliberately rejected. No --no-daemon switch or other Codex behavior change
  is introduced to hide that limitation. Real delivery after user review is
  mandatory before a new rollout proposal or attention activation.

Production remains recovered Phase 3B on
releases/20261022T163617.469413Z-497daec6. No release was staged or modified;
current, live files, global hooks/trust, workmux and loaded n/c compatibility
bindings are outside this patch. Standalone emacs -nw remains live; persistent
Doom/LaunchAgent activation is still deferred. The existing cdev backup
20261022T191900.472358Z-230b25df remains restored. The separate commit-keyed,
idempotent staging improvement remains a follow-up.

Only the two existing cdev payloads require a future new release. New test
fixtures and documentation are repository files. Preserve prior concurrent
documentation/audit edits; this entry is additive and does not deploy anything.
Next: explicit user review of the fixed native definitions in an isolated proof,
then actual ordinary-cdev delivery verification. Do not resume Phase 4.

---

# Current state and next action

## Final shimmer and key compatibility refinement — 2026-10-22

Baseline: clean HEAD 17c6f99. This bounded follow-up changes the working-title
renderer, offline preview, related tests/cheatsheet and documentation only.
The broader Emacs/event-tracking implementation below remains intact. No release
was staged; the only deployment release is still ec518f0. No 17c6f99 release was
found, and existing ec518f0 files/receipt/backup/pointer were preserved unchanged.

Fresh read-only observation confirms Ghostty's effective configured Cmd+Shift+N
text route is Ctrl+F n; the running tmux n creates in the pane directory, c is
standard creation, N is unbound, and Tab runs workmux last-agent. The companion
Ctrl+F c mapping and safe legacy-mode bridge from 17c6f99 are retained, with no
additional binding or routing change. Physical GUI delivery remains unverified.

Working now shows a connected band of at most three characters moving right
one step per second through dark-steel text. The red leading edge, blood-red
reflection and dark-crimson wake leave the right edge before the next pass.
The shared preview/renderer palette and every phase are tested; all foreground/
background pairs exceed 4.5:1. Stopped white dot, approval white ! on red,
untracked/idle appearance, event evidence and Dotbar ownership remain unchanged.
See ACTIVITY.md for exact colors and the updated preview.

**37 relevant regressions passed in 32.780s**, using:

```sh
python3 -B scripts/test.py --integration --match 'test_activity.*' --match 'test_cdev.*' --match 'test_dashboard.*' --match 'test_terminal.*' --match '*test_real_cdev_layout_dashboard_and_client_pane_close'
```

The new Ghostty-parser → serialized text bytes → attached private tmux PTY test
proves window creation throughout the coordinated bridge, then n attention,
c creation, N navigation, Cmd+1–9, pane navigation and window reordering/focus.
All protected bindings, including workmux/popup, compare unchanged. Existing
concurrent/stale/termination tests and combined real Doom-client/cdev test pass.
No production session served as a disposable test subject. Initial test-fixture
failures were corrected: +show-config needs private HOME/XDG, not --config-file;
the synthetic agent must use cdev's /usr/bin/python3 identity. No live fix occurred.
The prior complete 79-test result below remains evidence for unchanged work.

Paired private benchmark: 24-character working expansion 0.4803 ms versus
17c6f99's 0.3305 ms; the richer band adds 0.1498 ms. Idle expansion 0.0178 ms,
20-idle-window monitor 0.2386 ms, three-agent refresh 53.94 ms. Native 1Hz and zero
processes per animation step are preserved. This is local wall time, not live
GUI CPU/redraw acceptance.

Final comparison confirms unchanged live Ghostty/tmux files and complete
deployment metadata/content; unchanged tmux server/session/window/seven-pane
identities/root PIDs, prefix, all bindings and hooks. No application was reloaded,
no active window moved and no service/global hook/workmux configuration changed.
Final staged review passed: 10 files cleared the heuristic secret/path and
whitespace checks, all staged blobs matched reviewed working files, and all six
relative documentation links resolved. The authorized local commit deploys
nothing and is not pushed.

The coordinated rollout in MILESTONE-DEPLOYMENT.md is still mandatory: new
inactive release → legacy tmux bridge → companion Ghostty migration/reload and
physical verification → explicit second tmux reload enabling n. Until then n
creates windows. Physical shimmer/keyboard delivery and real Codex hooks/trust
remain acceptance gates. Rollback restores original forwarding before c's default.
The commit-keyed/idempotent staging-tool improvement remains a separate follow-up.

Next single action: review the committed refinement and separately approve
inactive staging of that exact new commit and the unchanged 15-file manifest.
No activation, migration, reload or service action is authorized by this record.

## Broader milestone record — 17c6f99

**2026-10-22 — activity dashboard + persistent Doom development milestone.**
Production remains ec518f0. The user reports that all original physical tmux
acceptance tests passed: popup appearance/navigation, window movement and
boundaries, focus preservation, Cmd+1–9 and pane shortcuts. This is user-reported
acceptance, distinct from the earlier agent reload/migration evidence below.

The new milestone is implemented in the development repository only. **No new
release has been staged or activated; no live configuration, global hooks,
workmux settings or application/service has been changed or reloaded.** Existing
standalone editors and Codex conversations have not been replaced. No persistent
LaunchAgent was installed, bootstrapped, enabled or restarted.

## Implemented and verified in isolation

- Imported cdev/cdev-pin Fish functions and the existing conversation-selection
  helper. Fresh/project-scoped --last/UUID-pin policy, naming, collision guards,
  concurrent reuse and no duplicate-agent behavior remain covered. Failed new
  panes stay visible rather than being killed or retried as fresh conversations.
- Added advisory invocation-local Codex hooks pinned to actual socket/pane/launch
  identity, a private event cache, native tmux format monitors, high-contrast
  crimson/silver title shimmer and session-local attention cycling. Global hook
  definitions, workmux configuration and notifications remain unchanged.
- Workmux commands can track plain panes, but none of the current cdev panes had
  usable status and its sole record was stale. New cdev launches get the scoped
  adapter. Existing sessions without evidence stay unlabelled. Real CLI hook
  trust/delivery, including whether review repeats for per-launch definitions,
  remains a live acceptance gate; there is no trust bypass.
- Keys: Ctrl+F n attention, c project-directory creation, Shift+N ordinary next
  window. n previously created a window; c was standard new-window. Shift+N is
  unbound in the installed defaults. Preflight refuses live key/title/hook-slot
  conflicts. A discovered Ghostty conflict is handled explicitly: Cmd+Shift+N
  forwards old n, so the candidate changes only that Ghostty line to Ctrl+F c.
  The installer keeps n as new-window until the companion is adopted/reloaded;
  background monitoring cannot rebind it. All other tested mappings remain
  unchanged, including Option+h/l,
  numeric selection, popup, pane navigation, Space next-layout and workmux Tab.
- Added one named Doom foreground manager, terminal clients with native Doom
  workspaces and stable per-frame roots, and a separate LaunchAgent definition/
  explicit management tool. SPC f f uses that frame's root; local C-x C-f and
  outside-project navigation retain buffer directories. Explicit standalone
  editor and dashboard-off modes reverse the two features independently.
- Imported a sanitized Doom module snapshot/public terminal preferences for tests,
  including the actual font and focus settings. No private Org/custom/identity
  content or captured environment dump is tracked. Audited generated-startup
  hashes fail before loading changed fixture dependencies.
- Extended the existing complete-release manifest to 15 payloads, new local
  parsers and @HOME@ rendering. Only two Fish functions and one LaunchAgent need
  additional adoption for the editor/service; full attention navigation also
  requires the separately approved Ghostty companion file. Helpers can stay
  release-local.
  No deployment transaction/backup framework was replaced.

## Validation evidence

Before changes: python3 -B scripts/test.py --integration passed all 47 existing
regressions. After implementation and fixes: **79 tests passed in 43.647s** with
python3 -B scripts/test.py --integration. No remaining automated failures.
Private sockets, inert native Codex stand-ins, synthetic history/hooks and
sanitized disposable Doom homes were used; production main was never a test
subject. Production queries were limited to read-only identity/binding/status
metadata and file fingerprints. No active window was reordered programmatically.

Coverage includes concurrent agents, stale launch/session/turn/server/PID data,
termination, disconnected clients, title/pane/window movement, approval/stop
transitions, empty/cycling attention queues and actual binding invocation;
bounded observer-lock contention and the Ghostty companion/fallback gate;
project naming/reuse/collisions/pins/resume failures; two real Doom terminal
frames with independent perspectives, nested files/scratch/workspace changes,
actual SPC f f and local C-x C-f, reconnection, retained unsaved buffers, client
pane closure, duplicate-manager rejection and unavailable-server behavior.
The inspected macOS 27.0/bundled-libgccjit native compilation workaround passes.

All old deployment regressions still pass. Added-component rollback refuses an
old release missing managed paths, then succeeds after restoring new component
backups, including contents, modes and original absence. New malformed Python,
Fish, Elisp and plist inputs are rejected. Launchctl mutations are mocked only.

Final private benchmark, 24-character titles: working expansion 0.3060 ms;
20-idle-window monitor 0.2352 ms; changed-cache refresh for three agents 47.14 ms;
unchanged working hook 23.27 ms. Native animation creates zero processes per
step. An unchanged monitor creates no renderer process; unchanged tool events
avoid a tmux/cache update, with a bounded 30-second lease renewal. These are
local wall-time measurements, not a system-wide CPU or live-redraw claim.

Read-only final comparison passed: all inspected live file bytes/modes/link
metadata and the full deployment tree (including ec518f0 receipt/payload/backup)
match baseline. Production server/session/window/pane identities and all loaded
binding/hook hashes are unchanged, including all seven pane IDs/root PIDs.
The original key/title/hook checks pass; strict attention preflight flags its
required Ghostty companion, while display-only preflight passes with old n.
No new named-server directory, dashboard state or Emacs/Doom launchd registration
exists. The current state environment matches the proposed
service default. Deployment preflight passed all 14 local checks and dependencies.
Its first sandboxed attempt could not create the isolated parser socket; the
narrowly approved retry passed. No blocked attempt is counted as a pass.
Final staged review: 43 files passed the heuristic secret/path scan and staged
whitespace check. All staged blobs matched the reviewed working files and all
22 relative documentation links resolved. The diff includes the previously
uncommitted migration/reload history below; that history was preserved.
The authorized local milestone commit includes these results; no commit deploys
and nothing has been pushed.

## Review artifacts and boundaries

- [Activity design/evidence and limits](ACTIVITY.md), including the
  [offline four-state preview](previews/dashboard.html).
- [Doom server/frame architecture](DOOM-SERVER.md).
- [Exact proposed staging/adoption/rollback sequence](MILESTONE-DEPLOYMENT.md).
- Manifest component/target matrix and independent Terminal.app recovery are
  documented. Restore companion Ghostty forwarding before restoring c's default;
  new Fish/service backups must precede pointer rollback to ec518f0. Keep pinned
  releases while processes may reference them.

Remaining live acceptance: Ghostty companion migration/reload/key delivery;
normal Codex hook trust/delivery, precise concurrent
approval-resolution limits, terminal redraw/appearance/physical keys, actual
private Doom/Org customization, launchd bootstrap/recovery/login/reboot. The
sanitized fixture's snippet warnings are not a claim about the private config.
Existing legacy editor panes remain standalone until the user changes them.

The commit-keyed/idempotent/exclusive staging guard remains a **separate**
follow-up. Its earlier tested temporary implementation has not been folded into
the checked-in tool during this milestone; stage still copies a clean reviewed
checkout to a unique ID. Preserve the original ec518f0 release and backup.

## Next single action

Review the committed candidate and request separate approval for **inactive
staging only** of that exact commit/15-file manifest. No activation, live
migration, reload, service installation or hook trust is implied. Follow
MILESTONE-DEPLOYMENT.md for each later approval. Stop before production writes.

---

The following is historical evidence; its earlier next-action statements do not
supersede the current milestone record above.

# Historical record — earlier deployment and reload

**As of 2026-10-22; tmux reload at 00:39 EDT (04:39 UTC). Agent-observed.**
The existing tmux server loaded the migrated ec518f0 configuration once, with
exit 0 and empty stdout/stderr. The session, four windows, seven panes and client
survived unchanged. Prefix/navigation/numeric/popup/reordering bindings are
verified. Diagnostic caveats are recorded below; physical acceptance is pending.
**No deployment files, Ghostty configuration or application processes were replaced.**

| Milestone | Status | Evidence |
|---|---|---|
| Targeted Ghostty/tmux audit | Complete | Exact sources/includes inspected; privacy-screened; original hashes in INVENTORY.md |
| Approved development imports | Complete | Four regular copies; unused Ghostty profile and empty macOS override not adopted |
| Popup and window reordering | Loaded; physical acceptance pending | Pinned helper/styles and M-h/M-l installed; no live movement or popup invocation used for verification |
| Three-layer architecture/tooling | Implemented in repo | Complete copied releases, pinned references, checks, backups, journals, activation, rollback and restore |
| Agent governance | Updated | Repo edits/tests/docs/reviewed local commits authorized; external actions remain separately gated |
| Final staged review | Complete | 28-file preflight, staged whitespace, preservation review and documentation links passed |
| Local version control | ec518f0 payload; 1f28195 tooling | HEAD remains 1f28195; clean before migration; this status update is uncommitted; no remote publication |
| Production staging | Complete; selected for tmux | Published ec518f0 payload unchanged; independent regular copies, mode 444; current established |
| Pointer-restoration repair | Committed as 1f28195 | Backup journal schema 2, pointer/drift/dependency guards and resumable restoration; 47 tests pass |
| Initial tmux migration | Complete and verified | Five links, three verified originals, two absent-path records; backup 20261022T040111.754783Z-a455ecd7 |
| Tmux reload | Authorized; performed once | source-file returned 0, no output; all identities/start times retained; diagnostic caveats below |
| Other application reload/restart | NOT PERFORMED | Ghostty, Doom and Codex processes/configuration preserved |
| Manual loaded UX acceptance | NOT PERFORMED | Physical keys, actual popup appearance/navigation and movement await user testing |

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

The latest approval authorized a fresh production preflight followed by backup,
initial pointer establishment, exactly five tmux file migrations and verification.
Those operations completed. It expressly withheld reload, Ghostty/adjacent
configuration changes, automatic rollback and new commits. This status record
documents the verified outcome; no commit was created during migration.

The next approval covered one controlled reload of the existing tmux server,
following source/plugin/hook inspection and parse-only validation, then read-only
verification. It withheld window movement tests, deployment changes, application
restarts, commits and unrelated repairs. No recovery or second reload was run.

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

## Verified pointer-restoration repair (before production migration)

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

## Production tmux migration — 2026-10-22 04:01 UTC

Preflight confirmed a clean working tree at exact HEAD
1f28195a6c7f06048b5e2e9d1e5c859c1e72daca, the intended staged manifest and rendered
ec518f0 blobs, all payload modes, dependencies/parsers, absent current and empty
backups/history. All five live states matched the previous audit. The actual
template migration/restore integration test was rerun in a temporary home and
passed, including all three original bytes/modes, two absent helpers and removal
of current. The helper remained readable at mode 444 through its explicit sh
invocation. No staged file was changed or replaced.

Production mutation used Deployment.migrate(RELEASE, "tmux") from the committed
tool under its existing writer lock, with baseline drift checks immediately
before it. All three verified backups and the durable journal preceded any live
replacement. No alternate migration or automatic rollback path was used.

Backup ID: **20261022T040111.754783Z-a455ecd7**

```text
/Users/czuba/.local/share/dotfiles-active/backups/20261022T040111.754783Z-a455ecd7
```

The journal is schema 2, status migrated, current_before null, and current_after
equal to the link text below. The backup directory is mode 700 and backup.json
mode 600. The three original regular files' hashes, modes (644), ownership and
modification times were verified; both originally absent helper paths are
recorded without fabricated backup files.

Current points to:

```text
releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16
```

All targets below are relative to /Users/czuba/.local/share/dotfiles-active:

| Live file | Verified symlink target |
|---|---|
| ~/.tmux.conf | current/tmux/tmux.conf |
| ~/.config/tmux/czuba-navigation.conf | current/tmux/czuba-navigation.conf |
| ~/.config/tmux/cheatsheet.txt | current/tmux/cheatsheet.txt |
| ~/.config/tmux/show-shortcuts.sh | current/tmux/show-shortcuts.sh |
| ~/.config/tmux/shortcuts.lesskey | current/tmux/shortcuts.lesskey |

Each resolves to the exact immutable-by-convention release file, mode 444, with
matching bytes/hash and payload inode. The staged release's metadata/content and
Ghostty's live regular file remained unchanged. Deployment history is empty;
there is exactly one completed migration backup and no pending recovery journal.

Post-migration metadata queries confirmed the same tmux server PID 72611, the
same session, all seven pane IDs/PIDs/window indices, and process start times.
Five matching protected application processes also retained their IDs/start
times. The loaded popup binding hash is unchanged. No live reload, restart,
session mutation, process termination or rollback was performed. Opening the
old popup may read new cheatsheet text before reload; colors/new bindings await
separate reload and acceptance.

Exact initial-migration rollback command, **not executed**; requires its own
authorization and preserves running processes:

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py restore --backup 20261022T040111.754783Z-a455ecd7 --approve
```

It restores original contents/modes, removes only the two originally absent
managed helper links, then removes current after dependency/drift checks.
Temporary verification evidence (not required to run restoration) is under:

```text
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/dotfiles-live-migration-xsampn4q/
```

baseline.json, preflight-passed.json, restore-rehearsal.log, tmux-before.json,
tmux-after.json and migration-result.json record the measured checks. No pane
contents, working directories, titles or command lines were captured.

## Controlled tmux reload — 2026-10-22 04:39 UTC

The five live symlinks, staged manifest/content/modes and original backup were
reverified. Existing sessions, windows, panes, clients and active pane/application
process identities were recorded before the reload. Source commands resolve to
the pinned navigation include and the installed Dotbar/TPM entrypoints. TPM's
only declared plugins are TPM, Rose Pine and Dotbar; no alternate/system tmux
config or legacy TPM list introduced additional plugins. Shell syntax checks
passed. No active global/session/window/pane hooks were found.

On server PID 72611, source-file -n parsed ~/.tmux.conf and the pinned navigation
include with exit 0 and no diagnostics. This did not execute the config. The
approved source-file ~/.tmux.conf was then executed **once**, with explicit socket
selection and no-start protection. It returned 0 with empty stdout/stderr.

Immediate before/after snapshots verified the same one session, four windows,
seven pane IDs/PIDs and active selections, one attached client, and 15 recorded
pane/application process IDs/start times. No window was moved or renumbered by
verification; no pane was killed, client detached, server restarted or popup
invoked. Effective session prefix is C-f, including inherited options.

Only prefix ?, M-h and M-l changed. All other binding definitions, including
Shift+H/L, window/pane menus and TPM's existing I/U/M-u bindings, are unchanged.
The installed h/j/k/l and Ctrl+h/j/k/l guards still prevent wrapping. Numeric
bindings 1–9 select :1–:9, base-index is 1 and renumber-windows is on; Ghostty's
Cmd+digit mappings and Cmd+Shift+P mapping remain unchanged.

Loaded M-h/M-l check window_start_flag/window_end_flag, then run the captured
session/window-ID swap, reselection and renumbering sequence. Both keys were
unbound before reload. The popup now pins show-shortcuts.sh and its sibling
cheatsheet/lesskey to ec518f0, invokes the mode-444 helper through sh, and has the
specified light/dark/blue styles. Q still provides list-keys -N help.

Dotbar status position/justification/colors, Rose Pine clock/copy-mode colors and
TPM bindings match their expected resulting state. No hooks appeared. Deployment
and backup trees, all five symlink objects and Ghostty's live file retain their
original hashes, permissions, inodes and modification/change timestamps.

Diagnostic caveats: the server's rolling log contains recurring no-such-pane/
window lookups for %2 (234 entries in the captured sample), matching the stale
pane context inherited by the verification client. Their attribution was not
fully established; they were preserved and not repaired. Two other messages
were caused by read-only verification probes using unsupported -q with
show-window-options; the queries were corrected to show-options. No config change
or second reload was used to address those verifier issues. TPM suppresses
individual plugin output, so plugin verification relies on observed diagnostics
and loaded postconditions rather than a claim that all child output was visible.

Evidence, including reload-command.json, reload-exit.json, reload.stdout.log,
reload.stderr.log, tmux-before-reload.json, tmux-after-reload.json,
option-api-diagnostics.json, diagnostic-candidates.txt and verification-summary.json:

```text
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/dotfiles-tmux-reload-2fzvmlfx/
```

The earlier temporary verifier failures are retained for review. They did not
trigger configuration repair, a deployment operation or another reload. HEAD
remains 1f28195; only this existing uncommitted status record was updated.

## Separate staging-tool follow-up

- Integrate the tested commit-keyed, idempotent staging guard into the checked-in
  deployment tooling. Render exact commit blobs, verify and reuse an identical
  existing release, reject mismatches/collisions without overwrite, and publish
  with an exclusive atomic rename. Test in temporary directories and preserve
  the separation between staging, activation and reload. This documentation
  follow-up does not change any payload, stage a release or trigger deployment.

## Unknowns and retained risks

The original audit's live socket read was denied. This approved migration used
narrow session/pane/process metadata reads and a popup binding hash to verify
continuity. The controlled reload subsequently verified loaded bindings and
plugin postconditions; physical behavior, suppressed plugin diagnostics and the
stale %2 client-context messages retain the limitations described above.
Workmux help attempted to initialize a real log and
failed in the sandbox; no retry against real account state occurred. Doom was
not initialized/evaluated and private Org/iCloud content was not read.
AeroSpace configuration was inspected only and its enabled state remains unknown.

Ghostty's installed CLI documents explicit reload but does not establish watcher
behavior across symlink pointer changes. No GUI watcher or visual contrast test
was authorized. Ghostty migration must address that uncertainty separately.
Syntax checks do not prove physical key delivery or running application behavior.

## Next action recorded then (superseded)

User performs physical/visual acceptance separately: Cmd+Shift+P, popup section
jumps/search/quit, Ctrl+F then Option+h/l (without Shift), movement boundaries and
focus, and Cmd+1–9. Do not programmatically move existing windows for acceptance.
Any investigation or repair of stale client-context diagnostics is a separate
task; no such fix is implied by the reload approval. Ghostty adoption remains
separate. Do not reload again or change deployment state from this milestone.
