#!/usr/bin/env python3
"""Explicit, copied releases. Nothing in this module reloads applications.

All mutation subcommands require --approve AND operation-specific user consent.
Tests pass an isolated home/state root; production defaults are never used there.
"""
from __future__ import annotations

import argparse
from collections import deque
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import uuid

from validation import ValidationError, syntax_checks


class DeployError(RuntimeError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def identifier(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,100}", value):
        raise DeployError("Invalid release/backup identifier")
    return value


def pointer_release(target: str) -> str:
    if not isinstance(target, str):
        raise DeployError("Invalid current symlink target")
    parts = PurePosixPath(target).parts
    if len(parts) != 2 or parts[0] != "releases":
        raise DeployError("current points outside the managed releases")
    return identifier(parts[1])


def relative(value: str) -> Path:
    p = PurePosixPath(value)
    if not value or p.is_absolute() or any(x in {"..", "."} for x in value.split("/")):
        raise DeployError("Manifest paths must be nonempty relative paths without traversal")
    return Path(p)


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]


def no_links(path: Path, base: Path) -> None:
    """Reject redirected files/parents inside the declared boundary."""
    try:
        parts = path.relative_to(base).parts
    except ValueError as exc:
        raise DeployError("Path escapes its declared boundary") from exc
    current = base
    if current.is_symlink():
        raise DeployError(f"Symlink boundary is not allowed: {base}")
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise DeployError(f"Unexpected symlink: {current}")


def sync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic_json(path: Path, value: dict, mode: int = 0o600) -> None:
    temporary = path.with_name("." + path.name + "." + uuid.uuid4().hex)
    try:
        with temporary.open("x") as handle:
            os.chmod(temporary, mode)
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        sync_dir(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_link(path: Path, target: str) -> None:
    temporary = path.with_name("." + path.name + "." + uuid.uuid4().hex)
    try:
        temporary.symlink_to(target)
        os.replace(temporary, path)
        sync_dir(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def manifest_check(value: dict) -> dict:
    if value.get("schema") != 1 or not value.get("files"):
        raise DeployError("Unsupported or empty manifest")
    for field in ("source", "path", "target"):
        names = [str(relative(item[field])) for item in value["files"]]
        if len(names) != len(set(names)):
            raise DeployError(f"Duplicate manifest {field}")
        if any(Path(a) in Path(b).parents for a in names for b in names if a != b):
            raise DeployError(f"Overlapping manifest {field}")
    paths = {item["path"] for item in value["files"]}
    if any(relative(path).parts[0] == "release.json" for path in paths):
        raise DeployError("release.json is reserved for the release receipt")
    for item in value["files"]:
        identifier(item["component"])
        if item["syntax"] not in {"tmux", "ghostty", "sh", "text"}:
            raise DeployError("Unknown syntax type")
        if any(ref not in paths for ref in item.get("references", [])):
            raise DeployError("Reference is missing from the complete release")
    for target in value.get("empty_guards", []):
        relative(target)
    return value


class Deployment:
    def __init__(self, repo: Path, home: Path, root: Path):
        self.repo = repo.resolve()
        self.home = home.resolve()
        original = root.expanduser().absolute()
        if original.is_symlink():
            raise DeployError("Deployment root must not be a symlink")
        # Resolve macOS /var and /tmp aliases, but reject redirection inside home.
        if original.is_relative_to(self.home):
            no_links(original, self.home)
        self.root = original.resolve()
        if self.root.is_relative_to(self.repo) or self.repo.is_relative_to(self.root):
            raise DeployError("Deployment and development trees must not overlap")
        if self.root == self.home or self.home.is_relative_to(self.root):
            raise DeployError("Deployment root must not contain the home directory")
        if not re.fullmatch(r"[A-Za-z0-9_./ -]+", str(self.root)):
            raise DeployError("Deployment path supports letters, digits, spaces, _, -, . and / only")

    def manifest(self) -> dict:
        path = self.repo / "deploy/manifest.json"
        no_links(path, self.repo)
        return manifest_check(json.loads(path.read_text()))

    @contextmanager
    def locked(self):
        self.root.mkdir(parents=True, mode=0o700, exist_ok=True)
        no_links(self.root, self.root)
        if self.root.stat().st_mode & 0o022:
            raise DeployError("Deployment root must not be writable by group or others")
        lock = self.root / ".lock"
        no_links(lock, self.root)
        with lock.open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            for name in ("releases", "history", "backups"):
                path = self.root / name
                no_links(path, self.root)
                path.mkdir(mode=0o700, exist_ok=True)
            yield

    def release_dir(self, release: str) -> Path:
        path = self.root / "releases" / identifier(release)
        no_links(path, self.root)
        if not path.is_dir():
            raise DeployError("Release directory is missing")
        return path

    def current_target(self) -> str | None:
        """Read the exact link text without requiring a healthy release to recover."""
        link = self.root / "current"
        if not link.is_symlink():
            if link.exists():
                raise DeployError("current is not a managed symlink")
            return None
        return os.readlink(link)

    def current(self) -> str | None:
        target = self.current_target()
        if target is None:
            return None
        release = pointer_release(target)
        self.release_dir(release)
        return release

    def live(self, item: dict) -> Path:
        path = self.home / relative(item["target"])
        no_links(path.parent, self.home)
        if path.is_relative_to(self.root):
            raise DeployError("Live target overlaps deployment state")
        return path

    def link_target(self, item: dict) -> str:
        return str(self.root / "current" / relative(item["path"]))

    def is_managed(self, item: dict) -> bool:
        live = self.live(item)
        return live.is_symlink() and os.readlink(live) == self.link_target(item)

    def dependencies(self, manifest: dict) -> None:
        for dep in manifest.get("dependencies", []):
            if "command" in dep:
                if not shutil.which(dep["command"]):
                    raise DeployError(f"Missing command: {dep['command']}")
            else:
                path = (self.home / relative(dep["home_path"]) if "home_path" in dep
                        else Path(dep["path"]))
                if not path.is_file() or dep.get("executable") and not os.access(path, os.X_OK):
                    raise DeployError(f"Missing required file/executable: {path}")
        for guard in manifest.get("empty_guards", []):
            path = self.home / relative(guard)
            no_links(path, self.home)
            if path.exists() and (not path.is_file() or path.stat().st_size):
                raise DeployError(f"Unmanaged override needs inspection: {path}")

    def layout_check(self, directory: Path, manifest: dict, final: Path) -> None:
        for item in manifest["files"]:
            path = directory / relative(item["path"])
            no_links(path, directory)
            data = path.read_text()
            if "@RELEASE@" in data:
                raise DeployError("Unrendered release reference")
            for ref in item.get("references", []):
                if not (directory / ref).is_file():
                    raise DeployError("Missing referenced file")
            if item["syntax"] == "tmux":
                for line in data.splitlines():
                    if line.startswith("source-file ") and not any(
                        line == f'source-file "{final / ref}"' for ref in item.get("references", [])
                    ):
                        raise DeployError("Unmanaged tmux include; declare and pin it to this release")
            if item["syntax"] == "ghostty":
                # No includes in the imported baseline. Future adoption needs an
                # explicit include-graph change, rather than reading mutable HOME.
                if re.search(r"(?m)^\s*config-file\s*=", data):
                    raise DeployError("Ghostty includes need an explicit managed include graph")

    def materialize(self, directory: Path, final: Path, manifest: dict) -> list[dict]:
        files = []
        for item in manifest["files"]:
            source = self.repo / relative(item["source"])
            no_links(source, self.repo)
            if not source.is_file() or stat.S_IMODE(source.stat().st_mode) not in {0o644, 0o755}:
                raise DeployError(f"Expected a regular 644/755 source: {item['source']}")
            data = source.read_text().replace("@RELEASE@", str(final)).encode()
            target = directory / relative(item["path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            mode = stat.S_IMODE(source.stat().st_mode) & ~0o222
            target.chmod(mode)
            files.append({"path": item["path"], "sha256": digest(data), "mode": mode})
        return files

    def check(self) -> list[str]:
        manifest = self.manifest()
        self.dependencies(manifest)
        with tempfile.TemporaryDirectory(prefix="dotfiles-check-") as folder:
            directory = Path(folder)
            self.materialize(directory, directory, manifest)
            self.layout_check(directory, manifest, directory)
            return syntax_checks(directory, manifest)

    def stage(self) -> str:
        manifest = self.manifest()
        self.dependencies(manifest)
        release = stamp()
        final = self.root / "releases" / release
        with tempfile.TemporaryDirectory(prefix=".staging-", dir=self.root / "releases") as folder:
            directory = Path(folder)
            files = self.materialize(directory, final, manifest)
            self.layout_check(directory, manifest, final)
            checks = syntax_checks(directory, manifest)
            record = {"schema": 1, "id": release, "manifest": manifest, "files": files,
                      "checks": checks, "source_tree": str(self.repo)}
            atomic_json(directory / "release.json", record, 0o444)
            for path in sorted(directory.rglob("*"), reverse=True):
                if path.is_dir():
                    sync_dir(path)
            sync_dir(directory)
            os.rename(directory, final)
            sync_dir(final.parent)
        return release

    def receipt(self, release: str, *, parse: bool = True) -> dict:
        directory = self.release_dir(release)
        record_file = directory / "release.json"
        no_links(record_file, directory)
        record = json.loads(record_file.read_text())
        if record.get("schema") != 1 or record.get("id") != release:
            raise DeployError("Invalid release receipt")
        manifest = manifest_check(record["manifest"])
        expected = {item["path"] for item in manifest["files"]}
        if {item["path"] for item in record["files"]} != expected:
            raise DeployError("Receipt does not describe the complete release")
        found = set()
        for path in directory.rglob("*"):
            no_links(path, directory)
            if not path.is_dir():
                if not path.is_file():
                    raise DeployError("Release contains a nonregular file")
                found.add(str(path.relative_to(directory)))
        if found != expected | {"release.json"}:
            raise DeployError("Release has missing or unrecorded files")
        for item in record["files"]:
            path = directory / relative(item["path"])
            if digest(path.read_bytes()) != item["sha256"] or stat.S_IMODE(path.stat().st_mode) != item["mode"]:
                raise DeployError(f"Release integrity check failed: {item['path']}")
        self.layout_check(directory, manifest, directory)
        self.dependencies(manifest)
        if parse:
            syntax_checks(directory, manifest)
        return record

    def pending(self) -> None:
        directory = self.root / "backups"
        no_links(directory, self.root)
        for path in directory.glob("*/backup.json"):
            no_links(path, self.root)
            if json.loads(path.read_text())["status"] in {"prepared", "restoring"}:
                raise DeployError(f"Incomplete migration/restore; recover backup {path.parent.name} first")

    def adopted(self) -> set[str]:
        targets = set()
        directory = self.root / "backups"
        no_links(directory, self.root)
        for path in directory.glob("*/backup.json"):
            no_links(path, self.root)
            journal = json.loads(path.read_text())
            if journal["status"] == "migrated":
                targets.update(item["target"] for item in journal["entries"])
        return targets

    def plan(self, release: str | None = None) -> dict:
        current = self.current()
        manifest = self.receipt(release, parse=False)["manifest"] if release else self.manifest()
        targets = []
        for item in manifest["files"]:
            path = self.live(item)
            kind = "managed" if self.is_managed(item) else "symlink (unmanaged)" if path.is_symlink() else "regular file" if path.is_file() else "missing" if not path.exists() else "unsupported"
            targets.append({"component": item["component"], "live": str(path), "state": kind,
                            "link": self.link_target(item)})
        return {"current": current, "candidate": release, "targets": targets,
                "warning": "The current pointer affects ALL already-managed targets; no application reload occurs."}

    def migrate(self, release: str, component: str) -> str:
        self.pending()
        record = self.receipt(release)
        current_before = self.current_target()
        current = pointer_release(current_before) if current_before is not None else None
        if current not in {None, release}:
            raise DeployError("Migration cannot switch an existing current pointer; activate separately")
        current_after = current_before if current is not None else "releases/" + release
        items = [item for item in record["manifest"]["files"] if item["component"] == component]
        if not items:
            raise DeployError("Unknown component")
        entries = []
        for item in items:
            path = self.live(item)
            if self.is_managed(item):
                continue
            if path.is_symlink() or path.exists() and not path.is_file():
                raise DeployError(f"Refusing to replace an unmanaged link or nonregular target: {path}")
            entries.append({**item, "existed": path.exists(),
                            "sha256": digest(path.read_bytes()) if path.exists() else None,
                            "mode": stat.S_IMODE(path.stat().st_mode) if path.exists() else None})
        if not entries:
            raise DeployError("Component is already migrated")
        backup = stamp()
        directory = self.root / "backups" / backup
        directory.mkdir(mode=0o700)
        journal = {"schema": 2, "release": release, "status": "prepared", "entries": entries,
                   "current_before": current_before, "current_after": current_after,
                   "targets": [item["target"] for item in record["manifest"]["files"]]}
        # All content/mode backups precede the first live replacement.
        for item in entries:
            if item["existed"]:
                original = self.live(item)
                saved = directory / "files" / item["target"]
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(original, saved)
                if digest(saved.read_bytes()) != item["sha256"] or stat.S_IMODE(saved.stat().st_mode) != item["mode"]:
                    raise DeployError("Backup verification failed; live paths were not changed")
                with saved.open("rb") as handle:
                    os.fsync(handle.fileno())
        for path in sorted(directory.rglob("*"), reverse=True):
            if path.is_dir():
                sync_dir(path)
        atomic_json(directory / "backup.json", journal)
        if self.current_target() != current_before:
            raise DeployError(f"Current pointer changed after backup; recover backup {backup}")
        if current is None:
            atomic_link(self.root / "current", current_after)
        for item in entries:
            if self.current_target() != current_after:
                raise DeployError(f"Current pointer changed during migration; recover backup {backup}")
            path = self.live(item)
            if path.is_symlink() or (path.exists() != item["existed"]) or (
                path.exists() and (digest(path.read_bytes()) != item["sha256"] or stat.S_IMODE(path.stat().st_mode) != item["mode"])
            ):
                raise DeployError(f"Live target changed after backup; recover backup {backup}")
            path.parent.mkdir(parents=True, exist_ok=True)
            atomic_link(path, self.link_target(item))
        journal["status"] = "migrated"
        atomic_json(directory / "backup.json", journal)
        return backup

    def activate(self, release: str, expected: str, *, operation: str = "activate") -> None:
        self.pending()
        current = self.current()
        if current != expected:
            raise DeployError("Current release changed or is absent; review a fresh plan")
        if release == current:
            raise DeployError("Release is already current")
        old = self.receipt(current)
        candidate = self.receipt(release)
        old_items = old["manifest"]["files"]
        new_map = {item["target"]: item["path"] for item in candidate["manifest"]["files"]}
        adopted = self.adopted()
        managed = []
        for item in old_items:
            path = self.live(item)
            if self.is_managed(item):
                if new_map.get(item["target"]) != item["path"]:
                    raise DeployError("Candidate removes or redirects a managed path; migration review required")
                managed.append(item)
            elif item["target"] in adopted or path.is_symlink() and os.readlink(path).startswith(str(self.root)):
                raise DeployError("Managed symlink drift needs inspection")
        if not managed:
            raise DeployError("No migrated targets; perform an approved initial migration first")
        event = {"from": current, "to": release, "operation": operation, "status": "prepared",
                 "targets": [item["target"] for item in managed]}
        event_path = self.root / "history" / (stamp() + ".json")
        atomic_json(event_path, event)
        atomic_link(self.root / "current", "releases/" + release)
        event["status"] = "applied"
        atomic_json(event_path, event)

    def rollback(self, expected: str) -> str:
        if self.current() != expected:
            raise DeployError("Current release changed; review a fresh rollback plan")
        directory = self.root / "history"
        no_links(directory, self.root)
        for path in sorted(directory.glob("*.json"), reverse=True):
            no_links(path, self.root)
            event = json.loads(path.read_text())
            if event["to"] == expected:
                previous = identifier(event["from"])
                self.activate(previous, expected, operation="rollback")
                return previous
        raise DeployError("No previous activation; use the initial migration backup instead")

    def depends_on_current(self, path: Path) -> bool:
        """Follow only the inspected path's symlink chain, never scan the home tree."""
        pointer = self.root / "current"
        pending = deque(path.parts[1:])
        resolved = Path(path.anchor)
        links = 0
        while pending:
            part = pending.popleft()
            if part == "..":
                resolved = resolved.parent
                continue
            resolved = resolved / part
            # Check before following the pointer or collapsing any later '..'.
            if resolved == pointer:
                return True
            if resolved.is_symlink():
                links += 1
                if links > 40:
                    raise DeployError("Cannot establish current dependencies: symlink loop or excessive depth")
                target = Path(os.readlink(resolved))
                resolved = Path(target.anchor) if target.is_absolute() else resolved.parent
                pending.extendleft(reversed(target.parts[1:] if target.is_absolute() else target.parts))
        return False

    def current_dependents(self, journal: dict) -> list[Path]:
        # Include every declared component, skipped managed targets, and targets
        # from later backups. Recovery must not orphan another component's links.
        targets = set(journal["targets"])
        for path in (self.root / "backups").glob("*/backup.json"):
            no_links(path, self.root)
            other = json.loads(path.read_text())
            targets.update(other.get("targets", []))
            targets.update(item["target"] for item in other["entries"])
        return [path for target in sorted(targets)
                if self.depends_on_current(path := self.live({"target": target}))]

    @staticmethod
    def original_matches(path: Path, item: dict) -> bool:
        if not item["existed"]:
            return not path.exists() and not path.is_symlink()
        return (not path.is_symlink() and path.is_file()
                and digest(path.read_bytes()) == item["sha256"]
                and stat.S_IMODE(path.stat().st_mode) == item["mode"])

    def restore(self, backup: str) -> None:
        directory = self.root / "backups" / identifier(backup)
        no_links(directory, self.root)
        journal_file = directory / "backup.json"
        no_links(journal_file, directory)
        journal = json.loads(journal_file.read_text())
        if journal.get("schema") == 1:
            raise DeployError("Legacy backup has no original pointer state; reviewed manual recovery required")
        if journal.get("schema") != 2 or journal.get("status") not in {"prepared", "migrated", "restoring", "restored"}:
            raise DeployError("Invalid backup journal")
        before, after = journal["current_before"], journal["current_after"]
        release = identifier(journal["release"])
        if (pointer_release(after) != release
                or before is not None and pointer_release(before) != release):
            raise DeployError("Invalid recorded pointer state")
        observed = self.current_target()
        if observed != after and observed != before:
            raise DeployError("Current pointer changed; refusing restore")
        # Inspect every target and backup before restoring any target. Newer user
        # changes are never overwritten. A partially completed restore is resumable.
        work = []
        for item in journal["entries"]:
            path = self.live(item)
            saved = directory / "files" / relative(item["target"])
            if item["existed"]:
                no_links(saved, directory)
                if not saved.is_file() or digest(saved.read_bytes()) != item["sha256"] or stat.S_IMODE(saved.stat().st_mode) != item["mode"]:
                    raise DeployError("Backup content or permissions changed")
            if self.original_matches(path, item):
                continue
            if not self.is_managed(item):
                raise DeployError(f"Live target drift; refusing restore: {path}")
            work.append((item, path, saved))
        # The old pointer is acceptable only before any migration write, or after
        # all file restores and the pointer restore completed but finalization
        # failed. A missing/replaced pointer with outstanding work is drift.
        if observed != after and (work or journal["status"] == "migrated"):
            raise DeployError("Current pointer changed; refusing restore")
        if journal["status"] == "restored":
            if work or observed != before:
                raise DeployError("Restored state changed; refusing repeated restore")
            return
        journal["status"] = "restoring"
        atomic_json(directory / "backup.json", journal)
        for item, path, saved in work:
            if self.current_target() != observed:
                raise DeployError("Current pointer changed during restore; recovery remains pending")
            if not self.is_managed(item):
                raise DeployError("Live target changed during restore; recovery remains pending")
            if item["existed"]:
                temporary = path.with_name("." + path.name + "." + uuid.uuid4().hex)
                try:
                    shutil.copy2(saved, temporary)
                    with temporary.open("rb") as handle:
                        os.fsync(handle.fileno())
                    os.replace(temporary, path)
                    sync_dir(path.parent)
                finally:
                    temporary.unlink(missing_ok=True)
            else:
                path.unlink()
                sync_dir(path.parent)
        # Files always precede the pointer. Leave the journal pending after any
        # error, including a failed pointer fsync or final journal publication.
        for item in journal["entries"]:
            if not self.original_matches(self.live(item), item):
                raise DeployError("File restoration incomplete; recovery remains pending")
        if self.current_target() != observed:
            raise DeployError("Current pointer changed during restore; recovery remains pending")
        if before is None:
            if self.current_dependents(journal):
                raise DeployError("Live configuration still depends on current; restore dependent backups first")
            if self.current_target() != observed:
                raise DeployError("Current pointer changed during restore; recovery remains pending")
            if observed is not None:
                (self.root / "current").unlink()
        elif observed != before:
            atomic_link(self.root / "current", before)
        if self.current_target() != before:
            raise DeployError("Pointer restoration incomplete; recovery remains pending")
        sync_dir(self.root)
        journal["status"] = "restored"
        atomic_json(directory / "backup.json", journal)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--state-root", type=Path)
    subs = parser.add_subparsers(dest="action", required=True)
    subs.add_parser("check", help="Validate development copies in a temporary directory")
    plan = subs.add_parser("plan", help="Read-only target/current inventory")
    plan.add_argument("--release")
    verify = subs.add_parser("verify", help="Validate a copied release without activating")
    verify.add_argument("--release", required=True)
    for name in ("stage", "migrate", "activate", "rollback", "restore"):
        sub = subs.add_parser(name)
        sub.add_argument("--approve", action="store_true", help="Accident guard; user consent is still required")
        if name in {"migrate", "activate"}:
            sub.add_argument("--release", required=True)
        if name == "migrate":
            sub.add_argument("--component", required=True)
        if name in {"activate", "rollback"}:
            sub.add_argument("--expect-current", required=True)
        if name == "restore":
            sub.add_argument("--backup", required=True)
    args = parser.parse_args()
    try:
        deployment = Deployment(args.repo, args.home, args.state_root or args.home / ".local/share/dotfiles-active")
        if args.action == "plan":
            print(json.dumps(deployment.plan(args.release), indent=2))
        elif args.action == "check":
            print("\n".join(deployment.check()))
        elif args.action == "verify":
            deployment.receipt(args.release)
            print("Release integrity, dependencies, references and parsers passed")
        else:
            if not args.approve:
                raise DeployError("Mutation requires --approve and explicit consent for this operation")
            with deployment.locked():
                if args.action == "stage":
                    print("Staged release: " + deployment.stage())
                elif args.action == "migrate":
                    print("Migration backup: " + deployment.migrate(args.release, args.component))
                elif args.action == "activate":
                    deployment.activate(args.release, args.expect_current)
                    print("Activated: " + args.release)
                elif args.action == "rollback":
                    print("Rolled back to: " + deployment.rollback(args.expect_current))
                elif args.action == "restore":
                    deployment.restore(args.backup)
                    print("Original files and previous deployment pointer state restored")
            print("No application was reloaded or restarted")
        return 0
    except (DeployError, ValidationError, OSError, ValueError, KeyError) as exc:
        print(f"dotfiles: {exc}", file=sys.stderr)
        print("No automatic rollback/reload. Inspect plan and any backup journal before recovery.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
