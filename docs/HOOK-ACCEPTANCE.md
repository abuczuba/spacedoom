# Real Codex hook acceptance — 2026-10-22

**Passed in disposable ordinary cdev sessions.** Implementation remains
`e38e18ddb0ebf3097f22ad95b94835ae97652fd5`; no code repair was needed during
acceptance. Production remains recovered Phase 3B. This result permits proposing
a new rollout, not executing one. See [the remaining Phase 4 plan](DASHBOARD-PHASE4.md).

## Test boundary

The installed Codex CLI 0.163.0 used the normal OpenAI provider in a private,
user-authenticated profile. The user personally reviewed and trusted the eight
inspected sessionFlags definitions. Automation neither wrote trust records nor
sent approval choices. No authentication file was read or copied by the test.

The unchanged standalone Fish cdev function launched independent, read-only
copies of the e38e18d helpers on an empty-config private tmux server. Its left
editor was inert; its right panes ran the real Codex CLI. Neither agent required
a workmux worktree. No synthetic lifecycle events were injected into these
real-event tests. Separate synthetic regressions are identified below.

Eight definitions, their source keys, command, timeout and native currentHash
values matched before review, after the user's review, on the second ordinary
launch, and after testing. All eight remained trusted in that profile. The
second CLI submitted and completed a real turn without another hook review.
The stable command used the private installation path; production has a different
path and requires its own native review.

## Observed delivery

Times below are measured by the test observer from each prompt submission;
they include CLI/model latency and are not hook execution benchmarks.

| Check | Actual evidence |
|---|---|
| Session binding and working | Pane `%2`: native session binding at 0.972s, working sequence 1 at 1.033s; crimson title rendering followed. |
| Stopped turn | The same real turn reached done sequence 2 at 3.831s; the white dot appeared by 4.774s. Done means stopped/review, not guaranteed success. |
| Second ordinary launch | Pane `%4` had a different nonce, native child PID and session ID; all eight hashes/trust entries were unchanged and no repeat review appeared. |
| Concurrent activity | Both panes were working simultaneously; `%2` stopped while `%4` remained working, then `%4` stopped. Each title rendered its own state. |
| Window movement | During those real turns, only the owned test windows were swapped, renumbered and renamed. Pane IDs and process identities stayed fixed; session/turn associations remained correct. |
| Actual approval request | Codex requested one-time approval for `/usr/bin/true` through its normal sandbox mechanism. PermissionRequest reached waiting sequence 6 at 5.211s; native approval UI and the white `!` on blood red were observed by 6.193s. |
| Approval resolution | Later native UI reported that the command was approved and ran. The originating agent settled to done sequence 8 with an empty pending set; the other agent's record was unchanged. Automation sent no approval or cancellation choice. |
| Normal exit | Native `/quit` produced idle/ended at 0.097s, then launcher finalization at 0.385s. The other live agent remained unchanged. |
| Abrupt exit while working | Closing only the owned second agent pane removed its displayed label in 0.468s; its native child exited. The orphaned cache still contained working, but a missing pane made it ineligible for display. |

The native sessions were:

- `%2`: `01a1656a-79c2-79d3-9073-594621a737d3`.
- `%4`: `01a1657d-a5f3-7430-8c46-1d8fd4444f5e`.

These observations demonstrate that actual hook subprocesses inherited usable
runtime context and passed the nonce, private-state, process-ancestry, server
boot and stable-pane checks in this installed ordinary-launch configuration.
Attribution did not depend on window number, title or project directory.

Two collector assumptions were corrected without changing product code: an
initial input attempt occurred while a model picker was open and submitted no
turn; SessionStart binding was lazy until the first submitted prompt. Only
successfully submitted real turns count as delivery evidence. Neither issue
was hidden by synthetic events or changes to Codex policy.

## Non-regression evidence

- **19/19 fresh activity/cdev regressions passed in 20.011s** with
  `python3 -B scripts/test.py --integration --match 'test_activity.*' --match 'test_cdev.*'`.
  These are deterministic fixtures, including synthetic dispatch; they are
  separate from the real delivery above. The prior full **90/90** e38e18d suite
  remains applicable because implementation, validation and tests are unchanged.
- Ordinary cdev retained project-window reuse without duplicate agents, its
  two-pane placement and standalone editor/compiler environment. The editor
  stand-in established invocation behavior; this test did not launch real Doom.
- The installed workmux `register-agent` and working/waiting/done commands all
  succeeded on an owned inert pane. They preserved title-format ownership, n/c
  bindings and both observer records. Those commands used explicit fixture
  metadata; they are compatibility evidence, not native workmux hook delivery.
- All seven existing global workmux definitions and their trust/configuration
  files remained unchanged. Native discovery regressions verify that adding
  the eight sessionFlags definitions retains the seven original source keys
  and hashes. The isolated profile intentionally did not run global hooks;
  combined production delivery remains a rollout smoke-test gate.
- Final production comparison matched the fresh baseline for sessions, windows,
  panes, clients, server identity, loaded hooks/monitors/options/bindings,
  protected process identities, Codex PIDs and bounded live/deployment files.
  Counts remained **1 session, 4 windows, 7 panes, 1 client and 3 Codex CLIs**.
  The pointer remains `releases/20261022T163617.469413Z-497daec6`.
  Both prefix n/c still create windows; attention remains off.
- Only the owned private test session and processes were closed. No production
  reload, deployment, global hook edit, Fish/Doom adoption or service activation
  occurred. Existing concurrent repository documentation edits were preserved.

## Evidence and remaining limits

Owner-only evidence remains under `/private/tmp/df-hook-acceptance-zcc5ujfz`.
The private server is closed; the previous attach instruction is historical.
Key reports are `ACCEPTANCE-RESULT.json`, `native-hooks-before-review.json`,
`native-hooks-after-user-review.json`, `native-hooks-second-launch.json`,
`native-hooks-final.json`, `real-turn-a.json`, `second-launch.json`,
`concurrent-real-turns.json`, `real-approval.json`,
`approval-resolution-observed.json`, `termination-real.json`,
`workmux-compatibility.json`, `production-verification-final.json` and
`cleanup.json`. These reports contain scoped metadata, not authentication files.

`expected-production-definitions.json` records a native read-only metadata
preview for the future production command, with all eight definitions untrusted.
It did not install, trust or execute that command. Recompute/compare at rollout,
particularly if the CLI version changes; native definition hashes do not attest
to the adapter file's bytes.

Waiting is established for real PermissionRequest, not arbitrary questions or
generic user input. Individual PreToolUse/PostToolUse callbacks were not all
sampled separately; Interrupt retains synthetic coverage. Stale/retired identity
rejection has deterministic coverage; the abrupt-exit observation proves display
cleanup, not cache-file garbage collection. A missing pane invalidates retained
records, and the existing lease bounds otherwise stale display evidence.

This test establishes the installed local CLI behavior. Remote/shared-server
topologies and other versions remain unverified and must fail unlabelled when
ancestry/context cannot be established. No forced no-daemon option was used.
Production needs a new immutable release, separate user hook review, combined
workmux/cdev smoke tests and physical dashboard/navigation acceptance under a
renewed consolidated authorization. Persistent Doom remains deferred.
