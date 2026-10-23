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
To remove acknowledgment alone after another component is adopted, unbind `a`,
unset only the panes' `@dotfiles-agent-ack` options, and refresh the dashboard.
For permanent removal keep the clipboard commit and revert only the separate
acknowledgment commit into a new approved release.

In terminal Doom, select with Evil `v`, `V` or `Ctrl+V`, then press **SPC y**.
This uses simpleclip's macOS transport and Evil's expanded selection (including
the final character, complete lines or a rectangle). It preserves the selection,
buffer, kill ring and ordinary `y` binding. Outside visual mode it gives a hint.

Ghostty's effective Cmd+C is `copy_to_clipboard:mixed`: it consumes the key before
tmux/Emacs. Its documented [keybinding actions](https://ghostty.org/docs/config/keybind)
do not select actions by the application in a tmux pane. `performable:` only
tests terminal selection; a chained forwarded key would also reach shell/Codex
panes. Preserve native terminal copying and use this Doom-native fallback.

The persistent server loads the addon through cdev.el. Existing clients acquire
it by loading only the addon once, without restarting the server or clients.
`CDEV_EDITOR_MODE=standalone cdev PROJECT` also loads it. For a direct standalone
invocation outside cdev, use `emacs -nw --load ~/.config/doom/clipboard.el` (or
`M-x load-file` in an already-running standalone). No private config.el is edited.

Independent clipboard recovery: run `M-x dotfiles-clipboard-uninstall` in Doom,
restore only the `doom-clipboard` migration backup, then roll back its pointer
activation to the acknowledgment release. Run the restored dashboard installer
to repin callbacks. Persistent buffers, clients and Codex remain running. Restoring
the backup removes only the new addon link, whose original state was absent.
