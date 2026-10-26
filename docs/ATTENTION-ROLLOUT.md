# Final acceptance and cleanup complete — 2026-10-22

The user reported physical PASS: Ctrl+F n alternates between both stopped agents,
and both dots persist. The dashboard milestone is now accepted and closed.
Release **20261023T002013.807639Z-023596db** (9a861dc) remains active.

Cleanup revalidated server 72611 / boot 1792558526, exact session $1 / creation
1792706023, pane identities, process starts, ancestry and descendants. The two
accidental split panes %29/%30 and their old shell processes were already absent.
The known remaining review resources and all protected production identities
were accounted for before action. No missing-resource event is attributed.

Only client 12520 (/dev/ttys014) needed redirection to main. Its identity was
checked immediately; both clients survived and the other client's main selection
was preserved by the operation. Both owned test CLIs in %26/%27 then exited using
native /quit. Their launchers and the owned helper PID 22404 exited; records are
ended/idle. Dead agent panes had exit status 0 and remain-on-exit on, preserving
existing cdev policy. The exact review session and its three inert/idle processes
were then removed, with no clients attached and no window linked to main.

Final state: only main, four original windows, seven original panes, two clients,
12 original core identities preserved; 17 distinct checked application/client/process
identities preserved, including Ghostty and production Codex/Doom processes.
No owned test process or stale review attention remains. Active pointer, eight
managed links, configuration bytes, bindings, native trust and workmux remain
unchanged. No cleanup reload, rollback, migration, commit or push occurred.

During preparation, a separate main selection change @5 -> @10 was observed
between phases, after client redirection had passed its own focus check and
before any native exit input. Its cause remains unestablished. No main selection
command was issued, and focus was not reversed. Main selection was stable across
the actual exits and exact-session removal.

Evidence is retained in `/private/tmp/df-attention-rollout-a506fio9/CLOSEOUT.json`
and `/private/tmp/df-attention-rollout-a506fio9/cleanup-dyryohik/`.
The earlier two diagnostic roots and trusted hook definitions are preserved;
ended cache records remain private evidence, safely ignored for absent panes.
Cleanup was limited to running disposable resources; it did not delete audit
files or alter global trust. No further dashboard acceptance/cleanup is pending.
Persistent Doom and other work await a separate task/approval.

Earlier rollout entries below are historical evidence retained verbatim.

---

# Attention-persistence rollout — physical acceptance pending

Repair source: **9a861dc8501b4e05f6ca1aeebbb5687aa1cdc3e9**.
Active release: **20261023T002013.807639Z-023596db**.
Release path:
`/Users/czuba/.local/share/dotfiles-active/releases/20261023T002013.807639Z-023596db`.
Previous release: `20261022T215047.249499Z-618a6bc8`, preserved unchanged.

## Scope and preflight

This is the bounded stopped-attention correction, not a dashboard redesign.
Only `tmux/agent-dashboard.py` and `tmux/agent-dashboard.conf` change behavior.
All 15 payloads match commit 9a861dc after declared release-path rendering, use
independent regular inodes, nlink 1 and mode 0444. Complete receipts, referenced
files, dependencies, privacy checks and configuration parsers passed. The
manifest and all hook/launcher/editor/theme code are unchanged.

Initial preflight stopped on a changed live Fish startup hash. The user confirmed
manually adding a function. Removing only the `passme` addition in memory
reconstructed the previous SHA-256 exactly. Non-executing Fish syntax passed;
the addition has no startup-event registration. The file was not changed by the
agent. Its accepted SHA-256 remains
`e09f7e85b4683a41ce2a7add4f58722626b6dde7c60081cc8b9faebc6a80c7d5`.
No other live configuration drift was found. This exception is explicitly
attributed to the user's confirmation, not silently accepted.

Fresh native hooks/list queries before and after deployment show the same eight
dashboard sessionFlags definitions and seven user workmux definitions, all
trusted/enabled with unchanged commands, source paths and native hashes. No trust
writes, global hook edits or authentication operations were performed.

All eight already-managed live paths continue through current: five tmux files,
Ghostty configuration and the two cdev helper files. No live directory or new
configuration path was adopted. Ghostty/cdev payload bytes are unchanged; Fish,
Doom, clipboard settings and services were not migrated or reloaded. Existing
standalone `emacs -nw` remains the production launcher. Persistent Doom and
LaunchAgents remain deferred. Ghostty may observe the pointer change through its
watcher, but its payload is identical; no manual Ghostty reload was performed.

## Executed operations

The established deployment tool staged exactly one new release, verified it
repeatedly without restaging, then atomically switched current:

```sh
python3 -B scripts/deploy.py stage --approve
python3 -B scripts/deploy.py activate --release 20261023T002013.807639Z-023596db --expect-current 20261022T215047.249499Z-618a6bc8 --approve
```

Activation history: `/Users/czuba/.local/share/dotfiles-active/history/20261023T002116.367790Z-26a1812e.json`.
The event is applied, references the exact previous release and lists all eight
managed targets. No new initial-migration backup was needed: existing regular-file
backups and all earlier immutable releases were verified and preserved.

Existing backup IDs:

- Tmux: `20261022T040111.754783Z-a455ecd7`.
- Ghostty: `20261022T183526.100129Z-0188b037`.
- Current cdev adoption: `20261022T215153.419622Z-a559508a`.
- The older failed cdev backup remains recorded as restored; it was not reused.

After renewed plugin/hash/hook/process checks, strict dashboard preflight and
`tmux source-file -n` passed on the exact production socket. Exactly **one**
executing reload occurred during this repair rollout:

```sh
tmux -N -S /private/tmp/tmux-501/default source-file /Users/czuba/.tmux.conf
```

No load errors/warnings or recovery operations occurred. Loaded formats changed
only to the expected expiry/state policy; all binding commands were preserved
apart from immutable release-path repinning. Native monitors use the new policy;
existing theme/plugin initialization and unrelated hooks remain unchanged.
The reload preserved sessions, windows, panes, clients, protected processes and
focus. No main window/pane was used as a test subject.

## Actual acceptance evidence

The original two real Stop records were **6,680 seconds old** when tested after
the repair (over 111 minutes). Their JSON bytes, timestamps, session/turn identities
and live launcher/Codex process identities remained unchanged. Both were visible
as white dots and eligible for attention. This demonstrates real aged-event
persistence without injecting events, editing cache timestamps or waiting on a
synthetic clock.

Nine calls through the actual installed n callback cycled the correct stable
panes in session $1. Tests included the two existing shell splits, a temporary
owned-window swap/renumber and a temporary title change. Order/title were restored;
all real records remained byte-identical after visits. Main focus, window/pane
identities and protected processes remained intact. No main window was reordered.

Fresh actual CLI turns then verified both agents working concurrently with
independent session/pane attribution. Each produced three distinct rendered
shimmer frames from one unchanged cached format, followed by a real stopped
white dot. A new turn replaced the old stopped attention. Existing workmux cache
states/pane PIDs/session IDs matched each agent.

A real PermissionRequest for `/usr/bin/true` produced both the native approval UI
and the white-on-blood-red alert, with matching workmux waiting state. No approval
choice was sent. A single Ctrl+C cancelled that owned request; actual interrupt
cleared the alert. A new harmless turn completed normally, leaving both agents
stopped and alive for the physical check. The other agent's record was unchanged
during the approval test. No synthetic lifecycle event substitutes for these
observations. Generic final-answer questions still do not imply approval waiting.

All original four main windows, seven panes, original client, three production
Codex CLIs and 12 protected process identities survived. Both clients and all
seven review panes survived. Main focus was unchanged throughout this rollout's
reload and automated acceptance. Historical unexplained selection changes remain
unattributed; this result does not establish their cause.

The accepted complete regression suite for this unchanged commit is **95 passed
in 54.409s**, including the five new persistence regressions. It was not needlessly
repeated during deployment. Candidate/staged/active syntax, integrity, dependency,
privacy and live-state checks were rerun. Native animation adds no per-frame #()
process or polling daemon; monitor refreshes occur on evidence/identity changes.

## Current keys and semantics

- Ctrl+F, release, n: session-local stopped/waiting attention. Empty queue keeps focus.
- Ctrl+F, release, c: new window in the pane directory.
- Ctrl+F, release, Shift+N: ordinary next-window.
- Ghostty Cmd+Shift+N: still forwards Ctrl+F c.
- Existing Command window/pane/popup shortcuts, Option H/L reordering and workmux keys remain intact.
- Visiting an agent does not acknowledge review. Stopped attention persists until
  another lifecycle event or invalidated launch identity clears it. Working and
  waiting retain the conservative 15-minute silence timeout.
- Ctrl+F s splits vertically. Session selection can use Ctrl+F : and switch-client.

## Required human check; cleanup is still gated

No additional reload or 15-minute wait is required. In the Ghostty client used for
testing, enter the tmux command prompt with Ctrl+F then `:` and run:

```text
switch-client -t df-dashboard-review-618a6bc8
```

The two agent windows are `blood-stone-a` / `blood-stone-b`, indices 2/3, panes
%26/%27. Press Ctrl+F, release, n repeatedly (with a new prefix each time). Confirm
it alternates between them and that both white dots remain after visiting. The
other shortcut/visual physical checks already passed; they need not be repeated
unless the user notices a regression. Return with the tmux command prompt:

```text
switch-client -t main
```

The milestone is not declared fully accepted or cleaned up until the user reports
this keyboard check. Cleanup authorization is already granted **after successful
acceptance**; do not request it again for the same verified resources.

Retained session $1 is `df-dashboard-review-618a6bc8` on server PID 72611 at
`/private/tmp/tmux-501/default`. Its exact inventory is in ATTENTION-DIAGNOSIS.md:
agent panes %26/%27, inert panes %18/%25 and idle shell panes %28/%29/%30.
Before cleanup, revalidate session creation identity, current PIDs/start identities,
ancestry and descendant jobs against preserved evidence. Safely redirect only
clients actually attached to $1, using exact client identities and preserving the
other client's main selection. Normally exit the two owned CLIs; verify launcher
exit/state retirement. Only then remove the isolated test session/inert panes and
verify main's protected resources. Stale PID numbers alone confer no authority.

**No cleanup has occurred.** Preserve both earlier diagnostic roots and this
rollout evidence root `/private/tmp/df-attention-rollout-a506fio9/` (0700; JSON 0600).
Key files: preflight.json, accepted-manual-fish-change.json, staged-release.json,
activation.json, reload-transaction.json, aged-real-attention.json,
real-state-acceptance.json and trusted-before/after.json. They contain scoped
metadata and owned-test evidence, not authentication data or captured environments.
No production config is linked into the development checkout.

## Bounded recovery references — not executed after success

For an approved runtime dashboard failure, disable using the active release,
verify n/c creation, removed labels/monitors and protected identities, then stop:

```sh
python3 -B /Users/czuba/.local/share/dotfiles-active/releases/20261023T002013.807639Z-023596db/tmux/agent-dashboard.py disable --socket /private/tmp/tmux-501/default
```

Do **not** follow disable with a full tmux reload; the full config turns it on.
If pointer rollback is necessary within the approved recovery scope, the exact
history-backed command returns to the preserved prior release:

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py rollback --expect-current 20261023T002013.807639Z-023596db --approve
```

Rollback changes current only; it does not replace already loaded formats or
reload anything. Reassess loaded state and validate before any necessary approved
reload. Initial tmux/Ghostty/cdev restoration is a different operation and is not
needed for this display-only repair. Do not remove an adapter that a live
instrumented client needs or restore unrelated components as a shortcut.
