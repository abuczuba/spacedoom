# Dashboard startup recovery

An empty tmux server loads configuration before its first session exists. The
old dashboard installer called `list-windows` then, failed, and never installed
its session-created hook. Reconstructing tmux therefore lost monitoring/pager
activation and left the fallback n=new-window binding. This failure reproduces
without the remote-resume repair or any user plugins.

The title slot still loads before Dotbar. A bootstrap at the end of tmux.conf
now registers the existing session-created hook using global checks only. Once
the first session exists, the normal installer performs all format/binding
checks and installs attention navigation and the native monitor. Later sessions
use watch mode, preserving keys. No new daemon or monitor type is introduced.

Tests load sanitized startup copies before the first session on empty private
servers, reconstruct the server, and check later sessions/idempotence. User
plugins are inert fixtures; production theme acceptance is checked separately.

Manual recovery after a successful preflight, when authorized (POSIX shell):

```sh
python3 -B ~/.local/share/dotfiles-active/current/tmux/agent-dashboard.py install --socket /private/tmp/tmux-501/default --pager-config ~/.config/cdev/pager.json
```

The installer does not reload tmux or restart agents. Existing runtime disable
removes only its monitors and restores safe window creation. Rolling back the
release pointer reverses this startup correction independently of c7142af's
hook registration repair; neither operation restarts applications.
