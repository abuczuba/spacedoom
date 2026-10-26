# Agent instructions — personal macOS dotfiles

## Mission and authority

Maintain a reproducible, minimal, keyboard-centric macOS environment. The
canonical development source is `~/dev/dotfiles`. Repository edits and commits
have **no authority to change the running workstation**.

Current development scope: Ghostty/tmux, the cdev Fish functions, an advisory
Codex activity observer, and a named persistent Doom server/client integration.
Production tmux has passed user-reported physical acceptance. Broad new milestone
features require approval; routine bounded repairs use the standing policy below.
Never alter global Codex hooks, workmux settings or authentication. AeroSpace
and unrelated Fish/Doom configuration still require a separate task. Application
repositories, including Tailscale, private-ai-ops-lab, JobApply and pluckd, are out
of scope. Do not spawn agents or workmux worktrees without an approved use case.

## Three separate layers

1. **Development:** this Git repository; agent edits and local commits belong here.
2. **Deployment:** `~/.local/share/dotfiles-active/releases/<id>/`; complete,
   validated copies independent of Git branches, dirty files and this checkout.
   `current` is the explicitly switched release pointer.
3. **Live:** existing application paths. After individually approved migration,
   exact files may link through the deployment pointer. Never link a live file
   or deployment file into the development checkout. Do not link whole config
   directories or adopt uninspected files.

The repository describes intended settings. It does not prove they are deployed
or loaded. `docs/STATUS.md` records observed deployment and acceptance state.
`docs/ENVIRONMENT.md` is a dated handoff, not a current inventory.

## Standing authorization

Allowed without additional approval within the authorized project scope:

- Inspect relevant configuration, exact includes and narrowly relevant local
  documentation. Do not recursively scan `$HOME`.
- Import inspected, nonsecret development copies, edit/refactor/reorganize the
  repository, maintain docs/status/decisions, and run local nondestructive tests.
- Create isolated temporary test fixtures and private tmux test servers. Always
  use an explicit private socket, an empty startup config and inert test panes;
  never use the live/default server. Clean up only resources created by the test.
- Start disposable Doom daemons with unique private sockets and sanitized homes,
  and connect owned test clients. Installed libraries are read-only dependencies;
  do not load private Org/custom configuration or captured environment dumps.
  Close/terminate only resources the test itself created. Never infer ownership
  from a process name or kill a discovered existing Emacs/Codex process.
- Make appropriately scoped local commits after reviewing the staged changes,
  running `python3 scripts/preflight.py` and `git diff --cached --check`.
- For a requested bounded, reversible change to already-managed dotfiles,
  complete focused tests, local commits, clean-release staging, backups,
  activation, canary checks and documented rollback using the existing tooling.
  This standing user authorization (2026-10-25) removes routine intermediate
  approval gates. Deploy only the requested change; exclude unrelated pending
  work. A commit or repository edit still never triggers deployment automatically.

Explicit, operation-specific user approval is required for:

- Broad/global changes, new live migrations or managed paths, and changes outside
  the requested bounded scope. Unexplained configuration drift, security or
  authentication changes, unexpected production impact and deployments without
  a verified safe rollback are substantive boundaries; stop and request review.
- Reloading/restarting applications, terminating processes, or modifying live
  tmux sessions, panes or windows.
- Installing, bootstrapping, kickstarting or unloading a persistent LaunchAgent;
  starting a production Doom daemon; trusting new Codex hooks. Invocation-local
  advisory hook definitions must preserve all approval/sandbox/notification
  settings and must never bypass hook trust or actual sandbox enforcement.
- Installing/removing packages; changing macOS settings, login items, permissions
  or services; destructive operations; work outside this project's scope.
- Changing Git remotes/configuration, pushing or publishing.

Standing authorization applies only to the requested bounded scope. A consolidated
user approval may additionally cover implementation, commit, staging and deployment;
continue authorized steps without routine confirmation. After an unexplained
production failure, investigate and validate its cause before another attempt.
Test the actual regression first; classify a permission fixture that generated
no request separately from a demonstrated lifecycle failure. A tool's `--approve`
flag is an accident guard, **not evidence of user consent**. Never auto-deploy/reload from Git hooks,
shell startup, tests, background jobs or an agent finishing its task. These rules
supplement actual Codex sandbox/approval enforcement; do not weaken or bypass it.

## Privacy and workstation protection

- Never access private keys, `~/.codex/auth.json`, tokens, Keychain, browser
  profiles, personal Org/iCloud content, archives or unrelated private files.
  Do not print environment dumps, secret-looking values or raw complete configs.
  If a source looks sensitive, stop copying/displaying it and propose redaction.
- Preserve Ghostty → Fish → tmux `main` → Doom/Codex; `Ctrl+F`, Command-driven
  shortcuts, no-wrap pane navigation, theme and existing processes unless a
  specific approved change says otherwise.
- No `sudo`, `curl | sh`, broad package upgrades, `rm -rf`, `git reset --hard`,
  `git clean -fd`, default-server `kill-server`, unapproved persistent daemons, broad home access or
  full-access sandbox shortcuts. A blocked live read remains unverified; do not
  request broad access to retry it. Narrow sandbox escalation for an isolated
  test must name the test and its private resources.
- Interactive shell is Fish; tool commands use Zsh/POSIX sh. Label examples by
  shell. Do not assume Fish syntax is portable shell syntax.

## Development and release workflow

Read `docs/STATUS.md` and the relevant source first. Read `docs/WORKFLOW.md` before
any release, backup, migration, activation or reload operation.

1. Establish the baseline, bounded behavior and exact files. Distinguish source
   inspection, isolated tests and live acceptance; do not describe plans as tests.
   At the start of each new development task, compare relevant live dotfiles,
   managed links and deployment state with the last accepted baseline and repository.
   Check for the user's intervening manual edits and preserve/reconcile them before
   implementation; never assume recorded status still describes the live workstation.
2. Make minimal repository changes; validate applicable syntax, dependencies,
   references and behavior without executing user plugin/startup code in tests.
   The approved Doom integration fixture may load installed Doom libraries with
   rebased startup COPIES and a sanitized private configuration. Test dashboard
   and editor reversibility independently, then their interaction. Baseline
   existing configuration before edits; never test on production main panes.
   For routine reversible repairs, run focused tests covering changed behavior
   and nearby regressions. Run the full suite only for cross-cutting changes,
   relevant failures or an explicit requirement. Avoid repetitive audits and
   elaborate reports; record the useful evidence once.
3. Review/stage the intended files, run preflight and staged whitespace checks,
   inspect the staged diff, then make the authorized local commit. Never bypass a
   failed hook or silently disable signing.
4. For deployment, show the exact candidate release, all currently managed paths
   affected by the shared pointer, dependency/drift checks, backups, failure plan,
   rollback target and reload effects. Proceed under the bounded standing policy
   or applicable consolidated authorization; ask only at a substantive boundary.
5. Initial migration backs up each exact target outside this repo, preserving
   content and modes, before any live replacement. Multiple path replacements
   are not jointly atomic. An interrupted migration requires explicit recovery.
6. Stage complete releases before activation. Verify hashes and references;
   switch the single deployment pointer atomically. Never mutate a release in
   place. Activation and rollback do not reload applications.
7. Verify loaded behavior only after separately authorized reload/manual UX
   acceptance. Keep an independent Terminal.app recovery path.
8. Update `docs/STATUS.md` with actual commands/results, changed repository/live
   files, confidence, backups if any, approvals and the next single action.

Give concise reports covering observed facts, unknowns, changes/proposals,
tests and the next authorization boundary. Never claim changes are live without
deployment and acceptance evidence.
