# Validation evidence — 2026-10-21–22

All implementation testing used development files, owned temporary homes and
private servers. The ec518f0 release was subsequently staged inactive; no live
configuration was migrated and no live application was reloaded. This is
isolated evidence, not workstation UX acceptance. STATUS.md records current
deployment state; original implementation results below are dated history.

## Pointer-restoration repair — 2026-10-22 UTC

`python3 -B scripts/test.py --integration`: **47 tests passed**, final run 1.642s
(37 unit tests and 10 integration tests). The initial sandboxed integration run
failed to create private tmux sockets; the permitted run used only temporary
homes, explicit private sockets, an empty startup config and inert test panes.
No failed sandbox run is counted as a pass.

Regression coverage now includes:

- Initial migration restores three original files' bytes/modes, removes both
  new helper links, and restores current's prior absence using actual templates.
- A preexisting older current preserves its exact symlink text while a newer
  staged release stays inactive; migration still refuses implicit activation.
- Partial migration, including failure before pointer creation, restores safely.
- Unexpected pointer targets, absence, regular files/directories and changes
  during restoration are refused without overwriting the unexpected state.
- Other components, skipped managed paths, relative/aliased links and paths
  containing current/.. prevent pointer removal while it is still needed.
- File removal, pointer removal, pointer-directory fsync and final journal
  failures return failure and retain a retryable restoring journal. An injected
  partial failure through the CLI returns nonzero with no success message.
- Successful repeats validate state without writes; later user changes are
  refused rather than deleted. Legacy backup journals without pointer evidence
  are refused rather than guessed.

Read-only before/after fingerprints confirmed production files, modes, link
states, inodes, mtimes, ctimes and deployment-directory members were unchanged.
Current remains absent and production backups/history remain empty. All staged
ec518f0 payloads still match their committed blobs after rendering. Release
receipt/manifest schema 1 is unchanged; only new backup journals use schema 2.
The original exact-state restore blocker is resolved without replacing the
staged release. A fresh live migration preflight is still required after renewed
authorization; no live session/pane acceptance is inferred from these tests.

## Original implementation commands and results — 2026-10-21

| Check actually run | Result |
|---|---|
| sh -n configs/tmux/show-shortcuts.sh | Passed |
| python3 scripts/test.py | 22 unit tests passed; 10 integration tests skipped explicitly |
| python3 scripts/test.py --integration | 32 tests passed; final run 1.320s |
| Actual dependency and empty-override checks through Deployment.dependencies | Passed; read-only, no plugin/program startup |
| Hash/type/mode comparison of four original live imports | Unchanged; regular files, 644 |
| Production deployment directory existence check | Absent |

Staged validation also passed: python3 scripts/preflight.py inspected all 28
files with no obvious indicators; git diff --cached --check passed. The complete
staged diff was reviewed without printing raw configs. Staged blobs matched the
reviewed working files; preservation comparisons confirmed the unchanged
Ghostty copy, the sole main-tmux include normalization and unchanged existing
navigation bindings. All relative Markdown links resolve. The scan is heuristic.
The test environment used Python 3.12.15, tmux 3.8, Ghostty 1.3.1 and less 668.
The initial sandbox denied private sockets; the integration suite was then
explicitly permitted outside the sandbox for its owned test resources only.
No failed sandbox run is counted as validation success.

## What the tests prove

- Copies have independent inodes and remain unchanged when development changes.
  Complete releases pin references to their own absolute directory, including
  when the stable deployment path contains spaces.
- A failed parser does not publish a selectable release. Release hashes, modes,
  file completeness, source ancestry, includes, dependencies and override guards
  reject unsupported/missing/drifted inputs. Mutation commands require an
  explicit accident-guard flag, and independent writers are locked out.
- Migration backs up every pre-existing target before replacing any live file
  in the fake home. Original bytes and POSIX permissions are restored exactly;
  originally absent helper files are removed only when still managed links.
- Activation, normal rollback, failed pointer replacement, interruption after
  the pointer changed but before journal finalization, interrupted migration
  recovery, user drift and damaged release refusal all have behavioral tests.
- A second component cannot silently activate another release. Parent/unknown
  symlinks, traversal, overlapping mappings and removed managed targets are
  refused. Normal planning/checking does not initialize deployment state.
- The real Ghostty/tmux templates can be staged, migrated and restored in a
  temporary home. Stub user plugins exit with failure if executed; parser tests
  use source-file -n and never run them.
- Explicit Ghostty validation ignores deliberately invalid default files,
  accepts the candidate and rejects an invalid candidate. This confirms the
  installed action's supported flag form rather than assuming CLI behavior.
- Private tmux servers confirm Alt+h/l is free in installed defaults; L and
  window/pane menu bindings are retained. Movement preserves the selected window
  ID, handles first/last/single-window boundaries and numbering gaps, ignores a
  marked window and keeps the numeric selection bindings consistent.
- A real pseudo-terminal exercises section jumps from different positions,
  anchored search, text search and q exit. ANSI stripping reproduces the plain
  source exactly; blue/rust sequences and ASCII-only content are verified.
- The documented macOS ln + mv -fh recovery restores the known good pointer in
  a temporary deployment without Python/application assistance for the actual
  recovery operation.

The palette's computed contrast ratios on #f3e8d2 are 12.8:1 for #20242b,
7.0:1 for #264f78 and 6.3:1 for #8b3a2f. Rendering inside the user's actual
Ghostty window has not been visually accepted.

## What remains unverified

- The loaded live tmux server and any plugin overrides. Its socket read was
  sandbox-denied and was not retried unsandboxed.
- Physical Command/Option key delivery through Ghostty and native macOS input.
- Popup border/background/reset-color appearance at the user's font/display,
  small terminal sizes and custom accessibility settings.
- Workmux CLI subcommands/last-agent; its help command tried to create a log and
  was sandbox-blocked. Candidate validation checks executable availability only.
- Doom's actual loaded mode-dependent keymaps. The reference explicitly marks
  those conventions and points to SPC h k for live inspection.
- AeroSpace's enabled state; its config was neither edited nor loaded.
- Ghostty GUI config-file watching and pointer-change effects. Installed action
  docs describe explicit reload and say some settings cannot apply at runtime;
  they do not document an automatic watcher guarantee. No live mutation was
  performed to test this. Ghostty migration remains a separate approval.
- Disk-failure/power-loss behavior, ACL/resource forks and malicious alteration
  of tool metadata. Hashes/locks/fsync are reliability checks, not guarantees of
  security or a transaction spanning every application read.

## Acceptance after separate migration and reload approvals

Have an independent Terminal.app shell available first. Record the exact
candidate, all five tmux targets and backup ID. Keep working panes/processes.

After an approved reload, manually open Cmd+Shift+P and check the light panel,
dark body, readable accents, aligned columns and prompt. Try keys 1–8 in several
orders, / search, n/N, Space/b, g/G and q. Check help in a terminal around 80
columns and in the normal working window.

With explicitly approved disposable test windows, move a selected window using
Ctrl+F then Option+h/l. Verify focus, status-bar order, numbering and Cmd+1–9,
including both boundaries. Confirm normal pane navigation, splits, zoom,
dashboard and the existing editor/agent panes remain usable. Do not close,
recreate or restart working sessions to perform these checks.

An approved rollback followed by an independently approved reload must be
accepted separately. Preserve all old releases while any running server may
still reference their helpers.
