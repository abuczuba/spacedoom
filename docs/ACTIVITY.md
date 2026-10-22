# Codex activity dashboard — repository candidate

Production remains the physically accepted ec518f0 tmux deployment. This
candidate has not been staged, activated or reloaded. The offline
[four-state preview](previews/dashboard.html) uses synthetic evidence.

## Discovery and the evidence boundary

Inspected on 2026-10-22: Codex CLI 0.163.0, workmux 0.1.276, tmux 3.8,
the live cdev/codex-session helper, existing global hooks, Dotbar's source and
the current server's narrow pane/status metadata. No credentials or conversation
contents were read. Global hooks and workmux settings remain unchanged.

The installed workmux commands register and update ordinary tmux panes without
a worktree. An isolated test verifies working/waiting/done caches and stable
socket/pane/PID/server identity. Its default format installer backs off if both
title formats already contain `@workmux_status`. Dotbar's title slot deliberately
contains that reference; Dotbar remains the sole owner of status formats, theme,
SSH labels, zoom marks and status positioning. No current window has a local
title-format override. The installer refuses such overrides and an occupied
session-created hook slot 882, rather than replacing unrelated customization.
Dotbar's existing SSH-host branch retains precedence when the active pane is
SSH; the cached activity title returns when its ordinary title branch is used.

However, **none of the three live cdev agent panes had workmux status**. The
single cached workmux record belonged to an older server/pane. The invoking
agent also has stale inherited pane context. Shared-server terminal environment
routing is a plausible cause, not a proven root-cause diagnosis. Presence of
global hooks does not establish working per-pane tracking in these sessions.

The safe adapter is an **invocation-local, advisory hook bridge** for future
cdev launches. Commands pin the actual socket, pane and random launch nonce;
they do not depend on the app-server's inherited TMUX variables. No policy,
sandbox, notification, global hooks file, authentication or workmux configuration
is replaced. Codex merges hook sources from different layers; hook trust still
applies. The installed CLI accepts the generated inline configuration in an
isolated config-reading test. Real CLI hook trust and delivery remain an explicit
live acceptance gate (including whether per-launch definitions require repeated
review); the tests simulate documented hook payloads and execute
the actual handlers. There is no trust-bypass flag or automatic trust editing.
See [OpenAI's hook contract](https://learn.chatgpt.com/docs/hooks) and
[workmux status tracking](https://workmux.raine.dev/guide/status-tracking/).

## What can be displayed

| Evidence | Display | Limits |
|---|---|---|
| UserPromptSubmit / PreToolUse / PostToolUse for a known live turn | Gunmetal title with a connected crimson/blood-red vein | Evidence of activity, not a progress percentage |
| PermissionRequest | White `!` on blood red | Approval requests; not every kind of user question |
| Stop | Static white `●` beside title | Turn stopped / review or reply; not proof of successful completion |
| SessionStart alone, Interrupt, SessionEnd, process exit, missing/expired/untrusted data | Original idle title | Unknown is deliberately unlabelled |

General questions in a final reply and a completed task both produce Stop;
there is no invented distinction. Permission requests are retained while other
tools run. PostToolUse clears matching tool-name requests. Hooks lack a fully
ordered approval-resolution stream: concurrent requests with the same tool name,
denials without a subsequent tool result, and another Stop hook continuing a
turn remain limitations. A new turn or terminal event resets pending evidence;
15-minute expiry removes abandoned signals. Never infer completion from silence.

Per-launch records are private JSON under
`$XDG_STATE_HOME/dotfiles-dashboard` (default `~/.local/state`). They contain
identity, lifecycle state, bounded retired turn IDs and timestamps; never prompts,
tool input/output, transcript paths or conversations. Files use mode 600, directory
700, advisory locking and atomic rename. Caches are ephemeral, not deployment
state and not resurrected into another tmux server.

The reader checks server boot identity, stable pane ID, pane root PID, live process
kind, launch nonce, known session/turn, age and termination. A late previous-launch
event cannot clobber a new marker. Previous-turn and post-terminal events are
rejected. Valid workmux records remain a fallback for direct foreground Codex
panes; ambiguous Python wrappers require the explicit cdev bridge. Existing
conversations, direct bare launches with unreliable hooks and restored sessions
without fresh evidence stay unlabelled. No automatic conversation reattachment
or agent restart is attempted.

## Rendering, navigation and cost

Tmux session-scoped native format monitors compare a compact agent signature
once per second, including identity, lifecycle marker, title and expiry. No
external process is launched for an unchanged signature. Normal windows contribute
an empty branch. Changed evidence invokes one bounded renderer; cache writes are
batched and serialized. A delayed initial refresh covers the monitor's first
comparison tick. Monitors continue with no attached client (tested).

The cached format colors the actual title. Integer arithmetic on tmux server age
moves one connected band right by one character per second. The red-lit leading
edge is followed by a blood-red reflection and a dark-crimson wake: at most three
adjacent characters, with the rest in weathered steel. The wake exits the right
edge before the next pass starts at the left; there are never two disconnected
highlights at opposite ends. No per-letter random phases, flashing or hue cycling.

Final working palette (foreground / background):

| Region | Colors |
|---|---|
| Charcoal and weathered steel | #85868C / #111214 |
| Red-lit leading edge | #CC4650 / #000000 |
| Blood-red reflection with one cold-silver accent | #D4D4D6 / #A42A36 |
| Dark-crimson wake | #B1B2B8 / #751B25 |

The deepest reds form the glow behind steel lettering; the leading red letter
uses black for contrast. All four pairs exceed 4.5:1. Darker suggested foreground
greys/reds would lose legibility on charcoal, so the steel reflections are raised.
The offline preview uses the same palette and phase model, checked by regression.
Stopped/waiting/idle treatments and Dotbar's surrounding theme remain unchanged.

No `#()` job, `date`, polling daemon
or 10Hz `A:` animation is used. Status interval is temporarily 1 while observed
agents work and returns to its prior value when they stop/expire. Unchanged tool
events avoid another cache write/render; an active lease renews at most every 30s.

Private benchmark, 24-character title, three samples of 2,000 expansions:

| Format | Median ms / expansion |
|---|---:|
| Idle | 0.0178 |
| Working | 0.4803 |
| Stopped | 0.0231 |
| Permission request | 0.0233 |
| Monitor over 20 idle windows | 0.2386 |

These are local wall-time bounds including tmux command parsing and captured
output, not system-wide CPU measurements. Animation launches zero processes.
Reproduce with `python3 -B scripts/benchmark_dashboard.py`; it always creates an
owned private socket, never uses production. In the same measurement session,
17c6f99's single-cell working format took 0.3305 ms; the three-cell band adds
0.1498 ms per 24-character expansion. Native 1Hz cadence and zero animation jobs
are unchanged. Changed-cache refresh for three inert agents measured 53.94 ms
wall time; an unchanged working hook measured 25.72 ms and performed no tmux/cache update.
Actual terminal redraw/plugin cost and real-hook latency still need live
observation after approved activation.

`Ctrl+F`, release, then `n` cycles **only waiting/stopped panes in the current
session**, in current status-bar window order, then stable pane-ID order. It
selects the agent pane, wraps predictably and leaves an empty queue untouched.
Other sessions, working and idle panes are never fallbacks. Window numbering,
Cmd+1–9 and Option+h/l remain unchanged. The old n binding was new-window, not
next-window: project-directory creation moves to `Ctrl+F c`, the existing standard
creation key. Shift+N adds ordinary next-window (unbound in inspected defaults);
Space remains next-layout. The installer refuses a conflicting N/n/c binding.
Tab remains workmux last-agent.

Final configured chain after coordinated adoption/reloads:

| Input | tmux route | Behavior |
|---|---|---|
| Ctrl+F, release, n | prefix n | Cycle attention panes; empty queue leaves focus |
| Cmd+Shift+N | text:\x06\x63 → prefix c | Create a window in the pane's directory |
| Ctrl+F, release, c | prefix c | Same window creation |
| Ctrl+F, release, Shift+N | prefix N | Ordinary next window |
| Cmd+1–9 | prefix 1–9 | Existing numbered-window selection |

Fresh read-only inspection on 2026-10-22 confirms the production n binding really
creates in the pane directory, c is standard creation, N is unbound and Tab runs
workmux last-agent. Ghostty's headless effective-config output confirms its old
Cmd+Shift+N route is n. GUI-loaded physical delivery still needs acceptance.

The new end-to-end regression parses both Ghostty snapshots through the installed
headless +show-config action using a private HOME/XDG config. It decodes the
serialized text action and writes its bytes into an actual attached private tmux
PTY. It tests both routes through every rollout phase, n attention, c creation,
N navigation, all nine Command-number routes, pane movement and window reordering.
Protected workmux/popup/other bindings are compared unchanged. This covers the
parser → text bytes → tmux input → binding → behavior chain, not macOS key-event
delivery or proof that a running Ghostty window loaded the file.

**Companion-key conflict:** the existing Ghostty Cmd+Shift+N sends Ctrl+F n.
Changing n alone would break new-window creation. The candidate changes exactly
that forwarding line to `text:\x06\x63` (Ctrl+F c); all other Ghostty mappings
remain byte-for-byte unchanged. Live Ghostty has not been modified. Until its
companion config is adopted/reloaded, installation retains n as new-window and
runs the display only. c creates in the pane directory in both modes, so old
and new forwarded bytes are safe during the transition. Strict preflight flags
this missing companion; --display-only validates the explicit fallback.

Installation enables attention only when the configured companion mapping is
present. That file check is not proof of running-Ghostty delivery: an approved
GUI reload and physical test precede the explicit tmux reload that enables n.
Background session monitoring never changes key bindings. The transition is not
jointly atomic; keep existing sessions and do not start new tmux servers in the
interval between Ghostty migration and its verified reload. See the precise
rollout and reverse order in MILESTONE-DEPLOYMENT.md.

## Independent reversal

All commands below require a separately approved live operation. First inspect
the actual socket/release and confirm no intervening binding/hook changes.

```sh
python3 -B /ABSOLUTE/RELEASE/tmux/agent-dashboard.py disable --socket /private/tmp/tmux-501/default
```

This removes only the owned monitors/hook, clears title caches, restores the
previous interval and accepted n behavior, and removes an owned Shift+N binding.
c retains directory-aware creation while Ghostty forwards c; restoring its old
default follows the separately approved Ghostty rollback/reload.
It removes its exact title slot while preserving Dotbar's surrounding formats,
restoring workmux's original format auto-detection. Late refreshes check the
disabled flag. It leaves Doom, panes, conversations and workmux settings intact. To omit
observer hooks on future launches, use Fish `CDEV_DASHBOARD=0 cdev PROJECT`.
The Fish function explicitly passes that setting into the new tmux agent pane.
Existing registered conversations are not edited; their advisory hooks may keep
updating private evidence while the display is disabled.

Re-enable through the reviewed candidate's separately authorized tmux reload.
Full release rollback must follow [the multi-component sequence](MILESTONE-DEPLOYMENT.md).
