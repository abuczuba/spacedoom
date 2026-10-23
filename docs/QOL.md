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

Normal `~/.config/doom/config.el` loads `(load! "clipboard")`, replacing its old
two-line simpleclip initialization. **No launch flags are needed** for `emacs -nw`,
a native Doom daemon, or cdev. All clipboard settings live in the managed
`configs/doom/clipboard.el`: `use-package! simpleclip` owns mode initialization;
`map!` owns SPC y. Keeping this one public settings unit separate avoids importing
or replacing unrelated personal Doom configuration. There is no launcher loader.

The audit found no user-defined Cmd+C override. Simpleclip supplied `s-c` in its
own minor-mode map; the config now retires just that package override and leaves
Emacs' global Command-key map, simpleclip cut/paste and other copy keys intact.
Reloading does not re-enable an already-active simpleclip mode, which would
otherwise overwrite its saved clipboard/kill-ring integration functions.

The deployment tool's `configure-doom-clipboard --release RELEASE
--expect-config-sha256 HASH --approve` backs up normal config.el privately,
preserves its mode, and atomically replaces only the exact inspected stanza.
It rejects drift, links, an unexpected current release and ambiguous stanzas.
The schema-2 backup uses the existing `restore --backup ID --approve` command;
restoration accepts only the recorded original or exact deployed contents/mode,
is retryable, and refuses subsequent personal edits. Config.el stays a regular
unmanaged file; private content never enters Git or copied release payloads.

To reverse normalization, restore that config.el backup **before** rolling the
release pointer back. The preceding accepted module and cdev launchers then work
as before. For the already-running daemon, load the previous clipboard file and
restore simpleclip's package-default s-c mapping if desired; do not restart clients.
Exact release/backup references are in STATUS.md. Do not remove the original
addon symlink unless reverting the entire earlier clipboard adoption separately.
