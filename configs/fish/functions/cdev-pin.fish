# Persistent pins change future new workspaces; never touch an existing agent.
function cdev-pin --description 'Set/show/remove a verified per-project Codex session pin'
    set -l action pin
    set -l identity
    set -l target .
    if test (count $argv) -lt 1; or test (count $argv) -gt 2
        printf 'usage: cdev-pin UUID [PROJECT] | cdev-pin --show [PROJECT] | cdev-pin --remove [PROJECT]\n' >&2
        return 2
    end
    switch "$argv[1]"
        case --show
            set action show
        case --remove
            set action unpin
        case '*'
            set identity "$argv[1]"
    end
    if test (count $argv) -eq 2
        set target "$argv[2]"
    end
    set -l helper '@RELEASE@/cdev/codex_session.py'
    if test "$action" = pin
        /usr/bin/python3 -B "$helper" "$action" --root "$target" --session "$identity"
    else
        /usr/bin/python3 -B "$helper" "$action" --root "$target"
    end
end
