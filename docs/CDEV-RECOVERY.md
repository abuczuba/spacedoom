# Exact cdev conversation recovery

`cdev PROJECT` still reuses its existing project window before starting anything.
The live Fish function, Doom-left/Codex-right layout and standalone `emacs -nw`
launcher are unchanged. Only the installed Python session helper needs deployment;
do not migrate the deferred Fish/Emacs client candidates.

The helper no longer delegates selection to `resume --last`. Private
`~/.local/state/cdev/pins.json` stores a verified UUID per canonical Git root
(or `$XDG_STATE_HOME/cdev/pins.json`). A single saved interactive project
conversation can bootstrap a pin; multiple candidates require `cdev-pin UUID PROJECT`.
Nested project directories resolve to their Git root. Missing pins, inconsistent
metadata, duplicate saved copies and wrong-project UUIDs fail without a fallback.
Only the first `session_meta` line is read; transcripts and credentials are not.
The three operator-supplied recovery mappings belong in private state, never Git.

For a verified local shared server, resume uses `--remote unix://SOCKET` with the
exact UUID. The helper checks socket ownership/permissions and reads only
`thread/loaded/list` over its local WebSocket. A busy writer must be loaded in that
server; an unexpected owner, stale socket or unavailable control API fails clearly.
With no endpoint and no busy writer, explicit local UUID resume remains available.
There is no server restart, lock stealing, alternate conversation or fresh retry.
The ownership check is a snapshot; Codex remains responsible for the final writer
lock. A race becomes a visible launch failure, never a different conversation.

Dashboard hook arguments and stable adapter paths remain unchanged. Remote hook
delivery still depends on Codex forwarding invocation context: existing ancestry
validation fails safely unlabelled rather than accepting another pane's events.
This repair does not weaken it or restart existing agents to test delivery.

Routine checks (POSIX sh/Zsh):

```sh
python3 -B scripts/test.py --integration --match '*Cdev*'
python3 -B scripts/test.py --match '*ActivityTests*'
```

Tests use private metadata, inert agents, private tmux sockets and a fake local
WebSocket; they never resume the protected live UUIDs. A read-only production
query can establish that each approved UUID is loaded with its writer lock busy.

Deploy a committed, verified release with the existing stage/activate tooling.
Compare every already-managed payload; only `cdev/codex_session.py` should change.
Back up private pins before updating them and preserve all other mappings. The
previous immutable release is the code rollback; the private pin copy is the
separate metadata rollback. Neither operation reloads tmux or replaces a process.
See STATUS.md for the actual release and recovery reference.

Protocol reference: [official CLI reference](https://learn.chatgpt.com/docs/cli/reference)
and [app-server protocol](https://learn.chatgpt.com/docs/app-server).
