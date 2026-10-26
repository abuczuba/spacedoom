# Recovery from macOS Terminal.app

Use the current task authority and exact recorded IDs. Repository edits alone
do not authorize recovery. File/pointer recovery never implies an application
reload or process restart. Equivalent filesystem operations are tested in private
homes, including macOS mv -h pointer replacement.

## Get an independent shell

Open Terminal.app from Spotlight or Applications → Utilities. Use its Shell →
New Command action to run `/bin/zsh -f` directly, without running inside the
configured login shell. This skips user Zsh startup files and does not require
Ghostty, Fish, tmux, Doom or Codex. Leave existing application processes alone.

Commands below are for that clean Zsh/POSIX shell. No sudo or system changes are
needed. Use the IDs recorded during staging/migration/activation; do not guess a
release from its timestamp alone. Stop on any error or unexpected symlink.

## Preferred: use the standard-library tool

If Python and the repository tooling work:

```sh
cd "$HOME/dev/dotfiles"
python3.12 scripts/deploy.py plan
```

After reviewing the current release and previous ID in deployment history,
and with rollback approval:

```sh
python3.12 scripts/deploy.py rollback --expect-current CURRENT_ID --approve
```

For initial migration failure, there may be no previous activation. Inspect the
recorded `backups/BACKUP_ID/backup.json`, then obtain restoration approval:

```sh
python3.12 scripts/deploy.py restore --backup BACKUP_ID --approve
```

Both operations preserve processes and perform no reload. The restoration tool
first restores original files and removes helper links recorded as originally
absent. It then returns current to the recorded current_before state: null means
remove it, otherwise preserve the exact prior symlink target. Releases, backups
and empty directories remain for inspection. Backup journal schema 2 is separate
from the unchanged schema-1 release receipt/manifest; existing releases do not
need to be restaged.

Review current_before, current_after, entries and targets in backup.json before
restoration. The observed pointer must match current_after. An interruption
before migration creates current, or after restore removes it but before journal
finalization, is also recoverable when every original file is already restored.
Unexpected pointer/file changes are refused, including on a repeated restore.
Never replace unexpected state merely to silence that refusal; review what
changed and obtain approval for its recovery.

If restore fails partway, keep the backup, releases and journal. A restoring
status blocks new migration/activation. After reviewing and resolving the cause,
retry the same approved restore command; it validates and skips completed work.
Even failure after pointer removal but before journal finalization is retryable.
Repeating a completed restore validates the recovered state and succeeds without
new file/pointer writes. A failure returns nonzero and prints no success message.

If another component still links through current, restore its backup before the
backup that originally created current. The tool checks all declared live paths
across backup journals, including relative links and symlink aliases, before
removing the pointer. An unresolved symlink chain fails safely; recovery does
not scan arbitrary home files for undeclared targets. A separately activated
release must be rolled back through its
own approved operation before initial-migration restoration.

Legacy schema-1 backup journals do not identify the prior pointer state. The
tool refuses automatic restoration of those journals; use a reviewed manual
plan and independent evidence instead of guessing. No production backup existed
when schema 2 was introduced.

## Emergency: change the pointer without Python or applications

Use this if normal validation/tooling is broken. It requires only macOS shell
utilities. Review the known working ID in your saved record or `history/` JSON.
This deliberately bypasses normal parser/hash validation, so inspect the release
and exact pointer carefully and obtain approval for this recovery operation.

```sh
cd "$HOME/.local/share/dotfiles-active"
/usr/bin/readlink current
/bin/test -r releases/KNOWN_GOOD_ID/release.json
/bin/test -r releases/KNOWN_GOOD_ID/tmux/tmux.conf
```

First ensure the known-good release contains every currently managed mapping.
If it predates newly adopted files, restore those component backups first; a raw
pointer flip must not leave new live links dangling. Choose an unused adjacent
temporary name. Then:

```sh
/bin/ln -s releases/KNOWN_GOOD_ID .current-recovery-UNIQUE_ID
/bin/mv -fh .current-recovery-UNIQUE_ID current
/usr/bin/readlink current
```

`mv -h` is macOS-specific: it replaces the directory symlink itself instead of
following it and moving a file into the release. Both paths are in the same
directory/filesystem, so this is an atomic rename. The temporary name must not
already exist; never use ln -f. This operation is covered by a temporary-directory
test. It does not append a normal tool history event; record the manual recovery
before resuming normal release work.

## Emergency: restore original regular files

If the first migration failed, restore the specific originals from its recorded
backup rather than guessing a prior release. First inspect `backup.json` and
confirm each target still has the expected managed link. The initial tmux
proposal has three pre-existing files; only use this sequence if that matches
the actual journal. Backups preserve file bytes and POSIX modes.

For example, restore the main config through an adjacent file, replacing the
symlink rather than writing through it:

```sh
/bin/cp -p "$HOME/.local/share/dotfiles-active/backups/BACKUP_ID/files/.tmux.conf" "$HOME/.tmux.conf.recovery-UNIQUE_ID"
/bin/mv -fh "$HOME/.tmux.conf.recovery-UNIQUE_ID" "$HOME/.tmux.conf"
```

Apply the same reviewed method to `.config/tmux/czuba-navigation.conf` and
`.config/tmux/cheatsheet.txt` from that exact backup. Do not copy a whole
directory or write with cp directly through a live symlink. Inspect permissions
with `ls -l`. Preserve backups and all releases until recovery is accepted.
The normal restore command removes only links recorded as originally absent.
For manual recovery, inspect each helper link against that journal and remove
only the exact expected managed link. Do not delete an unexpected file or link.

**Restore the pointer last.** Before removing current, check every declared
target in the journal and other backup journals (including other components),
and any known manually created aliases. All links that depend on current must
be gone. Do not recursively scan private home data. If dependency checks are
uncertain, leave the pointer in place and obtain a reviewed recovery plan.

Only if current_before was null, current still matches current_after, all file
restores have been verified and no live link depends on it, the approved final
manual step is:

```sh
/bin/rm "$HOME/.local/share/dotfiles-active/current"
```

If current_before recorded an existing link, preserve/restore that exact text
using the adjacent ln + mv -fh method above; do not derive a different spelling
from its resolved path. Preserve backup.json rather than marking manual recovery
complete by hand. Review the resulting file/pointer states before resuming the
tool, and never run a deployment writer concurrently with manual recovery.

Restoring files or the pointer cannot change already loaded tmux bindings. Keep
using this independent Terminal shell. A tmux/Ghostty reload is a separate
approval and verification step; no restart, kill-server, Doom shutdown or Codex
termination is part of recovery.


## Activity dashboard and named Doom server

Dashboard and named Doom are deployed; STATUS records actual releases/backups.
Restore newly adopted component files before rolling back to a release lacking
their mappings. Preserve Ghostty's verified c forwarding when disabling attention;
do not follow historical milestone commands as if they were current state.

Doom identity is an external mode-600 override. Restore the original Doom config
before retiring an identity sidecar created for an import, and remove it only if
its exact recorded hash still matches. Generated Custom, Codex hooks/trust/auth,
pins, workmux preferences and Collie state are not restored by a desktop rollback.

Terminal.app with /bin/zsh -f remains sufficient to run the deployment tool,
inspect the named service log and restore files. The service's manual foreground
fallback, after its own approval, is:

```sh
/usr/bin/python3 -B /ABSOLUTE/RELEASE/cdev/doom-server.py serve
```

Use only the named socket. Never use the old Fish daemon toggle, default-server
kill-emacs, pkill or a process-name search as authority to terminate editors.
Explicit dashboard disable leaves buffers/conversations alive. Editor launch
fallback does not stop the persistent daemon. Save buffers/close its clients and
approve shutdown separately before unloading a healthy service. Unresponsive or
unexpected socket/manager state requires preserved logs and reviewed exact-job
recovery, not automatic deletion or restarting. Keep all referenced releases:
existing processes may retain pinned helper/hook paths after a pointer rollback.
