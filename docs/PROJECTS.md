# Creating and opening projects

Personal defaults live in the managed `~/.codex/AGENTS.md`; project-specific
instructions and upstream safeguards remain in each repository. See STATUS.md
for the active release and acceptance results.

## New personal repository

In Fish:

```fish
cnew my-project
cdev my-project
```

`cnew` creates `~/dev/my-project` on branch `main` with README.md, AGENTS.md and a
small .gitignore for macOS metadata and local .env files (.env.example is allowed).
Fill in the purpose, then record verified setup/check commands and local safeguards
as the project develops. No stack, license, dependency, initial commit, remote,
application launch or `direnv allow` is selected automatically.

Names start with an ASCII letter/digit; subsequent characters may also be dots,
underscores or hyphens. Existing paths (even empty directories and broken links)
and creation inside another Git repository are refused. Git templates are disabled
for initialization. A failed initialization leaves its new directory for inspection;
retry refuses that partial directory rather than overwriting it.

`cdev` requires tmux. Bare names always mean `~/dev/NAME`, even if a same-named
directory exists in the current location. Explicit paths retain their meaning:

```fish
cdev my-project             # ~/dev/my-project
cdev ./my-project          # under the current directory
cdev ../another-project
cdev /absolute/path/to/repo
cdev                       # current Git working tree
```

Canonical Git roots still control window reuse and exact conversation UUID pins.
Renamed windows and symlinked/nested paths reuse the existing project agent.
Ambiguous/missing session metadata still fails clearly; there is no `resume --last`
fallback. The Doom-left/Codex-right layout, daemon/client behavior, lifecycle hooks
and attention navigation are unchanged. `cdev-pin` keeps its existing path interface.

## Cloned upstream repository

Clone normally into `~/dev/NAME`, inspect its README and instruction files, then
use `cdev NAME`. Do not run `cnew` on the clone or replace its AGENTS.md/CLAUDE.md
with personal templates. Follow the upstream toolchain and checks. No local
instruction file or compulsory planning documents need to be added to a clone.

## Instruction scope and inventory (2026-10-24)

| Repository | Existing convention, preserved unchanged |
| --- | --- |
| dotfiles | AGENTS.md: deployment approvals, session protection, isolated checks |
| pluckd | AGENTS.md: application/history policy, holds and applicant-data gates |
| private-ai-ops-lab | AGENTS.md: architecture, milestone and operational gates |
| collie | AGENTS.md delegates to CLAUDE.md: shared development/release agreement |

No additional instruction files were found in the other inspected `~/dev`
projects. No global AGENTS.md or AGENTS.override.md existed at inventory time;
the current Codex configuration has no instruction-discovery overrides.

The global source, `configs/codex/AGENTS.md`, contains only shared preferences
about local policies, minimal changes, proportionate tests, privacy and authority.
Project-specific policy, stacks, commands and release rules remain local.
[Codex loads global instructions before repository/deeper instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
CLAUDE.md is not a default discovery filename: Collie explicitly points to it, and
the global instructions ask agents to read it when present. No config.toml fallback,
hook, trust, authentication or sandbox setting is changed.

## Deployment and recovery boundary

The existing manifest adds independent `codex-instructions` and `fish-cnew`
components for `~/.codex/AGENTS.md` and `~/.config/fish/functions/cnew.fish`.
The existing `fish-cdev` payload gains name resolution only. No deployment code
or transaction/backup format changes are required.

The approved rollout uses normal preflight, a complete immutable release and
comparison of every already-managed path before switching `current`.
Inspect any then-existing global instructions/override before migration; never
silently replace manual changes. Migrate the two new components separately using
the normal tooling, which backs up originals and records prior absence. Keep each
backup ID. Do not link live files into this development checkout.

Fish caches loaded functions: accept using a new Fish process or an explicitly
approved function reload. Check global instructions in a future Codex launch;
existing agents are not restarted. No tmux reload is needed.

Restore each new component with `python3 -B scripts/deploy.py restore --backup ID
--approve`. Before rolling back to a release without these files, restore both
new components, then use `scripts/deploy.py rollback --expect-current NEW --approve`.
Use these commands within an authorized rollback; they do not reload applications. The
original files/modes or absence are restored independently; the shared pointer
changes atomically and incomplete recovery fails safely. See [WORKFLOW.md](WORKFLOW.md).

Focused checks use `scripts/test.py --match 'test_cnew.*' --match 'test_deploy.*'`
and `scripts/test.py --integration --match 'test_cdev.*' --match 'test_cdev_session.*'`.
All created repositories, agents and tmux sockets belong to disposable fixtures.
