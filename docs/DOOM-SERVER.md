# Persistent Doom clients — repository candidate

No live Fish/Doom configuration or persistent service has been changed. Existing
standalone Emacs and Codex processes remain in place. Only future, approved cdev
launches use the new client path; reuse never replaces an existing editor pane.

## Inspected baseline

The live 130-line cdev function creates/reuses a Git-root window, Doom left and
Codex right at 50/50. Its Python helper preserves fresh / project-scoped `resume
--last` / verified UUID-pin semantics. The previous temporary tests were inspected
and their restoration, naming, collision, concurrency and policy checks were
ported into repository tests. No user conversation content was read.

Installed Emacs and emacsclient are 31.1 from `/Applications/Emacs.app`, reached
through `/opt/homebrew/bin`. Doom is under `~/.config/emacs`; its source modules
live under `sources/doom+`, user configuration under `~/.config/doom`. Enabled
modules include Evil, Ivy, workspaces/persp-mode, Projectile, Org and vterm.
The working terminal launcher supplies `MACOSX_DEPLOYMENT_TARGET=27.0`. Doom's
captured environment contains that same value and the bundled libgccjit library
paths. The isolated native-compilation test passes with those paths and target.
No package install, Doom sync/env regeneration or graphical font fix was needed.

The inspected Fish config contains an unsafe legacy `toggle_emacs_daemon` that
can pkill all Emacs instances. It is not called or changed. Do not use it to manage
this service. Existing GUI helpers/default-server behavior are outside this task.
The candidate neither adopts nor sources the whole Fish config.

## Frame and project model

Each new cdev editor uses `emacsclient -t`, a dedicated absolute socket and
`--alternate-editor=/usr/bin/false`. No `-n`, empty alternate editor, automatic
daemon creation, GUI frame or fallback server is used. Server readiness is checked
before any new tmux pane. A race/failure remains visible; failed new panes are
retained for inspection, never silently killed/replaced or retried as fresh chats.

The terminal frame receives its canonical Git root as an escaped frame parameter.
After normal Doom startup, `doom/cdev.el` uses the **existing native workspace
implementation**. Its stable workspace name includes the root's basename and hash.
`+workspace-project` records project context. Native perspectives are frame-local;
there is no parallel workspace system or global directory hook. cdev project
workspaces opt out of Doom's normal auto-deletion when a client frame closes,
preserving their buffers and native window state for reconnection.

Installed `SPC f f` is `find-file`, remapped to `counsel-find-file`. The dedicated
server binds that leader key to a small delegating command: dynamically bind the
file picker's starting directory to **this frame's root**, then invoke the normal
remapped finder. The association survives workspace switches and other frames.
Buffer-local `default-directory` is never permanently reset. `SPC f F`, C-x C-f,
Dired, Projectile, absolute paths and explicit `../` navigation retain their
ordinary semantics. Non-cdev frames delegate from their usual buffer directory.

Two simultaneous real terminal clients were tested using the installed Doom
libraries in a sanitized disposable home. Actual `SPC f f` keys through each PTY
start Ivy in the correct root from nested files and scratch buffers; changing A's
workspace does not change B's perspective/root. Closing/reconnecting A preserves
its workspace, unsaved buffer and project-root picker behavior. A second test
uses actual cdev tmux clients and kills only its owned editor pane: the daemon,
other client, buffers and right-hand Codex stand-in survive.

Buffers are shared deliberately. Two clients editing the same file see the same
buffer contents. Workspace views/project associations are independent. Memory
persistence across client closure is tested; unsaved text is not guaranteed after
a daemon crash, shutdown or reboot. Normal Emacs backup/autosave behavior remains
owned by the existing Doom configuration.

## Daemon lifecycle

One named server uses `~/.local/state/cdev-emacs/server`, independent of the default
Emacs server. The directory must be owned by the user, mode 700; the socket must
be a user-owned Unix socket. Symlinked/unsafe directories and unexpected sockets
are refused, not removed. A held advisory lock prevents duplicate managers.
The manager waits for one foreground `--fg-daemon` child and forwards signals
only to that child; it does not poll or scan/kill other Emacs processes.

The proposed user LaunchAgent is `local.dotfiles.doom`. Its ProgramArguments pin
the complete release; it loads the integration **after** normal Doom startup.
It provides a fixed Homebrew/system PATH, deployment target 27.0 and umask 077.
Its private log directory is prepared by the separately approved bootstrap tool
before launchd opens stdout/stderr. Existing regular log content is preserved.

`RunAtLoad=true`, `KeepAlive=false` is intentional: launchd owns startup/process
tracking, and failure stays visible in job exit status/logs until explicit
recovery. There is **no unattended crash-restart loop**. `kickstart` omits `-k`,
so it cannot restart a running job. It starts a stopped loaded job after the user
has inspected the error. The tool refuses shutdown while clients/modified buffers
remain, or when safe shutdown state cannot be established.

Management commands, from POSIX sh/Zsh or as individual Fish commands:

```sh
python3 -B scripts/doom_service.py plan
python3 -B scripts/doom_service.py status
# Each line below requires its own operation-specific approval:
python3 -B scripts/doom_service.py bootstrap --approve
python3 -B scripts/doom_service.py kickstart --approve
python3 -B scripts/doom_service.py bootout --approve
```

The tool never installs a plist. The exact LaunchAgent file must first be
individually backed up/migrated through the deployment tool. No launchctl mutation
has been executed during development; those paths are tested with mocks only.

Manual foreground fallback, after separate production-daemon authorization:

```sh
/usr/bin/python3 -B /ABSOLUTE/RELEASE/cdev/doom-server.py serve
```

Use Terminal.app and keep that command running. Do not bootstrap launchd while a
manual manager owns the named server. Save/close owned clients and deliberately
stop the manual manager before transferring ownership; never kill discovered
standalone editors. No restart is necessary merely to reconnect clients. For an explicitly approved
manual shutdown, first save buffers and close its clients, then use only the
named socket (never the default server):

```sh
/opt/homebrew/bin/emacsclient -s ~/.local/state/cdev-emacs/server -a /usr/bin/false -e '(kill-emacs)'
```

This deliberately ends the named server and its in-memory state; the foreground
manager then exits and releases its lock. It is not an automatic recovery step.

## Failure and independent reversal

When unavailable, cdev returns a visible readiness error before creating a new
project window. Inspect `server.log` and `doom_service.py status`, then use the
approved serve/bootstrap/kickstart path. A stale socket is never auto-deleted:
confirm no manager/daemon owns it, preserve evidence, and approve exact-path
cleanup separately. A hung service requires reviewed Terminal.app recovery;
the tool refuses to guess whether its in-memory buffers are safe to discard.

Explicit per-invocation Fish fallback:

```fish
CDEV_EDITOR_MODE=standalone cdev /path/to/PROJECT
```

This restores the original `emacs -nw` launch/environment for **new** windows,
while retaining Codex restoration and optional activity tracking. Existing windows
are selected as-is. It neither stops the named daemon nor deletes its buffers.
Restoring the two original Fish functions is a separate approved file operation;
other Fish/Doom configuration remains unmanaged. See the exact
[deployment and rollback order](MILESTONE-DEPLOYMENT.md).

Unverified live behavior: full private Org/custom configuration in the new named
daemon, login/logout and reboot behavior, launchd bootstrap/recovery, real Codex
hook trust/delivery, and physical visual acceptance of the combined workflow.
The sanitized fixture excludes private Org/custom files and reports snippet
warnings; no claim is made that every private customization was exercised.
GNU's [server model](https://www.gnu.org/software/emacs/manual/html_node/emacs/Emacs-Server.html)
and [terminal client semantics](https://www.gnu.org/software/emacs/manual/html_node/emacs/emacsclient-Options.html)
are the upstream lifecycle references; installed Doom/persp/Ivy source and the
disposable tests establish the project-specific behavior above.
