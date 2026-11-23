# Workstation status — 2026-11-23

Evil insert-mode `kj` escape is live and persisted in release
**20261123T231833.268509Z-8b080c69**, from signed source commit **1a470bb**.
It uses Doom's installed, already-enabled `evil-escape`, preserving the 0.15-second
delay and existing exclusions. Only `doom/config.el` changes semantically across
the 51-payload release; all 49 managed links verify. The explicit live update set
only `evil-escape-key-sequence`; daemon PID 1283 and all four existing frames/views
were preserved. No daemon restart, full config reload or package install occurred.

A disposable Doom terminal test verified actual quick `kj` keypresses enter normal
state without inserting either character, while slower `k` then `j` stays literal
text in insert mode. Full release parser/dependency checks passed. Existing clients
need no restart or manual reload. Activation journal: `20261123T231838.750159Z-2dcf26c3.json`.

Rollback retains `20261123T081015.107999Z-e855ae1d`:

```sh
python3.12 scripts/deploy.py rollback --expect-current 20261123T231833.268509Z-8b080c69 --approve
emacsclient -s ~/.local/state/cdev-emacs/server -a /usr/bin/false --eval '(when (equal evil-escape-key-sequence "kj") (setq evil-escape-key-sequence nil))'
```

No rollback was needed. Earlier records below describe their historical releases.

## Previous workstation status — 2026-11-23

Editor-only shortcuts **aa89f90** are SSH-signed and active in release
**20261123T081015.107999Z-e855ae1d**. All 51 payloads and 49 managed links
verify; only Fish config, the Doom client helper and frame integration change.

- `emacs [FILES...]`: terminal client on the existing named Doom server.
- `emax [DIRECTORY]`: current folder by default; splash for a new workspace,
  existing buffers/workspace restored on reopening. `SPC f f` stays folder-local.
- `enw`: explicit standalone `command emacs -nw`.

Nine focused unit/startup checks, a real disposable-Doom integration and full
manifest validation passed. An owned old-to-new refresh preserved client state.
The user explicitly approved production activation and the targeted integration
refresh. Doom PID 1283, all four existing frames, their views/project contexts,
19 protected process generations, 11 panes/layouts and tmux bindings survived.
No daemon/service restart, tmux reload, Codex hook change or client replacement
was performed. The production helper passes its new readiness check.

**Next action: run `fishrc` in an existing Fish shell**, then use the shortcuts.
New Fish shells load them normally. Ordinary cdev behavior is unchanged. The
talking-clock repair also passed user-reported listening acceptance on 2026-11-23.

Activation journal: `20261123T082154.476959Z-451308c5.json`.
Rollback retains **20261119T221146.125623Z-b2a69e1b**:

```sh
python3.12 scripts/deploy.py rollback --expect-current 20261123T081015.107999Z-e855ae1d --approve
```

After pointer rollback, refresh the prior integration in the named Doom server
(no restart):

```fish
emacsclient -s ~/.local/state/cdev-emacs/server -a /usr/bin/false --eval '(progn (load "~/.config/doom/cdev.el" nil t) (makunbound (quote dotfiles-cdev-dashboard-if-new)))'
functions -e emacs emax
fishrc
```

No rollback was needed. Previous records below retain their historical release IDs.

## Talking-clock acceptance — 2026-11-23

The user confirmed that `thetime` works and authorized committing and publishing
the repair on 2026-11-23.
The script path now exists; the remaining failure was missing SoX `play` and
an unsafe nested shell invocation. New source `scripts/half-life_clock.pl` uses
macOS `/usr/bin/afplay`, resolves clips beside the script, joins compatible PCM
WAVs into one private temporary file, and reports missing clips/playback failures.
The Fish alias and immutable dotfiles release remain unchanged. Audio assets
stay outside Git. Five focused regressions pass, covering all 1,440 daily time
combinations, PCM concatenation, missing/mismatched/truncated clips, cleanup and
player failure. Native `afinfo` accepted four joined announcements using the
actual recordings; no audio was played automatically. The live regular script
now matches the repository candidate, with its original mode 700 preserved.
Verified original backup:
`~/scripts/half_life_talking_clock/half-life_clock.pl.before-afplay-20261122T045000Z`.
Listening acceptance is complete. The maintained source and regression tests
are ready for publication; no additional live migration or release change is needed.

## Previous workstation status — 2026-11-19

The `passme` repair **9b52edb**, with concise confirmation **cdd57de**,
is SSH-signed and deployed in **20261119T221146.125623Z-b2a69e1b**. All 51 payloads and 49 managed links verify;
only `fish/config.fish` changes behavior (other release-path substitutions are
mechanical). No application was reloaded or restarted; all 13 protected process
generations and seven panes/layouts survived. Collie and hooks were untouched.

`passme` now copies 48 uniformly random alphanumeric characters, guaranteeing
uppercase, lowercase and digits. Generator/dependency/output failures leave the
clipboard alone; copy failures return nonzero and never announce success. It
prints no password. Seven function tests, the nearby Fish startup test, the
isolated activation/rollback regression and full-manifest parser checks passed.
The seven function tests also passed against the deployed source, with real
OpenSSL and an isolated clipboard. The wording-only follow-ups passed the real
generation/clipboard-output test and full release validation; it retains
`Fly safe! o7`. The 256-bit label is a conservative strength shorthand, not a
character count. The user's actual clipboard was not touched.

New Fish shells load the function normally. **Next action: run `fishrc` once in
an existing Fish shell**, then use `passme` normally. No shell input was injected.
No new migration/backup was needed: the prior immutable release is retained.
Activation journal: `20261119T221208.377228Z-6d395ce2.json`.

Rollback (does not reload existing shells):

```sh
python3.12 scripts/deploy.py rollback --expect-current 20261119T221146.125623Z-b2a69e1b --approve
```

This returns to **20261119T220822.294960Z-d196d5c5** (the previous confirmation wording). The following consolidation
record is historical; the current release is the one above.

## Retained workstation consolidation — 2026-10-26

Canonical source commit **439266d** is SSH-signed and deployed as
**20261026T215339.759237Z-d3ef66f1**. All **51 payloads** and **49 exact live links**
verify. The two optional tmux helper aliases remain absent; loaded tmux callbacks
continue using their retained release. No application reload, service operation,
Doom/agent restart, layout/focus change or Collie modification was performed.

The repository now includes complete personal Doom modules/packages/config,
Org Lisp, all snippets/templates and custom helpers; full Fish startup/functions,
portable color preferences and the pinned fzf snapshot; Ghostty/profiles, tmux,
AeroSpace, Starship defaults, Git, gh, shell startup, Codex/cdev and Doom LaunchAgent.
Global Codex hooks/trust/config, workmux's live settings and private/generated
state remain external as documented in [inventory](INVENTORY.md).

All 18 pre-existing production source payloads remain byte-identical. The 33
new mappings preserve existing settings; Doom loads the same dashboard helper
from one source, promotes its two Custom defaults into normal config, and reads
the existing mail identity from an excluded mode-600 override. Generated Custom
and Fish variables stay writable/external. Existing Doom clients keep their
already-loaded configuration; fresh standalone/daemon startup was tested in
private homes with the complete public source. No Doom sync or package install
was necessary on this workstation.

## Verification

- **207 full regressions passed**; **50 clean-clone bootstrap/recovery checks passed**.
- The inherited native acceptance fixture passed 23 focused checks before commit.
- Parser/reference/dependency/source-export checks passed for every payload.
- Every original file/mode/absence and the guarded rollback path verify.
- All 14 protected project process generations, session/window/pane identities,
  dimensions, clients, hooks/bindings, services and UUID pins survived unchanged.
- Native title-format benchmark works without the obsolete hook CLI fixture;
  no per-frame animation processes. No new Codex native or physical phone test
  is claimed for source consolidation; that runtime payload is unchanged.
- Privacy scanning includes all Git objects/history; private Doom email and all
  five current production pins are absent. Full publication findings are in
  [PUBLICATION.md](PUBLICATION.md). The canonical publication target is the existing
  public `abuczuba/spacedoom` repository.

## New adoption backups

All live originals are outside Git under `~/.local/share/dotfiles-active/backups/`.

| Component | Backup ID | Original files / absent paths |
|---|---|---|
| doom-config | `20261026T215708.832520Z-c769116a` | 9 / 1 |
| fish-config | `20261026T215710.582737Z-e1ae3cf8` | 18 / 1 |
| aerospace | `20261026T215712.329688Z-c5fde513` | 1 / 0 |
| git-config | `20261026T215714.056983Z-e5ad673d` | 1 / 0 |
| shell | `20261026T215715.788339Z-c359b8b4` | 1 / 0 |
| gh | `20261026T215717.521978Z-885be239` | 1 / 0 |

Rollback: restore those six backups in **reverse table order**, then use
`python3.12 scripts/deploy.py rollback --expect-current 20261026T215339.759237Z-d3ef66f1 --approve`
to return to `20261026T191404.024651Z-db56a4bd`. Restore the Doom config before
removing this import's private identity override, and remove it only if its
recorded hash still matches. Its receipt is beside the Doom backup journal.
Rollback was checked, not executed. A guarded convenience command is
`python3.12 /private/tmp/dotfiles-public-_4oi06_e/rollback.py --check`;
`--approve` performs that exact bounded reversal. Durable backup IDs and the
normal repository tool remain sufficient if temporary test evidence is gone.

The complete dated rollout record is preserved in
[history/WORKSTATION-2026-10.md](history/WORKSTATION-2026-10.md).
Publication integration preserves the 30 modern signed commits and all four
original spacedoom commits without rewriting either history. The modern source
tree supersedes the old root-level Doom duplicates; their useful customizations,
snippets, template and simpleclip are already present under `configs/doom`.
Only publication documentation changes in this integration; all deployment
payloads remain byte-identical. Publication does not activate a workstation release.
The original `master` is retained; the integrated branch is `main`.
