#!/bin/sh
# READ-ONLY targeted audit. Does not read file contents or mutate state.
set -eu

printf '%s\n' '== Personal macOS dotfiles: targeted read-only audit =='
printf 'Date: %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
printf 'Platform: %s\n' "$(uname -sm)"
if command -v sw_vers >/dev/null 2>&1; then
  printf 'macOS: %s\n' "$(sw_vers -productVersion)"
fi
printf '\n'

check_path() {
  target=$1
  if [ -L "$target" ]; then
    state='SYMLINK (target intentionally not shown)'
  elif [ -f "$target" ]; then
    state='FILE'
  elif [ -d "$target" ]; then
    state='DIRECTORY'
  elif [ -e "$target" ]; then
    state='OTHER'
  else
    state='ABSENT'
  fi
  printf '%-12s %s\n' "$state" "$target"
}

printf '%s\n' '-- Candidate live files (metadata only) --'
check_path "$HOME/.config/ghostty/config.ghostty"
check_path "$HOME/.config/ghostty/config"
check_path "$HOME/.config/ghostty/profiles/spacemacs-dark.ghostty"
check_path "$HOME/Library/Application Support/com.mitchellh.ghostty/config.ghostty"
check_path "$HOME/Library/Application Support/com.mitchellh.ghostty/config"
check_path "$HOME/.tmux.conf"
check_path "$HOME/.config/tmux/czuba-navigation.conf"
check_path "$HOME/.config/fish/config.fish"
check_path "$HOME/.config/fish/functions/cdev.fish"
check_path "$HOME/.config/aerospace/aerospace.toml"

printf '\n%s\n' '-- Relevant executables (availability only) --'
for tool in git codex ghostty fish tmux emacs workmux aerospace; do
  if command -v "$tool" >/dev/null 2>&1; then
    printf '%-12s %s\n' "$tool" 'FOUND'
  else
    printf '%-12s %s\n' "$tool" 'NOT ON PATH'
  fi
done

printf '\n%s\n' '-- Working-directory Git state (read-only) --'
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'Git root: %s\n' "$(git rev-parse --show-toplevel)"
  git status --short --branch
else
  printf '%s\n' 'Not inside a Git worktree.'
fi
printf '\n%s\n' 'No file contents inspected. No changes performed.'
