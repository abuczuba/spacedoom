# Publication review: abuczuba/spacedoom

The canonical local source remains `~/dev/dotfiles`. The existing public
`abuczuba/spacedoom` repository is the publication target. Its four original
commits, ending at `2751a0855b9835ffacce15f64254bfa510eca606`, are connected to
our 30 signed commits ending at `c845231` by a signed merge. Neither history is
rewritten. The merge deliberately retains the modern tree after comparing every
old Doom source, snippet and template; no useful customization is missing.
Original `master` stays intact and `main` becomes the default branch.

The accidentally created empty `abuczuba/dotfiles` repository is outside this
publication and remains untouched. No workstation deployment accompanies this
Git integration.

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

Only integrated `main` is intended for the push. Original `master` remains unchanged.
The final review receipt records the exact tip/tree and signature results after
the documentation commit; future changes require another scan before publishing.

## Privacy and provenance findings

The scanner reads **all local Git objects**, including deleted historical blobs
and separately identified unreachable objects. No credential signatures, private
keys, notification topics, private network hostnames, sensitive state paths or
binary exports were found. Manual review additionally checked imports, ignored
files, old pager code and documentation. The private Doom email and the five
current production conversation UUID pins were compared without printing them;
none appears in the modern 30-commit history. Original spacedoom history retains
its already-public legacy personal email identities; those are intentional
public metadata, not credentials. This is a heuristic plus source review, not a
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

## Authorized publication operations

After the combined-history scan, signature checks and clean-checkout tests:

```sh
cd "$HOME/dev/dotfiles"
git push --dry-run origin main:refs/heads/main
git push -u origin main:refs/heads/main
gh repo edit abuczuba/spacedoom --default-branch main
gh repo view abuczuba/spacedoom --json nameWithOwner,visibility,defaultBranchRef
git ls-remote origin refs/heads/main refs/heads/master
```

Recheck original master immediately before pushing. No force push, branch
removal, tags, `--all`, `--mirror`, runtime files or deployment artifacts are
included. Existing authenticated GitHub CLI credentials are used without creating
tokens. Local SSH signature verification and GitHub's Verified badge are separate.
