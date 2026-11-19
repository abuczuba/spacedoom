# SPDX-License-Identifier: GPL-2.0-only
# Includes the Fish default prompt by Lily Ballard and fish-shell contributors.
# Personal adaptations by Matthew Nicholas Czuba; imported 2026-10-26.
# Migrated from original 2026-06-24 Fish config; preserves custom functions and aliases.
# Machine-specific behavior updated for /Users/czuba / Fish 4 on macOS.
#### reload fish config
alias fishrc="source ~/.config/fish/config.fish"

alias yo="echo 'wassup'"

#### Set Environment Variables
# set -gx EDITOR /usr/bin/vim
set -gx EDITOR emacs
set -gx VISUAL emacs
if test -x "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    set -gx BROWSER "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
end
set -gx PAGER /usr/bin/less

#### Persistent Terminal Behavior (New Addition)
set -gx LS_OPTIONS "-A --color=auto"

##### Greeting Moved to fish_greeting Function
# set -U fish_greeting "🐟"

#### Persistent Path Handling (Ensures All Binaries Work)
# Keep the old search-path intent without importing old Mac or Linux locations.
fish_add_path /opt/homebrew/bin /opt/homebrew/sbin
for candidate in $HOME/.local/bin $HOME/.emacs.d/bin $HOME/.config/emacs/bin $HOME/.cabal/bin
    if test -d $candidate
        fish_add_path $candidate
    end
end
if test -d /Library/TeX/texbin
    fish_add_path /Library/TeX/texbin
end

#### Vim-Like Clear
alias dG="clear"

#### Easy Tree on `cd`
alias t="tree"

#### No Hanging for Zathura
alias z="zathura --fork"

#### Open Ranger
alias r="ranger"

#### Helpful Aliases, some taken from gteixe7
alias cp="cp -i" # Confirm before overwriting something
alias mv="mv -i" # Confirm before overwriting something
alias df="df -h" # Human-readable sizes
alias free="free -m" # Show sizes in MB
alias np="nano -w PKGBUILD"
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"
alias ll="ls -Alh" # Always Show Dotfiles

#### Copy a cryptographically random, website-friendly password without printing it.
function passme --description 'Copy a 48-character random password'
    if not command -sq openssl; or not command -sq pbcopy
        printf 'passme: openssl and pbcopy are required.\n' >&2
        return 1
    end

    set -l attempts 0
    while test $attempts -lt 16
        set attempts (math $attempts + 1)
        if not set -l random (command openssl rand -base64 48)
            printf 'passme: secure random generation failed; clipboard untouched.\n' >&2
            return 1
        end
        if not string match -rq '^[A-Za-z0-9+/]{64}$' -- "$random"
            printf 'passme: unexpected generator output; clipboard untouched.\n' >&2
            return 1
        end
        # Discard +/ rather than mapping them: retained characters stay uniform.
        set -l password (string replace -ar '[+/]' '' -- "$random" | string sub -l 48)
        if not string match -rq '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[A-Za-z0-9]{48}$' -- "$password"
            continue
        end
        printf '%s' "$password" | command pbcopy
        set -l copy_status $pipestatus
        if test $copy_status[1] -ne 0; or test $copy_status[2] -ne 0
            printf 'passme: clipboard copy failed.\n' >&2
            return 1
        end
        echo 'Password copied to clipboard: 48 characters, including uppercase, lowercase and numbers. Fly safe! o7'
        return 0
    end
    printf 'passme: could not generate a compliant password; clipboard untouched.\n' >&2
    return 1
end

#### Pacman Goes Sudo; Aliases for Software Management
## Includes yay as aur helper - use `upall` to update everything
alias pacman="sudo pacman --color auto"
alias pac-update="sudo pacman -Syyu"
alias pac-upall="yay -Syu --noconfirm"

#### Half-Life Clock :)
alias thetime="perl $HOME/scripts/half_life_talking_clock/half-life_clock.pl"

#### Grub Update
alias update-grub="sudo grub-mkconfig -o /boot/grub/grub.cfg"

#### Add New Fonts
alias update-fc="sudo fc-cache -fv"

#### version
alias gstatus="git status"
alias pull="git pull"
alias push="git push"
alias fetch="git fetch"
alias branch="git branch -vv"
alias slog="git log --oneline -10"
alias vlog="git log --graph --oneline --all -15"

#### Custom Fish Prompt
function fish_prompt
    set -l last_pipestatus $pipestatus
    set -lx __fish_last_status $status
    set -l normal (set_color normal)
    set -q fish_color_status; or set -g fish_color_status red
    set -l color_cwd $fish_color_cwd
    set -l suffix '🐟'

    if functions -q fish_is_root_user; and fish_is_root_user
        set suffix (set_color yellow)"(><(((º>"(set_color normal)
    end

    set -l status_color (set_color $fish_color_status)
    set -l prompt_status (__fish_print_pipestatus "[" "]" "|" "$status_color" "$status_color" $last_pipestatus)

    echo -n -s (prompt_login) " " (set_color $color_cwd) (prompt_pwd) $normal (fish_vcs_prompt) " " $prompt_status $suffix " "
end

#### Fortune + Cowsay for Greeting
function fish_greeting
    if command -v fortune >/dev/null
        fortune | cowsay
        echo ""
    end
end

#### doom / emacs specific integration
##### daemon stuff (untested 03/20/25):
function toggle_emacs_daemon
    if pgrep -x Emacs >/dev/null
        echo "Stopping Emacs daemon..."
        emacsclient -e "(kill-emacs)"
        pkill -9 Emacs
        echo "Emacs daemon stopped."
    else
        echo "Starting Emacs daemon..."
        nohup emacs --daemon >/dev/null 2>&1 &
        echo "Emacs daemon started."
    end
end
##### client stuff:
###### old version that took no arguments:
#function emacs
#    nohup emacsclient -c -a '' >/dev/null 2>&1 &
#end
###### a fully functional fish alias for launching emacs with optional arguments:
function emacsgui
    if test (count $argv) -eq 0
        nohup emacsclient -n -c -a '' >/dev/null 2>&1
    else
        nohup emacsclient -n -c -a '' $argv >/dev/null 2>&1
    end
end

alias enw="emacs -nw"
##### bin/doom stuff:
alias dedit="doom edit"
alias dsync="doom sync"
alias dsyncup="doom sync -u"
alias ddoctor="doom doctor"
alias denv="doom env"
alias dpurge="doom purge"
##### client stuff junkyard (broken):
###### persistent emacs client frame from daemon, no debug log
###### if wishing to debug emacs issues, use this instead:
####### alias emacs="emacsclient -c -a '' & disown"
###### the following was chucked in favor of the functional implementation above:
####### alias emacs="nohup emacsclient -c -a '' >/dev/null 2>&1 &"

#### fish
# alias fconf="emacsclient -n -c -a '' ~/.config/fish/config.fish"
function fconf
    nohup emacsclient -n -c -a '' ~/.config/fish/config.fish >/dev/null 2>&1
end

#### Interactive Mode Hook (Retained from ThinkPad)
if status is-interactive
    # Commands to run in interactive sessions can go here
end

#### iCloud integration for all macOS environments
##### symlink for easy file management
set -l __icloud_root "$HOME/Library/Mobile Documents/com~apple~CloudDocs"
if test -d "$__icloud_root"; and not test -e "$HOME/icloud"; and not test -L "$HOME/icloud"
    ln -s "$__icloud_root" "$HOME/icloud"
end
##### alias for easy navigation
alias icloud="cd ~/icloud"

#### orgmode integration with iCloud, for all macOS environments
if test -d "$__icloud_root/org"; and not test -e "$HOME/org"; and not test -L "$HOME/org"
    ln -s "$__icloud_root/org" "$HOME/org"
end
alias org="cd ~/org"

#### Ensure Correct GHC Paths (From ThinkPad)
#set -q GHCUP_INSTALL_BASE_PREFIX[1]; or set GHCUP_INSTALL_BASE_PREFIX $HOME
#set -gx PATH $HOME/.cabal/bin /home/abucz/.ghcup/bin $PATH # ghcup-env
#set -Ux fish_user_paths $HOME/.cabal/bin $fish_user_paths

#set PATH $PATH /Users/abucz/.local/bin
# Old absolute path was /Users/abucz/.local/bin; handled above via $HOME.
if status is-interactive
    if command -sq starship
        starship init fish | source
    end
    if command -sq direnv
        direnv hook fish | source
    end
end

#### melange technologies
alias melnotes="cd ~/Documents/melange-org-notes"
if command -sq python3.12
    alias python3="python3.12"
end
alias mel="cd ~/melange-dev"

alias flushr="redis-cli flushall"
alias wm="workmux"

#### skinny graphing

function md
    source .venv/bin/activate.fish
    python3 generate_markdown.py
    deactivate
end

function mdpdf
    source .venv/bin/activate.fish
    python3 generate_markdown.py --pdf
    deactivate
end

function mdpdfl
    source .venv/bin/activate.fish
    python3 generate_markdown.py --pdf --local
    deactivate
end

function s
    pushd ~/repos/skinny-graph # Save current directory
    source .venv/bin/activate.fish
    python3 ozempic.py
    deactivate
    popd # Return to original directory
end

function pipe
    source .venv/bin/activate.fish
    python pipe.py run
    deactivate
end

function pipe3
    source .venv/bin/activate.fish
    python pipe.py run --days 3
    deactivate
end

#### (skinny) graph QA tewl
function q
    source .venv/bin/activate.fish
    python3 qag.py
    deactivate
end

function ppd
    source .venv/bin/activate.fish
    make run_app
    deactivate
end

#### parsing
# alias p="pipenv run python parse.py"
function p
    source .venv/bin/activate.fish
    python3 parse.py
    deactivate
end

# alias pdf="pipenv run python update_local_pdfs_from_cloud.py"
function pdf
    source .venv/bin/activate.fish
    python3 update_local_pdfs_from_cloud.py
    deactivate
end

# alias pos="pipenv run python interactive_pos_tagger.py"
function pos
    source .venv/bin/activate.fish
    python3 interactive_pos_tagger.py
    deactivate
end

#### graphing
# alias g="pipenv run python graph.py"
function g
    source .venv/bin/activate.fish
    python3 graph.py
    deactivate
end

#### refs
# quick ref reset (via skinny README)
function refs
    source .venv/bin/activate.fish
    pip install -r requirements.txt
    deactivate
end

# Reset refs (complete environment rebuild via skinny README)
function rr
    rm -rf .venv/
    python3.12 -m venv .venv
    source .venv/bin/activate.fish
    python3.12 -m pip install -r requirements.txt --force-reinstall
    deactivate
end

##### linting stuff on pwd
function lint
    isort --profile black .
    black .
end

##### run parser with langsmith tracing:
function pls
    source .venv/bin/activate.fish
    python ~/repos/parsing/langsmith_hook.py
    deactivate
end

##### evaluate with langsmith CLI tools:
function lsmith
    source .venv/bin/activate.fish
    python ~/repos/parsing/langsmith_cli.py $argv
    deactivate
end

##### other langsmith functionality:
alias plsr="lsmith recent"

#### SSH / SCP / Remote Toggling
function toggle_ssh
    if test (sudo systemsetup -getremotelogin) = "Remote Login: On"
        echo "Disabling SSH for security..."
        sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist
        echo "SSH is now OFF."
    else
        echo "Enabling SSH..."
        sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
        echo "SSH is now ON."
    end
end
if status is-interactive
    if command -sq fnm
        fnm env --use-on-cd --shell fish | source
    end
    set -gx GPG_TTY (tty)
end

# uv
fish_add_path "/Users/czuba/.local/bin"
