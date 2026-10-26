# Development and copied releases

The development checkout, immutable copied releases and live file symlinks are
three separate layers. Git commits, branch changes and tests never deploy or
reload anything. `AGENTS.md` defines standing permissions; the current task still
controls operational authority. `--approve` is an accident guard, not consent.

## Develop and verify

1. Read STATUS and relevant source. Compare exact live files/links, the current
   receipt, hooks, private-config hashes and process identities with the accepted
   baseline. Preserve manual edits and concurrent work; investigate unexplained drift.
2. Make the smallest change. Run focused tests and nearby regressions. Use the
   full suite for cross-cutting work. Private integration servers use explicit
   sockets, empty startup config and owned processes; never production panes.
3. Stage only reviewed files. Run `python3.12 scripts/preflight.py`,
   `git diff --cached --check` and inspect the staged diff. Preserve SSH signing.
4. Commit locally. Publication, authentication, hook trust, application reloads,
   service operations and destructive changes remain separately controlled.

Historical rollout notes are retained in Git and dated documents. They are
engineering evidence, not instructions to repeat an old migration or trust gate.

## Validate and stage

From a clean checkout (or verified clean Git export):

```sh
python3.12 scripts/deploy.py check
python3.12 scripts/deploy.py plan
python3.12 scripts/deploy.py stage --approve
python3.12 scripts/deploy.py verify --release NEW_ID
python3.12 scripts/deploy.py plan --release NEW_ID
```

The existing standard-library tool renders `@RELEASE@`/`@HOME@`, validates the
complete manifest/dependencies and writes hashes, modes and a receipt before
renaming its staged directory into `releases/ID`. It copies regular source
files, never hardlinks or checkout symlinks. Payloads lose write permission;
programs needing executable mode retain it. Every stage gets a unique ID; no
existing release is overwritten. Commit-keyed idempotent staging remains an
explicit future improvement, not a property claimed by this tool.

Keep release provenance with the operation: commit/signature, clean-export
hashes, exact changed payloads, expected current, managed mappings, validation
results and rollback target. Do not stage a dirty checkout as if it were HEAD.
The root is normally `~/.local/share/dotfiles-active`. `--repo`, `--home` and
`--state-root` support disposable tests; paths must remain disjoint and safe.

## First adoption of exact files

```sh
python3.12 scripts/deploy.py migrate --release CURRENT_OR_FIRST_ID --component COMPONENT --approve
```

Each component backs up every original regular file with contents and POSIX
mode, records absent paths, and verifies all backups before replacements.
Backups live at `backups/BACKUP_ID/files/` with `backup.json`. Only exact files
are linked through `current`; unknown symlinks/redirected parents are refused.
A later component must use the already-current release. No whole config tree
is adopted, and application state is excluded from the manifest.

Each replacement is atomic, but the collection of file links is not jointly
atomic. Stage all referenced files first and plan include/migration ordering.
An interrupted migration leaves a prepared journal and requires explicit restore;
it never silently reloads or rolls back applications. ACL/resource-fork backup
preservation is not certified; the tested contract is contents and POSIX mode.

Private Doom identity stays in a separate mode-600 file. Preserve it before
adopting a sanitized public config, and retain the original config in its migration
backup. Generated Custom, Fish variables, Codex trust/auth/pins and Collie state
remain writable/external; never turn them into read-only release payloads.

## Activate and roll back

```sh
python3.12 scripts/deploy.py activate --release NEW_ID --expect-current OLD_ID --approve
python3.12 scripts/deploy.py rollback --expect-current NEW_ID --approve
```

All already-managed paths share this pointer, including other applications.
Compare every payload, not just the requested component. Activation takes the
existing writer lock, refuses pending migrations and drift, validates both
releases, records a prepared history event, atomically renames `current`, then
marks the event applied. Rollback validates the previous release and makes
another logged pointer switch. Neither operation reloads/restarts anything.

A single pointer rename is atomic; independent reads across the rename are not
a distributed transaction. Release-pinned tmux includes avoid mixed reloads.
Retain old releases: loaded bindings and services may still reference them.
Files are immutable by convention, not resistant to their owner deliberately
changing permissions; receipt verification detects those changes.

If new paths were adopted after an older release, restore their component
backups before rolling back to a release lacking them. The tool refuses missing
managed mappings. Record backup IDs in STATUS, not in a public runtime-state file.

## Restore initial files / interrupted adoption

```sh
python3.12 scripts/deploy.py restore --backup BACKUP_ID --approve
```

Restore components in reverse adoption order. It validates backups and expected
live states first, restores files/modes or removes only links originally absent,
then restores the pointer's exact prior target/absence. `current` cannot be
removed while a remaining managed link depends on it. Unexpected file or pointer
changes are refused. A partial failure leaves a retryable restoring journal;
successful repeats validate state without deleting unrelated data. Legacy
schema-1 backups cannot prove original pointer state and require manual review.

## Reload and service effects

| Configuration | Takes effect |
|---|---|
| tmux bindings/theme | New server or explicit `source-file`; plugin startup runs on reload |
| tmux cached titles | Existing renderer callbacks; native shimmer creates no per-frame process |
| cdev Python | Next launcher/hook process; loaded retained readers need natural reopening |
| Fish startup/functions | New shell/autoload or an explicit user source; loaded definitions persist |
| Doom config | Normal new startup; active daemon/clients are not replaced |
| Ghostty | Explicit manual reload for supported settings; new surfaces for some settings |
| AeroSpace | New startup or explicit reload; default auto-reload is off |
| Git / gh | Next invocation reads the config |
| LaunchAgent | Separate explicit install/bootstrap; loaded definition may still pin an old release |

Ghostty's installed 1.3.1 manual says automatic config reload is unsupported;
symlink-watcher behavior was not physically certified. Preserve its verified
`Cmd+Shift+N → Ctrl+F c` chain before enabling attention on `n`. A full tmux
reload re-enables the dashboard; do not use one as a dashboard-disable recovery.
Use its documented `disable` operation when that is the authorized recovery.

For any reload, inspect plugins/hooks, record sessions/windows/panes/clients and
process starts, run a parse-only check, and obtain the relevant operational
authority. This repository never reloads from Git hooks, shell startup or tests.
[Terminal.app recovery](RECOVERY.md) works without Ghostty, Doom, tmux or Codex.
