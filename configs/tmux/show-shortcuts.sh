#!/bin/sh
# POSIX sh. Read only this release's siblings, never the development checkout.
set -eu
shortcuts_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)

render() {
    /usr/bin/awk '
        BEGIN {
            esc = sprintf("%c", 27)
            blue = esc "[1;38;2;38;79;120m"
            rust = esc "[38;2;139;58;47m"
            reset = esc "[0m"
        }
        /^@/ || /^SHORTCUTS/ || /^[-+=]+$/ || /^  [A-Z \/+]+$/ {
            print blue $0 reset; next
        }
        /^  / && index($0, " | ") {
            split_at = index($0, " | ")
            print rust substr($0, 1, split_at - 1) reset substr($0, split_at)
            next
        }
        { print }
    ' "$shortcuts_dir/cheatsheet.txt"
}

case ${1-} in
    --plain) cat "$shortcuts_dir/cheatsheet.txt"; exit ;;
    --render) render; exit ;;
    '') ;;
    *) printf '%s\n' 'Usage: show-shortcuts.sh [--plain|--render]' >&2; exit 2 ;;
esac

# No search history or inherited pager options. Custom keys affect this guide only.
# The tmux popup supplies the default dark foreground and light background.
export LESS= LESSHISTFILE=- LESSKEY=/dev/null LESSKEYIN=/dev/null
LESS_TERMCAP_so=$(printf '\033[38;2;32;36;43;48;2;225;205;162m')
LESS_TERMCAP_se=$(printf '\033[0m')
export LESS_TERMCAP_so LESS_TERMCAP_se
render | /usr/bin/less -R -i --incsearch --wordwrap \
    --lesskey-src="$shortcuts_dir/shortcuts.lesskey" \
    -P '1-8 sections | / search | n/N matches | g/G ends | q close'
