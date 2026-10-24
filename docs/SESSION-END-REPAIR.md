# Historical SessionEnd candidate — superseded for this rollout

The 2026-10-24 native A/B comparison passed the full failure sequence with the
connection-lifetime fix alone. The new release keeps production's activity.py
unchanged; a13eae3 and its earlier inactive release are preserved as history.
See [REMOTE-RESUME-REPAIR.md](REMOTE-RESUME-REPAIR.md). The original investigation
and candidate preparation below describe the earlier, superseded proposal.

---

# SessionEnd registration repair — release preparation, 2026-10-24

Signed repair-only commit and inactive staging are approved. Production activation,
reloads and changes to existing agents remain unapproved. STATUS.md records the
resulting commit/release IDs separately from inherited, uncommitted documentation.

Reopened 0.164.0 clients had live, matching launcher/child/pane identities, but
their records were ended=true, turn=null, sequence=0. Actual app-server metadata
showed active work, a completed turn and waitingOnApproval without corresponding
dashboard indicators. This identifies premature retirement in the adapter, not
the title renderer. The startup event's exact upstream ordering was not retained.

SessionEnd is now a state no-op. It has no launch generation or turn identifier
and cannot safely bind a session, retire a registration, clear attention, refresh
its timestamp or advance its notification revision. Launcher cleanup after the
owned child's exit still marks ended, clears status and closes the registration.
UUID/nonce/boot/pane/process-start checks, turn retirement and already-ended
rejection are unchanged. No hook definitions, launcher, renderer or pager change.

Regression evidence: six selected tests failed against the old implementation;
the corrected adapter passes **42 focused tests** in a repair-only temporary
export. Coverage includes both resume/start/end orderings, working/approval/stopped
transitions, repeated/delayed end notifications, same-UUID/same-pane reopening,
cross-agent isolation, retired turns, launcher/child/backend PID reuse or exit,
actual owned child-process termination, native hook hash stability and workmux
coexistence, shimmer/static rendering, attention and pager deduplication/retries.
Event injection is synthetic; native hash discovery and child exit are real
isolated operations. New real 0.164.0 turn delivery remains an acceptance check.

The export was built from committed HEAD 76b683d plus exactly:

- configs/cdev/activity.py
- tests/test_activity.py
- tests/test_remote_activity.py

It uses the production-identical **17-file manifest**; after normalizing release
paths, **cdev/activity.py is the only changed payload**. The pending cnew, global
AGENTS, Fish name-resolution, manifest and workflow changes are excluded.
Full candidate syntax/dependency/reference checks use this export too.

## Isolated release and rollback

1. Review/commit only the three repair files above and this note. If including
   STATUS.md, stage only this repair's entry; preserve all inherited/pending edits.
   Run the normal staged privacy/whitespace checks and preserve signing.
2. Export that exact repair commit with git archive into a fresh temporary
   directory. Stage from the export using the existing deploy.py --repo option,
   never directly from the dirty development checkout. No new worktree is needed.
3. Recheck current, all 14 managed paths, dependencies, drift and journal. Require
   the 17-file manifest and only the intended adapter difference. Stage/verify a
   complete immutable release and preserve the previous release/history.
4. Activate with expected current 20261023T164459.630188Z-30124092. This changes the
   shared pointer for all 14 managed paths, with no other semantic payload changes.
   No migration or new live path is involved; prior immutable payloads and the
   activation journal provide rollback. No tmux/Ghostty reload or service restart.
5. New hook subprocesses read the managed adapter immediately. Existing launchers
   keep their loaded module; their finalizer is unchanged. Verify real working,
   stopped and permission delivery on disposable launches before live acceptance.

Already-ended records are intentionally not revived by this patch. Affected
running agents remain untouched/unlabelled until naturally reopened through cdev
after deployment. Any in-place registration recovery requires separate approval
and identity review; changing code alone does not repair those records.

Future POSIX sh/Zsh recovery, using the recorded new release ID:

```sh
python3 -B scripts/deploy.py --repo CLEAN_EXPORT rollback --expect-current FIX_RELEASE --approve
```

This validates and atomically restores the previous release, expected to be
20261023T164459.630188Z-30124092. It does not reload applications or rewrite
runtime records/pins. Future new launches would again have the old SessionEnd
behavior. Stop on unexpected drift; no production activation is authorized now.

## Live acceptance after separately approved activation

1. Use Codex 0.164.0 in a disposable ordinary cdev project/window, leaving existing
   project agents alone. Verify the eight fixed hooks remain trusted; stop if a
   new review unexpectedly appears. Run a real brief read-only turn: its exact
   pane/UUID registration must stay live and its title must shimmer while working.
2. Let the turn finish: require the white stopped dot, a single review notification,
   and attention navigation. A dot means stopped, not guaranteed task success.
3. Exercise a genuine native approval request for a harmless read-only operation.
   While pending, require the red alert; after approval, require working then
   stopped. If the current policy cannot produce an observable approval request,
   record this state as unverified rather than injecting an event or changing policy.
4. Record the disposable conversation UUID. Quit only that test CLI normally and
   verify finalization clears its status. Close its owned test window, reopen the
   same project through cdev, and require the exact same UUID with a fresh valid
   launch identity. Repeat a real working/stopped turn and check notification
   deduplication. Remove only accounted-for disposable resources after acceptance.

Already-running ended registrations are not acceptance subjects to restart or
edit. Their owners may naturally close/reopen them later; no tmux reload is needed.
