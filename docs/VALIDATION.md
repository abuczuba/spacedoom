# Validation and its limits

The canonical-source consolidation passed **207 tests** with
`python3.12 scripts/test.py --integration` (184.121 s) on the inspected macOS
workstation. The inherited native acceptance harness separately passed 23 focused
checks before its signed commit. Initial full-config testing exposed a parser
bug: fundamental-mode `check-parens` treated valid Doom comments as code. The
validator now selects Emacs Lisp syntax under `emacs -Q`; its regression passes.
No user startup or package code runs during configuration parsing.

## What the tests establish

- The complete 51-file manifest materializes independent copied payloads with
  declared references, read-only modes and no checkout symlinks. Fish, Elisp,
  sh/Zsh, TOML, Git, JSON, plist, tmux and Ghostty checks use actual local parsers.
  The captured workmux/gh YAML is inspected source, not a claimed YAML schema test.
- A private full-manifest bootstrap backs up original contents/modes and records
  absent paths, migrates selected exact files, activates/rolls back another copy,
  and restores every original or absence. Repeated restores are idempotent.
  External identity/Custom, hooks/config and pins remain untouched. Dummy external
  dependency files are inert; this proves deployment behavior, not package installation.
- Complete public Doom configuration starts through normal standalone `emacs -nw`
  and a disposable daemon with two terminal clients. Identity resolves privately;
  clipboard binding, Org/theme settings and dashboard helper load automatically.
  Other tests exercise workspace/project isolation, reconnection, file navigation,
  native compilation, Evil selections/yanks and unchanged kill-ring behavior.
  Clipboard transport is replaced in tests; the user's clipboard is not accessed.
- Private Fish startup preserves functions, editor environment and the captured
  color choices. cnew/cdev tests cover creation/refusal, bare names and paths,
  window reuse, layout, exact UUID selection and shared-server ownership.
- Dashboard tests cover all supported cached states, native 1 Hz formats,
  selected-title underline boundaries, acknowledgment, attention cycling/empty
  queues, concurrent panes, stale events, native request IDs/resolutions and
  process-generation validation. Workmux and optional Collie forwarding are covered
  without changing either live integration.
- Acceptance-fixture tests verify per-pane environment propagation, UTF-8 background
  callbacks and real same-account socket pairs. Native `execpolicy check` reads
  an isolated rule; it does not authenticate, execute a turn or approve a request.
- The privacy scanner finds deleted-history credentials, distinguishes unreachable
  objects, withholds matched values and checks staged private-identity exclusion.
  All ten fzf files match the documented upstream commit and retained MIT notice.

## What requires separate evidence

Mock/cache tests do not establish real Codex events or phone delivery. Actual
Codex 0.164.0 working/stopped, remote UUID resume and genuine pending/resolved
approval were previously verified against the accepted repair, including its
activated payloads. That cdev/renderer payload is preserved by consolidation.
Physical Ghostty styling, keys and Doom clipboard/dashboard were accepted by the
owner in the recorded earlier milestones; import does not claim a new phone test.

No package installation, Doom sync/upgrade, service enablement, production reload,
agent restart or active-pane manipulation is performed by automated tests.
Native Codex profile authentication and hook trust remain human operations.
The optional native title-format benchmark measures formats only, not lifecycle
attribution or hook overhead. Linux-only helpers and alternate inactive Ghostty
profiles are retained as source; their everyday runtime behavior is not certified.

## Reproduce safely

```sh
python3.12 scripts/test.py
python3.12 scripts/test.py --integration
python3.12 scripts/deploy.py check
python3.12 scripts/benchmark_dashboard.py
python3.12 scripts/publication_audit.py
```

Integration requires the listed macOS tools and inspected installed Doom libraries.
The real-Doom fixture fingerprints generated startup before using rebased copies
and a sanitized HOME. Another installation must be reviewed; never replace those
fingerprints blindly to make a test green. No private Org, captured environment,
conversation, credentials or existing Emacs process is used as a disposable fixture.
Clean-checkout and production adoption results are recorded in STATUS.
