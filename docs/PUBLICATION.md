# Publication review: abuczuba/dotfiles

The canonical repository is `~/dev/dotfiles`, branch `main`. GitHub account
`abuczuba` is authenticated. The target repository returned 404 on 2026-10-26;
no repository or remote has been created. Public creation and pushing are the
remaining explicit owner gate. No separate source repository, history rewrite,
force-push, service change or Collie PR is part of publication.

## What will become public

- Every tracked file at the approved HEAD: actual application configuration,
  small deployment/session/dashboard tools, tests, dependency/bootstrap material,
  original-work license and third-party notices, plus engineering documentation.
- The complete existing `main` ancestry, including original signed engineering
  commits, retired ntfy implementation, repairs and newly curated source/history.
  No old commit or immutable deployment was removed or rewritten.
- Intentional metadata: the owner's name/public GitHub noreply identity, local
  username/home-path examples, legacy project/helper names, release/backup IDs,
  temporary test paths and some disposable session UUIDs in historical records.
  These are not credentials. Upstream author attribution includes a public email.

The exact tree and complete history are inspectable without any service:

```sh
git ls-tree -r --name-only HEAD
git log --reverse --format='%H %s' main
git log --format='%H %aN <%aE>' main
git remote -v
```

Only `main` is intended for the push. There are no tags or other branch refs.
The final review receipt records the exact tip/tree and signature results after
the documentation commit; future changes require another scan before publishing.

## Privacy and provenance findings

The scanner reads **all local Git objects**, including deleted historical blobs
and separately identified unreachable objects. No credential signatures, private
keys, notification topics, private network hostnames, sensitive state paths or
binary exports were found. Manual review additionally checked imports, ignored
files, old pager code and documentation. The private Doom email and the five
current production conversation UUID pins were compared without printing them;
none appears in tracked history. This is a heuristic plus source review, not a
mathematical guarantee that no private fact exists.

Excluded: authentication/Keychain/SSH or GPG key material, rclone config, Collie
credentials/pairing/push/Serve state, global Codex trust/auth/UI/project state,
conversation contents/pins, personal Org/iCloud/Dropbox documents, browser data,
backups, deployment journals/releases, environment captures and caches. Ignored
Python bytecode is local generated state and is not pushed.

Original code is MIT. Doom template portions and the exact fzf snapshot retain
MIT notices; simpleclip retains its complete BSD-2-Clause notice. The two
Fish-default-prompt-derived files remain GPL-2.0-only with their full license
and attribution. [THIRD_PARTY.md](../THIRD_PARTY.md) accounts for these exceptions.
No known credential or license blocker was identified. The original legacy Org
acknowledgement is retained; it is not presented as verified upstream authorship.

## Reproduction and scope

The full suite passed 207 tests; an independent clean local clone passed 50
bootstrap/recovery/startup checks. Source/manifest/preflight and license snapshot
checks passed. The source consolidation is deployed through the same immutable
release mechanism; STATUS records exact backups and unchanged production sessions.

Apple Silicon paths, macOS 27 compiler settings, matching Doom/Codex interfaces,
external tmux plugins/packages and the guarded installed-Doom test fingerprint
are machine-specific limits, documented in INSTALL. Cloning does not install
packages, enable services, grant hook trust or transmit private data. Linux-only
legacy helpers are preserved, not advertised as tested macOS programs.

## Exact publication operations — not executed

After approving the exact final HEAD and the intentional metadata above:

```sh
cd "$HOME/dev/dotfiles"
# Require the reviewed clean state and rerun the history scan.
git status --short
python3.12 scripts/publication_audit.py
# Create an EMPTY public repository; do not initialize another README/history.
gh repo create abuczuba/dotfiles --public --description "My macOS dotfiles: Doom Emacs, Fish, Ghostty, tmux, AeroSpace and Codex"
git remote add origin git@github.com:abuczuba/dotfiles.git
git push --dry-run origin main
git push -u origin main
# Verify the public target, branch and exact remote commit.
gh repo view abuczuba/dotfiles --json nameWithOwner,visibility,defaultBranchRef
git ls-remote origin refs/heads/main
```

No `--mirror`, `--all`, force push, GitHub secrets, release artifacts or private
runtime files are included. SSH push authentication has not been exercised
against a nonexistent repository; use the already-configured credentials and
stop for review if new authentication/security changes are needed. Local SSH
signature verification is separate from GitHub's displayed Verified badge.
