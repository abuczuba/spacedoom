# Codex approval state

For shared app-server cdev sessions, the existing retained connection refines
the hook-driven dashboard with native approval IDs. It does not start another
monitor, issue permission decisions, or infer activity from terminal text.

`PermissionRequest` runs before review, so its tool name cannot establish that a
person is still needed. An automatic reviewer may resolve it without presenting
a human prompt. See the [hook contract](https://learn.chatgpt.com/docs/hooks#permissionrequest).

- A native command, file-change or permission approval request supplies its
  request ID, thread, turn and item. Only a known live turn can become waiting.
- `serverRequest/resolved` retires that exact request. Other pending requests
  remain actionable. Resolution establishes answered/cleared, not the decision
  or task success. See [native approvals](https://learn.chatgpt.com/docs/app-server#approvals).
- Duplicate requests and resolutions are inert; early resolutions leave
  tombstones. Retired turns and conflicting IDs cannot revive waiting state.
  Integer and string request IDs remain distinct.

Every update rechecks the launch token, socket/pane/server identity, launcher and
child process births, and kernel-verified backend birth. The private cache stores
IDs and state, never commands, reasons, decisions or conversation contents.
Only the three approval methods and their resolution can update this ledger.
Hooks still establish working/stopped turns; Collie forwarding is unchanged.

The reader bounds complete JSON messages to 1 MiB, reads in 64 KiB chunks and
discards unrelated data. Unrelated messages cause no state reads or subprocesses.
Inactive request tombstones are bounded; live requests are not silently evicted.
Existing socket shutdown and reader cleanup remain in place.

Already-running launchers keep their loaded reader; natural cdev reopening
adopts the repair. Deployment does not restart them or rewrite their records.
Local launches without a retained shared connection keep their prior hook-only
compatibility behavior; precise approval resolution is not asserted for them.
Third-party workmux hooks are preserved rather than replaced.
