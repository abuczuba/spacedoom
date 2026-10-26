# cdev acceptance-fixture isolation

Current result: d84baaa is deployed and verified. The revised isolated sequence
and activated-launcher canary both passed, prioritizing two genuine remote
resumes before an independent real approval check. See the final section below.
Earlier native fresh-only results remain **local-only** evidence. The standing
bounded-work policy authorizes completing clean validated rollouts without a
routine additional approval gate; substantive new risks still require review.

The two production retries failed in the fixture, before real lifecycle
acceptance. `cdev` runs its first Python `plan` command in the invoking Fish
environment. Its `tmux new-window` and independent `tmux split-window` commands
create processes from tmux's **server/session** environment. Neither inherits
the invoking Fish pane's environment, nor does a split inherit the editor pane's
environment. The absolute helper path selected by Fish still reached the private
shim, whose XDG guard then correctly refused the inherited, nonprivate state.

## Corrected fixture and offline check

`tests/acceptance_harness.py` and `tests/fixtures/acceptance_probe.py` provide a
private socket, empty tmux startup configuration, clean environment allowlists,
and an argv wrapper which adds repeated `-e KEY=value` to **both** `new-window`
and `split-window`. It pins every tmux call to its private socket and rejects
alternate `-S`/`-L` options. It never changes tmux's global environment. The
server deliberately starts without the private XDG variables, so the test
cannot accidentally pass because its server already had the right environment.

The actual control Fish, preflight Python, editor probe and nested launcher
report their own allowlisted environment/path checks and PID/pane relationships.
The launcher remains gated until these pass; the test preflight helper does not
call the source `plan()` or write pins. After that gate, the unchanged session
helper launches an inert agent, whose real child invokes the private adapter
with an empty, invalid event. The agent, adapter and independent backend probe
are checked too. Only then may synthetic saved metadata exercise the real pin
writer. No native Codex, Emacs, login, actual event or ntfy publish runs here.

HOME, all XDG directories, CODEX_HOME, temporary/cache files and UNIX sockets
are under one owner-only fixture root. Path guards reject escape or symlink
redirection. The production activity module has a fixed account-wide remote
registry; the fixture rebases **that module attribute in its private processes**
to its own runtime directory, including in the private adapter. No release file,
hook definition or identity check is changed. This is configuration isolation,
not an OS filesystem jail or evidence of native Codex delivery.

Authentication is absent: no credentials are read/copied, credential environment
variables are not inherited, and the private profile specifies
`cli_auth_credentials_store = "file"`. Codex documents this as storage under
`CODEX_HOME/auth.json`, rather than the OS credential store:
[official authentication documentation](https://learn.chatgpt.com/docs/auth#credential-storage).
Native credential resolution has not been exercised by these inert tests.

Run against the clean signed export, excluding all pending repository features:

```sh
DOTFILES_ACCEPTANCE_SOURCE=/private/tmp/df-remote-release-hp41x7a8/export-d84baaaf7613f9c6232c6f6c2e28644527111cda \
  python3 -B scripts/test.py --integration --match '*AcceptanceEnvironmentTests*'
```

Seven regressions cover variables sent only to a tmux client, the broken
control-pane-only fixture, a partial new-window-only
fix, every actual descendant and state destination, socket/credential guards,
two concurrent fixtures with identical pane numbers, and shared-server hook
environments with an older pane marker/executable-shim PATH. The fixture does
not impose a second event-attribution rule: the unchanged source adapter owns
UUID/process-generation validation. A mutation check also
confirmed the positive descendant test fails when per-pane propagation is
disabled. Fixtures clean up only their owned private sessions/processes/files.

The locale correction adds four focused checks, for twelve harness regressions
in total (the earlier native-profile TOML guard is also included). Together with
five subscription/reader checks, all seventeen focused tests pass.

## Proposed final acceptance, requiring new authorization

1. Before production activation, rerun the offline gate against the exact
   prepared release and freeze the tested environment/pane wrapper. Verify the
   actual nested launcher, not just a control pane. Keep state/pins/cache/socket
   paths private for every subsequent launch; never restore the old production-
   profile fallback or remove the guard. Any new pane must pass the guard again.
2. For genuine turns, obtain a separately authenticated disposable Codex profile
   through the user's native login, without copying production credentials.
   Verify effective file-based credential storage; stop if managed policy
   requires another store. Preserve all approval/sandbox requirements. Use a
   private shared backend and the private registry/adapter; never attach this
   profile to production's authenticated backend. Private hook paths require
   native user review; production trust must not be assumed to transfer.
3. Test the immutable candidate before touching `current`: genuine fresh turn,
   working/shimmer, stopped/dot/attention, genuine approval canceled without
   automatic approval, normal exit, exact private UUID recovery twice, repeated
   transitions, deduplicated HTTP delivery, and clean reader/process exit.
   Record metadata only; visual and iPhone receipt require the user. Keep the
   tested wrapper/environment for acceptance rather than building another
   unverified fixture after activation.
4. Only after these pass, recheck production drift/identities and activate
   `20261024T235701.367069Z-b1475572` once, expecting
   `20261023T164459.630188Z-30124092`. Verify all 17 payloads, 14 live links,
   three unadopted absences, hooks/bindings, pins and protected processes.
   No tmux/service reload is needed. Existing agents transition naturally.
5. Any critical failure after activation uses the documented atomic rollback
   and stops. No speculative repair or automatic retry; pins are not part of
   release rollback. No activation, authentication or real-turn step above is
   authorized by the offline harness task.

The signed d84baaa payloads need no change for this correction. The implementation
is confined to test support and documentation, outside the production manifest.


## Native validation finding — 2026-10-24

The first genuine turn delivered working/stopped events but failed display
acceptance. The fixture's LC_ALL=C replaces tabs in tmux metadata with
underscores, breaking the renderer callback parser. Read-only UTF-8 queries
preserved the fields. The offline environment-path tests did not cover this
callback contract. Native approval/resume tests were stopped, without retry.
Before any further native run, a separately approved fixture-only correction
must use UTF-8 consistently and test tab-delimited metadata and the background
callback itself. No locale correction or production activation has been applied.
STATUS and /private/tmp/df-native-validation-zq_dsewa/ contain the exact evidence.

## Verified locale correction and native outcome — 2026-10-24

The fixture now sets **both LC_ALL and LANG to en_US.UTF-8** in its clean server
and client/pane environments. `/usr/bin/locale charmap` must report UTF-8 before
server creation. A non-UTF-8 locale fails preflight. The production code and
immutable release are unchanged.

The test-only `renderer_callback.py` invokes the unchanged renderer through the
actual installed tmux background monitor/timer, records its metadata reads, and
allows its real private tmux writes. Controlled synthetic cache input tests the
formatter without claiming native lifecycle delivery. The old C fixture is
deliberately recreated only in its negative test.

Exact metadata received by background callbacks:

| Callback locale | Codeset | Window metadata | Result |
| --- | --- | --- | --- |
| C | US-ASCII | `@0___` (zero tabs) | ValueError: expected 4 fields, got 1 |
| en_US.UTF-8 | UTF-8 | `@0\t\t\t` (three literal tabs) | Source callback updates/rendering succeed |

The UTF-8 test exercises working animation, stopped dot, waiting alert and idle,
plus real cdev reuse without a duplicate agent. Audit covers server/client
locale, explicit per-pane env, launcher-before-exec checks, callback shell and
Python interpreter, metadata parsing, explicit private socket/state arguments,
file-only auth, the private remote registry and absence of inherited secrets.
Callback HOME intentionally remains the private server-home; its state path is
an explicit private CLI argument. Production process-start parsing deliberately
uses C for ASCII `ps` output and needs no change.

The retained authenticated profile was safely reused with the identical eight
trusted commands/hashes; no login or hook review was repeated. A genuine fresh
0.164.0 turn passed: eight distinct native shimmer frames, white dot and matching
completed-turn metadata. A genuine PermissionRequest also produced the red alert.
No callback errors occurred and all observed callback locales were UTF-8.

The full native sequence nevertheless **stopped** at an invalid extra check in
the test driver: fresh cdev used local hook ancestry (no `--remote`), while the
driver asked the separate shared endpoint for `waitingOnApproval`. That endpoint
was not established as the fresh thread's runtime owner. `thread/read` can read
stored metadata without loading/subscribing to the thread; see the
[official app-server documentation](https://learn.chatgpt.com/docs/app-server#read-a-stored-thread-without-resuming).
The required two resumptions were not run, and there was no automatic retry.

The proposed verification correction is owner-aware: use the validated native
PermissionRequest/rendered alert for local mode, and require shared-server
active flags only after verifying the remote owner. This correction has NOT
been implemented or rerun. No production change follows from this test failure.

Evidence: `/private/tmp/df-native-validation-zq_dsewa/utf8-validation/`, especially
actual-callback-locale-comparison.json, fresh-turn.json, failure-diagnosis.json
and FINAL-RESULT.json. All disposable processes/servers are stopped and reaped;
the owner-only profile remains in place with its private test UUID pin for review.

## Validated shared-backend coverage — 2026-10-24

Inspection established the actual topology rather than assuming every launch is
remote. Both the production and signed d84baaa cdev implementations launch a new
conversation as `codex --cd PROJECT` with eight invocation-local hook overrides.
Pinned recovery launches `codex resume UUID --cd PROJECT --remote unix://SOCKET`
with the same overrides. All four protected production TUIs have the remote
argument; a read-only kernel peer check confirmed one live production client
connects to its shared app-server. Earlier fresh-only runs never covered this
remote path and must not count as remote-resume acceptance.

The fixture now replaces the invalid stored-thread ownership assertion with
`tests/acceptance_ownership.py` and the same-account, read-only macOS socket
probe `tests/fixtures/proc_unix.c`. Before and during remote turns it requires:

- Matching live launcher/client/backend process generations and child ancestry.
- The exact requested UUID and private `--remote` endpoint, with no local fallback.
- Reciprocal kernel socket peers for both TUI -> backend and retained hook-setup
  connection -> backend, plus that UUID in the connected backend's loaded list.
- Lifecycle session/turn attribution consistent with those live identities.

Local fresh mode is positively classified by local process ancestry, no remote
registration/connection, no shared loaded UUID, and an actual pending hook that
remains paused until cancellation. Shared `waitingOnApproval` is required only
after proving the remote owner. Stored `thread/read` metadata alone proves
neither local nor remote ownership. The private backend has zero global dashboard
hooks and zero hook overrides at startup, so it cannot mask the original defect.

All **24 focused checks** passed: 13 environment/callback/publisher checks, six
ownership checks and five subscription/reader regressions. Negative checks reject
the original early setup-connection close, stored metadata without a live TUI,
wrong process generation/endpoint and nonreciprocal peers. UTF-8 and per-pane
isolation remain mandatory; no production payload changed.

One native 0.164.0 run passed local fresh -> remote resume -> remote resume, all
using UUID `01a17123-36ad-7573-89da-155484a56db5`. Each cycle produced a genuine
completed turn, working animation (8/7/7 distinct rendered frames), white dot,
real permission request/red alert, keyboard attention selection, canceled-request
empty-queue preservation and normal exit. Both remote approvals independently
reported `waitingOnApproval` from the proven connected owner. All eight unchanged
definitions remained trusted. No approval, login, repeated trust or retry occurred.

The real publisher consumed these real transitions through a **local recording
transport**: exactly three priority-3 stopped and three priority-4 approval records,
one attempt each, no startup replay/duplicates. HTTP delivery and iPhone receipt
were not tested. All 27 actual background callbacks succeeded under UTF-8.
Private launchers, clients, backend/descendant and tmux server exited; stale owned
socket nodes were removed. The private authenticated profile remains owner-only.

Metadata-only evidence: `/private/tmp/df-native-validation-zq_dsewa/remote-validation/`,
especially `native-result.json`, `cycle-1-startup-ownership.json`,
`cycle-2-startup-ownership.json`, per-cycle turn/approval/navigation/notification
checks and `continuity.json`. Production remains
`20261023T164459.630188Z-30124092`; signed d84baaa candidate
`20261024T235701.367069Z-b1475572` is unchanged and inactive. No further native
retry or production activation follows automatically from this result.

## Primary regression first; controlled approval independently — 2026-10-25

Read-only diagnosis of the last canary established a fixture failure. Its normal
turn made two sleep tool calls. The approval-test turn started and stopped with
**zero tool calls**: no ps command or escalation was attempted. Both turns reached
the intended registration and rendered stopped state. No real PermissionRequest
was exercised; waiting 100 seconds did not demonstrate lost hooks, rejected
attribution or a rendering regression. Only metadata from the exact owned test
rollout was extracted; messages, arguments and responses were not recorded.

The minimal acceptance order is now:

1. Fresh cdev turn -> working/stopped, native rendered shimmer/dot and attention.
2. Normal exit -> exact-UUID remote resume -> another genuine working/stopped turn.
3. Repeat exit/resume once, with the same live ownership checks. Record primary
   PASS before any approval probe. Preserve hook trust, clean exits and no replay.
4. Independently run `/bin/echo dotfiles-approval-probe` under an explicit
   `decision="prompt"` prefix rule installed only in the disposable CODEX_HOME.
   Check that rule with native `codex execpolicy check` before launch. Confirm
   actual owner waitingOnApproval, correctly scoped waiting cache and red alert;
   cancel without approval. Remove the private rule during cleanup.
5. Verify deduplicated transitions and production continuity. A stopped turn with
   zero tool calls is an inconclusive approval fixture, not a failed launcher.
   A genuine pending approval whose event is lost/rejected/misrendered remains
   a real failure. Never waive identity/trust checks or automatically approve.

`tests/acceptance_evidence.py` supplies the harmless rule and metadata-only reader.
Four focused regressions cover the actual no-tool case, privacy, unrelated-project
rejection and the native rule's exact match/control command. All 28 focused checks
passed. The signed repair and production payloads were unchanged.

Both revised genuine 0.164.0 runs passed all phases. Isolated evidence:
`/private/tmp/df-native-validation-zq_dsewa/revised-isolated/`. Final activation and
canary evidence: `/private/tmp/df-native-validation-zq_dsewa/final-rollout/`.
The canary imported the installed managed active launcher through a verified
read-only alias, with its old source copy moved aside. Its private profile,
sockets, pins, state, UTF-8 callbacks and stable hooks remained isolated.

Release `20261024T235701.367069Z-b1475572` is active. Canary UUID
`01a1719e-cd49-7832-89ee-3b6f5621dfc2` resumed remotely twice; rendered working
frames were 8/9/9, all stopped dots/attention checks passed, and the genuine
approval showed the red alert before cancellation. Four publisher records
(3,3,3,4 priority) were deduplicated through a local recording transport;
HTTP/iPhone receipt was not tested. All owned resources/rules/aliases were cleaned
up; the owner-only authenticated profile is retained. No final rollback/reload/
agent restart occurred. Original production sessions/pins/hooks and current
Collie pilot identities remained intact; a previously recorded pilot client 6413
was already absent before this validation, with no cause attributed.
