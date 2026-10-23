# Small workstation conveniences

`Ctrl+F`, release, `a` acknowledges the **selected Codex pane's stopped turn**.
Its white dot and attention-queue entry disappear. Another stopped agent in the
same window still keeps its own dot. Shell, working and approval panes are no-ops.
Acknowledgment neither sends input nor edits the Codex lifecycle cache. The next
turn becomes actionable normally; merely visiting a pane still does not acknowledge.

The callback captures a displayed event hash and revalidates pane, launch, turn
and revision under the lifecycle cache lock. A delayed key cannot clear a newer
turn or another agent. The publisher continues to see the original snapshot,
preserving its existing notification deduplication. State lives in pane options;
there is no new hook, file store or background process.

Independent acknowledgment recovery: unbind only prefix `a`, roll back to the
recorded preceding release using the deployment tool, and run that release's
dashboard installer to repin its callbacks. No agent/editor restart is required.
Do not roll back a later unrelated component inadvertently; see STATUS.md for
the applicable release and backup references.
