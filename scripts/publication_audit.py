#!/usr/bin/env python3
"""Read-only scan of every local Git object; report locations, never matched values.

Heuristics support a human publication review. They do not certify absence of
secrets. Reachable objects are the publication surface; unreachable objects are
reported separately and are not sent by the documented main-branch push.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


PATTERNS = {
    "private-key": rb"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----",
    "github-token": rb"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{30,})",
    "api-token": rb"sk-[A-Za-z0-9_-]{25,}",
    "slack-token": rb"xox[baprs]-[A-Za-z0-9-]{18,}",
    "aws-access-key": rb"(?:AKIA|ASIA)[0-9A-Z]{16}",
    "notification-topic": rb"https?://ntfy\.sh/[A-Za-z0-9_-]{24,}",
    "private-network-host": rb"[A-Za-z0-9.-]+\.tail[a-z0-9]+\.ts\.net",
    "url-credential": rb"https?://[^/\s:@]+:[^/\s@]+@[^/\s]+",
}
EMAIL = re.compile(rb"[A-Za-z0-9_.+%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def findings(data):
    rows = []
    for kind, pattern in PATTERNS.items():
        for match in re.finditer(pattern, data):
            rows.append(dict(kind=kind, line=data[:match.start()].count(b"\n") + 1,
                             value_sha256=hashlib.sha256(match.group()).hexdigest()))
    return rows


def sensitive_path(path):
    p = PurePosixPath(path.lower())
    return (bool(set(p.parts) & {".ssh", ".aws", ".gnupg", "credentials", "secrets", "sessions"})
            or p.name in {"auth.json", "pins.json", "fish_variables", ".env", "rclone.conf"}
            or p.suffix in {".sqlite", ".db", ".pem", ".p12", ".pfx", ".key"})


def audit(repo):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=repo)
    reachable = {}
    for line in git("rev-list", "--objects", "--all").decode().splitlines():
        oid, _, path = line.partition(" ")
        reachable[oid] = path
    inventory = git("cat-file", "--batch-all-objects", "--batch-check=%(objectname) %(objecttype) %(objectsize)")
    objects, rows, domains = Counter(), [], Counter()
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for line in inventory.decode().splitlines():
            oid, kind, length = line.split()
            objects[kind] += 1
            if kind not in {"blob", "commit", "tag"}:
                continue
            process.stdin.write((oid + "\n").encode())
            process.stdin.flush()
            header = process.stdout.readline().decode().split()
            assert header == [oid, kind, length], "Git object stream changed"
            data = process.stdout.read(int(length))
            assert len(data) == int(length) and process.stdout.read(1) == b"\n"
            path = reachable.get(oid, "")
            found = findings(data)
            if path and sensitive_path(path):
                found.append(dict(kind="sensitive-path", line=0))
            if kind == "blob" and b"\0" in data:
                found.append(dict(kind="binary-requires-review", line=0))
            for row in found:
                rows.append(row | dict(object=oid, path=path or kind,
                                      reachable=oid in reachable))
            for address in EMAIL.findall(data):
                domains[address.rsplit(b"@", 1)[1].decode()] += 1
    finally:
        process.stdin.close()
        process.wait(timeout=5)
        process.stdout.close()
        process.stderr.close()
    assert process.returncode == 0
    return dict(head=git("rev-parse", "HEAD").decode().strip(), objects=dict(objects),
                commits=int(git("rev-list", "--count", "--all")),
                refs=git("for-each-ref", "--format=%(refname)").decode().splitlines(),
                findings=rows, email_domains=dict(sorted(domains.items())),
                limitation="Heuristic scan plus manual review; not a secret-scanning guarantee.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = audit(args.repo)
    print(json.dumps(result, indent=2))
    return 1 if any(row["reachable"] for row in result["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
