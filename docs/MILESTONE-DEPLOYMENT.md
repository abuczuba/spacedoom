# Dashboard automated rollout accepted — 2026-10-22

Release 20261022T215047.249499Z-618a6bc8 (e38e18d payloads) is active, both cdev
helpers are adopted with backup 20261022T215153.419622Z-a559508a, and the gated
attention reload passed. Native trust reuse and real production lifecycle/workmux
acceptance passed. Next is physical Ghostty acceptance only; persistent Doom
remains deferred. Use [DASHBOARD-ACCEPTANCE.md](DASHBOARD-ACCEPTANCE.md) for
current facts and recovery. Do not repeat any historical rollout steps below.
The documented recovery correction forbids reloading the full config after disable.

---

# Current dashboard rollout addendum — 2026-10-22

Phase 3B is complete; production is safely in n/c compatibility mode on
20261022T163617.469413Z-497daec6. The e38e18d repair has now passed
[isolated real hook acceptance](HOOK-ACCEPTANCE.md). Follow the
[remaining dashboard Phase 4 proposal](DASHBOARD-PHASE4.md) after renewed
authorization, including separate production native user review. Do not repeat
the historical Phase 1–3 steps or adopt Fish/Emacs components from the plan below.
No production changes are performed or authorized by this addendum. Existing
concurrent content is preserved as history.

---

# Proposed activity/Doom deployment and recovery

**Inactive staging complete; no activation, migration or reload.**
The finalized candidate is commit `8dad3727d022bdf59a8668feb53eb404e07b48c8`,
superseding 17c6f99. Its verified 15-file release ID is
`20261022T163617.469413Z-497daec6`; NEW_ID below means exactly that release.
See STATUS.md for retained commit-linkage, repeat-staging and continuity evidence.
The remaining sequence is a proposal and requires separate live approvals.
Production still uses:

```text
releases/commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16
```

The original five tmux links and backup 20261022T040111.754783Z-a455ecd7 remain
intact. Global Codex hooks, workmux settings, unrelated Fish/Doom files and
AeroSpace are outside this adoption. No live file has changed during development.

## Payload and exact new adoption targets

The complete candidate contains 15 regular payload files. Existing tmux mappings
stay unchanged. The Ghostty candidate changes **only Cmd+Shift+N forwarding**:
Ctrl+F n becomes Ctrl+F c, encoded explicitly as text:\x06\x63. The key still
creates a window in its directory; every other Ghostty mapping is unchanged.

| Payload/component | Exact live targets to adopt after separate approval |
|---|---|
| ghostty | ~/.config/ghostty/config.ghostty |
| fish-cdev | ~/.config/fish/functions/cdev.fish and cdev-pin.fish |
| doom-service | ~/Library/LaunchAgents/local.dotfiles.doom.plist |

Dashboard includes, Python helpers and doom/cdev.el are referenced directly in
the complete release. Their declared optional live targets under ~/.config/tmux,
~/.config/cdev and ~/.config/doom are unnecessary for this minimal adoption.
No whole directories, Doom init/config/Org files or Fish config.fish are migrated.

New sources are regular 644 files, released as 444, interpreted explicitly.
@RELEASE@ pins helpers; @HOME@ renders plist logs. Releases are home/path specific.
Preflight includes Python AST, Fish no-config syntax, Elisp reading/check-parens
without evaluation, plist structure, references, existing tmux/Ghostty/pager
checks and installed Emacs/Doom/Projectile/persp dependencies. No service starts.

## Why Ghostty must be coordinated

The old Cmd+Shift+N emits the same bytes as physical Ctrl+F n. Tmux cannot
reliably distinguish those inputs. Rebinding n alone would regress Ghostty's
new-window shortcut. The candidate therefore supports a safe **display-only /
legacy-navigation phase**: n remains new-window, c creates in the pane directory,
N selects the next window, and activity rendering works. Attention installation
is gated on the companion Ghostty mapping; background monitors never rebind keys.

A configured-file check is not proof that running Ghostty loaded it. A separately
approved Ghostty reload and physical delivery test precede the explicit tmux
reload that enables attention. Treat symlink migration as potentially immediately
observable: Ghostty watcher behavior remains unverified. Both old n and new c
create in the same directory during the bridge, so current sessions remain safe.
The apps cannot be switched jointly atomically. Do not start additional tmux
servers between Ghostty migration and its confirmed reload; existing main stays
in legacy mode until the second controlled tmux reload.

The isolated Ghostty-parser/PTY regression verifies this bridge with real input
bytes: old n creates before adoption; old n and new c both create through the
companion transition; only the later explicit tmux reload changes n to attention.
Physical acceptance must still confirm Cmd+Shift+N, Ctrl+F n/c/Shift+N, Cmd+1–9,
pane shortcuts and Ctrl+F then Option+h/l in the running Ghostty application.
Do not treat the file-based gate as GUI reload evidence or skip the bridge.

## First dashboard-only activation — proposed commands, NOT executed

Use Terminal.app with `/bin/zsh -f` available for independent recovery. These are
POSIX sh/Zsh commands; every mutation/reload below needs its own approval.
Recheck current, the five managed targets, backups, process identities and drift
immediately before each approved operation. No Fish or Emacs component is part
of this first activation.

```sh
cd /Users/czuba/dev/dotfiles
DASHBOARD_RELEASE=20261022T163617.469413Z-497daec6
DASHBOARD_PATH=/Users/czuba/.local/share/dotfiles-active/releases/$DASHBOARD_RELEASE
DASHBOARD_SOCKET=/private/tmp/tmux-501/default
python3 -B scripts/deploy.py verify --release "$DASHBOARD_RELEASE"
python3 -B "$DASHBOARD_PATH/tmux/agent-dashboard.py" preflight --socket "$DASHBOARD_SOCKET" --display-only
```

These read-only checks verify the copied release and legacy-mode compatibility.
After **display-only pointer activation approval**:

```sh
python3 -B scripts/deploy.py activate --release "$DASHBOARD_RELEASE" --expect-current commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16 --approve
```

This changes the shared pointer for only the five already-managed tmux files;
Ghostty stays a regular old file. It performs no reload. After separate first
reload approval, inspect plugin/hook drift, parse, then source exactly once:

```sh
tmux -N -S "$DASHBOARD_SOCKET" source-file -n /Users/czuba/.tmux.conf
tmux -N -S "$DASHBOARD_SOCKET" source-file /Users/czuba/.tmux.conf
```

`-N -S` prevents starting a server and selects the existing explicit socket;
`source-file -n` parses only; the second command loads config/plugins/installers.
Verify n remains directory-aware creation, c does the same, N selects next window,
and Cmd+Shift+N still creates. Do not use working panes as disposable fixtures.

After separate Ghostty migration approval and revalidated originals/backups:

```sh
python3 -B scripts/deploy.py migrate --release "$DASHBOARD_RELEASE" --component ghostty --approve
```

Record its actual backup ID. This adopts only the companion Ghostty file. The
installed 1.3.1 manual explicitly says auto-reload is unsupported, but no live
symlink-watcher experiment was performed; conservatively keep both n/c safe and
do not start new tmux servers during the transition. After separate GUI reload
approval, use Reload Configuration (documented Cmd+Shift+,) and physically verify
Cmd+Shift+N still creates and that the loaded forwarding is the c route. A file
check or headless parser alone is not that physical acceptance.

Only after that acceptance, run strict preflight and obtain separate second
reload approval:

```sh
python3 -B "$DASHBOARD_PATH/tmux/agent-dashboard.py" preflight --socket "$DASHBOARD_SOCKET"
tmux -N -S "$DASHBOARD_SOCKET" source-file -n /Users/czuba/.tmux.conf
tmux -N -S "$DASHBOARD_SOCKET" source-file /Users/czuba/.tmux.conf
```

The final source changes n to attention; c remains creation and N ordinary next.
Physically check Cmd+Shift+N, Ctrl+F n/c/N, pane/numeric/popup/workmux keys and
visual appearance. Existing conversations lacking event evidence remain
unlabelled. Current live cdev/helper lacks the new event bridge: real lifecycle,
Codex trust and shimmer/symbol acceptance in ordinary cdev sessions remain gated
on **separate launcher adoption approval**. Persistent Doom is independent and
must not be installed/started as a prerequisite; a separately approved standalone
editor route can be used later. Do not fake states or restart existing agents.

Independent reversal requires its own approval. Dashboard disable is the staged
helper's `disable --socket "$DASHBOARD_SOCKET"` action; it preserves jobs and
keeps c safe while Ghostty forwards c. To reverse Ghostty, disable attention
first, restore only its recorded backup with `deploy.py restore --backup ID
--approve`, separately reload Ghostty and physically verify its original n route.
Only then restore c's old default if desired. Full tmux reversal can subsequently
use `deploy.py rollback --expect-current "$DASHBOARD_RELEASE" --approve` to
restore ec518f0, followed by a separately approved old-config reload. Do not use
the original tmux unadoption backup for this feature reversal. No Fish/service
component was adopted by this slice, so their migrations/recovery are deferred.

## Exact approval sequence

Commands below are POSIX sh/Zsh, placeholders replaced only after inspection.
Each operation requires its own approval; --approve is only an accident guard.

1. **Completed: inactive staging of clean 8dad372.** The unchanged tool staged
   the exact 15-file manifest, including the one-line Ghostty companion, at NEW_ID.
   Every rendered blob/mode was compared with that commit and its receipt. Current
   stayed untouched. Repeated staging in an isolated fixture retained the first
   release unchanged and created a distinct second release. The production copy
   was staged once and verified repeatedly. Unique IDs are not idempotent reuse;
   commit-keyed/exclusive staging remains a separate follow-up. Do not restage
   merely to perform activation: verify this existing complete release.
2. Before activation, reverify NEW_ID, current OLD_ID, all five managed targets,
   original backups, dependencies, no pending journals and process identities.
   Run the inactive helper's read-only preflight --display-only on the explicit
   production socket. Strict preflight must report the missing Ghostty companion;
   that is the known full-navigation gate, not permission to ignore other failures.
   After **display-only activation approval**, run:

   ```sh
   python3 -B scripts/deploy.py activate --release NEW_ID --expect-current commit-ec518f0c6246a8e24b97627aecb74aad7b2d5f16 --approve
   ```

   This switches only already-managed tmux files. Ghostty remains its old regular
   file. No application reload or new path adoption occurs.
3. Approve the first controlled tmux reload for the explicit fallback. Inspect
   plugins/hooks, parse source-file -n, record identities, source ~/.tmux.conf once
   on /private/tmp/tmux-501/default, then verify display monitors and old n/new c
   both create in the pane directory. Cmd+Shift+N must still work. No existing
   window is reordered for testing. Existing conversations stay unlabelled without
   evidence. Preserve this bridge until Ghostty is confirmed loaded.
4. Obtain **separate Ghostty migration approval** for exactly its config file.
   Reverify the original regular file/hash/mode, empty/absent override guards,
   complete candidate, restore rehearsal, compatible n/c and watcher uncertainty.
   Back up/migrate through the established tool and record GHOSTTY_BACKUP:

   ```sh
   python3 -B scripts/deploy.py migrate --release NEW_ID --component ghostty --approve
   ```

   Only its managed symlink is adopted. Treat the key change as possibly immediate;
   no other Ghostty setting differs. No restart is authorized.
5. Approve a controlled Ghostty configuration reload and physical Cmd+Shift+N
   delivery test. Verify it now emits the c route and still creates in the same
   directory; preserve all existing windows/jobs. Then run strict dashboard
   preflight (no --display-only) and obtain **separate second tmux reload approval**.
   The explicit installer now enables Ctrl+F n attention; verify n/c/N, theme,
   popup, pane shortcuts, Cmd+1–9 and movement/focus without disposable use of
   working sessions. A failed preflight/reload stops; never infer authorization.
6. After service-file preflight/restore rehearsal, approve only the LaunchAgent
   migration and record SERVICE_BACKUP:

   ```sh
   python3 -B scripts/deploy.py migrate --release NEW_ID --component doom-service --approve
   ```

   Installing this file is its own boundary: RunAtLoad can affect the next login.
   It does not authorize bootstrap. Audit existing named/default servers, runtime
   permissions and legacy Doom cache/workspace overlap before production startup.
7. Separately approve python3 -B scripts/doom_service.py bootstrap --approve.
   It verifies the managed plist/release, singleton/socket state and private logs,
   then starts one new named daemon. It never replaces legacy editors. Verify
   readiness/socket ownership/job logs. No automatic restart loop, package install,
   stale-socket deletion or default-server fallback. Preserve failures and stop.
8. Approve migration of exactly the two Fish functions and record FISH_BACKUP:

   ```sh
   python3 -B scripts/deploy.py migrate --release NEW_ID --component fish-cdev --approve
   ```

   New shells/autoloads can see these immediately; existing definitions may remain
   loaded. Source the two files in the intended Fish shell only after separate
   reload approval. Existing project windows are reused as-is, never converted.
9. Physical acceptance on chosen projects: two client frames, nested files,
   scratch/workspace switches, reconnection, frame-root SPC f f/local C-x C-f,
   no duplicate on reuse, actual Codex lifecycle/trust (including repeated trust
   review), state visuals and n cycling. Never bypass trust or use live agents as
   disposable tests. Private Org/custom configuration and login/reboot behavior
   remain separate checks; do not interrupt active work to obtain them.

Each migration copies/verifies originals and records absence before replacing
any path. Independent renames are not jointly atomic. A partial failure preserves
its prepared journal and requires the established separately approved restoration
protocol. No implicit rollback, reload or service recovery follows any command.

## Independent and full rollback

From Fish, to change only editor launching, use CDEV_EDITOR_MODE=standalone cdev PROJECT
for new windows. To omit observer hooks use CDEV_DASHBOARD=0 cdev PROJECT.
Neither changes an existing window or discards the named daemon's buffers.

For dashboard-only recovery, approve its disable command on the explicit socket.
It restores n as directory-aware creation, removes its monitors/title slot and
owned N, restores interval/workmux detection, and retains c's directory behavior
while Ghostty forwards c. Doom and conversations remain running.

For a complete milestone rollback, use Terminal.app with /bin/zsh -f. Every
mutation requires its own approval:

1. Save buffers and deliberately close named-server clients, then approve
   doom_service.py bootout --approve before removing its plist. The tool refuses
   active clients, modified buffers or unverifiable state. Do not use the legacy
   Fish toggle, default-server kill-emacs or pkill. An unresponsive job needs logs
   and reviewed exact launchctl bootout gui/UID/local.dotfiles.doom recovery.
2. Approve dashboard disable first, making both n and c safe creation routes.
   Restore GHOSTTY_BACKUP while current is NEW_ID, returning the exact original
   regular file/mode. Treat this as potentially immediate, approve Ghostty reload,
   and physically confirm the original n route. Only then restore c's former
   default with an explicitly approved bind-key c new-window on the existing
   server. No server/window/process restart is needed.
3. Restore SERVICE_BACKUP and FISH_BACKUP through deploy.py restore --backup ID
   --approve. They restore exact originals/modes/absence, leaving current at
   NEW_ID. Restore any additional optional component backups if individually
   adopted. Explicitly source original Fish functions/use a new shell after
   approval; loaded definitions and existing processes do not follow pointer swaps.
4. Now deploy.py rollback --expect-current NEW_ID --approve can restore ec518f0.
   The tool correctly refuses this while new Fish/service mappings remain: old
   ec518f0 lacks them. The multi-component refusal and restore ordering are tested.
   Verify the five original managed tmux links, then separately approve one old
   tmux reload and acceptance. No auto-recovery operation is implied.

Keep every referenced release and original backup. Running agents may retain
pinned hook paths after rollback. The original tmux backup is reserved for complete
unadoption, not this feature reversal; see RECOVERY.md for files-before-pointer,
drift/dependency guards and independent recovery.
