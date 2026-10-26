# Codex activity in tmux

The existing window list is the dashboard; idle windows retain the normal theme.
The source is `configs/cdev/activity.py`, the retained shared-server connection in
`codex_session.py`, and `configs/tmux/agent-dashboard.py`. There is no notification
transport or independent background polling service in this repository.

| Evidence | Display | Attention queue |
|---|---|---|
| Known live turn working | Crimson/gunmetal wave through the actual title | No |
| Stopped turn | Static white `●`, possible review; not proof of success | Yes |
| Native pending human request | White `!` on blood red | Yes |
| Unknown, idle, untrusted or exited | Original theme | No |

The selected working title keeps its original shimmer and gains an amber
`#f6c177` underline, confined to visible title cells. Native focus evaluation
moves it with selection without waiting for an event. Animation advances at
approximately 1 Hz through tmux format arithmetic; no per-frame shell/Python
process, marquee or extra status row is introduced. The cache refresh is triggered
by changed evidence/window metadata through the existing tmux format mechanism.
Normal windows do not launch individual observers.

## Lifecycle identity

Eight deterministic invocation-local hook definitions call the stable live
adapter path. The user must trust them through native Codex review; launch
identity is runtime data, never interpolated into trusted commands. Registrations
bind socket/server boot, pane/root PID, launch token, process births and session.
Window renumbering/title changes do not change pane identity. Unknown or conflicting
identity fails closed. Seven global workmux definitions remain separate and
unchanged; their compatible cache is read when cdev does not own the pane.

Remote UUID resume retains its native hook-setup connection until the owned TUI
exits. That existing reader also consumes exact native approval and resolution
IDs. `PermissionRequest` alone runs before review and cannot establish that a
human is needed; automatic review can resolve it without a prompt. See
[approval state](APPROVAL-STATE.md) and [remote resume](REMOTE-RESUME-REPAIR.md).
Local launches without the retained stream retain hook-only compatibility;
precise resolution is not asserted for those sessions. Existing readers are
never injected/restarted by deployment; they adopt updates on natural reopening.

The private cache stores lifecycle IDs/status, not prompts, responses or tool
arguments. Stopped attention persists while launch identity is valid. A verified
exit/new meaningful lifecycle event retires old evidence; a stale event cannot
retire or overwrite a newer launch. Physical display and keyboard acceptance is
separate from mock/cache-format tests.

## Keys and safe startup

- `Ctrl+F n`: next actionable agent in the current session; empty queue keeps focus.
- `Ctrl+F a`: acknowledge the selected stopped pane/turn, retaining its process/state.
- `Ctrl+F c`: new window. Ghostty's `Cmd+Shift+N` explicitly forwards this route.
- `Ctrl+F Shift+N`: ordinary next window. Existing pane/number/reordering keys remain.

Tmux bootstrap registers its existing native cache callbacks after theme and
navigation. Strict preflight refuses mismatched Ghostty forwarding or bindings.
The historical display-only n/c bridge is for coordinated first migration, not
the accepted current state. `disable` restores safe creation bindings without
restarting processes; a full config reload turns the feature on again.

Run `scripts/benchmark_dashboard.py` for a bounded native-format
benchmark. It is not evidence of Codex hook delivery. Tests own private sockets;
the native 0.164.0 remote-resume/approval acceptance is recorded in the historical
log and current STATUS. Collie may independently consume its opted-in handoff;
its application/service/pairing configuration is outside this repository.
