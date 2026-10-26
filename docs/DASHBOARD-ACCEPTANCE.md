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

# Production dashboard acceptance — 2026-10-22

**Automated production acceptance passed. Physical keyboard/visual acceptance
is pending.** The dashboard is active; persistent Doom remains deferred.
Implementation and validation still match commit
`e38e18ddb0ebf3097f22ad95b94835ae97652fd5`. No new commit was created for rollout.

## Active deployment and backups

`~/.local/share/dotfiles-active/current` points to
`releases/20261022T215047.249499Z-618a6bc8`.
The complete 15-file release consists of independent regular copies, mode 0444,
verified against e38e18d with rendered references, receipt hashes and dependencies.
Existing immutable releases were preserved. Of the payload sources, only the two
cdev helpers differ from the previously active 8dad372 release. All six previously
managed Ghostty/tmux payloads are equivalent after release-path rendering;
Ghostty's contents are byte-identical.

Exactly two new live paths were adopted:

| Live path | Managed symlink target |
|---|---|
| `~/.config/cdev/codex_session.py` | `~/.local/share/dotfiles-active/current/cdev/codex_session.py` |
| `~/.config/cdev/activity.py` | `~/.local/share/dotfiles-active/current/cdev/activity.py` |

Backup **20261022T215153.419622Z-a559508a** is at
`~/.local/share/dotfiles-active/backups/20261022T215153.419622Z-a559508a/`.
It preserves the original regular mode-0644 launcher contents and records the
adapter's prior absence. Both backup and all eight live managed links were
verified. The six earlier mappings remain the five tmux files and Ghostty file
listed in DASHBOARD-PHASE4.md. No Fish, Doom, service or whole-directory migration
occurred. The unchanged live Fish function still launches standalone `emacs -nw`
with its existing compiler environment, layout and project reuse.

Production operations completed under the consolidated authorization
(POSIX sh/Zsh; historical commands, do not repeat):

```sh
python3 -B scripts/deploy.py stage --approve
python3 -B scripts/deploy.py activate --release 20261022T215047.249499Z-618a6bc8 --expect-current 20261022T163617.469413Z-497daec6 --approve
python3 -B scripts/deploy.py migrate --release 20261022T215047.249499Z-618a6bc8 --component cdev --approve
tmux -N -S /private/tmp/tmux-501/default source-file -n /Users/czuba/.tmux.conf
tmux -N -S /private/tmp/tmux-501/default source-file /Users/czuba/.tmux.conf
```

There was **exactly one executing production reload**, after native trust and
real production delivery gates passed. It exited 0 without output/errors.
Post-reload strict preflight and non-executing parsing passed. No recovery or
rollback was executed after success. No Ghostty reload was performed here.

## Native trust and real lifecycle evidence

The user reviewed the invocation-local definitions in the native CLI. An initial
read showed five trusted and three untrusted; both native metadata and the UI
identified the remaining entries. The cause of that partial persistence is not
established and is not attributed to user action. After the user reviewed the
remaining three, all eight stayed trusted through review-CLI exit, fresh ordinary
cdev launch, ordinary project resume, concurrent fresh threads and final checks.
**No identical-definition review prompt recurred.**

All eight source keys, fixed commands and native hashes match
[PRODUCTION-HOOK-REVIEW.md](PRODUCTION-HOOK-REVIEW.md). Automation never wrote
trust records, accepted a native approval, changed managed policy or bypassed
trust. The seven preexisting workmux definitions retained their source file,
hashes, enabled state and effective trust. Global notification/authentication
settings were not edited.

Real OpenAI-backed CLI turns used the production profile and migrated helpers,
in a dedicated owned tmux session with an inert editor. There was no model stub
or synthetic lifecycle injection. The first agent used the actual unchanged
ordinary cdev function. For same-project concurrency, a controlled second fresh
CLI used the same live observer API without resuming the first conversation;
the normal cdev reuse protections were preserved and independently verified.

| Production observation | Evidence |
|---|---|
| Working | Actual UserPromptSubmit/turn evidence reached its registered pane and produced the crimson/gunmetal title shimmer. |
| Stopped | Actual Stop evidence produced a static white dot; real model replies were separately observed. This means stopped/review, not guaranteed success. |
| Approval request | A native one-time request for `/usr/bin/true` produced waiting, native approval UI, white `!` on blood red and workmux waiting. Automation cancelled the owned test turn without approving; the alert cleared and a subsequent real turn completed. |
| Idle | Fresh agents remained unlabelled before activity; ordinary theme fallback stayed active. |
| Concurrent attribution | Two distinct native session IDs and runtime nonces produced independent pane records. Their actual workmux session IDs/pane PIDs matched. |
| Window movement | Only the owned test windows were swapped, renumbered and renamed during actual concurrent turns. Pane/process identities and attribution survived; original project windows were untouched. |
| Normal exit | The owned second CLI retired its record and cleared its title without changing the other agent's record. |
| Abrupt exit | Closing the owned first pane during a real working turn removed its label in **0.359s** and its native child exited. The orphaned working JSON remains ineligible because its pane is absent. |
| Trust reuse/reuse semantics | Fresh and resumed ordinary cdev launches retained all eight trusted hashes. Repeated cdev invocation selected its existing project window without adding agents or panes. |

Actual workmux working, waiting and done cache transitions coexisted with observer
updates, attributed to the same native sessions/pane PIDs. This is actual global
hook delivery, distinct from the earlier isolated manual workmux command tests.
Subagent hooks were preserved but not induced; no delegation was used.

## Active bindings and attention behavior

| Input | Effective behavior |
|---|---|
| `Ctrl+F → n` | Cycle stopped/waiting agents in the current session only |
| `Ctrl+F → c` | Create a window in the current pane directory |
| `Ctrl+F → Shift+N` | Ordinary next-window navigation |
| `Cmd+Shift+N` in Ghostty | Forward `Ctrl+F c`, preserving window creation |
| `Ctrl+F → Option+H/L` | Existing adjacent window reordering/focus preservation |
| `Cmd+1–9`, pane keys, workmux keys, popup | Existing definitions preserved |

Post-reload, four attention invocations cycled exactly `%26 → %27 → %26 → %27
→ %26` in the owned test session. Idle and working-only queues preserved focus;
there is no working/idle fallback. This exercised the deployed attention action;
physical key forwarding remains a user acceptance check.

Every binding other than n was preserved, allowing only the intentional popup
helper repin from the old immutable release to the new one. Themes, title-format
ownership and existing hook/monitor behavior passed comparison. No test created
windows through the live creation bindings. Automated selection/reordering
commands targeted only owned test windows.

## Animation cost and regression scope

Live working samples showed **one unchanged cached format and sequence**, with
four distinct rendered frames per agent. The title uses native tmux clock
expressions at approximately 1 Hz, with no shell expansion/process per animation
tick. Event-driven hook/cache updates remain separate from animation.

A fresh empty private-server benchmark used the deployed renderer, a 24-character
title and three samples of 2,000 expansions:

| Format | Median ms per expansion |
|---|---:|
| Idle | 0.0185 |
| Working | 0.4875 |
| Stopped | 0.0237 |
| Waiting | 0.0240 |
| Monitor across 20 idle windows | 0.2417 |

These are local wall-time bounds including tmux parsing/captured output, not
system-wide CPU or GUI redraw measurements. Benchmark visual fixtures are
synthetic; they are not the lifecycle evidence above. The older checked-in
benchmark's hook-timing section still uses retired nonce/CLI flags and needs a
separate repository-only update; it was not used to measure the repaired hook.

The complete **90-test suite passed in 54.814s** before rollout. After discovering
the recovery documentation error below, the existing isolated disable regression
passed again in **0.399s**. No implementation/tests/validation changed, so the full
suite was not redundantly repeated. Actual production checks additionally cover
fresh/resumed trust, concurrent events, approval cancellation/recovery, workmux,
termination, new renderer loading and attention behavior. Stale/retired-event
rejection and disconnected-client behavior also retain deterministic coverage.
An initialization-order error in the temporary concurrency launcher was corrected
before its Codex child started; it is not counted as successful event coverage.
The later concurrent real turns are separately recorded passing evidence.

## Session protection, retained fixtures and limits

The original **one session, four windows, seven panes, client and three Codex
CLIs** survived with the same identities, numbering and process start times.
All 12 originally protected application processes and every additional
pre-reload test process/client survived the reload. Focus stayed unchanged
through the successful launch/event/reload/attention checks. The earlier
**@10 → @2 change remains unattributed**; it was not reversed or assigned to
the user. Doom files/processes, clipboard bindings/configuration, Fish functions,
Ghostty contents and workmux settings were preserved. Clipboard content was not
read or changed. No persistent Emacs server, emacsclient workflow or LaunchAgent
was activated. No Git commit/push was performed, and concurrent docs were retained.

For physical inspection, the owned session `df-dashboard-review-618a6bc8` remains
open with control window @11, test windows @16/@17 and stopped agents %26/%27.
Its editor is an inert test stand-in. Totals including these fixtures are
2 sessions, 7 windows, 11 panes and 2 attached clients. Do not treat the extra
fixture processes as original project processes or terminate discovered agents
by name. Cleanup remains limited to proven owned resources after inspection.

Native approval requests are observable; arbitrary user questions are not a
separate reliable waiting state. Existing original agents were not restarted or
retroactively instrumented. They retain available workmux evidence; new ordinary
cdev launches receive the observer. Retained orphan caches are rejected, not
garbage-collected. The existing 15-minute evidence lease stays conservative.
Other Codex versions and remote/shared-server topologies remain unverified;
missing identity/context must leave them unlabelled.

Owner-only reports and harnesses are retained under
`/private/tmp/df-dashboard-phase4-ql9uc7fk`, notably FINAL-RESULT.json,
fresh-launch.json, production-real-turn-a.json, production-concurrent.json,
production-approval.json, production-termination.json, reload-transaction.json,
post-reload-acceptance.json, native-final-trust.json and format-benchmark.json.
No private authentication, browser artifacts or conversations were added to Git.

## Recovery references — do not execute after success

For an approved attention/display failure, the existing bounded recovery is
(POSIX sh/Zsh):

```sh
python3 -B /Users/czuba/.local/share/dotfiles-active/releases/20261022T215047.249499Z-618a6bc8/tmux/agent-dashboard.py disable --socket /private/tmp/tmux-501/default
```

Verify n/c creation, removed monitors/labels and original process identities,
then stop. **Do not reload the full tmux.conf after disabling:** it explicitly
sets the feature on again. The older claim that the off flag survives that reload
was corrected in DASHBOARD-PHASE4.md. Disable alone restores safe runtime bindings;
no additional reload was required or performed.

For the separately defined helper-adoption/delivery failure, the exact backup
restoration command is:

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py restore --backup 20261022T215153.419622Z-a559508a --approve
```

This restores the original regular launcher and adapter absence, while leaving
the current pointer on the new release. Running instrumented clients retain the
fixed adapter path; inspect those dependencies before removing it. Retire only
owned test clients for that recovery. If a user-owned instrumented client depends
on it, stop for a reviewed recovery plan; do not terminate it or remove its hook
target silently. Visual rollback uses disable and keeps the adapter available.
Do not restore Ghostty, use an old restored backup or roll back the shared pointer
as an automatic response. A broader rollback requires separate review.

## Next action: physical acceptance

In Ghostty, `Ctrl+F → )` is the preserved next-session binding. With the current
two sessions, it lets the user enter the disposable review session without
restarting applications. Pressing it again returns to the other session.

1. Check `Ctrl+F → n` cycles the two stopped test agents, with clear white dots.
2. During a harmless real test turn, inspect the cohesive crimson/gunmetal
   title shimmer, approximately 1 Hz, and stopped-dot legibility. Actual red-alert
   delivery was verified automatically; inspect its appearance on a genuine
   permission request if desired. Generic questions should not show that alert.
3. Confirm Cmd+Shift+N/P, available Cmd+1–9 selections, pane navigation,
   Ctrl+F → c/Shift+N and Ctrl+F → Option+H/L still feel correct in Ghostty.

Evidence expires conservatively; if inspecting much later, a fresh harmless
test turn renews a stopped indicator. No further reload/deployment is needed for
these checks. Report acceptance before moving to the persistent-Doom milestone.
