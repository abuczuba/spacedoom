# Stopped-agent attention expiry diagnosis — 2026-10-22

Production was inspected read-only. No production selection, key injection,
reload, configuration change, process termination or fixture cleanup was issued.
All changes described as the repair below are repository candidates, not deployed.

## Observed cause

At 23:09:44 UTC (19:09:44 EDT), both retained test agents had intact private
records in state `done`, `ended=false`, sequence 2. Their last actual Stop was
22:32:31 UTC; both records were 2,233 seconds old. They still matched the server
boot, stable pane ID, pane root PID and launch marker. Each native Codex child's
PID, parent and process start time also matched the recorded launch.

The deployed e38e18d reader applies a 900-second lease to every lifecycle state.
Both stopped records expired at **22:47:31 UTC (18:47:31 EDT)**. The native title
slot applies that same limit, and the monitor had cleared both cached titles.
Neither JSON record was deleted or ended. This is expiration of otherwise valid
attention, not agent termination or cleanup.

The loaded prefix is `C-f`. Its `n` binding correctly invokes the immutable
release's `agent-dashboard.py attention` with the explicit production socket,
state directory and originating session ID. Attention is enabled. A read-only
snapshot using that exact deployed reader returns an **empty queue**; by design,
empty attention does not change focus. This explains a current no-op without a
broken binding. There is no key-delivery log establishing the exact timing of
the user's attempted keystrokes; their actual keyboard delivery is not claimed
as proven by this inspection. Earlier owned attention cycles had passed before
the records aged out.

Attention is **session-local**. Invoking it in `main` does not visit test agents
in the review session, even if their records are fresh. The accidental splits
also do not invalidate another pane's stable identity. Loaded `s` is vertical
split; session cycling uses `)` rather than `s` in this configuration.

## Repository correction and semantics

The repair distinguishes stopped attention from an activity heartbeat:

- A valid `done` record, from cdev or the existing workmux fallback, survives
  elapsed time. It remains pending until a subsequent lifecycle event changes
  it or its launch/pane/server identity becomes invalid.
- Visiting or cycling to a pane is not an acknowledgement. There is no native
  reviewed event or new acknowledgement binding. A new turn, Interrupt,
  SessionEnd, process departure or invalid identity clears/replaces attention.
- Working and waiting retain their conservative 900-second silence timeout.
  Future timestamps and all existing identity, termination and trust checks
  continue to fail closed. Silence never creates a completed state.
- The reader, native title slot and native monitor use the same policy. A cached
  window-state option distinguishes stopped titles from expiring activity and
  is cleared with the display cache. No renderer, palette, hook definition,
  launcher, keybinding or navigation algorithm is replaced.
- Animation still uses native tmux formats, with no per-frame processes or new
  polling daemon. Untracked windows still contribute an empty monitor branch.

A read-only evaluation of the unchanged production records returns no agents
with the deployed code and the correct `%26`/`%27` pair with the candidate code.
This is validation evidence, not activation or a new real Codex lifecycle test.

## Verification

Five new regressions cover old stopped cdev/workmux records, invalid identities,
future timestamps, finite active-state timeouts, matching configuration/renderer
formats, native monitor/title expiry, delayed attention cycling with two extra
splits, stable IDs through movement/renumbering, title changes, repeated visits,
new turns, terminal events, empty queues and process exit with surviving splits.
Private callbacks execute the actual installed `n` command. The existing PTY
regression separately verifies Ctrl+F n bytes through a real private tmux client.
Fixtures use synthetic lifecycle records and inert processes; no live agent is
used as a disposable test subject.

Focused tests: **5 passed**. Complete suite:
`python3 -B scripts/test.py --integration` — **95 passed in 54.409s**.
This includes cdev reuse/layout/duplicate protection, native hook-definition hash
stability, installed workmux coexistence, Ghostty key forwarding, tmux movement,
popup, deployment/restore and isolated Doom integration. Doom production was not
modified or activated. Initial new-test assertion errors (unstripped tmux styles
and swap-window focus assumptions) were corrected before the successful run.

Production remains on `releases/20261022T215047.249499Z-618a6bc8`.
All eight managed symlinks retain their prior inode and target and resolve to
0444 files in that release. Global hook bytes and all 12 original protected
process identities are unchanged. The first read-only inspection preserved
main's focus within the sample. A later read-only sample observed main selected
`@5` instead of the earlier `@10`; no production focus command was executed.
The source of that intervening selection change is **unestablished**, not
attributed to the user or represented as proven external activity.

Private evidence is retained outside the cleanup candidate:
`/private/tmp/df-attention-diagnostic-g152po44/` (directory 0700; JSON 0600).
It contains `read-only-diagnostic.json`, `candidate-comparison.json`, the deployed
reader copy, and copies/hashes of preexisting documentation. The prior real-event
acceptance evidence remains under `/private/tmp/df-dashboard-phase4-ql9uc7fk/`.
Neither directory is tracked. Existing concurrent documentation bodies are
preserved, with status additions only.

## Cleanup inventory — proposed, not executed

Exact server: `/private/tmp/tmux-501/default`, PID 72611.
Exact disposable session: **`$1`, `df-dashboard-review-618a6bc8`**.
Its four windows are separate from main's four windows. As inspected:

| Window | Pane | Root / child PID | Role |
|---|---|---|---|
| @11 | %18 | 2958 | Owned control sleep |
| @16 | %25 | 33561 | Owned inert editor stub; sleep, not Doom |
| @16 | %26 | 33565 / 33577 | Owned cdev launcher / stopped Codex test agent A |
| @16 | %29 | 53667 | Idle shell split, no child process |
| @16 | %30 | 53734 | Idle shell split, no child process |
| @17 | %27 | 33592 / 33607 | Owned launcher / stopped Codex test agent B |
| @18 | %28 | 53215 | Additional idle shell window, no child process |

The two accidental splits are accounted for; there is also the third idle shell
in @18. Its precise creation action is not inferred. All three shell panes are
in the fixture directory and had no descendants at inspection. Eligibility must
be rechecked immediately before an approved cleanup, since a user can start work
in them later.

Client PID 12520, tty `/dev/ttys014`, is still attached to the review session.
The original main client is PID 72609, tty `/dev/ttys001`. Cleanup must not
terminate either client or redirect main. Before any session removal, the user
should leave/detach the disposable review client, or separately approve moving
that exact client; never infer this from the other client already showing main.

After separate cleanup authorization:

1. Recheck exact server/session IDs, four window IDs, seven pane IDs, process
   starts/ancestry, empty shell jobs, and absence of links to main. Preserve this
   evidence and the prior acceptance record.
2. Normally exit only the owned test Codex CLIs in `%26`/`%27` via `/quit` from
   their confirmed idle prompts. Verify their child/wrapper exits and invalidated
   status. Do not use a process-name kill or terminate production agents.
3. Once no client is attached and only the listed inert/idle fixtures remain,
   remove the exact session. Proposed Zsh/POSIX command (not run):

   ```sh
   tmux -N -S /private/tmp/tmux-501/default kill-session -t '$1'
   ```

4. Verify `$0` main's original windows/panes/processes remain, and retain both
   evidence directories. No server kill, broad cache deletion, global trust
   edit, hook removal, release rollback or configuration restoration is needed.

Cleanup is not approved by this diagnostic task and has not occurred. Deploying
this fix would require a newly approved immutable release, activation and a
controlled reload; no production operation is implied by a local repair commit.
