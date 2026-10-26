# Phase 3 Ghostty preparation — 2026-10-22

Preparation only. No production file, deployment pointer, binding, hook or service
was changed, and no application was reloaded during this investigation. The user
reports physical acceptance of the existing shortcuts after the Phase 2 reload.
Migration, Ghostty reload and any later tmux reload remain separate approvals.
The four preexisting modified documentation files were preserved unchanged;
their older staging-only status statements are superseded by the observations here.

## Focus-change finding

The saved attached-client snapshots show @2 active at 13:34:51 EDT and @7 active
at 13:35:28 EDT. The single source-file command ran from approximately 13:35:08.935
to 13:35:10.034 EDT. The evidence bounds the change to that 37-second interval;
it does not locate it inside or outside the reload itself. Window order, pane
selection within each window, server/client identities and process identities
were preserved.

Reviewed paths include the pinned configuration and dashboard helper, both
installed theme entry points, TPM and its startup helpers, the recorded
verification commands, and loaded global/session/window/pane hooks. Their
executed reload/monitoring paths contain no window-selection operation. The
dashboard's select-window/select-pane calls are confined to its attention
command, which was not invoked or bound. Its session-created[882] hook calls
watch, and its native @dotfiles-agents monitor calls refresh. Neither navigates.
Selection commands in key definitions are definitions, not commands executed by
loading those definitions.

The existing global Codex hooks contain six workmux set-window-status commands
and one register-agent command, with no explicit selection command. They and
workmux configuration were inspected without executing or changing them. This
does not prove what an independently invoked binary or user did historically.
The existing Doom after-make-frame focus hook is not loaded by the tmux reload;
no Emacs frame-creation command was issued by the reviewed reload/verification.

The tmux message history now contains 1,000 later entries and retains none of
the saved post-reload message hashes. No debug log was found at the exact
standard server/client locations checked, and none is open by the server.
The saved evidence contains message hashes, not a command/input trace.
The bounded macOS unified-log query was blocked with “Cannot run while sandboxed”;
no broader access, debug logging, signal or reproduction was attempted.

**Conclusion: historical cause is unresolved.** No evidence identifies loading
or verification as the cause. An external concurrent action is plausible but
unproven. Current hooks and reviewed execution paths reveal no automatic focus
change to repair. Conclusive attribution would require a contemporaneous trace;
none is available. Do not describe this as a proven external action.

During this preparation's read-only production observation (14:10–14:21 EDT),
active selection also changed from @2 to @5 without any production configuration
load. This shows that selection changes are not confined to reload operations;
it does not identify the actor or prove the earlier change's cause.

## Observed deployment and forwarding

- HEAD remains 8dad3727d022bdf59a8668feb53eb404e07b48c8; deployment code,
  manifest, configuration payloads and tests match that commit.
- current is releases/20261022T163617.469413Z-497daec6. All 15 payloads match
  the committed source after rendering and their receipt, with mode 0444.
  Integrity, dependency, reference and configuration-parser verification passed.
- Only the five existing tmux paths are adopted. Their links still resolve to
  that release. There is one original tmux backup and one applied activation
  history event; no pending migration/restore or Ghostty backup exists.
- Loaded n and c both run new-window -c "#{pane_current_path}"; N runs
  next-window. Prefix is C-f and @dotfiles-attention-installed is off.
- Existing live Ghostty is the regular mode-0644 file
  /Users/czuba/.config/ghostty/config.ghostty, SHA-256
  ce68f75b1a5da571a934a196eac1c116e70ad885450b13632217ab33c196cbf2.
  Its proposed managed link is
  /Users/czuba/.local/share/dotfiles-active/current/ghostty/config.ghostty.
- The candidate resolves to
  /Users/czuba/.local/share/dotfiles-active/releases/20261022T163617.469413Z-497daec6/ghostty/config.ghostty,
  mode 0444, SHA-256
  c4a5bf1f75b3bacb5892123a02ac0d80b56608cbb9c7c0fa4d324a2b950ccca2.

The entire Ghostty payload differs by exactly one line:

```diff
-keybind = super+shift+n=text:\x06n
+keybind = super+shift+n=text:\x06\x63
```

The installed Ghostty parser, using private HOME/XDG copies, produces bytes
06 6e for the old route and 06 63 for the new route. Every other text-forwarding
mapping is identical, including Cmd+1–9, pane shortcuts and the popup.
Both routes currently create a tmux window in its pane directory. Changing the
Ghostty file cannot enable attention: the monitoring watch path never rebinds
keys. Do not invoke prefix r or source tmux during this Ghostty phase.

The legacy XDG config is absent; the Application Support config is absent and
config.ghostty there is an empty regular file. No includes or parent symlinks
were found in the adopted Ghostty path. No ACL entries or file flags were shown;
the file has a com.apple.provenance extended attribute. The tool certifies bytes
and POSIX modes, not ACLs, provenance, resource forks or all macOS metadata.
An optional running-Ghostty argv probe was blocked by the sandbox; launch-time
CLI overrides and the GUI's in-memory configuration were not introspected.

## Reload behavior and process protection

Installed Ghostty 1.3.1's bundled ghostty.1.md, +edit-config (lines 185–190),
explicitly says configuration requires manual reload and automatic reload is not
yet supported. Bundled ghostty.5.md, reload_config, says runtime-supported changes
are re-read/applied; some settings cannot change at runtime. The parsed default
reload binding is super+shift+,=reload_config, or Cmd+Shift+,.

A running-GUI file-watcher test across symlink replacement has not been performed.
Retain the n/c bridge even if a file change becomes visible immediately. Both
old and new bytes are safe throughout migration and Ghostty reload. A later
strict dashboard preflight checks the file, not whether the GUI actually reloaded;
physical forwarding acceptance must precede attention activation.

The migration uses the already-current release, so it does not switch current.
It backs up the one exact Ghostty file before replacing it through an adjacent
symlink and atomic rename. It does not link the directory or touch tmux's five
paths. The deployment tool has no application restart, process termination,
client detach or tmux-window operation. Validators use CLI parsers and private
test servers; they do not open Ghostty windows. The only payload difference is
the forwarding line; shell/startup commands and existing windows are unchanged.

## Verified recovery and tests

The 38 existing deployment regressions passed. Two existing isolated integration
tests passed: the real Ghostty-parser → private tmux PTY forwarding bridge across
rollout phases, and explicit Ghostty validation ignoring unrelated defaults.
No production window was manipulated to reproduce the historical focus change.

A separate 14-check rehearsal used the real 15-file manifest, templates,
validators and deployment tool in a disposable home with inert dependency
fixtures. It verified Ghostty-only backup/migration/restore, exact bytes/modes,
the existing pointer text, all five tmux links and payloads staying unchanged,
repeat restore without replacement, interrupted migration recovery, and an
injected restore I/O error retaining a retryable restoring journal. Fixture
fault injection never targeted production. Failure did not report success.

Temporary recorder failures (directory-link hashing and a macOS xattr probe)
were corrected only in the temporary audit harness. One early isolated parser
probe failed before its diagnostics were recorded; subsequent serial live and
candidate parser checks and the forwarding regression passed. The isolated
Ghostty show-config action prints SentryInitFailed even with exit 0; this warning
was recorded, not treated as a configuration error or silently repaired.
No deployment code, staged payload or existing release was changed.

Final comparison preserved the Ghostty process and all recorded tmux/server,
client, pane-root and Codex process identities: one session, four windows, seven
panes, one client and three Codex processes. Deployment contents/metadata,
five managed links, loaded bindings/options/hooks and the four preexisting
modified documents were unchanged. No deployment lock holder or pending journal
was found. HEAD remains 8dad372; the only new repository file is this runbook.

## Proposed operations — run only after their individual approvals

Commands below use POSIX sh/Zsh from /Users/czuba/dev/dotfiles. They have **not**
been executed against production for migration or reload.

1. Immediately before approved migration, reverify the release and plan:

   ```sh
   python3 -B scripts/deploy.py verify --release 20261022T163617.469413Z-497daec6
   python3 -B scripts/deploy.py plan --release 20261022T163617.469413Z-497daec6
   python3 -B "$HOME/.local/share/dotfiles-active/releases/20261022T163617.469413Z-497daec6/tmux/agent-dashboard.py" preflight --socket /private/tmp/tmux-501/default --display-only
   ```

   Recheck current's exact text, the original Ghostty hash/mode/type above, three
   override guards, five managed tmux paths, no pending writer/journal, loaded
   n/c creation and attention off. Record fresh Ghostty/server/client/pane/Codex
   process identities. Stop on unexplained drift; the migration command has no
   expect-original-hash flag and must follow this immediate drift check.

2. With **Ghostty migration/backup approval only**, run:

   ```sh
   python3 -B scripts/deploy.py migrate --release 20261022T163617.469413Z-497daec6 --component ghostty --approve
   ```

   Record its printed GHOSTTY_BACKUP_ID. Verify the schema-2 journal contains
   exactly the one original regular file, mode 0644 and expected original hash.
   Its saved original is:

   ```text
   ~/.local/share/dotfiles-active/backups/GHOSTTY_BACKUP_ID/files/.config/ghostty/config.ghostty
   ```

   current_before and current_after must both equal the current release text.
   Verify the new link's exact text, resolved payload/hash/mode, unchanged pointer
   and tmux links/bindings, and process identities. Then stop. A migration error
   preserves evidence; it does not authorize automatic recovery.

3. After **separate Ghostty reload approval**, use Cmd+Shift+, once in the running
   app to invoke reload_config. Do not restart Ghostty or source tmux. Verify
   there are no new configuration errors and all recorded processes/clients
   survive. No Emacs, Fish or Codex hook adoption is part of this step.

4. Physical acceptance in a user-chosen test context: Cmd+Shift+N creates exactly
   one window in the intended directory; Ctrl+F c and Ctrl+F n still create;
   Shift+N navigates. Check Cmd+1–9, pane navigation, popup and Option+h/l movement
   without sacrificing working panes. Record acceptance and any naturally
   observed focus change. Automated parser/PTY tests do not prove GUI delivery.

5. Stop with attention off. Only after this acceptance may a later separately
   approved phase run strict preflight (without --display-only) and one tmux
   reload to enable n attention. That later action is not part of Phase 3.

## Independent Ghostty rollback

While attention remains off and n/c still create, obtain **separate restore
approval** and run from Terminal.app with /bin/zsh -f:

```sh
cd /Users/czuba/dev/dotfiles
python3 -B scripts/deploy.py restore --backup GHOSTTY_BACKUP_ID --approve
```

GHOSTTY_BACKUP_ID is a placeholder until an approved migration creates it; no
production Ghostty backup exists yet. Never substitute the original tmux backup
20261022T040111.754783Z-a455ecd7. Restore validates the saved bytes/mode and refuses
live-file/pointer drift. It reconstructs the original regular Ghostty file;
current, its release and all five tmux paths remain unchanged. Verify those
postconditions, then obtain separate Ghostty reload approval and physically
confirm the old n route. No tmux reload is needed for this Phase 3 reversal.

If attention has been enabled in a later phase, first obtain approval to disable
it and restore the n/c bridge before restoring Ghostty. If a restore fails, keep
its restoring journal, backup and releases; stop and review explicit recovery.
The same restore can be retried after its identified cause is resolved, with
the required approval. A successful repeat validates without replacing files.

Next single approval boundary: backup and migration of the one Ghostty file.
No technical payload or tooling blocker was found; historical focus attribution,
running-GUI watcher behavior and physical forwarding remain explicitly unverified.
