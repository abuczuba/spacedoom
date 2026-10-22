# Stable Codex lifecycle registration — 2026-10-22

Repository repair candidate; no live configuration, release or trust changes.
Production remains the recovered Phase 3B configuration, on
20261022T163617.469413Z-497daec6. Both prefix n and c create windows. Attention
navigation and persistent Doom infrastructure remain deferred.

This document supersedes the per-launch command-identity design in ACTIVITY.md
and the older rollout instructions. Deployment remains blocked until actual
Codex delivery, after explicit user hook review, passes the checks below.

## Root cause and direct evidence

The eight new definitions were SessionStart, UserPromptSubmit, PreToolUse,
PermissionRequest, PostToolUse, Stop, Interrupt and SessionEnd. Each was a
session-flags matcher group with one command handler, timeout 2 seconds, no
matcher and no policy/notification settings. The original command was:

```text
<python> -B <resolved activity.py> event --state <state> --socket <socket> --pane <pane> --token <uuid4>
```

The token changed on every launch. Pane ID changed when creating another pane;
socket/state changed with the runtime context. Resolving the module path also
embedded the installed release path. Interpreter location could change with
the Python installation. Handler type, timeout and event list were stable.

Installed Codex 0.163.0 was queried through its own read-only hooks/list RPC in
two owned stdio servers and sanitized homes. Holding interpreter, module, state,
socket and pane constant while changing only the nonce changed **all eight
currentHash values**. Their keys were
/<session-flags>/config.toml:<snake_case_event>:0:0 and source was sessionFlags.
Every new definition was untrusted and non-managed. This establishes the hash
problem directly without reimplementing Codex's hash algorithm or writing trust.
The previous real TUI test had already shown eight new/changed hooks and no
usable lifecycle events; its exec test completed a turn but emitted no observer
evidence. Neither is successful hook delivery.

OpenAI documents discovery from active hooks.json/config.toml layers and plugins,
merged rather than replaced; project discovery requires project trust. Exact
definitions require user trust; /hooks is the review interface. The documented
JSON supplies session_id, hook_event_name and event-specific turn_id. It does
not promise a per-client TMUX environment. See the
[official hook contract](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks)
and [hooks/list protocol](https://learn.chatgpt.com/docs/app-server).

The inspected user source contains seven workmux handlers: SessionStart,
UserPromptSubmit, PermissionRequest, PostToolUse, Stop, SubagentStart and
SubagentStop. Their existing trust records live under that source's positional
keys. Nothing is inserted into that file or its arrays. The native discovery
regression loads copies of those definitions alongside the eight sessionFlags
handlers and verifies all seven original keys/hashes survive unchanged. No trust
record, global hook, notification setting or workmux configuration is edited.

## Corrected registration

All eight definitions now invoke the same fixed command:

```text
<python> -B <installed lexical sibling path>/activity.py event
```

There are no runtime identity arguments. For the inspected standalone cdev
launcher, the expected approved installation path is
/Users/czuba/.config/cdev/activity.py. Python resolves an imported module through
a symlinked script's real sys.path; an experiment confirmed that behavior.
Consequently the main launcher's lexical __file__, rather than the imported
adapter's resolved path, supplies the sibling adapter path. A regression runs
the unchanged standalone Fish function against private managed helper symlinks.

Native Codex currentHash and source keys are identical across distinct launches,
nonces, panes, sockets and state locations at a fixed installed adapter path.
The definitions remain untrusted until the user reviews them. Moving the
installation/interpreter or changing a definition legitimately requires review.
Codex's definition hash does not attest to script contents: changing the adapter
behind a stable command must still undergo code review and approved immutable
deployment. Native trust is not a substitute for release integrity checks.

The launcher passes CDEV_ACTIVITY_CONTEXT only to its child process, as JSON in
the subprocess environment. It contains a version, socket, stable pane ID,
private state directory, nonce, launcher PID and process start identity. It is
not shell input, a Codex configuration override, a trust record or a credential.
An enclosing registration is removed before every tracked or untracked launch.
The private per-pane record separately stores the actual spawned child PID and
start identity. Early events racing that registration are ignored.

Before using an event, the adapter requires:

- Valid bounded context, private owner-only directory/record/lock, no symlinked
  state ancestry or linked/nonregular record, and matching launch nonce.
- Both the recorded child and launcher as live same-user ancestors of the hook,
  with matching start identities; a different intervening Codex is rejected.
- The exact tmux socket, server boot, stable pane ID and pane-root PID still
  matching the registered launch.
- Documented session/turn identity passing the existing stale-event state
  machine. cwd, inherited TMUX and transcript paths never select a registration.

The adapter reads only targeted ps ownership/parent/start/command-name metadata;
it never reads process environments, credentials or transcripts. JSON fields are
data, never evaluated or interpolated into shell commands. Atomic mode-0600
records and locks remain under a mode-0700 directory. Existing state shape,
renderer, native 1 Hz shimmer, attention navigation and expiry policy remain.
No socket listener, background daemon or per-frame subprocess is added.

This is an advisory same-account observer, not authentication against malicious
code already running as the account. The nonce fences stale launches. It never
authorizes Codex tools or changes its sandbox/approval policy.

## Evidence boundary and failure behavior

The runtime handoff has been exercised with **synthetic payloads in actual
owned parent/child process trees**, including two concurrent agents in the same
Git directory. Those tests establish environment handoff and attribution in the
fixture; they do **not** establish what a real Codex hook subprocess inherits.

The public hook documentation does not establish that client-specific runtime
environment reaches hooks on a shared app-server. The adapter therefore rejects
missing context or a shared server whose ancestry does not contain this exact
launcher and child. It never guesses by directory, trusts inherited TMUX, forces
--no-daemon, or changes global hooks to make a test pass. If ordinary Codex uses
such a shared process, this design stays unlabelled and rollout remains blocked.
Actual delivery and shared-server behavior must be demonstrated after review.

Untrusted hooks are skipped by Codex. Missing, malformed, failed, timed-out or
ambiguous evidence cannot mark an agent working. The adapter returns 0 without
policy output on runtime errors; Codex remains usable. Existing labels expire
under the renderer's 15-minute lease. Normal child exit marks the record ended,
sets idle and clears its nonce-fenced marker. Abrupt process/pane/server loss is
rejected by the renderer; old events cannot revive an ended or replaced launch.
No hook can turn a stopped turn into a guarantee of task success.

## One-time user review and real-delivery gate

Do not run the production procedure yet. This repair has no deployment approval.
First review this patch and the exact adapter artifact. A sandboxed proof uses an
owned tmux server, isolated configuration/state, a stable copied adapter, inert
standalone editor, and real installed Codex. Never seed trusted_hash, emulate
managed policy, replace workmux on PATH or use a trust bypass. Any native hook
review prompt is a hard stop for the agent; only the user may trust definitions.

After a separately approved installation, the production one-time review is:

1. Start an ordinary new cdev project window using the standalone launcher;
   preserve existing conversations and editor panes. At Hooks need review,
   choose Review hooks, not blanket trust of unrelated definitions.
2. Inspect exactly the eight sessionFlags entries above. Each must invoke only
   /usr/bin/python3 -B /Users/czuba/.config/cdev/activity.py event, timeout 2,
   with no dynamic flags, policy changes or unrelated handlers. Compare the
   approved adapter/release hash separately; inspect existing workmux entries
   without editing, disabling or reordering them.
3. Explicitly trust these reviewed definitions in Codex's UI. This is the user's
   native trust action; the deployment tool and launcher never perform it.
   /hooks is also available for inspection/review from an existing CLI UI.
4. Run a harmless no-tools turn. Require actual SessionStart/session binding,
   UserPromptSubmit working and Stop stopped evidence for the correct pane.
   Inspect only private state metadata and targeted process identity, never
   conversation contents. Then test a second ordinary launch with unchanged
   adapter/interpreter: the eight hashes must remain identical and must not
   request review again. Repeat with two concurrent panes, including the same
   cwd, movement/renumbering and clean exit.
5. Validate actual PermissionRequest/PostToolUse/Interrupt/SessionEnd separately
   in disposable owned contexts under normal sandbox/approval rules. Until
   observed, these transitions have synthetic coverage only. Do not induce
   approvals or alter existing production windows as test subjects.

Trust recorded in a disposable profile applies only there; a different adapter
path/hash requires a separate review. No temporary trust state is copied into
the live profile. Only successful real delivery permits a new consolidated
rollout proposal. Production n/c compatibility and Cmd+Shift+N remain intact;
attention navigation must not be enabled to compensate for missing evidence.

## Validation and recovery

The full-suite result and any native review observation are recorded in
STATUS.md. Existing renderer/key-forwarding, workmux ordinary-pane, cdev reuse,
standalone editor/compiler environment, terminal, deployment/restore and isolated
Doom regressions are retained. The new tests distinguish native discovery/hash
checks from synthetic dispatch; no test writes trust or executes unreviewed hooks.

The code changes affect only the two existing cdev payloads; no new managed path
or manifest/deployment framework is needed. Existing immutable releases,
including 8dad372, are not modified. A later approved rollout must stage a new
release and repeat helper-only backup/adoption and real delivery gates while
leaving standalone Fish and Doom intact. If adoption fails, restore only that
new cdev backup with the existing deploy.py restore procedure. No rollback,
pointer change, reload or existing-process termination belongs to this repair.
The separate idempotent commit-keyed staging follow-up remains outstanding.
