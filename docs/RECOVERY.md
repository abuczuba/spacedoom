# Recovery from macOS Terminal.app

These are future recovery operations. Agents need explicit approval before
changing an external file/pointer or reloading an application. Nothing here was
run on the live workstation during development. Equivalent filesystem operations
are tested in temporary homes, including macOS mv -h pointer replacement.

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
python3 scripts/deploy.py plan
```

After reviewing the current release and previous ID in deployment history,
and with rollback approval:

```sh
python3 scripts/deploy.py rollback --expect-current CURRENT_ID --approve
```

For initial migration failure, there may be no previous activation. Inspect the
recorded `backups/BACKUP_ID/backup.json`, then obtain restoration approval:

```sh
python3 scripts/deploy.py restore --backup BACKUP_ID --approve
```

Both operations preserve processes and perform no reload. The restoration tool
also removes newly introduced helper links when their originals were absent;
it retains empty directories and deployment releases/current for inspection.

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

Choose an unused adjacent temporary name. Then:

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
New helper links can be left temporarily for inspection; the normal restore
command removes only links recorded as originally absent. Do not delete an
unexpected regular file or link.

Restoring files or the pointer cannot change already loaded tmux bindings. Keep
using this independent Terminal shell. A tmux/Ghostty reload is a separate
approval and verification step; no restart, kill-server, Doom shutdown or Codex
termination is part of recovery.
