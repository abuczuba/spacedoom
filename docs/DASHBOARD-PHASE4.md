# Phase 4 completed through automated acceptance — 2026-10-22

All native trust/real production event/concurrency/workmux gates passed, followed
by exactly one successful production reload. Release
20261022T215047.249499Z-618a6bc8 is active; cdev backup is
20261022T215153.419622Z-a559508a. Attention is on; original resources survived.
See [DASHBOARD-ACCEPTANCE.md](DASHBOARD-ACCEPTANCE.md) for actual commands,
evidence, recovery and the remaining physical checklist. The next action is user
keyboard/visual acceptance, not repeating any stage/migration/reload below.
Persistent Doom/Emacs services remain deferred. Earlier instructions are retained
as history; the recovery correction immediately below supersedes the older
full-reload-after-disable instruction.

---

# Recovery correction — 2026-10-22

Source inspection during authorized Phase 4 acceptance found that tmux.conf
unconditionally sets @dotfiles-dashboard-enabled on. Therefore the older claim
below that dashboard-disable survives a full tmux.conf reload is incorrect.
**Do not run the full recovery reload shown in the historical proposal.**

The existing, tested disable command directly restores safe n/c window-creation
bindings, clears dashboard monitors/labels and restores the prior status interval.
For this rollout's bounded recovery, run disable once, verify bindings, hooks,
formats and original process identities by read-only queries, then stop. No extra
reload is necessary to restore those runtime bindings. A later full configuration
reload/new server would re-enable the feature and requires deliberate review.
This selects the already authorized disable operation and zero additional reloads;
it changes no deployed payload, hook trust, pointer, Doom or clipboard setting.
The approved initial attention reload remains gated on all real-event checks.

---

# Continuation stopped at native trust — 2026-10-22

After the user reported trusting all eight, fresh native metadata still reports
UserPromptSubmit, Stop and Interrupt untrusted, with unchanged definition hashes.
See [PRODUCTION-HOOK-REVIEW.md](PRODUCTION-HOOK-REVIEW.md). No real production
test prompt or reload followed. Preserve the current helper migration and backup;
resume the already approved gates only after native trust is actually complete.
The earlier focus change remains unattributed; the user cannot establish cause.

---

# Approved rollout in progress — 2026-10-22

The user approved the consolidated sequence below. New e38e18d release
20261022T215047.249499Z-618a6bc8 is active and the two cdev helpers are adopted.
Backup: 20261022T215153.419622Z-a559508a. The native user trust gate is pending;
no production reload or attention activation has occurred. See
[PRODUCTION-HOOK-REVIEW.md](PRODUCTION-HOOK-REVIEW.md) for exact definitions,
attach instructions, verification, recovery and the focus-selection observation.
After native review, use the remaining sequence with this actual release ID;
do not restage/reactivate/remigrate or repeat the completed Phase 1–3 work.
The earlier proposal below is preserved verbatim for its gated procedure.

---

# Remaining dashboard Phase 4 — proposed after real hook acceptance

**Proposal only; no production operation is authorized by this document.**
The isolated real-event acceptance of e38e18d passed; see
[HOOK-ACCEPTANCE.md](HOOK-ACCEPTANCE.md). Obtain renewed consolidated approval
for this bounded sequence and its recovery before running mutation commands.
Native hook trust always remains the user's own interactive decision.

This supersedes the uncompleted dashboard instructions in
[MILESTONE-DEPLOYMENT.md](MILESTONE-DEPLOYMENT.md). Do not repeat Phase 1–3 or
adopt the candidate Fish/Emacs launcher. Production is recovered Phase 3B:
`current -> releases/20261022T163617.469413Z-497daec6`, Ghostty forwards
Cmd+Shift+N to Ctrl+F c, both tmux n/c create windows, and attention is off.

## Candidate, affected paths and preflight

Only `configs/cdev/codex_session.py` and `configs/cdev/activity.py` differ between
the active 8dad372 payload sources and repair e38e18d. A complete new 15-file
release is required; never modify the existing release. The shared pointer
already serves these six paths, so all six must be inspected before activation:

| Live path | Payload through `~/.local/share/dotfiles-active/current/` |
|---|---|
| `~/.tmux.conf` | `tmux/tmux.conf` |
| `~/.config/tmux/czuba-navigation.conf` | `tmux/czuba-navigation.conf` |
| `~/.config/tmux/cheatsheet.txt` | `tmux/cheatsheet.txt` |
| `~/.config/tmux/show-shortcuts.sh` | `tmux/show-shortcuts.sh` |
| `~/.config/tmux/shortcuts.lesskey` | `tmux/shortcuts.lesskey` |
| `~/.config/ghostty/config.ghostty` | `ghostty/config.ghostty` |

Later helper-only migration adopts exactly two further paths:

| Live path | Expected pre-migration state | New payload through `current/` |
|---|---|---|
| `~/.config/cdev/codex_session.py` | Original regular 0644 helper | `cdev/codex_session.py` |
| `~/.config/cdev/activity.py` | Absent | `cdev/activity.py` |

Revalidate these expectations, original hashes and backup contents immediately
before migration. Preserve the existing live Fish functions, standalone
`emacs -nw`, compiler environment, reuse and duplicate-agent protection.
Do not migrate `fish-cdev`, `doom-client`, `doom-service` or `tmux-dashboard`;
dashboard scripts are already included directly from the complete release.

Before writing: inspect concurrent changes, deployment lock/journals and pending
recovery; verify release integrity, live targets, global hook/workmux hashes,
original backups, dependencies, socket/server identity and safe plugin/hooks.
Record fresh session/window/pane/client and protected-process identities.
Material drift stops the operation. Preserve unrelated dirty documentation.

## Stage once, verify, activate, then adopt only the helpers

POSIX sh/Zsh commands below are a future approved sequence. Replace the new ID
only with the tool's actual returned value; re-confirm the production socket.

```sh
cd /Users/czuba/dev/dotfiles
git diff --exit-code e38e18d -- configs deploy scripts tests AGENTS.md
python3 -B scripts/deploy.py check
python3 -B scripts/deploy.py stage --approve
# Record the returned ID and commit-to-rendered-payload audit before continuing.
DASHBOARD_RELEASE='<returned-release-id>'
DASHBOARD_OLD_RELEASE=20261022T163617.469413Z-497daec6
DASHBOARD_ROOT=/Users/czuba/.local/share/dotfiles-active
DASHBOARD_PATH="$DASHBOARD_ROOT/releases/$DASHBOARD_RELEASE"
DASHBOARD_SOCKET=/private/tmp/tmux-501/default
python3 -B scripts/deploy.py verify --release "$DASHBOARD_RELEASE"
python3 -B scripts/deploy.py plan --release "$DASHBOARD_RELEASE"
python3 -B "$DASHBOARD_PATH/tmux/agent-dashboard.py" preflight --socket "$DASHBOARD_SOCKET" --display-only
```

The existing stage tool creates unique timestamp IDs; it does not implement
commit-keyed idempotent reuse or store a Git commit in its receipt. Record the
e38e18d source audit externally, compare every rendered payload/mode with that
commit, and stage once. On retries, verify the recorded release instead of
blindly staging again. Commit-keyed idempotent staging remains a separate repair.

Confirm independent regular payload copies and receipt hashes, 0444 modes,
complete references and no symlinks into Git. Compare all unchanged sources;
rendered release-local includes legitimately use the new absolute path. Ghostty
must be byte/mode identical to its already accepted payload. Pointer changes can
be observed by file watchers even without a manual reload; identical Ghostty
bytes avoid a new key-forwarding transition. No Ghostty migration/reload belongs
to this phase.

Only after that review, under the renewed authorization:

```sh
python3 -B scripts/deploy.py activate --release "$DASHBOARD_RELEASE" --expect-current "$DASHBOARD_OLD_RELEASE" --approve
python3 -B scripts/deploy.py migrate --release "$DASHBOARD_RELEASE" --component cdev --approve
```

Record the **new** cdev backup ID. The tool backs up the original helper contents
and permissions and records the adapter's absence before replacing either path.
Verify both backups, links, resolved bytes, journal completion, all six existing
managed links and protected identities. Activation is an atomic pointer switch;
two helper replacements are not jointly atomic and an interrupted migration
requires the recorded transaction's recovery. Neither command reloads apps.

The earlier cdev backup `20261022T191900.472358Z-230b25df` is already restored;
it is historical evidence, not the new rollout's recovery ID. Existing tmux and
Ghostty backups remain reserved for their independently approved recoveries.

## Mandatory production native review and real-delivery gate

Start only a newly owned ordinary cdev smoke-test project/window. Do not restart
or instrument existing agents retroactively. At native hook review, stop for the
user to open `/hooks` and inspect exactly these eight sessionFlags entries:
SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse, Stop,
Interrupt and SessionEnd. Each must have command type, timeout 2, no matcher or
dynamic identity arguments, and this fixed command:

```text
/usr/bin/python3 -B /Users/czuba/.config/cdev/activity.py event
```

Compare native source keys/hashes with the preview and the approved adapter bytes
with the new release. Preserve all seven existing workmux definitions, trust
records, notification settings and policies. The user trusts only the eight
reviewed entries in the native UI. See the
[official hook review contract](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).
Never copy trust from the private profile, mark hooks managed or bypass review.

Require actual working/stopped events for the intended pane, real approval
evidence when available, unchanged definitions and no repeat review on a second
launch, private runtime ownership and no workmux conflict. Both integrations
must coexist with the global hooks present; the isolated test deliberately did
not execute those global hooks. A missed event or unexpected repeated review
blocks attention activation. No synthetic event substitutes for this gate.
Existing display monitors may show real statuses as soon as trusted new agents
emit events; the compatibility n/c bindings stay unchanged until the reload.

## One controlled reload and acceptance

Only after the previous gate and renewed plugin/hook/process checks:

```sh
python3 -B "$DASHBOARD_PATH/tmux/agent-dashboard.py" preflight --socket "$DASHBOARD_SOCKET"
tmux -N -S "$DASHBOARD_SOCKET" source-file -n /Users/czuba/.tmux.conf
tmux -N -S "$DASHBOARD_SOCKET" source-file /Users/czuba/.tmux.conf
```

The first source-file parses without executing. The second is the one authorized
reload; do not separately call install and then reload. Expected bindings:
Ctrl+F n cycles stopped/waiting agents, c creates a window, Shift+N selects the
next ordinary window, and Cmd+Shift+N still forwards to c. Empty attention queues
preserve focus. Verify loaded definitions, format ownership, monitors, no hook
errors and survival of every recorded session, pane, client and process.
Never reorder/close existing windows as automated test subjects.

Physical acceptance checks the crimson/gunmetal title shimmer near 1 Hz,
legibility, stopped white dot, genuine approval alert, attention cycling/empty
queue, Cmd+Shift+N/P, Cmd+1–9, pane shortcuts and Ctrl+F then Option+H/L.
Generic user questions are not classified as approval/input waiting; stopped
does not imply task success. Persistent Doom, emacsclient and launchd remain
deferred throughout.

## Bounded recovery to authorize with the rollout

Keep Terminal.app and `/bin/zsh -f` available independently of Ghostty/tmux.
If helper adoption or real delivery fails, preserve evidence and restore only
the new verified cdev backup:

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py restore --backup "$DASHBOARD_CDEV_BACKUP" --approve
```

Replace that variable with the actual new backup ID. Because migration occurs
after activation, its recorded original/current pointer is the new release;
helper restoration leaves that pointer and all Ghostty/tmux links intact. Verify
original regular helper content/mode and adapter absence. Never terminate an
agent/editor or clear native user trust as part of restoration.

If attention/reload fails, the bounded recovery is:

```sh
python3 -B "$DASHBOARD_PATH/tmux/agent-dashboard.py" disable --socket "$DASHBOARD_SOCKET"
tmux -N -S "$DASHBOARD_SOCKET" source-file -n /Users/czuba/.tmux.conf
# At most one additional reload, only if included in the renewed approval:
tmux -N -S "$DASHBOARD_SOCKET" source-file /Users/czuba/.tmux.conf
```

Disable restores safe window-creation bindings, clears labels/monitors and sets
the persistent dashboard-off option, so the recovery reload does not reinstall
attention. It refuses conflicting bindings. Verify n/c, theme and protected
identities, then stop. A failed recovery, unexpected drift, shared-pointer
rollback or Ghostty restoration requires separate review; do not improvise a
broader rollback or restart. Preserve incomplete journals for safe retry.
