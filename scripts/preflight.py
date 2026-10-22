#!/usr/bin/env python3
"""Conservative, read-only checks of Git's staged snapshot, not the worktree.

Not a secret scanner guarantee. Prints path+kind of finding, never secret text.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import PurePosixPath


def git(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


BAD_COMPONENTS = {
    ".ssh", ".gnupg", ".aws", ".config-backups", "private", "secrets",
    "credentials", "browser-profile", "bravesoftware", "icloud", "org",
    "backups", "sessions", "cookies", "resurrect",
}
BAD_NAMES = {"auth.json", ".env", "id_rsa", "id_ed25519", "credentials.json"}
BAD_SUFFIXES = {".pem", ".p12", ".pfx", ".key", ".kdbx", ".sqlite", ".db", ".zip"}
FINDINGS = (
    ("private-key block", re.compile(rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("possible GitHub token", re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}")),
    ("possible API token", re.compile(rb"sk-[A-Za-z0-9_-]{25,}")),
    ("possible Slack token", re.compile(rb"xox[baprs]-[A-Za-z0-9-]{18,}")),
)


def main() -> int:
    try:
        git("rev-parse", "--show-toplevel")
        staged = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split(b"\0") if p]
    except RuntimeError as exc:
        print(f"Preflight failed: {exc}", file=sys.stderr)
        return 2

    errors = []
    for path_bytes in staged:
        path = path_bytes.decode("utf-8", "surrogateescape")
        path_lower = path.lower()
        posix_path = PurePosixPath(path_lower)
        components = set(posix_path.parts)
        leaf = posix_path.name
        if (
            components & BAD_COMPONENTS
            or leaf in BAD_NAMES
            or leaf.startswith(".env.")
            or leaf.startswith("id_rsa")
            or leaf.startswith("id_ed25519")
            or posix_path.suffix in BAD_SUFFIXES
        ):
            errors.append(f"blocked sensitive-looking path: {path}")
            continue
        try:
            index_meta = git("ls-files", "--stage", "-z", "--", path)
            mode = index_meta.split(b" ", 1)[0]
            if mode != b"100644" and mode != b"100755":
                errors.append(f"non-regular staged file (symlink/submodule/conflict): {path}")
                continue
            blob = git("show", f":{path}")
        except RuntimeError as exc:
            errors.append(f"cannot inspect staged blob: {path} ({exc})")
            continue
        if b"\0" in blob[:65536]:
            errors.append(f"binary content requires explicit review: {path}")
            continue
        for kind, pattern in FINDINGS:
            if pattern.search(blob):
                errors.append(f"{kind} detected in staged file: {path}")

    if errors:
        print("Preflight BLOCKED staged files:", file=sys.stderr)
        for issue in errors:
            print(f"  - {issue}", file=sys.stderr)
        print("Do not force-add or bypass; inspect locally without exposing secrets.", file=sys.stderr)
        return 1

    try:
        git("diff", "--cached", "--check")
    except RuntimeError:
        print("Preflight BLOCKED: Git staged whitespace check failed.", file=sys.stderr)
        print("Inspect git diff --cached --check locally; do not paste secret values.", file=sys.stderr)
        return 1
    print(f"Preflight OK: inspected {len(staged)} staged file(s); no obvious indicators found.")
    print("This is heuristic: review 'git diff --cached' before committing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
