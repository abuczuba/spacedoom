# Proposed activity/Doom deployment and recovery

**Plan only. This milestone has not been staged, activated or reloaded.**
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

## Exact approval sequence

Commands below are POSIX sh/Zsh, placeholders replaced only after inspection.
Each operation requires its own approval; --approve is only an accident guard.

1. **Next: inactive staging only.** Approve the final clean commit and exact
   15-file manifest, including the one-line Ghostty companion. Run deploy.py check,
   stage with deploy.py stage --approve, record NEW_ID, then verify every rendered
   blob/mode against that commit and receipt. Current stays untouched. The checked-in
   stage command still uses unique IDs; commit-keyed idempotence/exclusive staging
   remains a separate follow-up. Do not imply stage is commit-independent/idempotent.
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
