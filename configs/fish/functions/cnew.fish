# Create only: opening the project is an explicit, separate cdev invocation.
function cnew --description 'Create a minimal personal Git project under ~/dev'
    if test (count $argv) -ne 1; or not string match -qr '^[A-Za-z0-9][A-Za-z0-9._-]*$' -- "$argv[1]"
        printf 'usage: cnew NAME (letters/digits first; then letters, digits, dots, underscores or hyphens)\n' >&2
        return 2
    end
    if not command -sq git
        printf 'cnew: git must be executable on PATH.\n' >&2
        return 1
    end
    set -l name "$argv[1]"
    set -l base "$HOME/dev"
    set -l target "$base/$name"
    if test -e "$target"; or test -L "$target"
        printf 'cnew: refusing existing path: %s\n' "$target" >&2
        return 1
    end
    set -l parent "$base"
    if not test -d "$base"
        set parent "$HOME"
    end
    if command git -C "$parent" rev-parse --git-dir >/dev/null 2>&1
        printf 'cnew: refusing to create a nested repository under %s.\n' "$base" >&2
        return 1
    end
    command mkdir -p -- "$base"; or return 1
    # mkdir is the ownership claim: concurrent calls cannot scaffold the same path.
    command mkdir -- "$target"; or return 1
    command git init --quiet --initial-branch=main --template= "$target"
    or begin
        printf 'cnew: git initialization failed; left %s for inspection.\n' "$target" >&2
        return 1
    end
    # Noclobber redirection also protects against files appearing after mkdir.
    printf '# %s\n\nDescribe the project purpose here, then add verified setup and usage.\n' "$name" >? "$target/README.md"
    and printf '# %s — project instructions\n\nRead README.md for the project purpose and usage.\n\nNo stack or setup/test commands have been established yet. Inspect the repository\nbefore choosing them; record verified commands and project-specific safeguards\nhere as they become known. Shared conventions belong in global instructions.\n' "$name" >? "$target/AGENTS.md"
    and printf '.DS_Store\n.env\n.env.*\n!.env.example\n' >? "$target/.gitignore"
    or begin
        printf 'cnew: scaffolding failed; left %s for inspection.\n' "$target" >&2
        return 1
    end
    printf 'cnew: created %s (main; no commits).\nOpen inside tmux: cdev %s\n' "$target" "$name"
end
