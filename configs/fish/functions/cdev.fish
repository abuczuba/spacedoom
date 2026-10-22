# Autoloaded; project-scoped conversation restoration preserves Codex policies.
function cdev --description 'Reuse or open a Git project in tmux: Doom left, Codex right'
    if not set -q TMUX; or test -z "$TMUX"
        printf 'cdev: run this command inside tmux.\n' >&2
        return 1
    end
    if test (count $argv) -gt 1
        printf 'usage: cdev [PROJECT_DIRECTORY]\n' >&2
        return 2
    end
    set -l target .
    if test (count $argv) -eq 1
        set target "$argv[1]"
    end
    set -l root (command git -C "$target" rev-parse --show-toplevel 2>/dev/null)
    if test $status -ne 0; or test -z "$root"
        printf 'cdev: not a Git working tree: %s\n' "$target" >&2
        return 1
    end
    set root (path resolve -- "$root")
    if string match -qr '[\r\n\t]' -- "$root"
        printf 'cdev: project paths containing tabs/newlines are unsupported.\n' >&2
        return 1
    end
    set -l session (command tmux display-message -p '#{session_id}' 2>/dev/null)
    if test $status -ne 0
        printf 'cdev: cannot reach the current tmux server.\n' >&2
        return 1
    end
    set -l digest (printf '%s' "$root" | command shasum -a 256 | string split ' ')[1]
    set -l lock cdev-workspace
    command tmux wait-for -L "$lock"; or return 1
    __cdev_open "$root" "$session" "$digest"
    set -l result $status
    command tmux wait-for -U "$lock"
    return $result
end

function __cdev_open --argument-names root session digest
    set -l name (path basename -- "$root" | string replace -ar '[^A-Za-z0-9_-]' '_')
    set -l occupied
    set -l windows (command tmux list-windows -a -F (printf '%s\t%s\t%s' '#{window_id}' '#{session_id}' '#{window_name}'))
    for row in $windows
        set -l fields (string split \t -- "$row")
        set -l recorded_root (command tmux show-options -w -q -v -t "$fields[1]" @cdev_root)
        if test "$fields[3]" = "$name"
            set -a occupied "$fields[3]"
        else
            # Protect a live project agent even if its window was renamed/generic.
            set -l programs (command tmux list-panes -t "$fields[1]" -F '#{pane_current_command}')
            if not contains -- codex $programs; and test "$recorded_root" != "$root"
                continue
            end
        end
        set -l paths (command tmux list-panes -t "$fields[1]" -F '#{pane_current_path}')
        set -l matches 1
        set -l saw_root 0
        for pane_path in $paths
            set -l pane_root (command git -C "$pane_path" rev-parse --show-toplevel 2>/dev/null)
            if test $status -eq 0; and test -n "$pane_root"; and test (path resolve -- "$pane_root") = "$root"
                set saw_root 1
            else
                set matches 0
            end
        end
        if test "$matches" = 1; and test (count $paths) -gt 0
            # Only select: never respawn, split, rename, or send keys to existing panes.
            command tmux select-window -t "$fields[1]"; or return 1
            if test "$fields[2]" != "$session"
                command tmux switch-client -t "$fields[2]"; or return 1
            end
            printf 'cdev: reused %s (%s)\n' "$fields[3]" "$root"
            return 0
        end
        if test "$saw_root" = 1; or test "$recorded_root" = "$root"
            printf 'cdev: agent window %s has mixed or unverifiable pane roots; no process launched.\n' "$fields[3]" >&2
            return 1
        end
    end
    if contains -- "$name" $occupied
        printf 'cdev: window %s exists with a different or unverifiable Git path; no process launched.\n' "$name" >&2
        return 1
    end
    set -l editor (command -s emacsclient)
    set -l agent (command -s codex)
    if test -z "$agent"
        printf 'cdev: codex must be executable on PATH.\n' >&2
        return 1
    end
    set -l helper '@RELEASE@/cdev/codex_session.py'
    set -l server '@RELEASE@/cdev/doom-server.py'
    set -l dashboard_mode 1
    if set -q CDEV_DASHBOARD
        set dashboard_mode "$CDEV_DASHBOARD"
    end
    set -l editor_command /usr/bin/python3 -B "$server" client --project "$root" --emacsclient "$editor"
    # Explicit, independently reversible editor fallback. Never auto-start a
    # daemon or silently substitute a separate editor when readiness fails.
    set -l editor_mode client
    if set -q CDEV_EDITOR_MODE
        set editor_mode "$CDEV_EDITOR_MODE"
    end
    switch "$editor_mode"
        case client
            if test -z "$editor"
                printf 'cdev: client mode requires emacsclient on PATH.\n' >&2
                return 1
            end
            /usr/bin/python3 -B "$server" check --emacsclient "$editor"; or return 1
        case standalone
            set editor (command -s emacs)
            if test -z "$editor"
                printf 'cdev: standalone fallback requires emacs on PATH.\n' >&2
                return 1
            end
            set editor_command "$editor" -nw
        case '*'
            printf 'cdev: CDEV_EDITOR_MODE must be client or standalone.\n' >&2
            return 2
    end
    # Preflight before creating any panes: bad/missing pins never become fresh chats.
    set -l restore_mode (/usr/bin/python3 -B "$helper" plan --root "$root")
    if test $status -ne 0
        return 1
    end
    # Direct command arguments avoid interpolation of project paths into shell code.
    set -l window (command tmux new-window -d -P -F '#{window_id}' -t "$session:" -n "$name" -c "$root" env MACOSX_DEPLOYMENT_TARGET=27.0 $editor_command)
    if test $status -ne 0; or test -z "$window"
        printf 'cdev: could not create the editor window.\n' >&2
        return 1
    end
    command tmux set-window-option -t "$window" automatic-rename off
    command tmux set-window-option -t "$window" remain-on-exit on
    command tmux set-window-option -t "$window" @cdev_root "$root"
    set -l right (command tmux split-window -d -h -l 50% -P -F '#{pane_id}' -t "$window" -c "$root" env CDEV_DASHBOARD="$dashboard_mode" /usr/bin/python3 -B "$helper" launch --root "$root" --codex "$agent")
    if test $status -ne 0; or test -z "$right"
        printf 'cdev: agent pane failed; editor window %s retained for recovery.\n' "$window" >&2
        return 1
    end
    sleep 0.3
    set -l states (command tmux list-panes -t "$window" -F '#{pane_dead}' 2>/dev/null)
    if test (count $states) -ne 2; or contains -- 1 $states
        set -l restore_error (command tmux show-options -p -q -v -t "$right" @cdev_resume_error 2>/dev/null)
        if test -n "$restore_error"
            printf 'cdev: %s\n' "$restore_error" >&2
        end
        printf 'cdev: editor/agent exited during startup; window %s retained for inspection; no process killed.\n' "$window" >&2
        return 1
    end
    command tmux select-pane -t "$right"
    command tmux select-window -t "$window"
    printf 'cdev: opened %s (%s; %s conversation mode)\n' "$name" "$root" "$restore_mode"
end
