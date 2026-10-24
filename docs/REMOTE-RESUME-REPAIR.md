# Codex 0.164.0 remote resume — connection-only repair

The setup-connection lifetime caused the missing events. The launcher primed the
shared server with its eight trusted invocation-local hooks, then disconnected
before starting the remote TUI. In the reproduced failure the turn completed,
but no turn hooks reached the valid registration. Holding that subscription
before TUI startup restored genuine delivery.

Remote hooks inherited an earlier pane marker. Existing UUID routing selected
the correct current pane; kernel/backend, launcher/child birth, socket and pane
validation passed. No attribution guard or hook definition needs changing.

## SessionEnd necessity comparison — 2026-10-24

Both variants used the same retained-connection launcher, reviewed hook commands,
Codex 0.164.0, disposable authenticated profile and approved test Git root. Fresh
launches used ordinary cdev fresh mode; both resumptions used the shared Unix
app-server and the exact UUID created by that fresh launch. Only the disposable
adapter copy changed. Private history was moved aside without reading/copying
its contents, then restored; production history and pins were never touched.

| Actual sequence | Production activity.py | SessionEnd no-op candidate |
| --- | --- | --- |
| Fresh working → stopped | PASS | PASS |
| Fresh genuine permission request, canceled | PASS | PASS |
| Normal exit → exact UUID resume → working/stopped | PASS | PASS |
| Second exit/resume → working/stopped/permission | PASS | PASS |
| Correct pane/process identity, eight unchanged trusted definitions | PASS | PASS |
| Owned CLI/backend exit and private server cleanup | PASS | PASS |

The connection-only variant needed no SessionEnd change. Its three launches
reused UUID `01a1704e-8d94-7f90-9b92-ecf41893a4bb`; the both-fix control reused
`01a1704f-ed23-70e2-b7aa-27aa7f0d8f50`. Metadata-only results are retained under
`/private/tmp/df-remote-release-hp41x7a8/{production,sessionend}/result.json`.
No screen, prompt, response or transcript captures were made. Native permission
requests were canceled, never approved automatically.

The smallest release therefore keeps **activity.py byte-identical to production**.
This commit restores its production behavior and corresponding tests from
76b683d, superseding the unactivated SessionEnd candidate a13eae3 without rewriting
history. Existing process/session/retired-turn guards remain unchanged. This
comparison establishes sufficiency for the reproduced sequence, not a general
claim about every possible future SessionEnd use case.

## Implementation and regression evidence

Only production payload `cdev/codex_session.py` changes. An ExitStack retains
setup until the owned client has finalized. One blocking I/O thread per resumed
launcher discards unused WebSocket data in chunks of at most 64 KiB and answers
pings. It neither decodes message content nor produces lifecycle evidence.
Setup errors remain advisory, and fresh arguments/UUID selection are unchanged.
There is no new daemon, dependency, hook/trust definition or status detector.

`tests/test_remote_subscription.py` covers setup/spawn errors, interruption,
backend EOF, large/fragmented data, ping/pong, socket-FD equality and shutdown
while a reader is blocked on an incomplete frame. Reader thread counts return
to baseline. The lifetime regression fails against the old launcher. The
existing remote API contract test now enters the retained context explicitly.

**42 focused tests pass**, including five private-tmux integrations: activity,
remote identity, subscription cleanup, project UUID recovery, workmux definition
coexistence and pager deduplication. Earlier genuine concurrent-client/window
movement and no-network pager-ledger checks are retained in the prior disposable
trace directory; the A/B comparison above is the release-selection evidence.
No external ntfy delivery was attempted during this preparation.

## Release and acceptance boundary

The committed 17-file production manifest and all 14 managed mappings are kept.
Export the signed repair commit, verify every file against Git, then stage from
that clean export. Exclude pending cnew/global AGENTS/Fish name-resolution and
inherited edits. STATUS records the exact commit, staged release, expected
current and rollback command; the old immutable candidates remain intact.

Production remains `20261023T164459.630188Z-30124092`. Staging does not activate,
reload, migrate, change pins or restart existing agents. After separate final
approval, activation is one atomic pointer switch. Existing launcher processes
keep their loaded code; future ordinary cdev launches use the repair. No tmux,
Fish, Doom or monitor reload is needed. Rollback atomically restores the previous
release without restarting applications or rewriting runtime state.

Live acceptance: use an approved disposable ordinary cdev project under the
production profile; verify working shimmer, stopped dot/one push and a genuine
approval alert; exit normally and reopen the exact UUID twice, checking repeated
turns and attention navigation. Stop on unexpected native hook review. Confirm
physical visuals and iPhone delivery. Keep all existing agents and session 2.
