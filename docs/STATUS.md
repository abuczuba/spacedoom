# Workstation status — 2026-10-26

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
  [PUBLICATION.md](PUBLICATION.md). No push, remote or public repository exists.

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
The next action is **owner approval to create the public abuczuba/dotfiles
repository and push the signed main history**. No further workstation change is
required for publication.
