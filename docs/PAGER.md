# Codex pager

The pager consumes **the dashboard's existing validated snapshot**. It adds no
Codex hooks, terminal scraper, lifecycle detector or persistent service. Working,
idle and unknown states are silent; verified waiting states publish priority 4
“Approval required”, and stopped turns priority 3 “Review needed”. A stopped turn
does not claim success. Only a verified Git project basename and fixed text leave
the Mac. Existing animation, attention navigation and workmux ownership stay intact.

The native tmux monitor calls the optional publisher on status changes. It writes
private dedup/outbox data, then starts a finite detached HTTP worker. No HTTP runs
in Codex or its hooks. Publishing uses a three-second socket timeout; explicit
rejections/connect failures retry at most three times while attention is still
valid. Unknown delivery outcomes or interrupted in-flight requests are suppressed
rather than replayed. Delivery is best effort, not guaranteed exactly once.
Initial/historical stopped states are baselined silently. Pending alerts expire
after two minutes or when the existing snapshot invalidates their agent/state.

Private configuration: `~/.config/cdev/pager.json`, owned by you, mode 600:

```json
{"enabled": true, "url": "https://YOUR-SERVER/YOUR-TOPIC"}
```

An optional `token` supplies bearer authentication. Never commit this file, a
real topic URL or credentials. Redirects and query-string credentials are refused.
The publisher uses the [documented ntfy HTTP API](https://docs.ntfy.sh/publish/).

After private configuration is prepared, the approved activation updates only
the existing native dashboard monitors using the release's `watch` command with
`--pager-config PATH`. That first refresh establishes the baseline. It does not
reload tmux, change keybindings or restart any agent. Release activation and
monitor installation are separately recorded parts of the authorized pager task.

Commands below use POSIX sh/Zsh. `RELEASE` and `SOCKET` must be the verified paths:

```sh
python3 -B RELEASE/tmux/pager.py status --socket SOCKET
python3 -B RELEASE/tmux/pager.py test --project dotfiles --approve
python3 -B RELEASE/tmux/pager.py disable --approve
```

The test command sends one explicit transport test, not a fabricated lifecycle
event. Confirm the iPhone receipt. Disabling preserves private credentials and
takes effect before the next publish (an already in-flight request may finish).
For code rollback, use the existing deployment tool to restore the prior pointer,
then run that release's `agent-dashboard.py watch --socket SOCKET`; it restores
the previous monitor without rebinding keys. No tmux reload is needed.

Ordinary cdev lifecycle fixtures and workmux status validation are tested in
isolation. Manually recovered/shared-server conversations currently produce no
valid pane records in production. They remain silent; this pager does not weaken
the existing runtime/ancestry checks or restart those conversations to label them.
Workmux lacks turn IDs, so repeated same-state samples are conservatively folded
until an observed state change. Shared-server event delivery remains a separate
native instrumentation limitation, not proof supplied by a transport test.
