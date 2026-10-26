# Current production: transport-free dashboard — 2026-10-25

Signed `c8bd5fa` is active in `20261025T063110.488579Z-723f7740`. The ntfy
transport and its private config/state are removed; shared dashboard/status/
attention behavior and the deployed project workflow remain intact. No phone
alerts from production agents are expected until Collie is connected separately.
See STATUS.md for acceptance and transport-free rollback. Old pager/release
handoffs below are historical; do not recreate their retired destination config.

---

# Current execution policy and remote-resume repair — 2026-10-25

Requested bounded, reversible repairs to existing managed dotfiles are authorized
through tests, commit, staging, activation, canary and documented rollback without
routine intermediate approval gates. Broad/global changes, new migrations,
security/authentication changes, unexplained drift, destructive operations,
unexpected production impact or missing safe rollback still require review.
Keep sandbox/trust enforcement, exact drift checks, immutable releases, existing
sessions and unrelated pending work protected. Never retry an unexplained
production failure before investigating and validating its cause. Git and shell
startup still never trigger deployment automatically.

Signed d84baaa is active in `20261024T235701.367069Z-b1475572`. The revised
primary-first isolated validation and activated-launcher canary passed, including
two exact-UUID remote resumes and an independent genuine approval canceled
without approval. No reload or agent restart was needed. Existing launchers gain
the repair on natural cdev reopening. See STATUS and ACCEPTANCE-HARNESS for
evidence and the exact rollback command. Entries below are historical handoffs.

# Pager and persistent Doom are active — 2026-10-23

Current: `20261023T042036.839310Z-1711bc49` (1118c0a), including accepted pager
commit d70421d. Thirteen exact managed files; the named Doom LaunchAgent is loaded.
Future cdev windows use terminal clients; existing standalone panes are preserved.
Focused tests and actual two-client/server recovery/iPhone acceptance passed.
STATUS.md records exact backups and independent rollback commands. Pager recovery
uses its disable command; Emacs recovery preserves the accepted pager release.
Existing shared-server lifecycle evidence limitations remain explicit. No tmux or
Ghostty reload was performed. Earlier rollout notes below are historical.

---

# Current cdev repair — 2026-10-22

Release `20261023T034028.602247Z-9d3ec165` (343faaf) is active. Only the Python
session helper changes; standalone Fish/Doom remains in use. Exact project UUID
pins and verified shared-server remote resume replace `--last`. No reload was
required. See STATUS.md and [CDEV-RECOVERY.md](CDEV-RECOVERY.md) for checks,
private backup and rollback. Earlier rollout notes below remain historical.

---

# Dashboard accepted; disposable review cleaned up — 2026-10-22

Physical Ctrl+F n acceptance passed. The review session and all owned test
processes have been removed after identity/descendant checks. Main's four windows,
seven panes, two clients and all checked production processes survive. Active
release is 20261023T002013.807639Z-023596db (9a861dc), with eight managed live paths.
No further dashboard action is pending. Persistent Doom remains deferred.
See STATUS.md and [ATTENTION-ROLLOUT.md](ATTENTION-ROLLOUT.md) for final evidence,
cleanup details and recovery. Entries below describe earlier rollout states.

---

# Attention-persistence repair is active — 2026-10-22

Current is releases/20261023T002013.807639Z-023596db (9a861dc). The one controlled
repair reload and actual aged-event/lifecycle checks passed; final physical n
acceptance and conditional cleanup are pending. Hook definitions, cdev/editor
launching and other keybindings are unchanged. All eight managed paths share the
pointer. The user's confirmed manual Fish function is preserved. See
[ATTENTION-ROLLOUT.md](ATTENTION-ROLLOUT.md) and STATUS.md for current evidence and
recovery; deployment commands below may refer to historical releases.

---

# Current deployment handoff — 2026-10-22

The Codex dashboard is active on release 20261022T215047.249499Z-618a6bc8 after
one authorized tmux reload; physical acceptance is pending. Eight managed live
paths now share current: five tmux files, Ghostty, and the two cdev helpers.
Every future pointer operation must account for all eight. Live Fish/Doom and
clipboard configuration remain unchanged; editor/service candidates are deferred.
See [DASHBOARD-ACCEPTANCE.md](DASHBOARD-ACCEPTANCE.md) and STATUS.md before
using historical commands below. Native trust is user-owned; repository edits
still confer no deployment/reload authority.

Bounded dashboard recovery is disable plus read-only verification. A full
reload explicitly turns the feature on again; do not use it to preserve the off
state. Helper restoration removes the fixed adapter path and requires inspection
of active instrumented clients. Broader rollback is not implied by a display issue.
The separate commit-keyed idempotent staging improvement is still outstanding.

---

# Development, deployment and activation workflow

## Authority and boundaries

The user's 2026-10-25 standing policy authorizes requested bounded, reversible
repairs through verified deployment and canary using the existing tooling.
Repository edits alone confer no deployment authority; the task and standing
policy define its scope. Broad/global changes and substantive risks still need
explicit review. Follow `AGENTS.md`; these rules supplement actual sandbox and
approval controls.

The three layers are the development checkout, copied releases under
`~/.local/share/dotfiles-active/`, and exact live paths. No live/deployment symlink
may point into the checkout. No automatic deployment or reload is allowed.

## Repository work

For creating personal projects and opening local or upstream repositories, see
[PROJECTS.md](PROJECTS.md). Global instructions, `cnew NAME` and `cdev NAME` are
deployed in signed 632b28d / `20261025T061731.748309Z-45cef594`; STATUS records
acceptance and the two new managed-path backups. Existing Fish processes retain
already-loaded function definitions; no session restart or tmux reload is needed.

1. Read current status and the relevant source. Inspect exact live sources as
   needed, without broad home scans, private data, or unrelated repositories.
2. Edit development copies. Preserve unrelated bindings, startup, theme and jobs.
   Imported tmux includes/popup commands use the `@RELEASE@` template token.
3. For routine reversible repairs, run focused tests for the changed behavior
   and nearby regressions. Use the full suite for cross-cutting changes, relevant
   failures or an explicit request. Integration servers always
   have private sockets, `-f /dev/null`, inert test panes and owned-session cleanup.
   User plugin code is not executed. Parser success is not live UX acceptance.
4. Review and stage intended files; run `python3 scripts/preflight.py`,
   `git diff --cached --check`, and inspect `git diff --cached`. Local commits are
   authorized; honor current signing settings. A commit performs no deployment.
5. Maintain a brief status and useful test/recovery evidence. Preserve concurrent
   edits; avoid repeated audits or elaborate reports. A consolidated approval
   covers the operations it explicitly names: continue successful authorized
   steps without seeking routine confirmation, stopping at genuine new boundaries.

Commands below use POSIX sh/Zsh syntax (also valid as individual Fish commands).
Mutation examples are instructions for future approved operations, not authority
to run them. `--approve` prevents accidental invocation; it is not user consent.

## Release design and why no Stow

The standard-library Python tool copies a manifest's complete file set into a
hidden staging directory on the deployment filesystem, renders release-local
references, validates it, writes hashes/modes and a receipt, then renames it to
`releases/ID`. Files become read-only; the tool never updates a release in place.
They are copies, not hard links or links to Git. An owner can still chmod/edit
them manually; integrity validation detects such drift, not malicious tampering.

GNU Stow links a package tree to live targets. It could link a stable copied
release, but would still need the copying, validation, backup, release pointer,
failure handling and rollback layer. It adds a dependency without simplifying
this design. No Stow installation or whole-directory adoption is planned.

Release files, history and original-file backups stay outside Git. The state
root supports spaces but rejects quote/control/shell metacharacters because
rendered tmux/shell paths must be unambiguous. Releases cannot be relocated:
their include/helper paths pin their original absolute release directory.

## Read-only preflight and plan

```sh
python3 scripts/deploy.py check
python3 scripts/deploy.py plan
```

Checks cover regular files and source ancestry, complete declared references,
private tmux parsing, sh syntax, Ghostty validation of the explicit candidate,
tool availability, external plugin files/executable permissions, supported
tmux/less versions and empty/absent unmanaged Ghostty overrides. They do not
install packages, execute plugins, call workmux, start Fish, load Doom, access
credentials or query the live tmux socket.

Ghostty's explicit `+validate-config --config-file=PATH` bypasses default config
files (tested). That action rejects the otherwise documented general
`--config-default-files` option, so it is not passed. Unknown Ghostty includes
are rejected until a managed include graph is explicitly adopted.

Plugin declarations and executable presence are checked; plugin contents,
workmux functionality, fonts/fallback appearance and active loaded bindings
still require manual acceptance. A blocked check fails; do not treat it as a pass.

## Operation 1: stage a complete release

Obtain approval to write this specific snapshot to the deployment root.
Then, from the checkout:

```sh
python3 scripts/deploy.py stage --approve
```

Record the returned release ID and review `releases/ID/release.json`. Staging
does not change `current`, back up live files, create live symlinks or reload apps.
A failed stage removes its owned incomplete temporary directory; no release
becomes selectable. Source files and deployed files have independent inodes.

## Operation 2: initial migration, one component at a time

First verify the candidate and inspect exact live targets:

```sh
python3 scripts/deploy.py verify --release RELEASE_ID
python3 scripts/deploy.py plan --release RELEASE_ID
```

Present the five tmux targets from the manifest, original file types/modes,
new parent directories if needed, expected immediate-read effects, and the
initial restore procedure. Ghostty migration is a separate operation and remains
unapproved. Its automatic reload behavior must be resolved before adoption.

After explicit approval for those tmux files, backups and managed symlinks:

```sh
python3 scripts/deploy.py migrate --release RELEASE_ID --component tmux --approve
```

The tool copies every existing exact target, preserves its content and POSIX
mode with copy2, verifies those backups, and records absent targets. All backups
precede any live replacement. They are in
`backups/BACKUP_ID/files/<original-relative-path>`, with a durable `backup.json`
journal. Backup journal schema 2 also records current_before (null for absence,
otherwise the exact symlink text), current_after, and every declared live path
across components. These records precede pointer/file changes. Record that ID
and path before any separately approved reload.
ACL/resource-fork preservation is not certified by these tests.

The first migration establishes `current -> releases/ID`. It replaces each live
file through an adjacent temporary symlink plus atomic rename. Parent-directory
symlinks, unknown live symlinks and nonregular targets are refused. Adding a
component later must use the existing current release; migration cannot silently
activate a different release. An older current release remains valid for
migration even when a newer release has been staged; the newer one stays inactive.
Pointer drift after the backup is refused rather than overwritten.

**The set of live paths is not switched atomically.** A failure can leave some
old files and some links to the complete new release. The prepared journal blocks
activation until explicit restoration/recovery. No implicit rollback or reload
occurs. Newly created empty parent directories may remain after restoration.

Initial migration can expose new reference text immediately: the old popup
binding reads the live cheatsheet path. New colors/bindings require the tmux
reload. This interim state must be included in the migration approval.

## Operation 3: later activation or rollback

A later stage remains inactive. Review its plan; it affects **every already
managed file** behind the shared pointer, including other migrated components.

```sh
python3 scripts/deploy.py activate --release NEW_ID --expect-current OLD_ID --approve
```

This requires its own approval. The tool locks deployment writers, checks the
expected current ID, all copied hashes/modes, references, parsers, dependencies
and managed-target drift, and records a prepared transition before atomically
renaming an adjacent symlink over `current`. It then marks the history event
applied. Removing/redirecting a managed mapping is refused.

Only the single pointer rename is atomic. Separate application reads on either
side of that rename can observe different releases. Tmux includes and popup
helpers pin a release so an explicit source operation does not mix includes.
There is no distributed transaction over multiple processes or simultaneous
independent path migrations. The lock coordinates this tool's writers, not
external editors. Stop concurrent manual edits during an approved migration.

To undo a later activation, first review the previous ID in `history/`, then
obtain rollback approval:

```sh
python3 scripts/deploy.py rollback --expect-current NEW_ID --approve
```

Rollback validates the previous release and performs another logged atomic
pointer change. It can toggle between the last two releases. The actual current
pointer is authoritative after a crash; a prepared event whose destination is
current records a switch that may have completed before the event was finalized.
If validation/dependencies are broken, use the independent recovery procedure.

To undo the initial adoption, or recover a partial migration, obtain separate
restoration approval:

```sh
python3 scripts/deploy.py restore --backup BACKUP_ID --approve
```

Restoration validates every backup and target first, refuses user drift, restores
original contents/modes by adjacent rename and removes only managed links whose
original files were absent. **Files are restored before the pointer.** If the
pointer originally did not exist, restoration removes it only after checking all
declared live paths from this and other backup journals for remaining dependencies,
including relative links and aliases. If another component still uses current,
its backup must be restored first. Existing pointer text is preserved exactly;
an unexpected replacement, deletion or different target is refused. Migration
still cannot switch releases; undo later activations through their separate
rollback procedure before restoring the initial migration.

The durable restoring journal blocks migration/activation until recovery is
complete. A failed file operation, dependency check, pointer operation or journal
finalization returns failure and keeps enough state to retry the same restore
command. Already restored files are validated and skipped. Repeating a successful
restore validates all backups, originals and the original pointer state without
rewriting or deleting anything. New user changes cause a refusal.

Releases, backups and empty directories are retained. Legacy schema-1 backup
journals lack the original pointer state and require reviewed manual recovery;
the tool never guesses that it was absent. **Release receipts and the payload
manifest remain schema 1** and existing staged releases remain usable unchanged.
No release garbage collector is provided: loaded tmux helpers may still use old
release paths.

## Reload and process effects

The tool never executes a reload/restart, sends keys, closes user panes or
terminates application processes.

| Change | When it can become visible |
|---|---|
| Git edit/commit or staged copy | Never changes live applications |
| Atomic current change | Immediately to a new open of a managed file |
| Tmux config/bindings | New server or explicit source-file; no file watcher |
| Pinned popup text, renderer, less keys | After that release's binding is loaded; later openings stay with that loaded release |
| Initial migration with the old popup binding | New text may be read immediately; old styling remains until reload |
| Ghostty appearance/keybinds | Explicit reload applies supported settings; symlink watcher behavior remains unverified |
| Ghostty command/initial-command | New terminal surfaces / first startup surface; existing jobs are not replaced |
| Fish cdev functions | Candidate only; new shells/autoloads can read changes immediately; loaded definitions need explicit source/new shell |
| Doom integration | Candidate only; loaded after normal startup of a new named server, never injected into existing editors |
| LaunchAgent | File installation/bootstrap/kickstart/shutdown require separate approval; a loaded job retains its pinned definition |
| Other Fish/Doom/AeroSpace | Unmanaged and outside this milestone |

Installed Ghostty 1.3.1's bundled ghostty.1.md (+edit-config, lines 185–190)
explicitly says automatic config reload is not yet supported; use a manual
reload. Its reload_config action also warns that not all settings apply at runtime.
A running-GUI watcher test across symlink changes was not authorized/performed.
Conservatively treat a Ghostty pointer change as potentially immediately
observable and retain the legacy n/c bridge until explicit GUI reload and physical
acceptance; do not rely on an untested watcher assumption as an ordering barrier.

For a tmux reload, propose the exact source command and effects separately.
Sourcing the main config also re-executes its existing plugin startup commands.
Do not run it, press Ctrl+F r, or trigger Ghostty's reload key without approval.
Manual acceptance then checks popup contrast, navigation, window order/focus and
Cmd+1–9 while preserving the user's working panes.

## Failure and recovery contract

- Parser/dependency/hash/drift failures stop before activation.
- A partial migration/restoration retains its original-file journal and blocks
  further migration/activation (prepared or restoring); no automatic recovery
  operation is implied. A restore is marked restored only after verifying the
  file states, restoring/verifying the pointer, and syncing its directory.
- Pointer replacement failure keeps the old pointer; a crash after replacement
  may leave the new pointer and a prepared history event. Inspect both.
- fsync and same-directory rename improve local filesystem durability. They are
  not a guarantee against storage failure, hostile mutation or power-loss loss
  of drive caches.
- Keep all working releases and original-file backups. Recovery must remain
  possible from [Terminal.app](RECOVERY.md), with no Ghostty/tmux/Doom/Codex.


## Activity and persistent-Doom milestone

The accepted production tmux release remains ec518f0. New dashboard, cdev/client
and LaunchAgent files are development candidates. Follow the exact
[milestone deployment order](MILESTONE-DEPLOYMENT.md), not an implicit extension
of the earlier five-file migration approval. Stage/activate/reload, migration of
two Fish functions, the companion Ghostty file/reload, installation of one
LaunchAgent and bootstrap are distinct
approval boundaries. Includes/helpers pin a complete release, so their optional
live mappings do not need adoption. Never migrate whole configuration trees.

New validators read Python AST, run Fish --no-config -n, read/check-parens Elisp
in Emacs -Q --batch without evaluation, and parse plist structure. No validation
starts a production daemon or loads private Doom startup. Templates additionally
render @HOME@ for logs; releases remain home/path specific.

Disposable Doom tests use an audited module snapshot, sanitized public terminal
preferences (including existing fonts/focus hook), generated-startup copies and
read-only installed libraries. A startup fingerprint refuses changed generated
code before loading it. Inspect paths/modules before updating that fingerprint;
never blindly bless new hashes to make a test green. No private Org/custom,
identity, clipboard content or captured environment dump belongs in the fixture.

Dashboard and editor reversal are independent: dashboard disable and
CDEV_DASHBOARD=0 leave Doom/conversations running; CDEV_EDITOR_MODE=standalone
leaves the dashboard and server buffers intact. These proposed live operations
still require their own approval. Once Fish/service mappings are migrated,
restore their backups before pointer rollback to ec518f0: that release lacks
those files. The multi-component refusal and recovery order are regression-tested.
The deployment/restore tool never controls application processes automatically.
