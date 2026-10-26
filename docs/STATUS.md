# Current: verified native approval-state repair — 2026-10-26

SSH-signed `8568518` is active in `20261026T191404.024651Z-db56a4bd`.
All 18 payloads and 16 managed links verify; only cdev/activity.py and
codex_session.py change semantically. No tmux reload, service operation, agent
restart or manual dashboard-state repair occurred. Inherited work is preserved.

PermissionRequest is a pre-review hook, not proof of pending human approval.
The existing retained reader now checks native request/thread/turn/item IDs and
exact resolutions, with launcher/child/backend births and pane/server validation.
No hooks, monitoring infrastructure, approval decisions or notification system
were added. See [APPROVAL-STATE.md](APPROVAL-STATE.md) for compatibility boundaries.

81 focused regressions passed, including a test that fails against the prior
code. Genuine Codex 0.164.0 reproduced automatic-review false waiting before
repair. The activated-byte disposable canary passed fresh working/stopped,
exact-UUID remote reopening, native shimmer, stopped dot and attention navigation.
Automatic review emitted PermissionRequest but no external human request and no
false waiting. A genuine human request stayed red/actionable until native No;
its exact resolution cleared pending before the terminal hook. Eight previously
trusted definitions were reused unchanged. One test-only invalid reviewer enum
was rejected before a turn began and corrected against the installed API schema.
Owned native clients/backend/private tmux were closed; private fixture files and
pins were restored. Production hooks, configuration and UUID pins are unchanged.

The authorized Collie pairing deployment explains the 14:05 EDT restart: current
is signed 1fd0899f, build 1.24.0-dev+1fd0899f.1793037779. Its backend is intentionally
byte-identical to a1d18dac; the earlier binary-only identification was incomplete.
The replacement client is a read-only ignore-size child of Collie, matching normal
watch reconnection. The original split/pane identities remain; resized dimensions
match Ghostty's viewport. The exact resize initiator is not recorded. The original
baseline was preserved and only these explained fields were reconciled.

Postflight preserves all 14 protected project process generations, session/window
identities, pane layout and current dimensions, clients, bindings, theme, hooks,
Collie and Doom services. Existing launcher readers adopt the correction on natural
cdev reopening; hook-only local launches retain their documented compatibility
limitation. No existing project session was reopened for this repair.

Rollback (not needed): from this repository, run
`python3 -B scripts/deploy.py rollback --expect-current 20261026T191404.024651Z-db56a4bd --approve`
to restore `20261025T193056.645557Z-0887d0d3` without a reload. Sanitized private
receipts are in /private/tmp/df-permission-fix.MOkf7eFt/ and
/private/tmp/df-permission-canary.d0tauzwm/. No publication was performed.

---

# Current: verified Collie completion notifications — 2026-10-25

Signed Collie a1d18dac is active via the existing LaunchAgent. Its existing poll
reads authoritative main-turn/thread/goal metadata from the existing private
app server, revalidates native identity, and confirms again before push delivery.
Transient screen idle, progress/tools, interruption/failure, old identities and
active continuations cannot establish success. Needs-you pushes are off; Finished
is on. The one-second delay, pairing/push state, Serve and agent controls remain.

Production metadata reproduced two active-turn idle gaps; replay changed from two
false success decisions to zero. Authenticated disposable two-client runtime proved
six completed shell tools + six commentary updates + final answer → one logical
completion; interruption → none. A real ephemeral Codex failed turn was also observed.
697 focused tests, both typechecks, lint and native arm64 compiled service pass.
The deployed bridge observed one natural pluckd completion at 20:17:43 UTC and one
notification decision at 20:17:44. Physical phone receipt confirmation is pending.
Only sanitized metadata is retained in diagnostic evidence.

The independent tmux red flicker is traced to the advisory PermissionRequest/
tool-name pending ledger, which can remain waiting while app-server has no pending
approval. It is not fixed here: no competing observer or changes to live retained
cdev readers. A reliable correction belongs in their existing subscription/activity
path and must respect natural/controlled reopening of those already-running readers.

Concurrent signed a161bfb / 20261025T193056.645557Z-0887d0d3 is preserved after
read-only reconciliation; its two rendering payload changes do not alter cdev or
lifecycle hooks. No dotfiles code/deployment, tmux reload, agent restart or Lab
operation occurred for the Collie repair. All inherited changes remain intact.
Private evidence and guarded Collie-only rollback (245430fc, Finished disabled to
avoid restoring noise): ~/.local/share/collie/profile/OPERATIONS.md and
~/.local/share/collie/profile/evidence/lifecycle-completion/.

---

# Current: selected working-title underline alignment — 2026-10-25

SSH-signed `a161bfb` is active in `20261025T193056.645557Z-0887d0d3`.
The private preview's selected style inherited `underscore`, decorating its
leading padding. A zero-width reset now precedes that existing padding for a
selected working window; only its title receives the theme's `#f6c177` underline.
Shimmer colours/timing, spacing, ordinary window styles and key behaviour remain.

All 30 focused regressions passed. A native terminal-cell regression reproduced
the old cells 0–5 versus title cells 1–5 and passed after correction, including
concurrent working windows and working/stopped/idle/approval transitions. Live
cached styles and native animation passed; final Ghostty visual acceptance is
pending. All 18 payloads, 16 links, existing sessions/windows/panes/clients,
geometry, 14 protected process generations, Collie/Doom services, hooks and pins
passed continuity checks. Only two dashboard payloads changed; inherited work
is preserved. Existing dashboard callbacks were updated without any reload.

Rollback target: `20261025T143619.293776Z-74424e92`. Verified guarded pointer,
exact title-slot and callback recovery: `python3 -B /private/tmp/df-underline-align.28rGh7xG/rollback.py`. Its `--check` passed;
rollback was unnecessary. Runtime snapshots and test logs are in that private
directory. Next action: user visual confirmation of first/last title-cell edges.

---

# Current: Collie shell-directory correction — 2026-10-25

The user personally accepted the 08b69e2f iPhone dashboard: all four Codex agents
and ordinary shells remain visible; four cdev Doom panes are hidden. Signed Collie
245430fc is now active through the existing LaunchAgent. New tabs use tmux's
existing -c support to default to server HOME (/Users/czuba), independently of
Collie's isolated HOME/release directory; explicit directories still win.

428 focused adapter/conformance tests, both typechecks and compiled arm64 HTTP
runtime passed. A normally paired isolated client exercised the real + endpoint
for default/blank/explicit paths; local tmux/Fish creation stayed visible. Final
live checks preserve original panes, process generations, geometry, hooks/config,
UUID pins, pairing/push state and Serve. No agent input/restart, direnv allow or
Fish change occurred. Fresh physical iPhone + confirmation is requested.

Dotfiles source 18a5314 and active release 20261025T143619.293776Z-74424e92 remain
unchanged; no managed deployment was needed. Guarded bridge rollback is to
08b69e2f. Private instructions/evidence: ~/.local/share/collie/profile/OPERATIONS.md
and evidence/new-shell-home/. Inherited source/documentation changes are preserved.

---

# Current: hide only cdev Doom editors in Collie — 2026-10-25

Signed dotfiles `18a5314` is active from clean export in
`20261025T143619.293776Z-74424e92`; rollback is
`20261025T081657.498631Z-8166177c`. All 18 payloads and 16 managed paths are
preserved; only cdev/codex_session.py changes semantically. cdev establishes an
explicit pane-scoped editor role bound to the inspected launch PID/command.
Unknown or stale roles stay visible, including editor-to-shell respawns. The
stable launcher works with already-loaded Fish functions; no reload is needed.

Signed Collie `08b69e2f` is deployed through the existing LaunchAgent. Its
AgentList hides only validated editor roles. All 11 backend panes are retained:
four Codex agents and three ordinary shells remain dashboard-eligible; exactly
four existing Doom editors are excluded. The iPhone-created %62 shell is retained.
Existing editors were marked after positive cdev/process checks, without input,
restart, layout changes or hook/configuration/UUID-pin edits. Auth/push/Serve state
and all original process generations and pane geometry are unchanged.

603 focused bridge tests, 164 UI tests, both typechecks, focused lint, native cdev
creation/reuse/standalone/respawn-race checks and compiled arm64 runtime passed.
An isolated native-tmux fixture verified real Collie createTab and local tmux
shells remain visible, while the editor stays addressable. All 15 access-gate
checks passed. Actual iPhone refresh/new-+ confirmation remains pending; no
physical phone acceptance is inferred from unit tests or API snapshots.

Private evidence and guarded code/source rollback are recorded in
`~/.local/share/collie/profile/OPERATIONS.md` and
`~/.local/share/collie/profile/evidence/dashboard-editors/`.
All inherited documentation and pending work remain intact and uncommitted.

---

# Persistent four-agent Collie installation — 2026-10-25

Signed ba5cc68 is active in `20261025T081657.498631Z-8166177c`; rollback is
`20261025T071258.621516Z-fc135dcc`. All 18 manifest payloads and 16 managed paths
are preserved; only activity.py changes semantically. The opt-in accepts four
explicit session UUIDs after existing cdev origin validation, allowing verified
same-UUID recovery. No hook/trust overwrite, tmux reload or agent restart.

The private Collie build cbbf0ca0 is installed under `~/.local/share/collie/`
and runs via the supported `herdr.collie` LaunchAgent. All four production Codex
footers/process generations/pins and terminal reads match. Existing phone token,
non-expiring `iphone171` authorization, VAPID keys and push subscriptions survive
ordinary restart and tested launchd crash recovery. The personal Serve address
and policy are unchanged; no Lab infrastructure was contacted or changed.

Focused forwarder/origin/lifecycle tests: 18 passed. Collie identity/beacon/runtime
checks: 282 passed; profile/fixture checks: 389 passed; nearby Surface/send/answer/
notification/push checks: 916 passed; both typechecks passed.
Two bounded Collie fixes cover fresh native identity beyond twelve idle hours and
a real wrapped-progress false-idle case. Production no-tool Lab/pluckd checks and
the dotfiles read-only UID command ran; the latter was automatically allowed,
so it does not establish a new human approval. Four-agent physical iPhone acceptance
and the final background push/deep link confirmation are pending. Earlier isolated
and single-dotfiles iPhone acceptance remain historical evidence.

Private exact commands, evidence, revocation and rollback:
`~/.local/share/collie/profile/OPERATIONS.md`. Production credentials were not
copied; temporary independently authenticated pilot fixtures remain for rollback.
All inherited documentation, global-AGENTS and unrelated pending work is preserved.

---

# Collie dotfiles canary accepted on the actual iPhone — 2026-10-25

Signed `210ae9a` is active in `20261025T071258.621516Z-fc135dcc`, from a clean
export. All 18 payloads and 16 managed paths are preserved; only activity.py
changes. Its exact-launch opt-in forwards sanitized native metadata into the
existing isolated Collie beacon pipeline. No hook registration, trust hash,
approval policy, dashboard rule, tmux binding or app-server configuration changes.
Six new forwarding tests, eight nearby regressions, preflight, signature and
both release integrity/syntax checks passed. Inherited working-tree edits remain.

Native /statusline now has thread-id first, followed by all three original items:
model-with-reasoning, current-dir and thread-name. Codex also persisted its
already-enabled status_line_use_colors=true. All other config semantics and
existing global hooks/UUID pins are unchanged. Genuine native UserPromptSubmit
and Stop delivery, exact UUID/pane/process attribution, working→done and the
stopped dashboard state passed on the idle dotfiles client. No other production
pane received input; no existing agent was restarted or signaled.

The former isolated bridge had already exited. Its existing source command now
runs on the same loopback port, pointed at the real tmux socket; Serve is unchanged.
Collie reports dotfiles as codex/idle and reads its terminal. Fifteen access-gate
checks and HTTPS unpaired refusal passed (normal certificate verification).
Disposable tmux/app-server/clients remain alive. The user personally confirmed
production iPhone read/prompt/status/reconnect acceptance: all checks passed. A
read-only follow-up verified the same dotfiles UUID/pane/process binding, bridge
generation and all pre-existing protected process generations. Production tool
approvals, production background notifications and other projects remain untested.

Owner-only evidence and scoped rollback:
`/private/tmp/collie-tailscale-preflight-f8c7ozwl/dotfiles-live/` (ROLLBACK.txt).
Handler rollback target: `20261025T063110.488579Z-723f7740`, guarded by expected
current `20261025T071258.621516Z-fc135dcc`. No tmux reload, agent termination,
Tailscale change, permanent service or publication occurred. ntfy remains retired.

---

# Current: transport-free dashboard — 2026-10-25

Production: `20261025T063110.488579Z-723f7740`, SSH-signed commit `c8bd5fa`.
The ntfy publisher, active imports/callouts, startup argument and deployment
payload are removed. Its private destination config and six delivery-state files
were deleted after verified quarantine/acceptance; no secret backup remains.
No legacy notification process or active ntfy dependency remains in the managed
workstation integration. Historical documentation/Git and immutable rollback
releases remain intentionally intact. Collie is separate and is not yet connected
to production agents, so those agents currently have no phone-alert transport.

The shared renderer, lifecycle validation, shimmer/dots/approval alerts,
acknowledgment, attention and UUID recovery remain unchanged. 120 focused
regressions and six isolated cleanup checks passed. All 18 immutable payloads,
16 managed paths, current 16 protected process generations, 11 Collie pilot
identities, session 2, sessions/windows/panes/clients, theme, binding behavior,
Codex config/trust/global hooks and UUID pins passed post-deployment checks.
Only owned native dashboard callback registrations were updated; no tmux reload,
agent/editor restart, service action, Collie/Tailscale change or push occurred.

One initial guarded cleanup attempt rolled back and restored the private files.
Its full-stat read guard incorrectly included access time; an isolated aged-atime
reproducer failed the old guard. The corrected guard retains identity/hash/mode/
size/mtime/ctime checks, excludes access time, and acquires writer locks before
reading delivery ledgers. Six regressions passed; the unchanged signed release
then completed retirement. A dynamic working/idle status interval was separately
validated against the existing saved interval rather than frozen as a theme value.
Concurrent project reopenings were observed before final activation, verified
against their unchanged exact UUID pins/remote clients and baselined immediately;
no cause or actor was assumed. The original snapshots are retained.

The user confirmed the unrelated 65-byte trusted-project entry for ~/dev/myproject
was a manual cnew test. That Codex configuration remains byte-identical, and the
test project was left alone. All other pending source work is preserved; only
obsolete optional publisher support was removed from three pending test fixtures.

Code rollback, if subsequently needed:

```sh
python3 -B ~/dev/dotfiles/scripts/deploy.py rollback --expect-current 20261025T063110.488579Z-723f7740 --approve
python3 -B ~/.local/share/dotfiles-active/current/tmux/agent-dashboard.py install --socket /private/tmp/tmux-501/default --state ~/.local/state
```

This returns to `20261025T061731.748309Z-45cef594` and reinstalls dashboard
callbacks without a destination argument. It does not recreate the retired
private destination or re-enable phone delivery. No component migration changed.
Evidence: /private/tmp/df-remove-ntfy.oIYzFzMt/verified-retry/; prior failure and
isolated cleanup reproduction remain in its parent. Earlier entries below are
historical and do not describe current phone-notification recovery.

---

# SessionEnd rollout failed real resume acceptance; rollback verified — 2026-10-24

Release 20261024T205823.447579Z-6108de71 (signed repair a13eae3) was activated
after clean-export, 17-file manifest, integrity, drift and continuity checks.
Real acceptance used the installed ordinary cdev in a private tmux server and
the already trusted, empty workmux-test fixture. The historical cdev-smoke
conversation was reported active and was left untouched.

Actual Codex **0.164.0 fresh-launch** results passed: working state and moving
native shimmer frames; stopped white dot; actual Ctrl+F n navigation; one stopped
ntfy publish accepted with one attempt. A genuine read-only ps approval request
produced waiting/red alert and one approval publish. The request was canceled
without elevated execution; Interrupt correctly cleared the indicator to idle.
Approved-command continuation and physical iPhone receipt were not verified.

The fresh test CLI quit normally and its launcher/child exited; registration
finalization passed. Ordinary cdev then recovered the exact test UUID with a new
pane/token and shared-backend registration. **Critical failure:** the resumed CLI
ran its real read-only command, printed its final answer and recorded a completed
turn, while its observer remained session=null, turn=null, idle, sequence=0,
ended=false. No resumed shimmer/dot/notification resulted. SessionEnd no longer
retired it, but an additional remote-delivery/attribution gap remains unlocalized;
do not claim that hook invocation versus identity rejection is established.

Authorized rollback completed and was verified. **Production current is again
20261023T164459.630188Z-30124092.** Rollback journal:
20261024T212310.063818Z-cce0f01c.json. All 14 live links, payloads, original session,
five windows/nine panes, bindings, original client/process start identities,
Codex configuration/trust, workmux definitions and exact original pins survived.
Main client 98442 selected @19 before and @20 afterward; cause is unattributed
and that focus was not reset. No application reload/restart occurred.

Both owned test Codex launches exited normally. The private test client/server,
test editor frames and only the newly added test pin were cleaned up; the test
conversation is idle. Owner-only evidence remains at
/private/tmp/df-session-end-live-i1_740qt, including real event samples,
CRITICAL-ACCEPTANCE-FAILURE.json, cleanup.json and RESTORATION-VERIFIED.json.
No deployment/session manual recovery is required. Existing production dashboard
registrations were not edited or restarted, so their earlier regression remains.

The repair release is retained inactive/immutable. Pending cnew/global-AGENTS/
cdev-name changes and inherited repository work are preserved; no new commit or
push was made. Stop after rollback; further remote-path diagnosis is a separate
authorized step, not another automatic activation attempt.

---

# SessionEnd repair signed and staged inactive — 2026-10-24

SSH-signed repair-only commit **a13eae3858e54222719e54cac07a517195cd6dec**
(`fix(cdev): keep live registrations through SessionEnd`) contains only activity.py,
its two test files and SESSION-END-REPAIR.md. Signature verified with a temporary
allowed-signers file and the same ED25519 key as the previous signed commit;
no Git signing configuration changed. Mixed STATUS/inherited/workflow edits were
excluded from the commit and their previous contents preserved.

Inactive release **20261024T205823.447579Z-6108de71** is an independent copied
release under ~/.local/share/dotfiles-active/releases/, staged from a clean archive
of that exact commit. Its 17-file manifest is identical to production's. All files
match the commit after normal rendering and are regular independent copies, mode
0444. Only cdev/activity.py changes source/behavior; tmux.conf, navigation, cdev.fish
and the LaunchAgent differ only in their regenerated release-local references.
Pending cnew/global-AGENTS/cdev-name features are not included or deployed.

Final privacy, dependency, reference, syntax, drift and integrity checks passed;
four isolated deployment/rollback guards passed. The accepted 42-test repair's
executable/test bytes are unchanged. Real 0.164.0 delivery acceptance is pending.

**Current and rollback target remain 20261023T164459.630188Z-30124092.** All 14 live
links still resolve there. The one session, five windows, nine panes, client focus,
loaded bindings, Codex trust configuration, workmux hooks and UUID pins are
unchanged. Only one inactive release was added; no activation history or backup
was created/changed. No application reload, agent termination or live cache repair.

After a separately approved activation, exact rollback from the checkout is:

```sh
python3 -B scripts/deploy.py rollback --expect-current 20261024T205823.447579Z-6108de71 --approve
```

This returns to the verified previous release without reloads or runtime-record
rewrites. [SESSION-END-REPAIR.md](SESSION-END-REPAIR.md) contains the live working,
stopped, genuine-approval and exact-UUID recovery acceptance procedure. Existing
ended registrations require natural fresh cdev launches; no active agent is to
be restarted automatically. **Stop before production activation.**

---

# SessionEnd registration repair tested — source only, 2026-10-24

The adapter now ignores SessionEnd for launch state. Only owned-child finalization
permanently retires a registration; UUID/nonce/process-start/pane checks and turn
retirement are unchanged. Delayed end notifications cannot bind a wrong session,
clear a newer turn/approval/dot, advance pager revisions or suppress future events.

Six selected regressions failed before the fix. **42 focused tests passed** from
a temporary export of committed HEAD plus only the adapter and its two test files:
resume/end orderings, transitions, concurrent/reopened identities, delayed events,
PID reuse/death, real inert-child exit, native hook hashes/workmux, title rendering,
attention and pager behavior. Synthetic dispatch is not real 0.164.0 turn delivery.

[SESSION-END-REPAIR.md](SESSION-END-REPAIR.md) records the repair-only release plan.
Its export retains production's 17-file manifest and only activity.py differs;
pending cnew/global-AGENTS/cdev edits and inherited work are preserved. No commit,
production cache repair, release staging/activation, reload or restart occurred.
Already-ended agents require natural reopening after a separately approved rollout;
this source patch does not silently revive them. Production remains on
20261023T164459.630188Z-30124092. Next step: review this isolated repair.

---

# Personal project workflow implemented in source only — 2026-10-24

Read-only instruction inventory covered dotfiles, pluckd, private-ai-ops-lab,
Collie and the other scoped ~/dev projects. Project-specific policies and upstream
AGENTS.md/CLAUDE.md files are preserved. [PROJECTS.md](PROJECTS.md) records the
inventory, instruction scope, usage and future deployment/recovery boundary.

New candidates: a concise global Codex AGENTS.md (`codex-instructions` component)
and `cnew NAME` (`fish-cnew`) for minimal, uncommitted personal repositories under
~/dev. Existing paths and nested repositories are refused. `cdev NAME` now resolves
to ~/dev/NAME; explicit paths/no argument retain their meaning. Conversation UUID
recovery, reuse, dashboard hooks and Doom launching code are unchanged.

**67 focused tests passed:** 9 creation/refusal/concurrency cases, 39 deployment/
recovery cases (including independent global-instruction/cnew restore), and 19
isolated cdev/session-recovery cases. Complete candidate dependency/reference and
configuration parsing passed. The sandbox initially blocked test socket creation;
the isolated socket tests then passed with narrowly approved test access.

Read-only final comparison passed: active release
**20261023T164459.630188Z-30124092**, all 17 payloads and 14 managed links remain
valid; live cdev, Codex configuration, UUID pins, inspected instruction files,
original sessions/windows/panes/clients, client focus and loaded tmux keys are
unchanged. No global instruction or cnew file was created live; no production
staging, activation, reload, process replacement or new live agent launch occurred.
Inherited uncommitted documentation is preserved. These are undeployed source
changes; the next boundary is explicit approval for staging and activation.

---

# Doom dashboard charcoal correction accepted — 2026-10-23

Commit **76b683d** corrects the reversed intent of 9550d3a. The desired background
is the original **lighter charcoal behind the ASCII**, now extended to the entire
dashboard buffer. Original banner inheritance resolves to **#262626** in the live
terminal, verified directly from the theme/comment face rather than screenshot
estimates. The color is derived at runtime, not hardcoded.

The old two-face global customization/callback was removed and original cyan
banner/loaded faces restored. Only dashboard-local default/fringe backgrounds
are remapped; Solaire remains on and cannot re-cover them with its darker mapping.
Normal startup uses the corrected inline block in config.el. No other theme,
frame, font, clipboard or application configuration changes were made.

**9 focused tests passed**: seven targeted configuration/recovery cases and two
real terminal cases (standalone and fresh client). They verify uniform body/fringe/
banner/loaded backgrounds, preserved cyan/text/menu layout, Solaire reactivation,
idempotent local remaps and unchanged real file/Org/vterm buffers and another
client frame. Live verification also reports all non-dashboard buffer remappings
and other frame/global-face attributes unchanged. Daemon **78809**, all 14 protected
process identities and four original windows/seven panes survived; tmux keys,
monitor, pager/hooks, UUID pins and 14 managed links remain intact.

Active release **20261023T164459.630188Z-30124092** and its 17 payloads are unchanged.
No pointer switch, app/client restart, tmux/Ghostty reload or package/service change.
Backup **20261023T182742.184605Z-ec9ceee3** preserves the exact pre-correction config
and permissions; that real backup restored twice in an isolated temporary home.

```sh
python3 -B scripts/deploy.py restore --backup 20261023T182742.184605Z-ec9ceee3 --approve
```

This file restore returns to the previous flat 9550d3a appearance on future startup.
For matching runtime rollback, remove the three named `dotfiles-dashboard-background`
hooks, remove only their two buffer-local remap cookies from dashboard buffers,
and evaluate the previous six-line 9550d3a block. Never reload unrelated personal
configuration or restart clients. Existing older backups remain untouched.

**User physical visual acceptance PASS:** the entire splash has the intended
uniform lighter charcoal background, with no rectangular artifacts. Cyan artwork
and menu styling are preserved. Planned workstation ricing milestones are closed;
no further configuration changes or testing are requested.

Before future development, recheck relevant live dotfiles and deployment state for
manual changes since this accepted baseline; preserve and reconcile those edits
before implementation. Concurrent documentation edits remain preserved.

---

# Doom dashboard background corrected; GUI font checked — 2026-10-23

Signed commit **9550d3a** is deployed as a six-line customization inline in normal
`~/.config/doom/config.el`, copied from `configs/doom/dashboard-faces.el`.
Active release **20261023T164459.630188Z-30124092** and all its 17 payloads remain
unchanged; no new release or pointer switch was needed for this regular-file edit.

Actual cause: current Doom's `+dashboard-banner` and `+dashboard-loaded` inherited
`font-lock-comment-face`, including its explicit background. Live terminal values
were **#262626** for that background and **#1c1c1c** for Solaire's dashboard default.
The two faces now retain the cyan foreground (**#008787** in that terminal) but
have no comment parent or explicit background. Solaire's buffer background shows
through. Theme/default/comment/Solaire faces, widgets and ASCII art are unchanged.

**46 focused tests passed**: 44 deployment/recovery tests and two real terminal
dashboard tests (standalone and new client), including theme-customization refresh,
text/layout preservation, clipboard binding and targeted runtime face restoration.
AppKit and an invisible private Emacs NS frame resolve Source Code Pro; Doom's
normal font initializer also selects it for default/fixed/variable faces in an
invisible private NS frame. The historical lookup error was not reproduced and
its cause remains unestablished. No font settings, installations or packages changed.
These are font-resolution checks, not acceptance of visible GUI rendering.

Existing daemon **78809** received only the two face customizations. All 14
protected process identities, four original windows/seven panes and clients
survived. Loaded tmux keys, its single monitor, pager/hooks, UUID pins and clipboard
configuration remain intact; all 14 managed links verified. No app/client restart,
tmux/Ghostty reload, service change or GUI font reload occurred in production.

Backup: **20261023T175822.361707Z-ebecfd11**, containing the previous normal config
with contents/mode 0644 verified; that actual backup restored twice in an isolated
home. File recovery (does not change current or reload applications):

```sh
python3 -B scripts/deploy.py restore --backup 20261023T175822.361707Z-ebecfd11 --approve
```

For runtime reversal in daemon 78809, first remove only its new customization
callback named **doom--customize-themes-h-74** from `doom-customize-theme-hook`
(find the actual symbol by name; it is generated). Then call
`custom-theme-reset-faces` for user specs of `+dashboard-banner`/`+dashboard-loaded`
and `face-spec-recalc` for those two faces on each frame. This precise sequence
was tested in disposable Doom; no whole-theme reload is required. Reinspect if
daemon/callback identity changes. Concurrent documentation edits remain preserved.

Remaining physical check: visually confirm the banner/loaded rectangles are gone
in standalone Doom and a terminal client. Optional GUI check: visible font appearance.
No additional infrastructure work is proposed.

---

# Doom clipboard normalized through normal startup — 2026-10-23

User physical acceptance of `n`, `a` and visual **SPC y -> macOS paste** passed.
Final cleanup is deployed: signed commit **d047165**, active release
**20261023T164459.630188Z-30124092**.

Root cause: normal config.el enabled simpleclip but never loaded the SPC y unit;
cdev and explicit `--load` worked around that gap. Normal config.el now has just
`(load! "clipboard")` in place of its previous two-line simpleclip setup. The
single managed clipboard.el holds `use-package!` initialization and `map!` binding;
it stays separate to keep unrelated personal settings out of Git/releases.
Both clipboard launcher loaders and their manifest references were removed.
No user-defined Cmd+C mapping was found: simpleclip's packaged s-c override is
now retired. Its cut/paste, other copy keys and Emacs' global Command map remain.

**49 focused tests passed**: 43 deployment/recovery tests, three real disposable
terminal clipboard launch paths, two cdev reuse/fallback tests, and two-client
project isolation/reconnection. Native daemon and standalone `emacs -nw` use no
clipboard load flags. Tests exercise character/reversed/line/block selections,
Evil yanking, kill ring, paste bindings and idempotent configuration reload.
Clipboard transport in automated tests is stubbed; the prior physical copy/paste
acceptance covers the unchanged copy implementation. Fresh standalone physical
acceptance without flags has been requested and remains pending.

Only four release payloads change. All 17 payloads, 14 managed links, exact
config.el edit/permissions and unchanged init.el/packages.el were verified.
Daemon **78809** loaded only the clipboard unit; its frames, kill-ring object,
saved clipboard functions and global Command map were preserved. All 13 baseline
protected process identities and three original windows/five panes survived.
An additional window/two panes appeared concurrently (cause unestablished); they
were left untouched. Loaded tmux keys, dashboard monitor, pager, hooks and UUID
pins remain unchanged. No client/agent restart or tmux/Ghostty reload occurred.

Private config.el backup: **20261023T164618.996874Z-8401fac6**, under deployment
`backups/`. Contents and mode 0644 verified; that real backup restored twice in
an isolated temporary home. Config.el remains a regular file. Existing schema-2
restore now recognizes its exact regular-file replacement and refuses later
personal edits; failed restores remain retryable. No private config is in Git.

Normalization recovery (not performed on production): restore the normal config
before the pointer, then reload only the preceding clipboard unit if needed.
The preceding accepted release and all original migration backups are retained.

```sh
python3 -B scripts/deploy.py restore --backup 20261023T164618.996874Z-8401fac6 --approve
python3 -B scripts/deploy.py rollback --expect-current 20261023T164459.630188Z-30124092 --approve
```

That returns to **20261023T060524.343451Z-46053935**. For complete runtime reversal
in the existing daemon, load the preceding clipboard.el and restore the packaged
`simpleclip-mode-map` s-c -> simpleclip-copy binding and s-c copy-keystroke entry;
no client restart is needed. See [QOL.md](QOL.md). Concurrent documentation edits
remain preserved and uncommitted. No further infrastructure work is planned.

---

# Acknowledgment and terminal Doom copy deployed — 2026-10-23

The dashboard/ntfy milestone is **closed by user acceptance**, including iPhone
delivery. Two independent QOL commits are now deployed:

- **b5a0f61**: `Ctrl+F -> a` acknowledges only the selected Codex pane's stopped
  turn; hides its dot and attention entry without changing lifecycle evidence.
  Stale keys cannot acknowledge a newer turn. Pager deduplication is unchanged.
  Independent release: **20261023T055916.769268Z-224dd2ba**.
- **f26a7d4**: visual-mode **SPC y** copies through simpleclip without changing
  Evil yanks or the kill ring. Ghostty intercepts Cmd+C for terminal selections;
  that shell/Codex behavior is preserved. Existing persistent Doom loaded only
  the addon; standalone cdev adds `--load`. Direct standalone invocation outside
  cdev uses `emacs -nw --load ~/.config/doom/clipboard.el`. Private config.el is
  untouched. See [QOL.md](QOL.md) for the limitation and independent removal.

Active release: **20261023T060524.343451Z-46053935**. Both commits retain SSH
signatures. **45 distinct focused checks passed**, plus payload/dependency/privacy
and parser validation. Real disposable client and standalone terminals exercised
SPC y for character, reversed, line and block selections; clipboard transport was
stubbed, so actual macOS clipboard acceptance remains manual. An older combined
test needed the accepted deferred-bootstrap fixture; it then passed.

All 16 protected process birth identities, four windows/seven panes, client,
UUID pins, global hooks, pager and Ghostty survived. Fourteen managed links and
all 17 immutable payloads verified. No agent/editor restart or tmux reload.
Client selection differed between snapshots (`@1/%2` to `@3/%5`); cause is
unestablished and focus was left alone. Concurrent documentation is preserved.

The sole new migration backed up the addon path's original absence:
**20261023T060555.262807Z-b8747573**, under the usual deployment `backups/`.
Clipboard-only recovery, without restarting processes (not executed):

```sh
# First run M-x dotfiles-clipboard-uninstall inside Doom.
python3 -B scripts/deploy.py restore --backup 20261023T060555.262807Z-b8747573 --approve
python3 -B scripts/deploy.py rollback --expect-current 20261023T060524.343451Z-46053935 --approve
```

That returns to the acknowledgment release; repin its dashboard callbacks using
the installer described in QOL.md. The pre-acknowledgment rollback reference is
**20261023T054130.403606Z-e8aefd8b**; do not roll back across clipboard adoption
when only acknowledgment should be removed. No older releases were modified.

Remaining physical checks: acknowledge a white-dot Codex pane and confirm `n`
skips it; a later stopped turn must return. In Doom, visually select text, press
SPC y and paste into another app; ordinary shell/Codex Cmd+C should still work.

---

# Dashboard runtime restored with fresh-server recovery — 2026-10-23

Active release **20261023T054130.403606Z-e8aefd8b**, signed commit **3c99050**.
The existing installer restored production monitoring, pager and n/c/Shift+N
bindings. No tmux reload or protected agent/editor restart was needed.

Root cause reproduced before the first session on an empty private server:
the old installer failed at `list-windows`, before it could register recovery.
Tmux reconstruction exposed this startup-order defect; c7142af did not change
those payloads. Bootstrap now runs after theme/navigation setup, registers the
existing session-created hook, and defers session-dependent activation. Later
sessions use watch mode without rebinding keys. No new daemon/monitor type.

**32 focused dashboard/pager tests passed**, including fresh server startup,
server reconstruction, later sessions, idempotence, hook conflicts, forwarding,
attention persistence and notification deduplication. Two old synthetic fixtures
were missing the required pager sequence field; their metadata was corrected.

One disposable remote-resumed CLI produced real working hooks, moving native
crimson title frames, a stopped white dot, and exactly one ntfy `sent` record
(priority 3, one attempt, no replay). **User confirmed iPhone receipt** of
“Turn stopped; review may be needed.” Runtime restoration acceptance is complete.
The owned CLI exited gracefully and its unattached session was removed. All
16 protected process identities, original four windows/seven panes, client focus,
project UUID pins, global hook/trust files, Ghostty and persistent Doom survived.
Existing project agents were not reopened; they may transition naturally.

Only three dashboard startup payloads change. All 13 managed links were verified.
Rollback: `python3 -B scripts/deploy.py rollback --expect-current
20261023T054130.403606Z-e8aefd8b --approve` returns to accepted hook-repair release
**20261023T051907.812473Z-4094d7cb**. Applied journal:
`history/20261023T054131.750899Z-bd85806d.json`. Existing migration backups remain;
no new file migration was needed. See [startup recovery](DASHBOARD-STARTUP.md).
Private evidence: `/private/tmp/df-dashboard-runtime-i0youngf/evidence/`.
Concurrent documentation edits remain preserved and uncommitted.

---

# Remote cdev hook repair deployed; loaded dashboard needs restoration — 2026-10-23

Commit **c7142af**, release **20261023T051907.812473Z-4094d7cb** is active.
Only `cdev/activity.py` and `cdev/codex_session.py` change behavior; all other
payloads match the previous release after normalizing pinned release paths.
The eight hook commands/hashes/trust entries and seven workmux definitions are
unchanged. Exact project UUID pins, persistent Doom and all 15 checked protected
process identities, four windows, seven panes and the client survived.

**45 focused tests passed.** Actual fresh and repeated remote-resumed turns,
two concurrent remote UUIDs on the shared backend, working/stopped states,
pane attribution across private moves/renames/splits and graceful exit passed.
Real transitions reached the existing pager queue; mock transport verified
dedup/restart behavior without extra phone pushes. No new trust decision occurred.
The historical reopened smoke process had exited, so its exact argv was unavailable;
current pluckd used explicit remote resume, and an owned UUID reproduced the defect.

**Remaining live-state discrepancy:** the current production server has no
dashboard/pager monitor, no attention-installed marker, n=new-window, c=new-window
and no Shift+N binding. This rollout made no production binding changes or reload.
The existing strict dashboard preflight passes. Runtime monitor/attention
restoration is left pending inspection/authorization; do not claim live shimmer,
pager or attention acceptance from the isolated real-event tests. Existing agents
also need natural reopening to acquire the new registration; none was restarted.

Rollback (no reload): `python3 -B scripts/deploy.py rollback --expect-current
20261023T051907.812473Z-4094d7cb --approve` returns to
**20261023T042036.839310Z-1711bc49**. Applied activation journal:
`history/20261023T051928.711973Z-e045d465.json`. No new file migration/backup was
necessary. Private evidence: `/private/tmp/df-resume-diagnosis-jnc8e0mx/evidence/`.
All owned test CLIs/private tmux resources were closed; existing documentation
edits remain preserved and uncommitted.

---

# Pager and persistent Doom deployed — 2026-10-23

Active release **20261023T042036.839310Z-1711bc49**, commit **1118c0a**.
Pager commit **d70421d** was independently deployed/accepted first in release
**20261023T041041.629838Z-fb1ae206** and is unchanged in the current release.

Pager: **27 focused checks passed**, one bounded real test accepted by ntfy and
confirmed on the iPhone. It uses the existing validated snapshot, finite detached
workers and private dedup/configuration; no new Codex hooks or persistent service.
The three manually recovered remote agents currently have no valid dashboard
records and remain silent. Real remote-hook delivery is not claimed from the
synthetic lifecycle tests. Topic/credentials remain outside Git, mode 600.

Doom: **27 focused checks passed**, plus actual disposable launchd startup/recovery
and two real terminal clients against the new production server. Native workspace
isolation, project-root SPC f f, normal buffer directories, Org/Evil/theme,
closing a client, retained buffers and reconnecting all passed. Owned test clients,
workspaces, buffers and temporary files were removed. The named server remains
running under **local.dotfiles.doom** (initial server PID 78809, manager 78807).
It starts at user login, independently of Ghostty/tmux, with no crash-restart loop.
Use guarded kickstart to recover a stopped job; stale/unsafe sockets are refused.

Future `cdev PROJECT` windows use `emacsclient -t`; existing project windows are
reused without respawn. The three original standalone Doom/Codex pairs, four
windows/seven panes, original client and all 17 protected process identities
survive. Thirteen managed links and all copied permissions/hashes verified.
UUID pins, the eight stable dashboard definitions, seven global workmux hooks,
Ghostty, tmux bindings, clipboard and unrelated configuration are unchanged.
No production tmux/Ghostty reload or agent/editor replacement occurred.

Migration backups under `~/.local/share/dotfiles-active/backups/`:
- **fish-cdev:** `20261023T042434.411916Z-d119e7a5` — two original regular files,
  contents and modes verified.
- **doom-service:** `20261023T042058.264860Z-1ec72ea9` — original plist absence.
- **doom-client:** `20261023T042057.964241Z-4ea3e8f7` — both helper/addon paths absent.

Independent recovery (POSIX sh/Zsh commands; no recovery executed):
- Disable notifications without touching Doom or keys:
  `python3 -B ~/.local/share/dotfiles-active/current/tmux/pager.py disable --approve`.
- Standalone editor for a future new window:
  `CDEV_EDITOR_MODE=standalone cdev PROJECT`.
- Recover a stopped managed server:
  `python3 -B scripts/doom_service.py kickstart --approve` (never `-k`).
- Full Emacs rollback to the accepted pager release: **stop on any failed guard**.
  Current must still be the active release above; first restore the Fish backup,
  then stop the named server only when its clients are closed/buffers saved,
  restore the two addon/service backups, then roll back the pointer. A refusal
  leaves the daemon/data intact; do not force shutdown or skip a failed step.

```sh
python3 -B scripts/deploy.py restore --backup 20261023T042434.411916Z-d119e7a5 --approve
python3 -B scripts/doom_service.py bootout --approve
python3 -B scripts/deploy.py restore --backup 20261023T042058.264860Z-1ec72ea9 --approve
python3 -B scripts/deploy.py restore --backup 20261023T042057.964241Z-4ea3e8f7 --approve
python3 -B scripts/deploy.py rollback --expect-current 20261023T042036.839310Z-1711bc49 --approve
```

After Emacs adoption, use pager disable for independent notification rollback;
shared-pointer rollback past the pager release would also affect editor files.
See [PAGER.md](PAGER.md), [DOOM-SERVER.md](DOOM-SERVER.md) and WORKFLOW.md for
Terminal.app recovery. Private compact evidence is in
`/private/tmp/df-pager-rollout-conkdu0r/` and
`/private/tmp/df-doom-rollout-li9n0866/`. Previous releases/backups are preserved.
Existing concurrent documentation bodies below remain intact and unstaged.

Both workstreams are complete within observable-source limits. Optional remaining
physical check: appearance and SPC f f in a future new cdev project window.
No further activation is pending. Clipboard/Cmd+C work remains deferred.

Earlier entries below are historical evidence.

---

# Pager deployed; iPhone test passed — 2026-10-23

Commit **d70421d**, active release **20261023T041041.629838Z-fb1ae206**.
The optional publisher consumes the existing validated dashboard snapshot; no new
Codex hooks or persistent service. Approval/review priorities are 4/3, working
and unknown states are silent. Private topic configuration is mode 600 outside
Git. One real transport test was accepted by ntfy and confirmed on the iPhone.
**27 focused regressions passed**, plus deployment/parser/privacy/integrity checks.
All eight managed links, four windows, seven panes, original client and 17 checked
process identities survived. Keys, global hooks, UUID pins and standalone Doom
are unchanged. Only the native dashboard monitor commands were updated; no reload.

Rollback reference: previous immutable release **20261023T034028.602247Z-9d3ec165**.
Private config was previously absent; disabling preserves it and its credentials.
See [PAGER.md](PAGER.md) for disable, pointer rollback and restoring the old monitor.
Private evidence: `/private/tmp/df-pager-rollout-conkdu0r/complete.json`.
The current three manually recovered/shared-server agents have no valid dashboard
records and remain silent. Synthetic lifecycle pipeline tests are not represented
as real remote-hook delivery. Existing source identity checks were not weakened.

Pager transport acceptance is complete; persistent Doom work now proceeds under
the user's consolidated authorization. Existing concurrent doc bodies follow.

---

# cdev exact-session recovery deployed — 2026-10-22

Commit **343faaf** is active in release **20261023T034028.602247Z-9d3ec165**.
Only `cdev/codex_session.py` changes behavior. All 15 copied 0444 payloads and
all eight managed links verified; no Fish candidate, editor integration, hook,
authentication, Ghostty setting or tmux binding changed. No reload was needed.

`resume --last` is removed. The three operator-supplied UUIDs were verified
against saved first-line metadata and bootstrapped into private project pins,
preserving every other mapping. Shared-server ownership was verified read-only:
all three UUIDs are loaded and their writer locks are busy. Installed-helper
plans choose their exact UUIDs and explicit local-socket remote resume. Missing,
ambiguous, wrong-project or unexpectedly owned sessions fail without fallback.

**24 focused regressions passed** (17 cdev identity/reuse/transport/standalone
integration tests, 7 dashboard hook/state tests), plus deployment syntax,
dependency, privacy and integrity checks. No full suite or live-agent relaunch.
Four windows/seven panes, the original client, and all 16 persistent protected
process identities survive. A transient Python inspection child exited. Client
selection changed between read-only samples; cause is unestablished, no focus
command was issued, and the current view was preserved.

Private pins backup (contents and mode verified):
`~/.local/state/cdev/backups/20261023T034226.202049Z-cdev-recovery/pins.json`.
Previous complete code release: `20261023T002013.807639Z-023596db`.
Code rollback, POSIX sh/Zsh, under explicit rollback authority:

```sh
python3 -B scripts/deploy.py rollback --expect-current 20261023T034028.602247Z-9d3ec165 --approve
```

Rollback does not reload applications or undo the separately backed-up private
pin map. Keep the correct pins unless metadata restoration is specifically
needed; preserve concurrent pin updates when restoring. Private verification and
recovery hashes: `/private/tmp/df-cdev-repair-66kya5lx/complete.json` and
`recovery.json`. Existing migration backups and immutable releases are untouched.

Next reboot/relaunch has not been exercised: the protected conversations stayed
running. Remote dashboard hook delivery remains dependent on native invocation
context/ancestry and is not newly claimed; hooks and their safety checks are
unchanged. See [CDEV-RECOVERY.md](CDEV-RECOVERY.md). Routine development guidance
now uses focused tests and honors consolidated approval. Existing concurrent
documentation bodies remain intact. Persistent Doom/LaunchAgent activation is
still deferred; this repair is complete.

Earlier entries below are historical evidence, retained verbatim.

---

# Dashboard milestone accepted and closed — 2026-10-22

**Physical acceptance PASS, reported by the user:** Ctrl+F n cycles both test
agents, both attention dots persist, and the user returned to main.
Active release remains **20261023T002013.807639Z-023596db**, source **9a861dc**.
The 95 accepted regressions, real 111-minute Stop persistence, nine automated
attention cycles, concurrent actual lifecycle events and keyboard acceptance now
complete this dashboard milestone. Persistent Doom remains a separate milestone.

The already-authorized cleanup completed with fresh session creation, pane,
process start, ancestry and descendant checks. Exact session `$1`,
`df-dashboard-review-618a6bc8`, was removed. Both native Codex test CLIs exited via
/quit with status 0; their launchers and owned code-mode helper also exited. The
existing remain-on-exit policy retained dead test panes, which were verified as
successful exits and removed with the exact session. Two accidental shell splits
and their processes were already absent; their disappearance is not attributed.
Only the remaining two inert sleeps and idle shell were removed with the session.
No owned test process or stale review attention remains.

Client 12520 on /dev/ttys014 was redirected from review to main after rechecking
its identity. Both clients survived. Main retains four windows/seven panes; all
12 original core identities and 17 distinct checked production/application/client
identities survive. Client redirection and session removal preserved main's view.
A separate between-phase @5 -> @10 selection change was preserved as unattributed;
no main selection command was issued and no focus reversal was attempted.

All eight managed links, current pointer, global hooks/workmux settings, accepted
manual Fish function, standalone Doom and clipboard configuration are unchanged.
Cleanup performed no reload, deployment, rollback, service operation, new commit
or push. Diagnostic roots and private evidence are preserved, including
`/private/tmp/df-attention-rollout-a506fio9/CLOSEOUT.json` and cleanup evidence at
`/private/tmp/df-attention-rollout-a506fio9/cleanup-dyryohik/`.
See [ATTENTION-ROLLOUT.md](ATTENTION-ROLLOUT.md) for operations and recovery.

**No dashboard acceptance or cleanup action remains.** The separate staging-guard
and legacy-benchmark follow-ups remain documented; no new implementation or
persistent-Emacs activation is implied. Existing concurrent documentation bodies
remain intact and unstaged.

Earlier entries below are historical evidence, retained verbatim.

---

# Attention repair deployed — final keyboard check pending — 2026-10-22

Active release: **20261023T002013.807639Z-023596db**, source **9a861dc**.
All 15 independent 0444 payloads verified; only the two intended dashboard files
change behavior. Eight managed paths now resolve through the new current pointer;
previous releases/backups are preserved. Exactly one controlled tmux reload passed
with no errors/warnings, unexpected binding/hook/plugin change or resource loss.

Both original actual Stop records remained actionable at **6,680 seconds old**
(over 111 minutes), without record/clock edits. Nine installed-n callback cycles
passed across existing splits and owned window swap/renumber/title changes;
visits left the records byte-identical. Test order/title were restored. Main
focus and all original sessions/windows/panes/clients/protected identities survived.
Fresh actual events passed: concurrent working shimmer (three native frames each),
stopped white dots, genuine permission-request red alert, cancelled request,
interrupt clearing and recovery to stopped. Workmux metadata and independent pane
attribution matched; all eight dashboard plus seven workmux definitions remain
trusted, enabled and unchanged. No automatic hook trust or approval occurred.

The Fish drift was the user-confirmed manual passme function. Its addition alone
reconstructs the previous hash when removed in memory. Syntax passed; no startup
event is registered. The file is preserved. No Fish/Doom/clipboard/service migration,
Ghostty reload, authentication change, new commit or push occurred. The accepted
95 regressions still match this unchanged commit; deployment checks were rerun.

**Next single action:** physical Ctrl+F n acceptance in review session $1, then
already-authorized controlled cleanup after the user reports success. Both actual
test agents remain stopped with dots. No additional reload or 15-minute wait is
required. Review session/resources are preserved; cleanup has not occurred.
See [ATTENTION-ROLLOUT.md](ATTENTION-ROLLOUT.md) for exact keys, evidence,
rollback/disable commands and the identity-checked cleanup sequence. Existing
concurrent documentation bodies remain intact; the two earlier separate
follow-ups (staging guard and legacy benchmark timing) remain deferred.

Earlier entries below are historical evidence, retained verbatim.

---

# Attention repair rollout stopped before staging — 2026-10-22

The user approved staging/activation/reload of 9a861dc, real and physical
acceptance, then controlled cleanup. Essential preflight found unexpected live
Fish startup drift and stopped before all production mutation. HEAD and intended
source/manifest are correct; only the two intended dashboard payloads differ
from the active release. The eight managed links, prior release integrity,
references/dependencies/parsers, four backup contents/modes, deployment journal
and all 12 original protected process identities passed their checks.

`~/.config/fish/config.fish` differs from the previously verified baseline:
- Previous SHA-256: `25bae14c2b6521d5d96bcc7e4257c5bd875070a59acb0ab4411cfb6075fcf92d`
- Current SHA-256: `e09f7e85b4683a41ce2a7add4f58722626b6dde7c60081cc8b9faebc6a80c7d5`
- Current modification: 2026-10-22T20:10:00.593899-04:00

No cause or authorization for that edit was established. The file was neither
changed nor reverted by this task. Because Fish is the tmux default shell, its
startup contents can affect reload-time commands; do not silently accept it as
the previously reviewed reload environment. Fresh native hook metadata checks
were not reached; global hook/config bytes otherwise match the prior baseline.

Current remains `releases/20261022T215047.249499Z-618a6bc8`. No new release,
backup, pointer change, application reload, attention invocation, agent prompt,
process termination, session cleanup, commit or push occurred. The review session
and its agents remain available. The already passed 95 regressions remain the
repository repair evidence; they were not needlessly repeated during this check.

Private evidence: `/private/tmp/df-attention-rollout-a506fio9/`, particularly
`preflight-file-drift.json` and `preflight-stopped.json`. Existing documentation
bodies are preserved. Next action: establish whether this Fish edit is expected
and review its relevant startup effects before resuming the approved sequence.
Persistent Doom and unrelated work remain deferred.

Earlier entries below are retained verbatim.

---

# Stopped-attention expiry defect — repository repair only — 2026-10-22

Physical dashboard visuals and existing shortcuts passed per the user; attention
navigation remains unresolved in production. Read-only diagnosis found both test
agents alive with unchanged Stop records, but the blanket 15-minute lease expired
them at 18:47:31 EDT. The loaded n binding is correct; its queue is empty. Main's
queue is session-local and cannot navigate agents in the separate review session.

Repository fix preserves stopped attention while its launch identity remains
valid; new lifecycle/terminal events clear it. Merely visiting does not acknowledge
it. Working/waiting retain the 15-minute silence timeout. Reader, native monitor
and title expiry agree. **5 focused and 95 complete regressions passed**. No new
Codex hook definitions, launcher changes or per-animation processes are added.
Repair commit: **9a861dc** (local, SSH signature attached); only source/tests and
the new diagnosis document were committed. Preexisting concurrent doc edits stay
unstaged. Signature verification requires the currently unconfigured
gpg.ssh.allowedSignersFile; no Git configuration was changed to supply one.

Production remains 20261022T215047.249499Z-618a6bc8. All eight links, global hook
bytes and all 12 protected identities are intact. No production focus, reload,
configuration or cleanup command was issued. Main selection changed @10 -> @5
between read-only samples; its cause remains unestablished and unattributed.

Diagnostics are preserved privately. Review session $1 still holds four windows
and seven panes: two test agents, two inert stubs and three idle shells (including
the two accidental splits). A client is still attached. Exact identities and the
proposed gated cleanup are in [ATTENTION-DIAGNOSIS.md](ATTENTION-DIAGNOSIS.md).
No cleanup or deployment is authorized by this repair. Existing concurrent docs
are preserved. Next boundary: review this candidate, then separately authorize
staging/activation/reload or exact fixture cleanup as desired.

Earlier entries below remain historical evidence.

---

# Phase 4 production rollout passed — physical acceptance pending — 2026-10-22

**Dashboard active; automated acceptance passed.** Implementation remains e38e18d.
current -> releases/20261022T215047.249499Z-618a6bc8. The two cdev helper paths
are managed; backup **20261022T215153.419622Z-a559508a** and all eight live links
were verified. Existing releases and concurrent documentation were preserved.
No Fish/Doom/service migration or clipboard configuration change occurred.

All eight dashboard definitions now remain trusted, with identical native hashes,
across review-CLI exit, a fresh ordinary cdev launch, project reuse/resume,
concurrent threads and final inspection. No review prompt recurred after the
remaining three were trusted. The earlier partial-trust cause remains unknown;
automation wrote no trust state. All seven workmux definitions/trust are unchanged.

Actual production-profile OpenAI events passed: working shimmer, stopped white
dot, genuine permission-request red alert, independent concurrent attribution
and matching workmux session/pane metadata. The request was cancelled without
approval; the agent remained usable. Normal exit retired its record; abrupt owned
pane closure during actual work cleared its label in **0.359s**. Orphaned cache
is rejected rather than deleted. No synthetic lifecycle event substitutes for
this evidence.

Exactly **one** production tmux reload completed, with no reported errors.
Ctrl+F n now cycles stopped/waiting agents in the current session. c still creates
in the pane directory, Shift+N remains next-window, and Ghostty Cmd+Shift+N still
forwards c. Other bindings/theme are preserved; the popup helper is repinned to
the new release. Four owned attention cycles passed, and idle/working-only queues
preserved focus. Native animation showed four frames from one unchanged cached
format/sequence, with zero per-animation-tick processes.

The original session, four windows, seven panes, client, three Codex CLIs and
12 protected application processes survived. Every pre-reload process/client
survived the reload; original focus stayed fixed throughout these successful
checks. The earlier @10 -> @2 change remains **unattributed**, not assigned to the
user. The owned review session adds three windows/four panes and a client, for
current totals of 2 sessions, 7 windows, 11 panes and 2 clients. Its agents %26/%27
are stopped and retained for physical checks; its editor is inert.

**90 full regressions passed (54.814s)** before rollout; the isolated bounded-disable
regression passed again (0.399s). Fresh private renderer timings: working 0.4875ms
and idle 0.0185ms per 24-character expansion; 20-idle-window monitor 0.2417ms.
These are format wall-time bounds, not system-wide CPU/redraw measurements.
Final release, backup, trust, files, protected identities and strict parser checks
passed. Source/test/deployment/validation files still match e38e18d; no commit/push
or automatic rollback was made.

Next single action: physical Ghostty acceptance using the owned review session.
See [DASHBOARD-ACCEPTANCE.md](DASHBOARD-ACCEPTANCE.md) for precise evidence,
active keys, retained fixture identities, physical checklist and recovery commands.
Ctrl+F then ) cycles sessions; Ctrl+F then n should cycle its two stopped agents.
Persistent Doom remains deferred until a subsequent approved milestone.

Recovery correction: use the existing dashboard disable command and verify n/c;
**do not follow it with a full reload**, which explicitly sets the feature on.
No recovery was needed/executed. Helper restoration removes the adapter path;
preserve any instrumented user-owned clients before considering that operation.
Separate follow-ups remain: commit-keyed idempotent staging guard, and updating
the legacy benchmark's retired hook-CLI timing section. Neither changes this
verified immutable release or authorizes another deployment.

All earlier entries below are historical evidence retained verbatim.

---

# Phase 4 paused — three native hooks still untrusted — 2026-10-22

The user reported explicitly trusting all eight production sessionFlags hooks,
preserving workmux, and authorized continuation. Fresh read-only native metadata
still reports **UserPromptSubmit, Stop and Interrupt untrusted**; the other five
are trusted. All eight keys/commands/currentHash values are unchanged from the
review manifest. The seven existing workmux handlers remain enabled/trusted and
unchanged. No cause for the incomplete persisted trust has been established.

Stopped at the mandatory native trust gate without sending any actual test
prompt, changing trust, reloading production or enabling attention. Active release
remains 20261022T215047.249499Z-618a6bc8; the verified two-helper migration and
backup 20261022T215153.419622Z-a559508a remain intact. Pending native review is
not a failed-delivery gate and does not trigger helper restoration. Both n/c
still create windows; standalone Doom/Fish, global hooks and workmux are intact.
All original four windows/seven panes, the original client and 12 protected
processes survived; the user added a review client. The @10 -> @2 focus change
remains unattributed. The user cannot establish its cause; do not attribute it
to their actions or silently restore focus.

Next: user native inspection of the three exact entries in
[PRODUCTION-HOOK-REVIEW.md](PRODUCTION-HOOK-REVIEW.md), then fresh metadata must
confirm all eight trusted before real event/concurrency/workmux acceptance and
the gated reload can continue under the existing authorization. None of those
remaining production acceptance checks is claimed to have passed in this turn.
Persistent Doom remains deferred. Existing concurrent documentation is preserved.

---

# Approved Phase 4 — helpers adopted; native review pending — 2026-10-22

Active release is now **20261022T215047.249499Z-618a6bc8**, independently verified
against repair e38e18d. The complete 15-file release passed syntax/dependency,
privacy, mode and commit-content checks. All six previously managed Ghostty/tmux
payloads are equivalent after release-path rendering; Ghostty is byte-identical.
The only changed payload sources are the two cdev helpers. Existing immutable
releases and concurrent repository documentation are preserved.

Authorized activate and cdev-only migrate completed. Backup
**20261022T215153.419622Z-a559508a** preserves the original regular 0644 launcher
and activity.py's prior absence; all eight managed links, resolved bytes/modes,
backup metadata and completed journal passed verification. The live standalone
Fish function/emacs -nw environment is unchanged. No Emacs/client service,
global hook edit, production reload or attention activation occurred. Both
Ctrl+F n/c still create windows; Cmd+Shift+N still forwards to c.

**90/90 full regressions passed in 54.814s.** The exact private two-helper
restoration rehearsal also passed, including contents/mode/mtime, prior absence,
unchanged current pointer and repeat restoration. All original four windows,
seven panes, attached client, three Codex agents and 12 protected processes
survived. Loaded bindings/options/original hooks/monitors are unchanged. Main's
selected window was observed changing @10 -> @2; the cause is unproven and no
focus restoration was attempted. Reconcile that observation before proceeding.

The owned production-profile review session is df-dashboard-review-618a6bc8,
Codex pane %20, window @12. Its CLI is at the native Folder access trust screen
for the inspected empty test Git project, before hook review. No model prompt,
folder trust choice or hook trust choice has been sent. Exactly eight native
sessionFlags definitions match the inspected production-command hashes and are
untrusted; all seven preexisting global workmux hooks remain trusted/unchanged.
The observer safely remains idle/unlabelled. The original client is unaffected;
the review session adds only two owned windows/three panes.

Next human action: attach from Terminal.app, review the owned folder, then use
/hooks to personally inspect/trust only the eight exact entries in
[PRODUCTION-HOOK-REVIEW.md](PRODUCTION-HOOK-REVIEW.md). Stop if anything differs.
After the user reports review completion, continue the existing consolidated
authorization through real production delivery/coexistence gates, then the one
gated reload; do not enable attention while those gates are pending. Bounded
helper restoration command and evidence are in that document. Persistent Doom
and commit-keyed idempotent staging remain separate follow-ups.

All previous documentation content is retained below as historical evidence.

---

# Isolated real hook acceptance passed — 2026-10-22

The user completed native review of exactly the eight inspected lifecycle hooks.
Real OpenAI-backed Codex 0.163.0 turns through the unchanged standalone cdev
function passed working, stopped and genuine PermissionRequest delivery in two
disposable panes. Both concurrent sessions retained distinct session/turn and
process identities across private window swapping/renumbering/title changes.
All eight native hashes stayed fixed and trusted; the second ordinary launch
completed a real turn without repeated review. Automation sent no trust or tool
approval choices. Normal exit retired the record; abrupt pane closure during a
real working turn cleared its label in 0.468s. Retained orphan cache is ignored,
not deleted. See [HOOK-ACCEPTANCE.md](HOOK-ACCEPTANCE.md) for evidence and limits.

Fresh activity/cdev regressions: **19/19 passed in 20.011s**. The prior full
**90/90** suite remains applicable: implementation/tests/validation still match
e38e18d exactly, and no code fix or new commit was needed. Installed workmux
commands passed isolated compatibility checks; global seven-hook files/trust
were unchanged. Combined actual global-workmux/cdev delivery still needs the
future approved production smoke test.

Production comparison passed for all recorded session/window/pane/client,
protected-process, loaded binding/hook/monitor and bounded file identities:
1 session, 4 windows, 7 panes, 1 client, 3 Codex CLIs. current still points to
releases/20261022T163617.469413Z-497daec6; n/c compatibility remains active and
attention remains off. No deployment, production reload, global hook edit,
Fish/Doom adoption or service activation occurred. The owned private server and
agents were closed; owner-only evidence/profile remains at
/private/tmp/df-hook-acceptance-zcc5ujfz. Its old attach instructions below are
historical and no longer apply.

Next: review the [revised consolidated Phase 4 proposal](DASHBOARD-PHASE4.md).
It requires renewed authorization, a new immutable release, helper-only backup
and adoption, **separate production native user hook review**, real production
delivery checks, then one gated tmux reload and physical acceptance. No operation
follows automatically. Persistent Doom stays deferred; commit-keyed idempotent
staging remains a separate follow-up. Existing concurrent docs are retained
unchanged below; earlier pending statements are historical.

---

# Isolated hook acceptance — awaiting native sign-in/review — 2026-10-22

The user authorized disposable real-CLI acceptance of e38e18d. HEAD and all
candidate implementation/validation files still match that commit. No production
migration, reload, hook install, trust edit or attention activation was performed.
The intervening repeated Phase 3A request was not executed.

An owner-only fixture is retained at /private/tmp/df-hook-acceptance-zcc5ujfz.
Its empty-config tmux socket is /private/tmp/df-hook-acceptance-zcc5ujfz/tmux.sock,
session hook-review, Codex pane %2. It runs the unchanged standalone Fish function
against independent read-only copies of the repaired helpers, with an inert
editor. Native definitions were inspected twice with hooks/list: exactly eight
sessionFlags entries, identical hashes, fixed adapter command, timeout 2,
non-managed/untrusted, no dynamic identity arguments. Full keys/hashes/targets
and the adapter/dependency checksums are in HOOKS-TO-REVIEW.md,
native-hooks-before-review.json and dependencies.json in that fixture.

The profile uses the normal OpenAI provider; production authentication was not
read or copied. The actual native CLI is waiting at Sign in with ChatGPT before
it can reach hook review. No trust choice or model prompt has been sent. The
user must sign in inside this isolated profile, open Review hooks or /hooks,
compare the eight intended definitions, and personally trust only those entries.
If any displayed definition differs, stop. This trust belongs only to the test
profile; production will require its own review after approved adoption.

Actual lifecycle delivery, repeated-launch trust reuse, concurrent attribution
and termination acceptance remain pending; native hash discovery is not event
coverage. The previous full 90-test regression pass remains applicable because
candidate code/tests are unchanged. This step added only disposable test resources
and this status entry. Two temporary harness bookkeeping issues (binding-key
lookup and -N on initial server creation) were fixed before any Codex turn;
neither is treated as lifecycle evidence.

Production comparison passed for sessions, windows, panes, clients, server,
loaded options/bindings/hooks, protected process identities, all bounded live
configuration/deployment files, and the seven global workmux definitions. Active
release remains 20261022T163617.469413Z-497daec6; production n/c compatibility stays
intact. All previous documentation content is preserved below.

Attach from Terminal.app with:

```sh
/bin/sh /private/tmp/df-hook-acceptance-zcc5ujfz/attach.sh
```

Leave the private CLI at its normal prompt after reviewing, and report completion
so actual-turn tests can continue. Do not deploy or resume the production rollout.
Only this owned private server/profile may be used for acceptance testing.

---

# Hook-registration repair candidate — 2026-10-22

**Repository repair tested; actual Codex hook delivery remains a user-review
gate. No live changes are authorized or performed by this milestone.** See
[HOOK-REGISTRATION.md](HOOK-REGISTRATION.md) for evidence, the runtime protocol,
failure behavior and the exact one-time native review procedure. It supersedes
the older nonce-in-command bridge and rollout instructions below.

- Codex 0.163.0's own hooks/list API confirms that changing only the original
  launch nonce changes all eight definition hashes. The eight new entries are
  SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, PostToolUse,
  Stop, Interrupt and SessionEnd, from sessionFlags rather than the workmux file.
- Repaired definitions contain only a fixed /usr/bin/python3 invocation of the
  installed lexical activity.py path and event action. Distinct runtime nonces,
  panes, sockets and state locations now produce identical native currentHash
  values and source keys. Tests preserve all seven workmux keys/hashes. No
  trusted_hash is written, and all new native definitions remain untrusted.
- Private runtime JSON is passed in the child environment. The adapter verifies
  the registered Codex child and launcher as live same-user ancestors, process
  start identities, nonce, server boot and stable pane ID before binding the
  documented session/turn IDs. It does not select by cwd or inherited TMUX.
  Records/locks are 0600 under 0700 state; symlinks, unsafe permissions, stale
  identities and unrelated process origins fail closed. Missing/failed hooks
  leave the CLI usable and unlabelled; owned child termination clears evidence.
- **90/90 full regressions passed in 53.806s** with
  `python3 -B scripts/test.py --integration`. Native discovery/hash checks are
  real Codex RPC calls; event dispatch is explicitly synthetic, through actual
  owned process trees and private sockets. Tests cover two same-cwd agents,
  cross-pane context rejection, window movement, stale/ended sessions, cleanup,
  failure/lock contention, existing renderer/keys, workmux, standalone cdev
  reuse/compiler handling, isolated Doom clients and deployment recovery.
  `python3 -B scripts/deploy.py check` also passed. Two fixture assumptions found
  during the first full run were corrected: wait for the finalizer's marker
  write, and dispatch the Doom integration's synthetic events inside its agent
  ancestry. No production workaround or renderer change was needed.
- Actual hook-subprocess environment propagation, repeated native trust reuse,
  real working/stopped/approval delivery and shared-app-server behavior are not
  established by those tests. A shared server outside the registered ancestry
  is deliberately rejected. No --no-daemon switch or other Codex behavior change
  is introduced to hide that limitation. Real delivery after user review is
  mandatory before a new rollout proposal or attention activation.

Production remains recovered Phase 3B on
releases/20261022T163617.469413Z-497daec6. No release was staged or modified;
current, live files, global hooks/trust, workmux and loaded n/c compatibility
bindings are outside this patch. Standalone emacs -nw remains live; persistent
Doom/LaunchAgent activation is still deferred. The existing cdev backup
20261022T191900.472358Z-230b25df remains restored. The separate commit-keyed,
idempotent staging improvement remains a follow-up.

Only the two existing cdev payloads require a future new release. New test
fixtures and documentation are repository files. Preserve prior concurrent
documentation/audit edits; this entry is additive and does not deploy anything.
Next: explicit user review of the fixed native definitions in an isolated proof,
then actual ordinary-cdev delivery verification. Do not resume Phase 4.

---

# Phase 4 — blocked at real hook delivery; safely recovered — 2026-10-22

**BLOCKED; dashboard rollout is not complete.** The user's consolidated Phase 4
authorization covered helper adoption, real lifecycle verification, one production
tmux reload only after that gate, and bounded recovery. The actual interactive
Codex test stopped at its hook-trust review before a turn could run. No production
tmux reload or attention activation was attempted. The adopted helpers were
restored under the authorized recovery procedure; no further live work follows
from this record.

Observed production state after recovery:

- current remains releases/20261022T163617.469413Z-497daec6; the immutable 15-file
  payload/receipt and pointer metadata are unchanged. The five tmux links and
  Ghostty link still resolve to that release. There is no pending recovery.
- Phase 3B's Ghostty reload and keyboard checks passed according to the user.
  Ghostty forwards Cmd+Shift+N through Ctrl+F c. Loaded tmux n and c both create
  in the current directory, Shift+N selects the next window, prefix is Ctrl+F,
  and @dotfiles-attention-installed remains off. The display renderer/theme and
  existing workmux/pane/numeric/reordering bindings remain as loaded in Phase 2.
- All original identities survived: one session, four windows, seven panes,
  one attached client, three standalone Doom pane processes and three Codex CLI
  processes, plus Ghostty and the recorded application processes. No original
  production window was reordered, closed or used as a disposable test subject.
- Fish cdev/cdev-pin, their standalone emacs -nw behavior and
  MACOSX_DEPLOYMENT_TARGET=27.0 handling remain byte-identical. No emacsclient,
  Doom daemon, LaunchAgent, global Codex hook/trust/policy or workmux configuration
  was activated or changed. No production Ghostty reload was performed by this
  attempt, and no existing conversation was restarted.

The narrow dashboard-only adoption path was verified: the existing live Fish
function already invokes ~/.config/cdev/codex_session.py. It did not need the
candidate Fish launcher that defaults to the deferred Emacs client. The approved
existing-tool operation was:

```sh
python3 -B scripts/deploy.py migrate --release 20261022T163617.469413Z-497daec6 --component cdev --approve
```

It temporarily adopted only ~/.config/cdev/codex_session.py and activity.py.
Backup **20261022T191900.472358Z-230b25df** preserves the original regular mode-0644
helper and records activity.py's prior absence. Its original-helper SHA-256 is
ac424056da4dff15ca27ef4326a2ded94772e9182bc9e2319d6146366ae4d4b7.
After the delivery gate failed, this exact authorized recovery completed:

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py restore --backup 20261022T191900.472358Z-230b25df --approve
```

The journal is now restored. Original helper contents/mode/mtime and activity.py's
absence were verified. The pointer, Ghostty, tmux and unrelated files were not
rolled back. Original tmux backup 20261022T040111.754783Z-a455ecd7 and Ghostty backup
20261022T183526.100129Z-0188b037 remain intact and migrated.

Verification results:

- **74 regressions passed in 23.459s**: python3 -B scripts/test.py --integration
  with test_activity.*, test_cdev.*, test_dashboard.*, test_terminal.* and
  test_deploy.* patterns. These cover the native animation/rendering, concurrent
  synthetic transitions, stale/termination handling, attention/empty-queue
  navigation, real installed workmux on a plain private pane, key forwarding,
  popup/reordering behavior and transaction/recovery failures.
- A separate **13-check private fixture passed** with the unchanged live Fish
  function and candidate symlinked helpers: standalone editor/compiler arguments,
  two project/pane identities and nonces, layout, reuse without duplicate agents,
  eight invocation-local hooks per agent and no release bytecode writes. Its
  editor and agent were inert stand-ins; this did not prove real hook delivery.
- The real installed Codex CLI was then run through that unchanged cdev function
  in owned private tmux contexts. A harmless exec --ephemeral test returned exit 0
  with actual thread.started, turn.started, item.completed and turn.completed
  events, but the advisory cache stayed idle with null session/turn and sequence 0.
  This was not accepted as lifecycle coverage. A temporary recorder was corrected
  before the repeated probe; no deployed code or security setting was changed.
- The actual ordinary interactive CLI then displayed **Hooks need review** and
  **8 hooks are new or changed**, with review/trust/continue-without-trusting
  choices. The model turn had not begun. No trust choice or bypass was used;
  no usable lifecycle evidence reached the observer. Only the owned test CLI,
  terminal client and private server were closed afterward.
- Recovery was behavior-tested in another owned inert context: standalone
  launch/compiler environment, window reuse with no duplicate agent, no injected
  hook flags and no observer marker all passed. Final production comparison
  preserved original processes, sessions, loaded options/bindings/hooks and
  inspected configuration/release/history contents.

The bridge pins socket, pane and a fresh launch nonce inside each invocation-local
hook command. Codex's documented trust is tied to the exact hook-definition hash:
[official hook review contract](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).
Because those commands change per launch, repeated review is a design concern,
not something the passing simulated-event tests resolve. The observed interactive
trust prompt is the concrete blocker; future-launch repetition was not tested
by trusting hooks. Real approval/input classification and real working/stopped
rendering remain unaccepted. No successful lifecycle coverage or task success
is inferred from synthetic states or a stopped turn.

Next action: review a supported hook-registration/trust design that retains
per-pane isolation and existing security/global-hook behavior, then validate it
with an ordinary interactive Codex turn before considering attention activation.
Do not mutate the current release, change current, auto-trust hooks, or use a
trust/sandbox bypass. Any new deployment or additional live policy scope needs
its own concrete review. Persistent Doom/Emacs remains deferred. The separate
commit-keyed/idempotent staging follow-up remains outstanding.

Detailed owned test/recovery evidence for this attempt is in
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/df-dashboard-phase4-mreype4h/;
temporary artifacts may expire, so the verified findings above are retained here.
This status entry preserves the entire preexisting document below and does not
commit or overwrite the unrelated concurrent documentation edits. HEAD remains
8dad372; no commit or push was made.

---

# Inactive 8dad372 release staging — 2026-10-22

**TESTED for inactive staging only. No activation, migration, reload or service
operation was performed.** Baseline HEAD was the exact clean commit
`8dad3727d022bdf59a8668feb53eb404e07b48c8`; it supersedes 17c6f99 for rollout.
Production remains `commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16`.

Staged independent complete release:

```text
/Users/czuba/.local/share/dotfiles-active/releases/20261022T163617.469413Z-497daec6
```

The unchanged checked-in `scripts/deploy.py stage --approve` created that unique
ID. All 15 payloads match the intended commit after exact @RELEASE@/@HOME@
rendering; the manifest matches the committed blob. All payloads and release.json
are regular mode-444 copies with independent inodes and one hard link. All 18
declared dependencies and three empty/absent Ghostty override guards passed.
The 15 payloads cleared the existing heuristic secret patterns and targeted
private-context checks; this is not an exhaustive secret-scanning guarantee.

`python3.12 -B scripts/deploy.py check` passed all 14 local checks. Python AST,
Fish no-config syntax, Elisp read/check-parens without evaluation, plist structure,
Ghostty syntax, private empty-server tmux parsing, sh syntax and less-version
checks ran. No user plugin/startup code or production Emacs service was executed.
`python3.12 -B scripts/test.py --integration --match 'test_deploy.*' --match
 'test_terminal.*' --match 'test_dashboard.*'` passed **63 tests in 10.056s**.
These include deployment/restore guards, shimmer output and the real Ghostty
parser → private tmux PTY forwarding bridge. Physical GUI input is separate.

Safe repeat staging was tested with the unchanged real tool in a temporary
state root: two distinct complete releases matched all 30 rendered commit blobs;
the first release's contents/modes/metadata remained identical. This is
**non-overwrite behavior, not idempotent reuse**. Commit-keyed/exclusive staging
remains a separate tooling follow-up. Production was staged only once, then
verified repeatedly without changes. No temporary tooling patch or monkeypatch
was used. Exact commit linkage is retained separately, without rewriting its
immutable release receipt:

```text
~/.local/share/dotfiles-active/staging-evidence/commit-8dad3727d022bdf59a8668feb53eb404e07b48c8.json
~/.local/share/dotfiles-active/staging-evidence/audit-8dad3727d022bdf59a8668feb53eb404e07b48c8/
```

Before/after comparison preserves all inspected live paths, the ec518f0 payload
and receipt, original backup/history, current symlink metadata, server/session/
window/pane identities and root PIDs, loaded bindings/global hooks, and all eight
recorded protected application process IDs/start times. Active window focus
changed from @7 to @5 during observation; no production focus command was issued,
no cause is inferred, and no corrective focus change was attempted. No working
window/pane was created, reordered, killed or used as a disposable test subject.
The first audit-recorder attempt incorrectly treated current's directory symlink
as a file; the read-only recorder was corrected before staging. No deployment
tool or live configuration repair was involved.

The staged dashboard's read-only `preflight --display-only` passes against
`/private/tmp/tmux-501/default`. Strict preflight correctly stops at the missing
Ghostty companion. The candidate differs from live Ghostty by **exactly one line**:
Cmd+Shift+N forwards Ctrl+F c instead of Ctrl+F n. Installed Ghostty 1.3.1's bundled
`ghostty.1.md` (+edit-config, lines 185–190) explicitly says automatic config reload
is not supported and a manual reload is needed. GUI behavior across a symlink
replacement was not physically tested; keep the safe n/c bridge regardless.

**Acceptance limit:** current live cdev has no CDEV_DASHBOARD option and its helper
has no activity-bridge import. Existing agents without fresh evidence must remain
unlabelled. Dashboard-only activation cannot prove real Codex lifecycle/trust in
ordinary cdev launches. That needs a later separately approved launcher/event
adapter adoption, with standalone editor mode if persistent Doom is deferred.
No live Fish, Doom, Codex hooks, workmux or LaunchAgent was changed here.

Next single action: request approval for **display-only activation** of the exact
staged release, followed by a separately authorized first tmux reload. Retain n
creation until Ghostty migration, explicit GUI reload and physical forwarding
acceptance pass; only a separately approved second tmux reload enables attention.
The concrete sequence and independent reversals are in MILESTONE-DEPLOYMENT.md.
Only continuity/rollout documentation is updated after staging; no Git commit or
push is authorized or performed.

---

# Current state and next action

## Final shimmer and key compatibility refinement — 2026-10-22

Baseline: clean HEAD 17c6f99. This bounded follow-up changes the working-title
renderer, offline preview, related tests/cheatsheet and documentation only.
The broader Emacs/event-tracking implementation below remains intact. No release
was staged; the only deployment release is still ec518f0. No 17c6f99 release was
found, and existing ec518f0 files/receipt/backup/pointer were preserved unchanged.

Fresh read-only observation confirms Ghostty's effective configured Cmd+Shift+N
text route is Ctrl+F n; the running tmux n creates in the pane directory, c is
standard creation, N is unbound, and Tab runs workmux last-agent. The companion
Ctrl+F c mapping and safe legacy-mode bridge from 17c6f99 are retained, with no
additional binding or routing change. Physical GUI delivery remains unverified.

Working now shows a connected band of at most three characters moving right
one step per second through dark-steel text. The red leading edge, blood-red
reflection and dark-crimson wake leave the right edge before the next pass.
The shared preview/renderer palette and every phase are tested; all foreground/
background pairs exceed 4.5:1. Stopped white dot, approval white ! on red,
untracked/idle appearance, event evidence and Dotbar ownership remain unchanged.
See ACTIVITY.md for exact colors and the updated preview.

**37 relevant regressions passed in 32.780s**, using:

```sh
python3 -B scripts/test.py --integration --match 'test_activity.*' --match 'test_cdev.*' --match 'test_dashboard.*' --match 'test_terminal.*' --match '*test_real_cdev_layout_dashboard_and_client_pane_close'
```

The new Ghostty-parser → serialized text bytes → attached private tmux PTY test
proves window creation throughout the coordinated bridge, then n attention,
c creation, N navigation, Cmd+1–9, pane navigation and window reordering/focus.
All protected bindings, including workmux/popup, compare unchanged. Existing
concurrent/stale/termination tests and combined real Doom-client/cdev test pass.
No production session served as a disposable test subject. Initial test-fixture
failures were corrected: +show-config needs private HOME/XDG, not --config-file;
the synthetic agent must use cdev's /usr/bin/python3 identity. No live fix occurred.
The prior complete 79-test result below remains evidence for unchanged work.

Paired private benchmark: 24-character working expansion 0.4803 ms versus
17c6f99's 0.3305 ms; the richer band adds 0.1498 ms. Idle expansion 0.0178 ms,
20-idle-window monitor 0.2386 ms, three-agent refresh 53.94 ms. Native 1Hz and zero
processes per animation step are preserved. This is local wall time, not live
GUI CPU/redraw acceptance.

Final comparison confirms unchanged live Ghostty/tmux files and complete
deployment metadata/content; unchanged tmux server/session/window/seven-pane
identities/root PIDs, prefix, all bindings and hooks. No application was reloaded,
no active window moved and no service/global hook/workmux configuration changed.
Final staged review passed: 10 files cleared the heuristic secret/path and
whitespace checks, all staged blobs matched reviewed working files, and all six
relative documentation links resolved. The authorized local commit deploys
nothing and is not pushed.

The coordinated rollout in MILESTONE-DEPLOYMENT.md is still mandatory: new
inactive release → legacy tmux bridge → companion Ghostty migration/reload and
physical verification → explicit second tmux reload enabling n. Until then n
creates windows. Physical shimmer/keyboard delivery and real Codex hooks/trust
remain acceptance gates. Rollback restores original forwarding before c's default.
The commit-keyed/idempotent staging-tool improvement remains a separate follow-up.

Next single action: review the committed refinement and separately approve
inactive staging of that exact new commit and the unchanged 15-file manifest.
No activation, migration, reload or service action is authorized by this record.

## Broader milestone record — 17c6f99

**2026-10-22 — activity dashboard + persistent Doom development milestone.**
Production remains ec518f0. The user reports that all original physical tmux
acceptance tests passed: popup appearance/navigation, window movement and
boundaries, focus preservation, Cmd+1–9 and pane shortcuts. This is user-reported
acceptance, distinct from the earlier agent reload/migration evidence below.

The new milestone is implemented in the development repository only. **No new
release has been staged or activated; no live configuration, global hooks,
workmux settings or application/service has been changed or reloaded.** Existing
standalone editors and Codex conversations have not been replaced. No persistent
LaunchAgent was installed, bootstrapped, enabled or restarted.

## Implemented and verified in isolation

- Imported cdev/cdev-pin Fish functions and the existing conversation-selection
  helper. Fresh/project-scoped --last/UUID-pin policy, naming, collision guards,
  concurrent reuse and no duplicate-agent behavior remain covered. Failed new
  panes stay visible rather than being killed or retried as fresh conversations.
- Added advisory invocation-local Codex hooks pinned to actual socket/pane/launch
  identity, a private event cache, native tmux format monitors, high-contrast
  crimson/silver title shimmer and session-local attention cycling. Global hook
  definitions, workmux configuration and notifications remain unchanged.
- Workmux commands can track plain panes, but none of the current cdev panes had
  usable status and its sole record was stale. New cdev launches get the scoped
  adapter. Existing sessions without evidence stay unlabelled. Real CLI hook
  trust/delivery, including whether review repeats for per-launch definitions,
  remains a live acceptance gate; there is no trust bypass.
- Keys: Ctrl+F n attention, c project-directory creation, Shift+N ordinary next
  window. n previously created a window; c was standard new-window. Shift+N is
  unbound in the installed defaults. Preflight refuses live key/title/hook-slot
  conflicts. A discovered Ghostty conflict is handled explicitly: Cmd+Shift+N
  forwards old n, so the candidate changes only that Ghostty line to Ctrl+F c.
  The installer keeps n as new-window until the companion is adopted/reloaded;
  background monitoring cannot rebind it. All other tested mappings remain
  unchanged, including Option+h/l,
  numeric selection, popup, pane navigation, Space next-layout and workmux Tab.
- Added one named Doom foreground manager, terminal clients with native Doom
  workspaces and stable per-frame roots, and a separate LaunchAgent definition/
  explicit management tool. SPC f f uses that frame's root; local C-x C-f and
  outside-project navigation retain buffer directories. Explicit standalone
  editor and dashboard-off modes reverse the two features independently.
- Imported a sanitized Doom module snapshot/public terminal preferences for tests,
  including the actual font and focus settings. No private Org/custom/identity
  content or captured environment dump is tracked. Audited generated-startup
  hashes fail before loading changed fixture dependencies.
- Extended the existing complete-release manifest to 15 payloads, new local
  parsers and @HOME@ rendering. Only two Fish functions and one LaunchAgent need
  additional adoption for the editor/service; full attention navigation also
  requires the separately approved Ghostty companion file. Helpers can stay
  release-local.
  No deployment transaction/backup framework was replaced.

## Validation evidence

Before changes: python3 -B scripts/test.py --integration passed all 47 existing
regressions. After implementation and fixes: **79 tests passed in 43.647s** with
python3 -B scripts/test.py --integration. No remaining automated failures.
Private sockets, inert native Codex stand-ins, synthetic history/hooks and
sanitized disposable Doom homes were used; production main was never a test
subject. Production queries were limited to read-only identity/binding/status
metadata and file fingerprints. No active window was reordered programmatically.

Coverage includes concurrent agents, stale launch/session/turn/server/PID data,
termination, disconnected clients, title/pane/window movement, approval/stop
transitions, empty/cycling attention queues and actual binding invocation;
bounded observer-lock contention and the Ghostty companion/fallback gate;
project naming/reuse/collisions/pins/resume failures; two real Doom terminal
frames with independent perspectives, nested files/scratch/workspace changes,
actual SPC f f and local C-x C-f, reconnection, retained unsaved buffers, client
pane closure, duplicate-manager rejection and unavailable-server behavior.
The inspected macOS 27.0/bundled-libgccjit native compilation workaround passes.

All old deployment regressions still pass. Added-component rollback refuses an
old release missing managed paths, then succeeds after restoring new component
backups, including contents, modes and original absence. New malformed Python,
Fish, Elisp and plist inputs are rejected. Launchctl mutations are mocked only.

Final private benchmark, 24-character titles: working expansion 0.3060 ms;
20-idle-window monitor 0.2352 ms; changed-cache refresh for three agents 47.14 ms;
unchanged working hook 23.27 ms. Native animation creates zero processes per
step. An unchanged monitor creates no renderer process; unchanged tool events
avoid a tmux/cache update, with a bounded 30-second lease renewal. These are
local wall-time measurements, not a system-wide CPU or live-redraw claim.

Read-only final comparison passed: all inspected live file bytes/modes/link
metadata and the full deployment tree (including ec518f0 receipt/payload/backup)
match baseline. Production server/session/window/pane identities and all loaded
binding/hook hashes are unchanged, including all seven pane IDs/root PIDs.
The original key/title/hook checks pass; strict attention preflight flags its
required Ghostty companion, while display-only preflight passes with old n.
No new named-server directory, dashboard state or Emacs/Doom launchd registration
exists. The current state environment matches the proposed
service default. Deployment preflight passed all 14 local checks and dependencies.
Its first sandboxed attempt could not create the isolated parser socket; the
narrowly approved retry passed. No blocked attempt is counted as a pass.
Final staged review: 43 files passed the heuristic secret/path scan and staged
whitespace check. All staged blobs matched the reviewed working files and all
22 relative documentation links resolved. The diff includes the previously
uncommitted migration/reload history below; that history was preserved.
The authorized local milestone commit includes these results; no commit deploys
and nothing has been pushed.

## Review artifacts and boundaries

- [Activity design/evidence and limits](ACTIVITY.md), including the
  [offline four-state preview](previews/dashboard.html).
- [Doom server/frame architecture](DOOM-SERVER.md).
- [Exact proposed staging/adoption/rollback sequence](MILESTONE-DEPLOYMENT.md).
- Manifest component/target matrix and independent Terminal.app recovery are
  documented. Restore companion Ghostty forwarding before restoring c's default;
  new Fish/service backups must precede pointer rollback to ec518f0. Keep pinned
  releases while processes may reference them.

Remaining live acceptance: Ghostty companion migration/reload/key delivery;
normal Codex hook trust/delivery, precise concurrent
approval-resolution limits, terminal redraw/appearance/physical keys, actual
private Doom/Org customization, launchd bootstrap/recovery/login/reboot. The
sanitized fixture's snippet warnings are not a claim about the private config.
Existing legacy editor panes remain standalone until the user changes them.

The commit-keyed/idempotent/exclusive staging guard remains a **separate**
follow-up. Its earlier tested temporary implementation has not been folded into
the checked-in tool during this milestone; stage still copies a clean reviewed
checkout to a unique ID. Preserve the original ec518f0 release and backup.

## Next single action

Review the committed candidate and request separate approval for **inactive
staging only** of that exact commit/15-file manifest. No activation, live
migration, reload, service installation or hook trust is implied. Follow
MILESTONE-DEPLOYMENT.md for each later approval. Stop before production writes.

---

The following is historical evidence; its earlier next-action statements do not
supersede the current milestone record above.

# Historical record — earlier deployment and reload

**As of 2026-10-22; tmux reload at 00:39 EDT (04:39 UTC). Agent-observed.**
The existing tmux server loaded the migrated ec518f0 configuration once, with
exit 0 and empty stdout/stderr. The session, four windows, seven panes and client
survived unchanged. Prefix/navigation/numeric/popup/reordering bindings are
verified. Diagnostic caveats are recorded below; physical acceptance is pending.
**No deployment files, Ghostty configuration or application processes were replaced.**

| Milestone | Status | Evidence |
|---|---|---|
| Targeted Ghostty/tmux audit | Complete | Exact sources/includes inspected; privacy-screened; original hashes in INVENTORY.md |
| Approved development imports | Complete | Four regular copies; unused Ghostty profile and empty macOS override not adopted |
| Popup and window reordering | Loaded; physical acceptance pending | Pinned helper/styles and M-h/M-l installed; no live movement or popup invocation used for verification |
| Three-layer architecture/tooling | Implemented in repo | Complete copied releases, pinned references, checks, backups, journals, activation, rollback and restore |
| Agent governance | Updated | Repo edits/tests/docs/reviewed local commits authorized; external actions remain separately gated |
| Final staged review | Complete | 28-file preflight, staged whitespace, preservation review and documentation links passed |
| Local version control | ec518f0 payload; 1f28195 tooling | HEAD remains 1f28195; clean before migration; this status update is uncommitted; no remote publication |
| Production staging | Complete; selected for tmux | Published ec518f0 payload unchanged; independent regular copies, mode 444; current established |
| Pointer-restoration repair | Committed as 1f28195 | Backup journal schema 2, pointer/drift/dependency guards and resumable restoration; 47 tests pass |
| Initial tmux migration | Complete and verified | Five links, three verified originals, two absent-path records; backup 20261022T040111.754783Z-a455ecd7 |
| Tmux reload | Authorized; performed once | source-file returned 0, no output; all identities/start times retained; diagnostic caveats below |
| Other application reload/restart | NOT PERFORMED | Ghostty, Doom and Codex processes/configuration preserved |
| Manual loaded UX acceptance | NOT PERFORMED | Physical keys, actual popup appearance/navigation and movement await user testing |

## Authorization recorded

The user explicitly approved importing relevant Ghostty/tmux sources, improving
the popup, adding nonconflicting window reordering, implementing deployment/
rollback tooling in temporary fixtures, updating governance/docs and making local
commits. Future repository development and reviewed local commits are standing
permissions. This supersedes the starter's M1-only write/commit gates.

The user subsequently approved inactive staging of ec518f0, which completed
without changing live files or current. Initial tmux-only migration was then
approved subject to all preflight conditions passing, with instructions to stop
on any failure. The exact-state restore condition was not met, so migration was
not attempted. The next task explicitly authorized a bounded repository repair,
isolated tests, recovery/status documentation and a local commit. It explicitly
withheld live migration, production pointer changes, application reload and
replacement of the staged release. Reload, Ghostty adoption, unrelated
repositories and AeroSpace changes remain outside this approval.

The latest approval authorized a fresh production preflight followed by backup,
initial pointer establishment, exactly five tmux file migrations and verification.
Those operations completed. It expressly withheld reload, Ghostty/adjacent
configuration changes, automatic rollback and new commits. This status record
documents the verified outcome; no commit was created during migration.

The next approval covered one controlled reload of the existing tmux server,
following source/plugin/hook inspection and parse-only validation, then read-only
verification. It withheld window movement tests, deployment changes, application
restarts, commits and unrelated repairs. No recovery or second reload was run.

## Repository changes

- Imported configs/ghostty/config.ghostty unchanged from its inspected source.
- Imported configs/tmux/tmux.conf, changing only its hardcoded navigation include
  to @RELEASE@/tmux/czuba-navigation.conf. Existing plugins/startup remain intact.
- Imported and updated configs/tmux/czuba-navigation.conf and cheatsheet.txt.
- Added configs/tmux/show-shortcuts.sh and shortcuts.lesskey.
- Added deploy/manifest.json, scripts/deploy.py, validation.py, test.py, and two
  test modules. Test artifacts use owned temporary directories, not live paths.
- Updated AGENTS.md, README, workflow, decisions, inventory and continuation
  prompt. Added validation evidence and independent Terminal.app recovery docs.
- Starter local controls and historical ENVIRONMENT.md remain in the repository;
  no live Codex configuration or other application repository was accessed.

## Behavior in the candidate

Cmd+Shift+P still sends Ctrl+F then ?. The popup has #f3e8d2 background,
#20242b text, #264f78 headings and #8b3a2f keys. Plain ASCII columns fit within
73 columns; section keys 1–8, tags, search, paging and a persistent prompt improve
navigation. Ctrl+F sequences are explicit. Copy-mode Escape is corrected; stale
task commentary and irrelevant legacy alias inventories were removed. Doom,
workmux and AeroSpace limitations are stated rather than presented as verified.

Window movement uses Ctrl+F, release, then Alt+h/l (Option on this Mac).
The preferred Shift+L conflicts with tmux's previous-client binding; < and >
also have existing menus. Those bindings are preserved. Candidate Alt+h/l is
unbound in installed defaults and inspected custom files. Movement uses captured
session/window IDs, retains focus, ignores marked windows, renumbers from 1 and
stops at first/last boundaries. Numeric tmux selection is tested; physical
Command/Option delivery awaits live acceptance.

## Original milestone commands and observed validation

- sh scripts/audit.sh: targeted path/availability/Git inventory completed.
- tmux -V: 3.8; ghostty +version: 1.3.1; /usr/bin/less --version: 668;
  Python used for tests: 3.12.15.
- sh -n configs/tmux/show-shortcuts.sh: passed.
- python3 scripts/test.py: 22 unit tests passed, 10 integration tests explicitly
  skipped without --integration.
- python3 scripts/test.py --integration: **32 tests passed**, final run 1.320s.
  Covers parsers, PTY navigation, full actual-template staging/migration/restore
  in a fake home, activation/rollback, backup permissions, interrupted migration
  and post-pointer journal recovery, drift, corrupt releases, bad references,
  symlinks/traversal, writer lock and Terminal-only emergency pointer replacement.
- Actual dependency/override preflight method: passed read-only executable/file
  availability and empty/absent Ghostty override guards. No plugins were run.
- Original source SHA-256/mode checks: all four live imports still match their
  original hashes and remain regular files, mode 644; reconfirmed during the
  migration preflight below.
- Computed text contrast: body 12.8:1; blue 7.0:1; rust 6.3:1 on the light panel.
- python3 scripts/preflight.py: all 28 staged files passed the heuristic scan.
- git diff --cached --check: passed. Complete staged diff reviewed; all staged
  blobs matched reviewed regular development files. Preservation comparisons
  confirmed Ghostty is unchanged, main tmux only normalizes its include and all
  pre-popup navigation bindings are identical. Relative Markdown links resolve.

See VALIDATION.md for proof boundaries. Earlier development failures were fixed;
sandbox-denied private sockets were not misreported as successful tests.

## Inactive release and stopped migration preflight (before repair)

The approved inactive staging created this release, with no preexisting
deployment root encountered at staging time:

```text
/Users/czuba/.local/share/dotfiles-active/releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16
```

Staging used a temporary commit-keyed guard because the checked-in stage command
does not yet provide idempotent release IDs or exclusive publication. The guard
verified repeated staging reuses the identical release without writes and that
collisions are refused. Staging parser/dependency checks passed. The permanent
release.json and the temporary staging-result.json record that operation.

The stopped pre-repair preflight verified:

- All six payload files match the exact committed blobs after release-path
  rendering; the manifest matches the commit. Payloads and release.json remain
  regular mode-444 files. Payloads have independent inodes, one hard link and no
  symlinks into the checkout. Dependencies and release-local references pass.
- The five tmux destinations match the staging baseline: ~/.tmux.conf,
  ~/.config/tmux/czuba-navigation.conf and ~/.config/tmux/cheatsheet.txt are
  regular mode-644 files with their original SHA-256 values. show-shortcuts.sh
  and shortcuts.lesskey under ~/.config/tmux remain absent. Existing parents
  are ordinary directories; no target or parent symlink was adopted.
- The configured popup command explicitly invokes sh with the staged helper
  path. That exact shell command passed a PTY invocation at mode 444, including
  section jumps, search and quit. Plain/render modes preserve the reference
  text. Executable permission on the helper is unnecessary. This did not open
  a popup or load bindings in the live server.
- A temporary-home rehearsal used copies of the three existing originals,
  the actual manifest and the real migration/restore methods. It verified all
  three backups' bytes and POSIX modes and both absent-path records, restored
  all three regular files exactly, and removed both newly created live helper
  links. Parser calls were isolated from this filesystem rehearsal; no fresh
  tmux parser/server test was needed after the stop condition was established.
- **Failed condition:** the same rehearsal starts with current absent but
  restore leaves current -> releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16.
  The journal does not record the previous pointer state. This matches the
  documented retention behavior but falls short of exact pre-migration state.
  No restore-tool or staged-payload repair was attempted.

Only temporary fixtures and this repository status record were written during
this preflight. Production current remains absent; backups and history remain
empty. No production backup ID or rollback operation exists. No active tmux or
Ghostty process was accessed, reloaded, restarted or terminated; active session
and pane continuity was not queried because migration did not proceed. Ghostty's
live regular file remains byte-identical, mode 644. No process-related success
claim is inferred from the isolated helper test.

Temporary evidence for this preflight (not a permanent dependency):

```text
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/dotfiles-migrate-preflight-d2jawzi2/
```

baseline.json, helper-result.json and restore-result.json contain the measured
manifest, invocation result and before/after restore difference. The backup ID
inside restore-result.json belongs only to the temporary fixture.

## Verified pointer-restoration repair (before production migration)

Repository changes are limited to scripts/deploy.py, the two existing test
modules, and STATUS/WORKFLOW/RECOVERY/VALIDATION documentation. Config templates,
deploy/manifest.json and the published release were not changed.

New backup journals use schema 2 and record the exact current_before link text
(null for absence), current_after and all declared targets. Restoration validates
the pointer/files first, restores originals and removes new helper links, then
restores the pointer state. It refuses pointer drift and removal while any
declared live configuration still depends on it, including another component's
links, skipped managed paths, relative links and aliases. The existing rule
against migration silently switching releases remains in force: the older
current-release case is tested with a newer inactive release present.

Failures retain a restoring journal and block new migration/activation. Retries
skip validated completed work, including after pointer removal. Successful
repeats validate recovered state without new writes; later user changes are
refused. Legacy schema-1 backup journals lack pointer evidence and require
reviewed manual recovery. Release receipts and payload manifests remain schema 1.

Observed repair validation:

- python3 -B scripts/test.py --integration: **47 tests passed in 1.642s**
  (37 unit tests and all 10 integration tests). The initial sandbox run blocked
  private sockets; the permitted complete suite used isolated homes, private
  sockets, empty startup configs and inert test panes only.
- Real-template integration now checks all five tmux links and mode-444 release
  targets, all three backups' bytes/modes, restoration of all three originals,
  absence of both new helpers, and current's original absence, including repeat
  restoration. CLI failure injection returns nonzero without a success message.
- Recovery interruptions during migration/file restoration, pointer removal, pointer
  directory fsync and final journal publication are covered. Pointer drift before
  restoration and during file/dependency checks is refused safely.
- Read-only production fingerprints before/after testing matched: contents,
  permissions, symlink/absence states, inodes, mtimes, ctimes and deployment
  directory members. Current remains absent; backups/history remain empty.
- The staged release matches ec518f0's committed manifest and rendered blobs.
  Its schema-1 receipt and every payload remain unchanged and compatible with
  the repaired tool. No replacement release or new staging operation is needed.
- python3 -B scripts/preflight.py: all seven staged repair files passed the
  heuristic scan. git diff --cached --check passed; staged files matched the
  reviewed regular working files. The Terminal-only pointer removal example
  was also exercised in a temporary directory without altering its release.

The original five-file migration plan and preflight requirements can be reused
unchanged with the repaired repository tool: the failing exact-state restore
check now passes in isolation. This is not a fresh live migration acceptance;
recheck drift, dependencies, helper invocation and process/reload effects before
any newly approved live operation. No live session/pane query was performed.

## Production tmux migration — 2026-10-22 04:01 UTC

Preflight confirmed a clean working tree at exact HEAD
1f28195a6c7f06048b5e2e9d1e5c859c1e72daca, the intended staged manifest and rendered
ec518f0 blobs, all payload modes, dependencies/parsers, absent current and empty
backups/history. All five live states matched the previous audit. The actual
template migration/restore integration test was rerun in a temporary home and
passed, including all three original bytes/modes, two absent helpers and removal
of current. The helper remained readable at mode 444 through its explicit sh
invocation. No staged file was changed or replaced.

Production mutation used Deployment.migrate(RELEASE, "tmux") from the committed
tool under its existing writer lock, with baseline drift checks immediately
before it. All three verified backups and the durable journal preceded any live
replacement. No alternate migration or automatic rollback path was used.

Backup ID: **20261022T040111.754783Z-a455ecd7**

```text
/Users/czuba/.local/share/dotfiles-active/backups/20261022T040111.754783Z-a455ecd7
```

The journal is schema 2, status migrated, current_before null, and current_after
equal to the link text below. The backup directory is mode 700 and backup.json
mode 600. The three original regular files' hashes, modes (644), ownership and
modification times were verified; both originally absent helper paths are
recorded without fabricated backup files.

Current points to:

```text
releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16
```

All targets below are relative to /Users/czuba/.local/share/dotfiles-active:

| Live file | Verified symlink target |
|---|---|
| ~/.tmux.conf | current/tmux/tmux.conf |
| ~/.config/tmux/czuba-navigation.conf | current/tmux/czuba-navigation.conf |
| ~/.config/tmux/cheatsheet.txt | current/tmux/cheatsheet.txt |
| ~/.config/tmux/show-shortcuts.sh | current/tmux/show-shortcuts.sh |
| ~/.config/tmux/shortcuts.lesskey | current/tmux/shortcuts.lesskey |

Each resolves to the exact immutable-by-convention release file, mode 444, with
matching bytes/hash and payload inode. The staged release's metadata/content and
Ghostty's live regular file remained unchanged. Deployment history is empty;
there is exactly one completed migration backup and no pending recovery journal.

Post-migration metadata queries confirmed the same tmux server PID 72611, the
same session, all seven pane IDs/PIDs/window indices, and process start times.
Five matching protected application processes also retained their IDs/start
times. The loaded popup binding hash is unchanged. No live reload, restart,
session mutation, process termination or rollback was performed. Opening the
old popup may read new cheatsheet text before reload; colors/new bindings await
separate reload and acceptance.

Exact initial-migration rollback command, **not executed**; requires its own
authorization and preserves running processes:

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py restore --backup 20261022T040111.754783Z-a455ecd7 --approve
```

It restores original contents/modes, removes only the two originally absent
managed helper links, then removes current after dependency/drift checks.
Temporary verification evidence (not required to run restoration) is under:

```text
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/dotfiles-live-migration-xsampn4q/
```

baseline.json, preflight-passed.json, restore-rehearsal.log, tmux-before.json,
tmux-after.json and migration-result.json record the measured checks. No pane
contents, working directories, titles or command lines were captured.

## Controlled tmux reload — 2026-10-22 04:39 UTC

The five live symlinks, staged manifest/content/modes and original backup were
reverified. Existing sessions, windows, panes, clients and active pane/application
process identities were recorded before the reload. Source commands resolve to
the pinned navigation include and the installed Dotbar/TPM entrypoints. TPM's
only declared plugins are TPM, Rose Pine and Dotbar; no alternate/system tmux
config or legacy TPM list introduced additional plugins. Shell syntax checks
passed. No active global/session/window/pane hooks were found.

On server PID 72611, source-file -n parsed ~/.tmux.conf and the pinned navigation
include with exit 0 and no diagnostics. This did not execute the config. The
approved source-file ~/.tmux.conf was then executed **once**, with explicit socket
selection and no-start protection. It returned 0 with empty stdout/stderr.

Immediate before/after snapshots verified the same one session, four windows,
seven pane IDs/PIDs and active selections, one attached client, and 15 recorded
pane/application process IDs/start times. No window was moved or renumbered by
verification; no pane was killed, client detached, server restarted or popup
invoked. Effective session prefix is C-f, including inherited options.

Only prefix ?, M-h and M-l changed. All other binding definitions, including
Shift+H/L, window/pane menus and TPM's existing I/U/M-u bindings, are unchanged.
The installed h/j/k/l and Ctrl+h/j/k/l guards still prevent wrapping. Numeric
bindings 1–9 select :1–:9, base-index is 1 and renumber-windows is on; Ghostty's
Cmd+digit mappings and Cmd+Shift+P mapping remain unchanged.

Loaded M-h/M-l check window_start_flag/window_end_flag, then run the captured
session/window-ID swap, reselection and renumbering sequence. Both keys were
unbound before reload. The popup now pins show-shortcuts.sh and its sibling
cheatsheet/lesskey to ec518f0, invokes the mode-444 helper through sh, and has the
specified light/dark/blue styles. Q still provides list-keys -N help.

Dotbar status position/justification/colors, Rose Pine clock/copy-mode colors and
TPM bindings match their expected resulting state. No hooks appeared. Deployment
and backup trees, all five symlink objects and Ghostty's live file retain their
original hashes, permissions, inodes and modification/change timestamps.

Diagnostic caveats: the server's rolling log contains recurring no-such-pane/
window lookups for %2 (234 entries in the captured sample), matching the stale
pane context inherited by the verification client. Their attribution was not
fully established; they were preserved and not repaired. Two other messages
were caused by read-only verification probes using unsupported -q with
show-window-options; the queries were corrected to show-options. No config change
or second reload was used to address those verifier issues. TPM suppresses
individual plugin output, so plugin verification relies on observed diagnostics
and loaded postconditions rather than a claim that all child output was visible.

Evidence, including reload-command.json, reload-exit.json, reload.stdout.log,
reload.stderr.log, tmux-before-reload.json, tmux-after-reload.json,
option-api-diagnostics.json, diagnostic-candidates.txt and verification-summary.json:

```text
/private/var/folders/l3/8pzyw2ld3378f1j8nwgb4jzc0000gn/T/dotfiles-tmux-reload-2fzvmlfx/
```

The earlier temporary verifier failures are retained for review. They did not
trigger configuration repair, a deployment operation or another reload. HEAD
remains 1f28195; only this existing uncommitted status record was updated.

## Separate staging-tool follow-up

- Integrate the tested commit-keyed, idempotent staging guard into the checked-in
  deployment tooling. Render exact commit blobs, verify and reuse an identical
  existing release, reject mismatches/collisions without overwrite, and publish
  with an exclusive atomic rename. Test in temporary directories and preserve
  the separation between staging, activation and reload. This documentation
  follow-up does not change any payload, stage a release or trigger deployment.

## Unknowns and retained risks

The original audit's live socket read was denied. This approved migration used
narrow session/pane/process metadata reads and a popup binding hash to verify
continuity. The controlled reload subsequently verified loaded bindings and
plugin postconditions; physical behavior, suppressed plugin diagnostics and the
stale %2 client-context messages retain the limitations described above.
Workmux help attempted to initialize a real log and
failed in the sandbox; no retry against real account state occurred. Doom was
not initialized/evaluated and private Org/iCloud content was not read.
AeroSpace configuration was inspected only and its enabled state remains unknown.

Ghostty's installed CLI documents explicit reload but does not establish watcher
behavior across symlink pointer changes. No GUI watcher or visual contrast test
was authorized. Ghostty migration must address that uncertainty separately.
Syntax checks do not prove physical key delivery or running application behavior.

## Next action recorded then (superseded)

User performs physical/visual acceptance separately: Cmd+Shift+P, popup section
jumps/search/quit, Ctrl+F then Option+h/l (without Shift), movement boundaries and
focus, and Cmd+1–9. Do not programmatically move existing windows for acceptance.
Any investigation or repair of stale client-context diagnostics is a separate
task; no such fix is implied by the reload approval. Ghostty adoption remains
separate. Do not reload again or change deployment state from this milestone.


## 2026-10-24 — Remote-resume source repair verified; production unchanged

Codex 0.164.0 loses the invocation-hook setup when its short-lived prewarm
subscription closes before the remote TUI attaches. Retaining that subscription
for the owned client restores genuine working/stopped/permission events. Server
pane markers were stale, but existing UUID attribution selected the correct pane.
46 focused tests passed (including five private-tmux integrations), plus real
resume/reentry, concurrent same-root agents, window changes and pager deduplication.
Eight native test definitions retained their trust/hashes; global workmux hooks
are unchanged. Owned disposable processes/session were closed. See
[REMOTE-RESUME-REPAIR.md](REMOTE-RESUME-REPAIR.md) for evidence and acceptance steps.

Production remains `20261023T164459.630188Z-30124092` (17 payloads/14 links verified).
Protected main windows/panes/client and process birth identities remain intact.
An additional production session `2` was observed and left untouched; its origin
is not established. No commit, staging, activation, reload or production state
repair occurred. Inherited/project-workflow edits are preserved; this entry only
appends to the existing STATUS content. Next: review the isolated launcher repair
before authorizing a new repair-only commit/release.


## 2026-10-24 — Connection-only release prepared; final activation unapproved

Signed and SSH-verified commit `d84baaaf7613f9c6232c6f6c2e28644527111cda`:
`fix(cdev): retain shared-server hook setup until client exit`. Native Codex 0.164.0 A/B comparison passed with production
activity.py plus the connection fix and with both fixes: each completed an
ordinary fresh turn/permission request and two exact-UUID resumes with further
working/stopped/permission events. Test approvals were canceled. The SessionEnd
change is unnecessary for this failure; source activity.py and its tests now
match production semantics. Earlier commit a13eae3 and its inactive release
remain preserved. See [REMOTE-RESUME-REPAIR.md](REMOTE-RESUME-REPAIR.md).

Inactive release: `20261024T235701.367069Z-b1475572`
under `~/.local/share/dotfiles-active/releases/`, staged solely from the clean
Git export of the signed commit. All 78 export files matched Git. Complete
17-file manifest, permissions, references/dependencies and payload integrity
verified; 14 managed mappings and three unadopted absent helper paths preserved.
Only `cdev/codex_session.py` changes behavior. The four normal release-path-only
changes are tmux/tmux.conf, tmux/czuba-navigation.conf, fish/functions/cdev.fish
and launchd/local.dotfiles.doom.plist. Pending cnew/global AGENTS/Fish argument
resolution and inherited work are excluded.

Verification: 42 focused regressions plus four deployment/rollback safeguards
passed from the clean export. An additional isolated activation/rollback using
all 17 real payloads restored all 14 links/content and three prior absences.
Reader/thread and socket-FD counts returned to baseline, including blocked-frame
shutdown; all recorded disposable CLIs, descendants, backend and private servers
exited. Two inert tmux socket files were removed only after confirming no listener.
Eight private native hook definitions retained hashes/trust; global workmux hooks
were unchanged. No test push was sent.

Production remains `20261023T164459.630188Z-30124092`. Sessions, windows, panes, clients,
16 protected process birth identities, session 2, UUID pins, Codex configuration,
14 links and deployment history match the preflight baseline. No activation,
application reload/restart or production runtime repair occurred.

Rollback **after a separately approved activation** (POSIX sh/Zsh; restores the
current production release above without application reload):

```sh
python3 -B /private/tmp/df-remote-release-hp41x7a8/export-d84baaaf7613f9c6232c6f6c2e28644527111cda/scripts/deploy.py rollback --expect-current 20261024T235701.367069Z-b1475572 --approve
```

The clean export and metadata-only preparation evidence are retained at
`/private/tmp/df-remote-release-hp41x7a8`. This entry appends without changing inherited STATUS content.
Next boundary: final authorization to activate this specific release with
expected current `20261023T164459.630188Z-30124092`, followed by disposable production
acceptance and physical visual/iPhone confirmation. Existing agents reopen only
naturally; session 2 remains untouched.


## 2026-10-24 — Production acceptance stopped at pin isolation; rollback verified

The user approved activation of 20261024T235701.367069Z-b1475572 (d84baaa).
Signature/export, all 17 payloads, expected current, 14 links, hooks/bindings and
protected process identities passed fresh preflight. Atomic activation completed
without application reload/restart.

Acceptance then failed its pin-integrity guard before any test turn. The test
launcher incorrectly supplied isolation variables to the tmux client process;
the already-running server did not pass them to the new pane. Actual cdev used
the normal helper/pin store and resumed the previous disposable conversation.
It added `~/dev/workmux-test` → `01a16fc3-7f70-7633-a529-c4fe8b9943d7`.
All pre-existing conversation mappings remain unchanged. This is an acceptance
fixture error; production lifecycle behavior of the repair was not evaluated.

The authorized documented rollback restored `20261023T164459.630188Z-30124092`. All 14 links,
sessions/windows/panes/clients, loaded keys/hooks and 16 protected process birth
identities match the baseline; session 2 is preserved. The test CLI exited
normally and its new editor/control panes and disposable session were closed.
No test notification was queued. No original agent/service was restarted or
replaced. The signed candidate release remains intact and inactive.

Residual state: the one added test pin above remains. The release rollback does
not restore session metadata, and the user explicitly prohibited pin changes;
no further production pin edits were attempted. A guarded removal using the
existing helper's unpin action was tested on a temporary copy and restored the
exact original pin-file SHA-256. Proposed operation, requiring renewed approval:

```sh
python3 -B /private/tmp/df-remote-live-gslkyxyl/restore-test-pin.py
```

The fixture now passes environment assignments as the actual pane command and
checks them before sourcing/calling cdev. An isolated existing-server dry run
reproduced rejection of the previous approach and passed the corrected one,
without launching Codex/Doom or changing production pins.

Evidence and the tested recovery script: `/private/tmp/df-remote-live-gslkyxyl`.
Next boundary: operator review/approval to remove only the added test pin and
retry the rollout with the corrected fixture. No automatic reactivation.


## 2026-10-24 — Test-pin recovery succeeded; single retry rolled back before Codex startup

The user approved recovery of only workmux-test →
01a16fc3-7f70-7633-a529-c4fe8b9943d7 and one corrected acceptance retry.
`restore-test-pin.py` was inspected and executed under the existing pin lock,
with exact preimage and mapping guards. The owner-only verified backup is
`/private/tmp/df-remote-live-gslkyxyl/pins-before-approved-restore.json`.
Only that test mapping was removed. Original pin bytes (SHA-256
f3899d3282dfa9a9212175e9425448f7c091123fc81f83d47d6301b546b22451)
and mode 0600 were restored and remain unchanged.

The signed d84baaa release 20261024T235701.367069Z-b1475572 passed integrity,
expected-current and continuity checks and was activated once. The disposable
control pane passed private XDG/editor checks, but that preflight did not cover
cdev's subsequently created nested agent pane. That pane inherits tmux's
server/session environment, where the private XDG variables were absent.
The guarded test shim exited status 1 before any activity registration or
Codex startup. This is another acceptance-fixture failure; zero real turns and
zero notifications were produced. Fresh/resumed lifecycle, shimmer, stopped,
approval, attention and iPhone acceptance were not reached in this retry.
No conclusion about production lifecycle delivery follows from this attempt.

The immediate authorized rollback succeeded: production is
**20261023T164459.630188Z-30124092**. Journal:
20261025T011051.335324Z-2f8f33b9.json. Both immutable 17-payload receipts,
14 managed links, three unadopted absences, loaded keys/hooks/status formats,
Codex config/trust and pins were verified. All original sessions/windows/panes,
clients and 16 protected process birth identities survive, including session 2.
No application reload/restart occurred. Only owned private test resources and
their verified non-listening socket were removed. The candidate release remains
intact and inactive. All 19 other pending files remain byte-identical; this entry
appends without overwriting existing STATUS content. No commit or push occurred.

Metadata-only evidence: `/private/tmp/df-remote-live-gslkyxyl/retry/`, including
startup-failure.json, final-rollback-verification.json, cleanup.json and closeout.json.
No further automatic retry is authorized. A future acceptance fixture must prove
isolation in the actual cdev-created agent pane, including tmux server/session
inheritance, before another separately authorized activation. No physical check
or manual production recovery is required for this failed attempt.


## 2026-10-24 — Acceptance harness corrected and independently validated; no activation

The precise loss is at tmux new-window and, independently, split-window:
processes inherit server/session environment, not the calling Fish pane or
editor pane. The fixture now injects its allowlisted private environment through
creation-time -e argv on both commands, with a private-socket-only wrapper.
No tmux global environment is changed. Real control/preflight/editor/launcher
probes gate source launch; inert agent, actual private adapter subprocess and
backend probes verify descendant identity and paths before any pin write.

Seven harness regressions passed against the frozen signed d84baaa export:
client-only environment, control-pane-only environment, incomplete new-window-
only propagation, all descendants/state paths, alternate-socket/credential
rejection, concurrent fixtures with matching pane numbers, and legitimate
shared-backend stale pane markers. The positive test was also deliberately run
with the old propagation disabled and failed before launcher release/pin writes.
Five nearby connection/subscription cleanup tests and three cdev UUID/reuse/
instrumentation tests passed: 15 unique focused tests total. Syntax/whitespace
checks passed. No full suite was run.

The fixture uses a clean environment, private HOME/XDG/CODEX_HOME/temp/cache/
UNIX sockets, and an empty file-credential profile. It rebases the activity
module's account-wide registry attribute only inside private test processes;
source files and identity checks remain unchanged. No credentials were read or
copied, no native Codex/editor or ntfy publish ran, and no real event delivery or
native credential resolution is claimed. A future genuine private-profile run
requires native login/review and effective credential-store verification before
production activation. Configuration isolation is not an OS filesystem jail.

Production remains 20261023T164459.630188Z-30124092. The immutable candidate
20261024T235701.367069Z-b1475572 still matches signed d84baaa across all 17
payloads; both receipts, 14 managed links and three absences were verified.
All 16 protected process birth identities, sessions/windows/panes/clients,
session 2, loaded keys/hooks, original UUID pins and Codex config are unchanged.
No deployment, reload, restart, auth change, commit or push occurred. All 19
other pre-existing pending files remain byte-identical. Tests used and cleaned
only owned private resources. This entry preserves prior STATUS content.

Source changes: tests/acceptance_harness.py, tests/fixtures/acceptance_probe.py,
tests/test_acceptance_harness.py and docs/ACCEPTANCE-HARNESS.md, plus this appended
status entry. No production-manifest or configuration-payload change is needed.
Metadata-only results: /private/tmp/df-harness-proof-xguwyb4h/.
Next boundary: review the harness and proposed pre-activation native acceptance
in docs/ACCEPTANCE-HARNESS.md; no further production retry is authorized.


## 2026-10-24 — Isolated native validation prepared; manual login/review pending

No activation occurred. Native Codex 0.164.0 is open in the proven private
fixture /private/tmp/df-accept-77_9rnb2, tmux socket tmux.sock, session acceptance.
The actual control/editor/launcher/agent/adapter/backend environment proof passed
before native launch; production pin hash remains the exact recovered baseline.
Native config/read verified effective file-only credential storage in both the
owned metadata server and private Unix backend (peer PID 34635). The fresh CLI
is child 34943 of launcher 34715 in private pane %6; eight sessionFlags hooks
were audited as untrusted. No model turn or trust decision was automated.

Manual native login and review are pending. Exact definitions, commands, source
paths and hashes: /private/tmp/df-native-validation-zq_dsewa/NATIVE-REVIEW.md.
All test code is frozen there by hash. No production credentials were read or
copied. Production remains 20261023T164459.630188Z-30124092; all 16 protected
process birth identities are unchanged, including unidentified session 2.
The signed release and pending project-initialization work are untouched.

A small test-only profile guard adjustment allows normal native project-trust
TOML sections while still requiring the root file-credential setting. All eight
focused harness regressions pass, including rejection of keyring mode. Remaining
work after the user gate: genuine working/stopped/approval, normal exit and exact
UUID resume twice, then report and stop before production activation.


## 2026-10-24 — Genuine isolated validation stopped: fixture locale breaks renderer metadata

The user completed private login and native review. Read-only native hooks/list
confirmed all eight sessionFlags definitions trusted with identical reviewed
hashes. The effective private credential store remained file; no credentials
were read or copied. Exactly one genuine Codex 0.164.0 turn was submitted.

Working and Stop events reached the correct private pane %6 / launcher 34715 /
child 34943. The cache bound UUID 01a170d8-e854-7761-8489-017a2f03e887 and turn
01a170dc-582a-7831-a515-319f5102a833; native turn metadata independently reported
that same turn completed with items unloaded. The registration remained live.
However, no shimmer or white dot rendered: the private window state option
remained empty. Acceptance therefore FAILED and stopped before approval or
UUID-resume tests. No automatic retry or correction was attempted.

Root cause is another fixture condition, not established as a production or
hook-repair regression: its LC_ALL=C makes tmux replace literal metadata tabs
with underscores. The background renderer then raises ValueError (expected
four fields, got one), suppressed by --quiet. Read-only diagnostics under the
exact callback environment reproduced the error. The same metadata query under
en_US.UTF-8 preserved all six tabs/four fields per window. No actual refresh,
server-environment mutation or native retry was used for this comparison.
Proposed next correction is UTF-8 in the fixture's server/client environment,
with a regression for the real callback's metadata/format contract; NOT applied.

The disposable CLI quit normally; its launcher/child/descendants exited and the
registration finalized idle/ended. The exact private backend was stopped and
its tmux session removed. The owner-only authenticated private profile and test
code remain at /private/tmp/df-accept-77_9rnb2 for review, retained by idle test
controller 34546 (tool session 18151); no Codex frontend/server remains running
there. This intentional retained fixture is not a production service.

Production remains 20261023T164459.630188Z-30124092. The candidate release and
both 17-payload receipts, 14 live links, original pin hash, loaded bindings/hooks,
all original sessions/windows/panes/clients and 16 protected process birth
identities were verified unchanged, including session 2. The 19 other pending
files are unchanged. No activation/reload/restart/commit/push occurred.
Metadata-only evidence: /private/tmp/df-native-validation-zq_dsewa/,
including FINAL-RESULT.json, fresh-turn.json, locale-root-cause.json,
exact-callback-dry-run.json, trust-after-user-review.json and cleanup.json.
Next boundary: operator review. Approval, attention, repeated UUID recovery and
notification acceptance are not established by this failed isolated run.


## 2026-10-24 — Locale repair verified; native sequence stopped at approval-owner check

User authorized the fixture-only locale repair, automated preflight, then one
full native validation without deployment/retries. The fixture now verifies
UTF-8 before startup and consistently sets LC_ALL/LANG=en_US.UTF-8 for server,
client, created panes and callbacks. New tests execute the actual background
renderer, record its real metadata, and exercise all four synthetic states.
The negative C callback received @0___ (zero tabs) and raised expected-4/got-1;
the UTF-8 callback received literal tabs and rendered correctly. All 17 focused
checks passed: 12 harness integrations and five connection/reader regressions.
Source syntax/whitespace passed. No production code was changed.

Boundary audit additionally covered per-pane env injection, callback interpreter
and explicit socket/state, private HOME/CODEX_HOME/cache/auth/registry paths,
stale pane markers, and real cdev reuse without duplicate agents. The retained
profile was handed off from its exact idle owner after identity/open-file checks;
no credentials were read/copied. The old profile keeper is stopped. Authentication
and all eight identical trusted definitions were reused without another review.

Genuine fresh Codex 0.164.0 PASS: UUID 01a170fa-c8f7-7a81-81bb-72b34a3309d9,
working -> completed turn 01a170fa-d397-7ca0-9328-5826bd2db392, eight distinct
crimson/steel rendered frames, stopped white dot. A genuine PermissionRequest
produced the waiting/red-alert renderer output. The full sequence STOPPED at an
extra test-driver assertion: it queried waitingOnApproval on the separate shared
endpoint, although this fresh launch used local ancestry and no remote identity.
That was not a valid owner-specific runtime check. No approval was sent; cleanup
canceled the request. No retry or UUID resumptions were performed. Normal-exit/
resume acceptance remains incomplete; this is not production activation readiness.
Proposed verification-only correction: native local event evidence for local
mode, activeFlags only after verifying shared ownership. NOT implemented/rerun.

The disposable launcher/child and backend are gone, the backend was reaped,
the private tmux session and stale sockets were removed. No profile-keeper
process remains. The owner-only authenticated profile is retained at
/private/tmp/df-accept-77_9rnb2, with only its private project UUID pin above.
Prior private native history was renamed within that fixture without reading
or copying its contents; production history and pins were untouched.

Production remains 20261023T164459.630188Z-30124092. Both 17-payload immutable
receipts, candidate 20261024T235701.367069Z-b1475572 (d84baaa), 14 live links,
three absences, original production pin hash, config/hook/binding hashes,
sessions/windows/panes/clients and 16 protected process birth identities were
verified unchanged, including session 2. All 19 other inherited pending files
are unchanged. No deployment/reload/restart/commit/push occurred.

Source changes are tests/acceptance_harness.py, tests/test_acceptance_harness.py,
new tests/fixtures/renderer_callback.py and concise workflow/status updates.
Evidence: /private/tmp/df-native-validation-zq_dsewa/utf8-validation/.
FINAL-RESULT.json distinguishes the successful locale/fresh-render checks from
the stopped full sequence. Next boundary: operator review; no further native
run or production activation is authorized automatically.

## 2026-10-24 — Corrected remote-topology native validation PASS; no deployment

User authorized one corrected isolated sequence, preserving the signed candidate,
UTF-8/path guards and production. Investigation confirmed fresh cdev launches are
local by design; pinned recovery explicitly uses the shared Unix app-server.
All four protected production clients use --remote. Earlier fresh-only evidence
is local-only and did not cover remote-resume hook lifetime.

Replaced the faulty stored-thread ownership assertion with live process-generation,
exact argv/endpoint/UUID and reciprocal kernel socket-peer checks. Remote mode
requires both TUI and retained setup connections to the same native server, its
loaded UUID, and matching attributed lifecycle events. Local mode has separate
positive ancestry/no-remote/pending-event checks. The private backend has no global
dashboard hooks or startup hook overrides. Tests reject a prematurely closed setup
connection even if stored metadata and the live TUI still look valid.

All 24 focused preflight tests passed (13 environment/callback/publisher, six live
ownership, five subscription/reader). The single genuine Codex 0.164.0 run passed:
fresh local -> exact UUID remote resume -> exact UUID remote resume, each with
working -> completed turn, rendered shimmer/white dot, genuine permission request
and red alert, attention keyboard selection, canceled-request empty queue and
normal exit. UUID: 01a17123-36ad-7573-89da-155484a56db5. Distinct working frames:
8/7/7; all 27 actual callbacks succeeded under en_US.UTF-8. Both remote approvals
also showed waitingOnApproval on the proven live owner. All eight unchanged hooks
remained trusted across launches; no login, trust decision, approval or retry.

The existing publisher recorded exactly six actionable transitions (three stopped
priority 3, three approval priority 4), one attempt each, without duplicates or
startup replay. This used a local recording transport: HTTP/iPhone delivery and
physical appearance are NOT established by this run.

Production is still 20261023T164459.630188Z-30124092. Candidate
20261024T235701.367069Z-b1475572 / signed d84baaa is unchanged/inactive. Both
17-payload receipts passed integrity/mode/reference/parser checks; all 14 live
links and three unadopted absences remain correct. Original hooks, bindings,
session pins, sessions/windows/panes/clients, session 2 and all 16 protected process
birth identities are unchanged. Pin SHA-256 remains
f3899d3282dfa9a9212175e9425448f7c091123fc81f83d47d6301b546b22451.
All 78 clean-export blobs match d84baaa; 19 other inherited pending files match
the baseline. No production code/release, reload, restart, commit or push occurred.

Owned private launchers/clients/backend/descendant and tmux server exited; stale
owned socket nodes were removed. Owner-only authenticated fixture retained at
/private/tmp/df-accept-77_9rnb2; no credentials or transcripts were read/copied.
Evidence: /private/tmp/df-native-validation-zq_dsewa/remote-validation/,
including native-result.json, per-cycle live ownership/turn/approval/navigation/
notification records, continuity.json and final-private-cleanup.json.

Source changes are limited to acceptance support/tests and documentation, outside
the production manifest. Next boundary: final production activation authorization;
no further retry or deployment is automatic. Preserve the tested wrapper/env for
any acceptance. Production activation needs no tmux or service reload; existing
agents transition naturally, with visual/iPhone confirmation separately reported.

## 2026-10-25 — Approved activation aborted on unexpected Codex configuration drift

The user authorized activation of d84baaa / 20261024T235701.367069Z-b1475572,
conditional on an unchanged production baseline. The recorded SSH signing key
verified the commit using the existing release-local allowed-signers file; no Git
configuration was changed. Both immutable 17-payload receipts, modes/references/
parsers and identical deployment manifests passed. Only codex_session.py changes
behavior; activity.py is byte-identical to the current production release.

Preflight found ~/.codex/config.toml changed from accepted SHA-256
c4976322a54a814a1695d821ce5831062a8f2897377e5be3b22c90f99a3679c5 to
d48c34e0ec5a260461eb6087b0800012f7332cdfbc2f8b31dde599f21b94ef00.
Observed mtime: 2026-10-25T04:13:29.327728Z; permissions remain 0600. Its contents
and cause have not been reconciled; no attribution to the Collie pilot is made.
Per the explicit abort-on-drift requirement, NO activation or native canary was
attempted. No rollback was needed. No fixture launcher changes were made.

Current remains releases/20261023T164459.630188Z-30124092. All 14 managed links,
three unadopted absences, global hooks, production pins, loaded bindings/formats,
two sessions (including 2), six windows, ten panes, one client and all 16 protected
process birth identities match the accepted baseline. Deployment locking is
available and no incomplete migration exists. The 19 other pending files are
unchanged. No application reload/restart, process signal, Collie server/listener/
Tailscale operation, commit or push occurred.

Metadata-only evidence:
/private/tmp/df-native-validation-zq_dsewa/production-activation/aborted-preflight.json.
Next boundary: reconcile the unexpected Codex configuration change before any
renewed activation; production acceptance has not run under this authorization.

## 2026-10-25 — Approved baseline recorded; canary stopped and atomic rollback verified

User accepted the exact 45-byte addition notice.hide_rate_limit_model_nudge=true
and authorized a new baseline, activation of the existing d84baaa release, one
bounded canary and rollback on critical failure. Current config SHA-256 remains
d48c34e0ec5a260461eb6087b0800012f7332cdfbc2f8b31dde599f21b94ef00.
The original baseline and config were preserved. New exact-hash baseline:
/private/tmp/df-native-validation-zq_dsewa/production-activation/reviewed-baseline.json.
It records the original baseline hash/provenance and the sole added preference;
no wildcard, semantic-ignore rule, hook edit or trust decision was introduced.

SSH signature, all 78 clean-export files, both immutable 17-payload receipts,
manifest, 14 mappings and three absences passed; only codex_session.py changes
behavior. All 24 focused harness/ownership/subscription checks passed. Activation
to 20261024T235701.367069Z-b1475572 succeeded atomically, journal
20261025T050205.459101Z-33b065ba.json, without reloads/restarts. The canary read the
managed activated launcher through a verified read-only private alias, with its
older copy moved aside. Its environment guards, UTF-8 callbacks, stable private
hook definitions and ownership checks remained intact.

Genuine fresh 0.164.0 turn passed: UUID 01a17170-1d64-7c63-8bd7-501cfec60952,
matching completed turn, eight distinct working frames, stopped white dot and
actual prefix-n attention selection. The subsequent genuine-approval check did
not observe a waiting state within 100 seconds; inspection found that new turn
already stopped. The cause is unestablished. The run stopped before either
remote resume; no production acceptance claim is made for those phases. No
permission was automatically approved and no retry occurred. Two distinct stopped
transitions were recorded once each by the real publisher with a no-network
transport; HTTP/iPhone delivery and the approval indicator remain unverified.

The documented atomic rollback restored 20261023T164459.630188Z-30124092,
journal 20261025T050417.826105Z-d42bb5da.json. All 16 protected process births,
12 recorded Collie pilot process identities, session 2, tmux objects/bindings/
hooks/formats, pins, reviewed config and 14 links passed restoration checks.
Owned canary launcher/client/backend and private tmux exited; stale owned socket
nodes were removed and the private source alias restored. Authenticated private
profile remains owner-only. No Collie listener or Tailscale operation occurred.

Evidence: /private/tmp/df-native-validation-zq_dsewa/production-activation/accepted-canary/,
including activated-source proof, fresh-turn.json, verified-rollback.json and
CLOSEOUT.json. The raw native failure file inherits an isolated-harness placeholder
production_activation=false; CLOSEOUT and deployment journals explicitly record
the actual activation/rollback. The raw evidence is preserved. Candidate release,
19 other pending files and all excluded features remain unchanged. No commit or
push. Stop for review; no further activation or native retry is authorized.

## 2026-10-25 — Remote-resume repair deployed and verified; bounded-work policy adopted

The user superseded routine stop-before-deployment gates with authorization to
finish this repair after corrected isolated validation and clean preflight.
Broader/global changes and substantive security/drift/recovery risks still need
review. AGENTS.md and WORKFLOW.md record that standing policy; unrelated pending
features remain excluded. No new source/release repair or Git commit was needed.

Read-only diagnosis established the prior approval timeout's cause: its test turn
made zero tool calls, while the preceding normal turn made two sleep calls. No
permission-requiring operation was attempted. Working/stopped attribution and
rendering were correct; no defect in d84baaa was demonstrated. The harness now
finishes fresh -> normal exit -> exact-UUID remote resume twice before independent
approval testing. A native-validated prompt rule for harmless echo in the private
profile triggers a real request, canceled without approval. Four added focused
regressions plus the existing 24 checks passed. Production code was unchanged.

Revised isolated validation PASSED all phases, then final preflight verified the
signed d84baaa export, all 17 payloads, 14 mappings, three absences, exact reviewed
config/hooks/pin hashes and protected processes. Atomic activation succeeded:
current = releases/20261024T235701.367069Z-b1475572
journal = 20261025T055304.851536Z-6c0b4cc9.json
Only codex_session.py changes behavior; SessionEnd changes remain excluded.

The production canary read the installed managed launcher, not an older copy.
Genuine Codex 0.164.0 UUID 01a1719e-cd49-7832-89ee-3b6f5621dfc2 completed fresh
and two remote-resumed turns with matching native/session/pane/process-generation
identities and reciprocal TUI/setup socket peers. Working frames 8/9/9, stopped
white dots, actual prefix-n navigation and empty-queue focus all passed. The
independent real approval produced waitingOnApproval and the red alert, then
canceled cleanly. Eight trusted definitions retained hashes; global workmux and
all 15 production trust records/config/pins remained unchanged.

Post-canary verification preserved all 16 protected process births, session 2,
main's original objects/client, loaded bindings/hooks/formats, 14 links and both
immutable receipts. All 11 Collie pilot identities present at this run's start
survived. Former pilot tmux client 6413 was already absent before isolation; its
cause is unestablished. No pilot session/listener or Tailscale operation occurred.
No reload, agent restart or rollback was needed for this final rollout. Existing
agents gain the launcher repair when naturally reopened; none were disturbed.

Four publisher records (three stopped priority 3, one approval priority 4), each
one attempt, no replay or duplicates, passed through a no-network recording
transport. HTTP/iPhone delivery and physical appearance are not claimed by this
canary. Nine owned test process identities exited; private tmux/backend sockets,
prompt rule and source alias were cleaned up. Private authenticated profile is
retained owner-only. No production auth, pin or hook changes and no push.

Evidence: /private/tmp/df-native-validation-zq_dsewa/final-rollout/CLOSEOUT.json
and /private/tmp/df-native-validation-zq_dsewa/revised-isolated/.
The original baseline is preserved; the approved current-config baseline remains
production-activation/reviewed-baseline.json under the same evidence root.

Rollback, only if subsequently needed (no application reload):
python3 -B /private/tmp/df-remote-release-hp41x7a8/export-d84baaaf7613f9c6232c6f6c2e28644527111cda/scripts/deploy.py rollback --expect-current 20261024T235701.367069Z-b1475572 --approve

The repair is deployed and verified. No further deployment gate or automatic
retry is pending; physical iPhone/visual observations remain separately reported.


## 2026-10-25 — Remote-resume milestone closed; project workflow deployed

The user accepted the remote-resume repair as complete and personally confirmed
its crimson working shimmer in cdev-smoke. No further lifecycle diagnostics are
pending for that milestone. Existing repair, hooks, renderer and pager are preserved.

The previously reviewed project workflow is now deployed from SSH-signed commit
632b28dd50a3dace1cd719b22e84a1fd96ccc5da (signature verified):
current = releases/20261025T061731.748309Z-45cef594
previous = 20261024T235701.367069Z-b1475572

Only eight relevant source/test/documentation files were committed; all inherited
work remains uncommitted. Clean export matches all 82 Git blobs. Of 17 existing
payloads only fish/functions/cdev.fish changes behavior (bare names use ~/dev);
two additions provide codex/AGENTS.md and fish/functions/cnew.fish. All 19 copied
payloads passed hashes, modes, dependencies, references and private syntax parsers.
Global instructions preserve repository/upstream safeguards; cnew creates only a
main-branch repository with README.md, AGENTS.md and .gitignore, without commits,
remotes, application launches or direnv authorization. Explicit cdev paths, UUID
recovery, window reuse, layout, Doom and dashboard behavior remain unchanged.

72 focused tests passed (creation, cdev, UUID recovery, remote connection lifetime,
deployment/rollback). Additional staged and installed-file canaries used actual
Fish/Git, disposable homes and private tmux sockets with inert editor/Codex stand-ins.
They verified autoload, minimal scaffolding, repeat refusal, bare/absolute/relative/
current paths, exact private UUID pins, two-pane layout and no duplicate launch.
No real Codex lifecycle or iPhone delivery was retested for these shell-only changes.

Both new live paths were absent before migration. Independent schema-2 backups:
- codex-instructions: 20261025T062014.818188Z-883ab6a5
- fish-cnew: 20261025T062015.277953Z-57ee123b
Their journals preserve original absence and the exact current pointer; resulting
links resolve through current to verified read-only release payloads. All 16 managed
links and three unadopted absences passed post-deployment checks. The 16 current
protected process generations, all 11 current Collie pilot identities, session 2,
tmux sessions/windows/panes/client/bindings/hooks/formats, global Codex config/trust,
workmux hooks and production UUID pins remained unchanged. The dotfiles project
had naturally reopened before this task; current identities were baselined before
any mutation. No application reload/restart, service action, live event injection,
production pin write or push occurred. No rollback was needed.

If rollback is subsequently needed, restore BOTH new paths before the pointer
(the prior release lacks their payloads), using the existing tooling:

```sh
python3 -B ~/dev/dotfiles/scripts/deploy.py restore --backup 20261025T062015.277953Z-57ee123b --approve
python3 -B ~/dev/dotfiles/scripts/deploy.py restore --backup 20261025T062014.818188Z-883ab6a5 --approve
python3 -B ~/dev/dotfiles/scripts/deploy.py rollback --expect-current 20261025T061731.748309Z-45cef594 --approve
```

Existing Fish shells can retain their already-loaded cdev definition; new Fish
processes load the new version. Existing agents were not restarted for global
instructions. No required physical check remains for this workflow. Evidence and
exact migration plans: /private/tmp/df-project-workflow.MAygFP7K/.
