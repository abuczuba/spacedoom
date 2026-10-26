# Installing or borrowing this setup

Start with the files you actually want. These are my opinionated Apple Silicon
configs, including `/opt/homebrew` paths, a few Linux-only aliases and personal
project helpers. Edit Git identity/signing references and review Fish before
adopting it. Legacy `toggle_emacs_daemon`, `toggle_ssh`, package-update and `rr`
helpers are opt-in old utilities; they are not used by cdev or this installer.

## Prerequisites

The tested workstation runs macOS 27, Python 3.12.15, Fish 4.9.3, tmux 3.8,
Ghostty 1.3.1, Starship 1.27.0, Emacs/emacsclient 31.1, Doom 2.2.4, Codex
0.164.0 and workmux 0.1.276. Python 3.11+ supplies `tomllib`; the older release
tool still reads historical receipts, but the complete manifest needs TOML checks.
System `/usr/bin/less` must be 668+. Install Xcode Command Line Tools for native
Emacs modules and the optional macOS socket tests.

1. Install [Homebrew](https://brew.sh/) using its own instructions. Review the
   optional [Brewfile](../Brewfile), then run `brew bundle --file=Brewfile` if
   you want those packages. Nothing in our deployment tool installs packages.
2. Supply a matching Emacs and emacsclient at `/opt/homebrew/bin`. This machine
   links to `/Applications/Emacs.app`; it is not an Emacs build recipe. Terminal
   fonts come from Ghostty; graphical Emacs font resolution depends on your build.
3. Install [Doom](https://github.com/doomemacs/core#install) at `~/.config/emacs`
   and run its `bin/doom install`. Keep upstream Doom and `.local/` outside this
   repository. Our real module/package choices are in `configs/doom/`.
4. Install [Codex](https://github.com/openai/codex) and
   [workmux](https://github.com/raine/workmux) separately if using cdev/dashboard.
   Authenticate privately. Codex 0.164.0's native hook review must be completed by
   the operator; copied trust files and automatic trust are not part of bootstrap.
5. Put [TPM](https://github.com/tmux-plugins/tpm),
   [tmux-dotbar](https://github.com/vaaleyard/tmux-dotbar) and
   [Rose Pine](https://github.com/rose-pine/tmux) under `~/.tmux/plugins/`.
   For a fresh home, clone those repositories to `tpm`, `tmux-dotbar` and `tmux`
   respectively. Existing plugin installations must be inspected before replacement.

Fonts used here are Source Code Pro and FiraCode Nerd Font. The small legacy fzf
Fish integration is included with its MIT license and exact upstream revision;
no Fisher download is required. Starship uses built-in defaults. Other language
servers, TeX, Haskell and Linux utilities are optional dependencies of my helpers,
not prerequisites for every part of the desktop.

## Bootstrap using copied releases

These commands are POSIX sh/Zsh; run them deliberately on the target machine.
Do not run installation commands as a regression test on a working home.

```sh
mkdir -p ~/dev
git clone https://github.com/abuczuba/dotfiles.git ~/dev/dotfiles
cd ~/dev/dotfiles
python3.12 scripts/deploy.py check
python3.12 scripts/deploy.py plan
python3.12 scripts/deploy.py stage --approve
```

Record the returned ID as `RELEASE`. Staging copies the manifest, validates
syntax/dependencies/references, and leaves `current` unchanged. A clean checkout
is the release input; Git edits and commits never deploy automatically. Staging
assigns a new ID each time; it does not silently reuse or replace another release.

Adopt chosen components one at a time, reviewing each plan and backup:

```sh
python3.12 scripts/deploy.py verify --release "$RELEASE"
python3.12 scripts/deploy.py plan --release "$RELEASE"
python3.12 scripts/deploy.py migrate --release "$RELEASE" --component tmux --approve
```

Available components are listed by `plan`/`deploy/manifest.json`. The desktop
additions are `doom-config`, `fish-config`, `aerospace`, `git-config`, `shell`
and `gh`. The original integrations use `ghostty`, `cdev`, `fish-cdev`,
`fish-cnew`, `codex-instructions`, `doom-client`, `doom-clipboard`, and
`doom-service`. The optional `tmux-dashboard` live helper aliases need not be
adopted: tmux pins its renderer directly inside the release.

Each migration backs up exact existing files/modes and records absent targets
before making file symlinks. No whole directories or checkout files are linked.
Multiple live file replacements are not jointly atomic; keep original-file
backups until the new startup paths have been checked.

For Doom, create an optional private `~/.config/doom/identity.el` from
`configs/doom/identity.example.el` before adopting `doom-config`; keep it mode
600 and out of Git. Without it, the public noreply identity is used. Custom's
generated `custom.el` remains writable and external; its two current preference
values are already present in `config.el`. After adopting `init.el`/`packages.el`,
run `~/.config/emacs/bin/doom sync` yourself, then `doom doctor`. Never copy
another machine's generated startup or environment snapshot.

## Start and reload explicitly

The release tool starts/reloads nothing. Open a new Fish shell to read new
functions. Keep Ghostty's `Cmd+Shift+N → Ctrl+F c` forwarding before enabling
attention navigation on `n`; see [workflow](WORKFLOW.md). Load tmux only on an
inspected server, and review its plugin startup before any reload.

For persistent Doom, first use `scripts/doom_service.py plan` and `status`.
`bootstrap --approve` is the explicit opt-in service operation after its plist
is migrated. It is a user login service, not a root boot daemon. Its compiler
workaround is `MACOSX_DEPLOYMENT_TARGET=27.0`; adapt that for other systems.
No second daemon or automatic fallback is started by cdev. `CDEV_EDITOR_MODE=standalone`
selects ordinary `emacs -nw`; see [Doom lifecycle](DOOM-SERVER.md).

Global Codex hooks/config/trust and workmux preferences are reviewed reference
copies, not auto-installed security configuration. Merge their desired values
manually; do not replace a populated Codex config with the example. Collie is
independent and opt-in; no Collie installation, pairing or service operation
occurs here. No command runs `direnv allow`.

## Borrowing less and checking changes

For a partial managed installation, edit the manifest/dependencies in your fork
before staging; keep the referenced-file closure. Or borrow plain config files
individually after your own backup. Files containing `@RELEASE@`/`@HOME@` are
templates and must be rendered or deliberately adapted, never sourced verbatim.
Do not remove mappings that are already live: restore their backups first.

Run `python3.12 scripts/test.py` for unit tests and `--integration` for private
tmux/PTY/Doom tests. The real-Doom fixture fingerprints the installed generated
startup and fails closed on another installation; review it rather than blindly
updating hashes. Native credentials and trust are not loaded by automated tests.
See [validation](VALIDATION.md), [rollback](WORKFLOW.md) and
[Terminal.app recovery](RECOVERY.md).
