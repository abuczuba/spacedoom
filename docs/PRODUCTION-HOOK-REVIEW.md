# Production trust and event acceptance passed — 2026-10-22

All eight dashboard entries and seven workmux entries are enabled/trusted, with
unchanged native source keys/commands/hashes. After the user's remaining-three
review, trust survived CLI exit, fresh ordinary cdev launch, resume, concurrent
threads and final checks without another review prompt. The prior partial-trust
cause is not established; no automation wrote trust or bypassed review.

Actual production events/coexistence passed and the one gated tmux reload is
complete. See [DASHBOARD-ACCEPTANCE.md](DASHBOARD-ACCEPTANCE.md) for current
production state and physical acceptance. Do not repeat native trust, staging,
migration or reload merely because the historical pending instructions below
are retained. Definitions and their hashes remain the exact reviewed artifacts.
The earlier focus change remains unattributed and is not assigned to the user.

---

# Native production trust discrepancy — 2026-10-22

The user reported personally reviewing and trusting all eight definitions and
leaving workmux unchanged, then authorized continuation. Fresh native hooks/list
queries report **five trusted dashboard definitions and three untrusted**:

| Event | Exact key | Unchanged native hash |
|---|---|---|
| userPromptSubmit | `/<session-flags>/config.toml:user_prompt_submit:0:0` | `sha256:2b3cccf85b7fe8e348f7452ead927adecb23828d7a1ac3735e8807b556e5fdd7` |
| stop | `/<session-flags>/config.toml:stop:0:0` | `sha256:28e8fd56f0dccde535cb7bc170f0599911f91590db8476899b81b49fc3599269` |
| interrupt | `/<session-flags>/config.toml:interrupt:0:0` | `sha256:7ec14f17245f7dc1cda721d78df34fa8ea95b92c98e7d26deb79209abf2f10b3` |

All eight source keys, commands and currentHash values still match the inspected
repair. The seven workmux definitions are enabled/trusted with unchanged hashes;
their source file/settings were not edited. The cause of incomplete persisted
trust is not established; do not attribute it to the user's actions. Automation
has not written trust, disabled hooks or bypassed the native gate.

No real production test prompt was sent and no attention binding/reload was
performed. Native review remains pending, which the documented procedure does
not classify as a delivery failure. The verified cdev migration/backup and active
release are retained; no helper restoration or pointer change was performed.
Both n/c still create windows. The original session/window/pane/client identities
and all 12 protected processes survived. The user attached one additional review
client; it remains attached. The earlier @10 -> @2 focus change is **unattributed**;
the user cannot establish its cause, and no focus restoration is attempted.

Next human gate: in the existing disposable CLI, open /hooks and inspect the
three entries above. If the native UI differs from this read-only metadata,
report the discrepancy before proceeding. Only the user may explicitly trust
these definitions. A subsequent fresh native hooks/list must show all eight
trusted before actual production lifecycle tests can start. Existing consolidated
rollout authorization remains the authority for later routine steps; no additional
blanket approval is needed, but native trust cannot be supplied by the agent.

Evidence: /private/tmp/df-dashboard-phase4-ql9uc7fk/native-trust-discrepancy.json,
after-user-review.json and native-review-discrepancy-ui.json. No authentication,
conversation or private browser data is included in repository documentation.

All earlier instructions/evidence are retained below as history.

---

# Production hook review — eight new definitions

User-only native review. No trust choices or model prompts have been sent.

Commit: e38e18d; release: 20261022T215047.249499Z-618a6bc8.

Source: sessionFlags; source path: /<session-flags>/config.toml. This is an invocation-local source label, not an on-disk file.

All eight: command handler, timeout 2 seconds, synchronous, no matcher, enabled, non-managed and untrusted.

```text
/usr/bin/python3 -B /Users/czuba/.config/cdev/activity.py event
```

| Event | Exact key | Native currentHash |
|---|---|---|
| preToolUse | `/<session-flags>/config.toml:pre_tool_use:0:0` | `sha256:9b96aeade26b382f277eea4dcaad0966bdccbe2ef214333b4d8281ea32718a1b` |
| permissionRequest | `/<session-flags>/config.toml:permission_request:0:0` | `sha256:68f3f749508c6d24303c24a577d16dce0fddbd4a4793d3b54ff8d559c2d18705` |
| postToolUse | `/<session-flags>/config.toml:post_tool_use:0:0` | `sha256:001d65ce92f285a09a96a2884d4f98813d9ef6b240a1d6135f288723335fa772` |
| sessionStart | `/<session-flags>/config.toml:session_start:0:0` | `sha256:760693aa4b54a00681f7e2f1e247031ee35075c3d5503fe7daddb8b5ce6ac75f` |
| sessionEnd | `/<session-flags>/config.toml:session_end:0:0` | `sha256:d90ebb3369559b0dfdd307dcc2258f7c52da5bf4d4d065149095f2312b47a266` |
| userPromptSubmit | `/<session-flags>/config.toml:user_prompt_submit:0:0` | `sha256:2b3cccf85b7fe8e348f7452ead927adecb23828d7a1ac3735e8807b556e5fdd7` |
| stop | `/<session-flags>/config.toml:stop:0:0` | `sha256:28e8fd56f0dccde535cb7bc170f0599911f91590db8476899b81b49fc3599269` |
| interrupt | `/<session-flags>/config.toml:interrupt:0:0` | `sha256:7ec14f17245f7dc1cda721d78df34fa8ea95b92c98e7d26deb79209abf2f10b3` |

Adapter resolves to /Users/czuba/.local/share/dotfiles-active/releases/20261022T215047.249499Z-618a6bc8/cdev/activity.py.
Adapter SHA-256: `d6e5440ee07c72742dad1d2dcde3bf73e85d4ce4e6d48c9efa4cbb4994b131e4`.
The seven existing workmux definitions from /Users/czuba/.codex/hooks.json remain trusted and unchanged; do not edit or re-trust them.

From Terminal.app outside an existing tmux client:

```sh
/bin/sh /private/tmp/df-dashboard-phase4-ql9uc7fk/attach-review.sh
```

If native project trust appears first, this owned Git project contains only the inspected README and an empty-template .git directory; no .codex hooks or executable project code.
After entering the CLI, open /hooks and personally trust only the eight matching sessionFlags definitions above.
Stop if anything differs. Leave the CLI at its normal prompt and report completion.

## Observed rollout state before review

The user approved the consolidated e38e18d rollout. Active release is now
20261022T215047.249499Z-618a6bc8. All 15 payloads were independently compared
against that commit; six previously managed payloads are equivalent after
release-path rendering, and Ghostty is byte-identical. Only the two cdev
payload sources differ from the previous release. All payloads are regular
independent copies, mode 0444, with validated receipt/references/dependencies.

The existing deployment tooling activated the new release, then migrated
only ~/.config/cdev/codex_session.py and activity.py. Backup
20261022T215153.419622Z-a559508a preserves the original regular 0644 helper
and the adapter's prior absence. All eight managed links and backups passed
verification. The live Fish functions, standalone emacs -nw/compiler
environment, global hooks, workmux settings and authentication were not edited.
No production reload, attention activation or persistent Emacs/service change
was performed. No release or commit was changed in place.

The complete regression suite passed: 90 tests in 54.814s. An exact private
two-helper migrate/restore rehearsal also preserved original bytes/mode/mtime,
prior absence and the activated pointer, including repeated restoration.
Temporary fixture setup/target-format corrections were made before Codex
launched; no trusted adapter, repository implementation or production setting
was repaired to bypass a failing check.

All original session/window/pane/client identities and 12 protected processes
(including the three original Codex CLIs) survived. Their bindings, options,
hooks and monitors match baseline. The original four windows/seven panes remain;
the owned review session adds two windows and three panes. Main's selected
window changed from @10 to @2 during this interval. Its cause is not established;
no corrective focus action was attempted. Review commands selected only owned
test window @12/pane %20. This selection observation must be reconciled before
further production activation; identity survival is not proof of unchanged focus.

The current CLI screen is **Folder access / Trust this folder?**, preceding
hook review for this new owned repository. Automation stopped at that native
trust boundary. The eight new definitions are still untrusted, the seven
workmux entries are trusted and unchanged, and the observer is idle/unlabelled
with no session/turn bound. No model prompt, project trust choice or hook trust
choice was sent. After the user handles folder trust, /hooks must show the
same eight definitions before the user trusts them.

Evidence: /private/tmp/df-dashboard-phase4-ql9uc7fk contains baseline.json,
commit-source-audit.json, helper-restore-proof.json, release-verification.json,
adoption-verification.json, production-native-definitions-review.json,
live-fixture.json and review-gate-verification.json. No authentication or
conversation data was copied into the repository.

## Bounded helper recovery

Only under the already approved failure-recovery conditions, restore the two
helpers with the new backup (POSIX sh/Zsh):

```sh
python3 -B /Users/czuba/dev/dotfiles/scripts/deploy.py restore --backup 20261022T215153.419622Z-a559508a --approve
```

This leaves current on the new release, because migration recorded that pointer
as both current_before and current_after. It restores the original regular
launcher and removes only the newly adopted adapter link. Do not use the old
already-restored cdev backup, restore Ghostty, roll back the shared pointer or
terminate existing agents. Native review being pending is not a delivery failure.

After user review and reconciliation of the focus observation, resume the
[authorized gated sequence](DASHBOARD-PHASE4.md): actual production events,
seven-hook coexistence, concurrent identity/trust reuse and cleanup first;
strict preflight/parse and the one controlled reload only after those pass.
Attention and all new physical acceptance remain pending.
