from __future__ import annotations

import json
import io
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
import fcntl
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

import deploy
from deploy import Deployment, DeployError, manifest_check


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="dotfiles-unit-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.repo = self.base / "checkout"
        self.home = self.base / "home with spaces"
        self.root = self.base / "stable releases"
        (self.repo / "deploy").mkdir(parents=True)
        (self.repo / "configs").mkdir()
        self.home.mkdir()
        self.manifest = {"schema": 1, "files": [
            {"source": "configs/main", "path": "tmux/main", "target": ".tmux.conf",
             "component": "tmux", "syntax": "text", "references": ["tmux/helper"]},
            {"source": "configs/helper", "path": "tmux/helper", "target": ".config/tmux/helper",
             "component": "tmux", "syntax": "text", "references": []},
            {"source": "configs/ghostty", "path": "ghostty/config", "target": ".config/ghostty/config",
             "component": "ghostty", "syntax": "text", "references": []},
        ], "dependencies": [], "empty_guards": []}
        self.write_manifest()
        for name in ("main", "helper", "ghostty"):
            source = self.repo / "configs" / name
            source.write_text(f"first {name} @RELEASE@\n")
            source.chmod(0o644)
        self.original = self.home / ".tmux.conf"
        self.original.write_bytes(b"original config\n")
        self.original.chmod(0o640)
        self.deployment = Deployment(self.repo, self.home, self.root)

    def write_manifest(self):
        (self.repo / "deploy/manifest.json").write_text(json.dumps(self.manifest))

    def mutate(self, method, *args):
        with self.deployment.locked():
            return getattr(self.deployment, method)(*args)

    def first(self):
        release = self.mutate("stage")
        backup = self.mutate("migrate", release, "tmux")
        return release, backup

    def second(self):
        (self.repo / "configs/main").write_text("second @RELEASE@\n")
        return self.mutate("stage")

    def journal(self, backup):
        return json.loads((self.root / "backups" / backup / "backup.json").read_text())

    def assert_originals(self):
        self.assertFalse(self.original.is_symlink())
        self.assertEqual(self.original.read_bytes(), b"original config\n")
        self.assertEqual(stat.S_IMODE(self.original.stat().st_mode), 0o640)
        self.assertFalse(os.path.lexists(self.home / ".config/tmux/helper"))

    def restore_cli(self, backup):
        return subprocess.run([sys.executable, "-B", str(Path(deploy.__file__)),
                               "--repo", str(self.repo), "--home", str(self.home),
                               "--state-root", str(self.root), "restore", "--backup", backup,
                               "--approve"], text=True, capture_output=True)

    def test_stage_is_independent_and_has_pinned_references(self):
        release = self.mutate("stage")
        path = self.deployment.release_dir(release) / "tmux/main"
        first = path.read_bytes()
        self.assertIn(str(self.deployment.release_dir(release)).encode(), first)
        self.assertNotEqual(path.stat().st_ino, (self.repo / "configs/main").stat().st_ino)
        (self.repo / "configs/main").write_text("dirty development edit")
        self.assertEqual(path.read_bytes(), first)
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o444)
        self.assertEqual(self.original.read_bytes(), b"original config\n")
        self.assertIsNone(self.deployment.current())
        self.deployment.receipt(release)

    def test_plan_and_check_never_initialize_deployment(self):
        plan = self.deployment.plan()
        self.assertIsNone(plan["current"])
        self.deployment.check()
        self.assertFalse(self.root.exists())
        self.assertFalse(self.original.is_symlink())

    def test_cli_requires_approval_before_any_state_creation(self):
        result = subprocess.run([sys.executable, str(Path(deploy.__file__)), "--repo", str(self.repo),
                                 "--home", str(self.home), "--state-root", str(self.root), "stage"],
                                text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires --approve", result.stderr)
        self.assertFalse(self.root.exists())

    def test_backup_precedes_every_live_replacement_and_preserves_modes(self):
        release = self.mutate("stage")
        original_link = deploy.atomic_link

        def inspect_then_link(path, target):
            journals = list((self.root / "backups").glob("*/backup.json"))
            self.assertEqual(len(journals), 1)
            saved = journals[0].parent / "files/.tmux.conf"
            self.assertEqual(saved.read_bytes(), b"original config\n")
            self.assertEqual(stat.S_IMODE(saved.stat().st_mode), 0o640)
            return original_link(path, target)

        with patch.object(deploy, "atomic_link", side_effect=inspect_then_link):
            backup = self.mutate("migrate", release, "tmux")
        self.assertEqual(self.deployment.current(), release)
        self.assertTrue(self.original.is_symlink())
        self.assertTrue((self.home / ".config/tmux/helper").is_symlink())
        self.assertFalse((self.home / ".config/ghostty/config").exists())
        self.assertEqual(json.loads((self.root / "backups" / backup / "backup.json").read_text())["status"], "migrated")

    def test_activation_rollback_and_initial_restore(self):
        first, backup = self.first()
        old_data = self.original.read_bytes()
        second = self.second()
        stable_link = os.readlink(self.original)
        self.mutate("activate", second, first)
        self.assertEqual(os.readlink(self.original), stable_link)
        self.assertTrue(self.original.read_text().startswith("second"))
        self.assertEqual(self.mutate("rollback", second), first)
        self.assertEqual(self.original.read_bytes(), old_data)
        self.mutate("restore", backup)
        self.assertFalse(self.original.is_symlink())
        self.assertEqual(self.original.read_bytes(), b"original config\n")
        self.assertEqual(stat.S_IMODE(self.original.stat().st_mode), 0o640)
        self.assertFalse((self.home / ".config/tmux/helper").exists())
        self.assertFalse(os.path.lexists(self.root / "current"))

    def test_component_migration_does_not_activate_another_release(self):
        first, _ = self.first()
        second = self.second()
        with self.assertRaisesRegex(DeployError, "cannot switch"):
            self.mutate("migrate", second, "ghostty")
        self.assertEqual(self.deployment.current(), first)
        self.mutate("migrate", first, "ghostty")
        self.assertTrue((self.home / ".config/ghostty/config").is_symlink())

    def test_stale_activation_is_rejected_without_pointer_change(self):
        first, _ = self.first()
        second = self.second()
        with self.assertRaisesRegex(DeployError, "Current release changed"):
            self.mutate("activate", second, "stale")
        self.assertEqual(self.deployment.current(), first)
        self.assertEqual(list((self.root / "history").iterdir()), [])

    def test_failed_pointer_change_keeps_old_release_and_rollback_history(self):
        first, _ = self.first()
        second = self.second()
        self.mutate("activate", second, first)
        third = self.mutate("stage")
        with patch.object(deploy, "atomic_link", side_effect=OSError("injected pointer failure")):
            with self.assertRaises(OSError):
                self.mutate("activate", third, second)
        self.assertEqual(self.deployment.current(), second)
        self.assertEqual(self.mutate("rollback", second), first)

    def test_interrupted_event_finalize_still_allows_rollback(self):
        first, _ = self.first()
        second = self.second()
        original_json = deploy.atomic_json

        def fail_after_switch(path, data, *args):
            if path.parent.name == "history" and data.get("status") == "applied":
                raise OSError("injected interruption after current rename")
            return original_json(path, data, *args)

        with patch.object(deploy, "atomic_json", side_effect=fail_after_switch):
            with self.assertRaises(OSError):
                self.mutate("activate", second, first)
        self.assertEqual(self.deployment.current(), second)
        self.assertEqual(self.mutate("rollback", second), first)

    def test_corrupt_release_blocks_activation(self):
        first, _ = self.first()
        second = self.second()
        path = self.deployment.release_dir(second) / "tmux/main"
        path.chmod(0o644)
        path.write_text("corrupt")
        with self.assertRaisesRegex(DeployError, "integrity"):
            self.mutate("activate", second, first)
        self.assertEqual(self.deployment.current(), first)

    def test_managed_target_replaced_with_regular_file_is_drift(self):
        first, _ = self.first()
        second = self.second()
        self.original.unlink()
        self.original.write_text("manual edit")
        with self.assertRaisesRegex(DeployError, "drift"):
            self.mutate("activate", second, first)
        self.assertEqual(self.original.read_text(), "manual edit")

    def test_interrupted_migration_blocks_activation_then_restores(self):
        first = self.mutate("stage")
        original_link = deploy.atomic_link

        def fail_second_target(path, target):
            if path.name == "helper":
                raise OSError("injected partial migration")
            return original_link(path, target)

        with patch.object(deploy, "atomic_link", side_effect=fail_second_target):
            with self.assertRaises(OSError):
                self.mutate("migrate", first, "tmux")
        self.assertTrue(self.original.is_symlink())
        backup = next((self.root / "backups").iterdir()).name
        second = self.second()
        with self.assertRaisesRegex(DeployError, "Incomplete"):
            self.mutate("activate", second, first)
        self.mutate("restore", backup)
        self.assertEqual(self.original.read_bytes(), b"original config\n")
        self.assertFalse(self.original.is_symlink())
        self.assertFalse((self.home / ".config/tmux/helper").exists())
        self.assertFalse(os.path.lexists(self.root / "current"))

    def test_initial_restore_recovers_absent_pointer_and_repeats_without_writes(self):
        release, backup = self.first()
        journal = self.journal(backup)
        self.assertEqual(journal["schema"], 2)
        self.assertIsNone(journal["current_before"])
        self.assertEqual(journal["current_after"], "releases/" + release)
        self.assertEqual(set(journal["targets"]), {item["target"] for item in self.manifest["files"]})
        self.mutate("restore", backup)
        self.assert_originals()
        self.assertFalse(os.path.lexists(self.root / "current"))
        saved = self.root / "backups" / backup / "files/.tmux.conf"
        self.assertEqual(saved.read_bytes(), b"original config\n")
        self.assertEqual(stat.S_IMODE(saved.stat().st_mode), 0o640)
        unrelated = self.root / "keep-this-file"
        unrelated.write_text("unrelated state")
        with patch.object(deploy, "atomic_json", side_effect=AssertionError("Repeat must not write")):
            self.mutate("restore", backup)
            self.mutate("restore", backup)
        self.assert_originals()
        self.assertEqual(unrelated.read_text(), "unrelated state")
        self.assertEqual(self.journal(backup)["status"], "restored")
        self.deployment.receipt(release)

    def test_restore_preserves_exact_older_current_with_newer_release_inactive(self):
        older = self.mutate("stage")
        newer = self.second()
        exact_target = "releases/./" + older
        deploy.atomic_link(self.root / "current", exact_target)
        with self.assertRaisesRegex(DeployError, "cannot switch"):
            self.mutate("migrate", newer, "tmux")
        backup = self.mutate("migrate", older, "tmux")
        self.assertEqual(os.readlink(self.root / "current"), exact_target)
        journal = self.journal(backup)
        self.assertEqual(journal["current_before"], exact_target)
        self.assertEqual(journal["current_after"], exact_target)
        self.mutate("restore", backup)
        self.mutate("restore", backup)
        self.assert_originals()
        self.assertEqual(os.readlink(self.root / "current"), exact_target)
        self.assertEqual(self.deployment.current(), older)
        self.deployment.receipt(newer)

    def test_migration_interrupted_before_pointer_creation_restores_cleanly(self):
        release = self.mutate("stage")
        with patch.object(deploy, "atomic_link", side_effect=OSError("injected initial pointer failure")):
            with self.assertRaises(OSError):
                self.mutate("migrate", release, "tmux")
        backup = next((self.root / "backups").iterdir()).name
        self.assertEqual(self.journal(backup)["status"], "prepared")
        self.assertIsNone(self.deployment.current())
        self.mutate("restore", backup)
        self.mutate("restore", backup)
        self.assert_originals()
        self.assertFalse(os.path.lexists(self.root / "current"))

    def test_restore_refuses_unexpected_pointer_states_before_touching_files(self):
        release, backup = self.first()
        other = self.second()
        pointer = self.root / "current"
        for target in ("releases/" + other, "releases/./" + release, "/unrelated", None, "regular", "directory"):
            with self.subTest(target=target):
                pointer.unlink()
                if target == "regular":
                    pointer.write_text("unrelated pointer data")
                elif target == "directory":
                    pointer.mkdir()
                elif target is not None:
                    pointer.symlink_to(target)
                original_link = os.readlink(self.original)
                with self.assertRaises(DeployError):
                    self.mutate("restore", backup)
                self.assertEqual(os.readlink(self.original), original_link)
                self.assertTrue((self.home / ".config/tmux/helper").is_symlink())
                self.assertEqual(self.journal(backup)["status"], "migrated")
                if target == "directory":
                    pointer.rmdir()
                elif target is not None:
                    if target == "regular":
                        self.assertEqual(pointer.read_text(), "unrelated pointer data")
                    else:
                        self.assertEqual(os.readlink(pointer), target)
                    pointer.unlink()
                pointer.symlink_to("releases/" + release)

    def test_repeated_restore_refuses_new_user_files_and_changed_pointer(self):
        release, backup = self.first()
        self.mutate("restore", backup)
        helper = self.home / ".config/tmux/helper"
        helper.write_text("new user data")
        with self.assertRaisesRegex(DeployError, "drift"):
            self.mutate("restore", backup)
        self.assertEqual(helper.read_text(), "new user data")
        helper.unlink()
        deploy.atomic_link(self.root / "current", "releases/" + release)
        with self.assertRaisesRegex(DeployError, "Restored state changed"):
            self.mutate("restore", backup)
        self.assertEqual(self.deployment.current(), release)
        self.assert_originals()

    def test_partial_file_restore_is_resumable_and_cli_reports_failure(self):
        release, backup = self.first()
        helper = self.home / ".config/tmux/helper"
        original_unlink = Path.unlink

        def fail_helper(path, *args, **kwargs):
            if path == helper:
                raise OSError("injected helper removal failure")
            return original_unlink(path, *args, **kwargs)

        args = [str(Path(deploy.__file__)), "--repo", str(self.repo), "--home", str(self.home),
                "--state-root", str(self.root), "restore", "--backup", backup, "--approve"]
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(Path, "unlink", autospec=True, side_effect=fail_helper), \
                patch.object(sys, "argv", args), redirect_stdout(stdout), redirect_stderr(stderr):
            self.assertEqual(deploy.main(), 1)
        self.assertNotIn("Original files", stdout.getvalue())
        self.assertIn("injected helper removal failure", stderr.getvalue())
        self.assertEqual(self.original.read_bytes(), b"original config\n")
        self.assertFalse(self.original.is_symlink())
        self.assertTrue(helper.is_symlink())
        self.assertEqual(self.deployment.current(), release)
        self.assertEqual(self.journal(backup)["status"], "restoring")
        with self.assertRaisesRegex(DeployError, "Incomplete"):
            self.mutate("migrate", release, "ghostty")
        for _ in range(2):
            result = self.restore_cli(backup)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("previous deployment pointer state restored", result.stdout)
        self.assert_originals()
        self.assertIsNone(self.deployment.current())

    def test_pointer_removal_failure_preserves_journal_and_can_retry(self):
        release, backup = self.first()
        original_unlink = Path.unlink

        def fail_pointer(path, *args, **kwargs):
            if path == self.root / "current":
                self.assert_originals()
                raise OSError("injected pointer removal failure")
            return original_unlink(path, *args, **kwargs)

        with patch.object(Path, "unlink", autospec=True, side_effect=fail_pointer):
            with self.assertRaisesRegex(OSError, "pointer removal"):
                self.mutate("restore", backup)
        self.assertEqual(self.journal(backup)["status"], "restoring")
        self.assertEqual(self.deployment.current(), release)
        self.mutate("restore", backup)
        self.assert_originals()
        self.assertIsNone(self.deployment.current())

    def test_interruption_after_pointer_removal_can_finalize_on_retry(self):
        _, backup = self.first()
        original_json = deploy.atomic_json

        def fail_finalize(path, data, *args):
            if path.name == "backup.json" and data["status"] == "restored":
                raise OSError("injected final journal failure")
            return original_json(path, data, *args)

        with patch.object(deploy, "atomic_json", side_effect=fail_finalize):
            with self.assertRaisesRegex(OSError, "final journal"):
                self.mutate("restore", backup)
        self.assert_originals()
        self.assertIsNone(self.deployment.current())
        self.assertEqual(self.journal(backup)["status"], "restoring")
        self.mutate("restore", backup)
        self.assertEqual(self.journal(backup)["status"], "restored")

    def test_pointer_fsync_failure_after_unlink_is_reported_and_retryable(self):
        _, backup = self.first()
        original_sync = deploy.sync_dir

        def fail_pointer_sync(path):
            if path == self.root and not os.path.lexists(path / "current"):
                raise OSError("injected pointer fsync failure")
            return original_sync(path)

        with patch.object(deploy, "sync_dir", side_effect=fail_pointer_sync):
            with self.assertRaisesRegex(OSError, "fsync"):
                self.mutate("restore", backup)
        self.assert_originals()
        self.assertIsNone(self.deployment.current())
        self.assertEqual(self.journal(backup)["status"], "restoring")
        self.mutate("restore", backup)
        self.assertEqual(self.journal(backup)["status"], "restored")

    def test_other_component_must_be_restored_before_removing_shared_pointer(self):
        release, tmux_backup = self.first()
        ghostty_backup = self.mutate("migrate", release, "ghostty")
        with self.assertRaisesRegex(DeployError, "still depends on current"):
            self.mutate("restore", tmux_backup)
        self.assert_originals()
        self.assertEqual(self.deployment.current(), release)
        self.assertTrue((self.home / ".config/ghostty/config").is_symlink())
        self.assertEqual(self.journal(tmux_backup)["status"], "restoring")
        self.mutate("restore", ghostty_backup)
        self.assertEqual(self.deployment.current(), release)
        self.mutate("restore", tmux_backup)
        self.assertIsNone(self.deployment.current())
        self.assertFalse(os.path.lexists(self.home / ".config/ghostty/config"))

    def test_skipped_managed_target_still_prevents_pointer_removal(self):
        release = self.mutate("stage")
        helper = self.home / ".config/tmux/helper"
        helper.parent.mkdir(parents=True)
        helper.symlink_to(self.root / "current/tmux/helper")
        backup = self.mutate("migrate", release, "tmux")
        self.assertEqual(len(self.journal(backup)["entries"]), 1)
        with self.assertRaisesRegex(DeployError, "still depends on current"):
            self.mutate("restore", backup)
        self.assertTrue(helper.is_symlink())
        self.assertEqual(self.deployment.current(), release)

    def test_pointer_dependency_check_follows_relative_links_and_aliases(self):
        release, backup = self.first()
        other = self.home / ".config/ghostty/config"
        other.parent.mkdir(parents=True)
        alias = self.home / "pointer-alias"
        alias.symlink_to(self.root / "current")
        for target in (os.path.relpath(self.root / "current/tmux/helper", other.parent),
                       os.path.relpath(alias / "tmux/helper", other.parent),
                       str(self.root / "current" / ".." / release / "ghostty/config")):
            with self.subTest(target=target):
                other.symlink_to(target)
                with self.assertRaisesRegex(DeployError, "still depends on current"):
                    self.mutate("restore", backup)
                self.assertEqual(self.deployment.current(), release)
                self.assertEqual(os.readlink(other), target)
                other.unlink()
        self.mutate("restore", backup)
        self.assertIsNone(self.deployment.current())

    def test_pointer_drift_during_dependency_check_is_not_overwritten(self):
        release, backup = self.first()
        other = self.second()
        original_check = self.deployment.current_dependents

        def check_then_change_pointer(journal):
            dependents = original_check(journal)
            deploy.atomic_link(self.root / "current", "releases/" + other)
            return dependents

        with patch.object(self.deployment, "current_dependents", side_effect=check_then_change_pointer):
            with self.assertRaisesRegex(DeployError, "Current pointer changed during restore"):
                self.mutate("restore", backup)
        self.assert_originals()
        self.assertEqual(self.deployment.current(), other)
        self.assertEqual(self.journal(backup)["status"], "restoring")

    def test_pointer_drift_during_restoration_preserves_pending_state(self):
        release, backup = self.first()
        other = self.second()
        original_replace = os.replace

        def replace_then_change_pointer(source, destination):
            result = original_replace(source, destination)
            if destination == self.original:
                deploy.atomic_link(self.root / "current", "releases/" + other)
            return result

        with patch.object(os, "replace", side_effect=replace_then_change_pointer):
            with self.assertRaisesRegex(DeployError, "Current pointer changed during restore"):
                self.mutate("restore", backup)
        self.assertEqual(self.deployment.current(), other)
        self.assertTrue((self.home / ".config/tmux/helper").is_symlink())
        self.assertEqual(self.journal(backup)["status"], "restoring")
        with self.assertRaisesRegex(DeployError, "Current pointer changed"):
            self.mutate("restore", backup)
        # Explicit recovery of the fixture's known pointer allows a safe retry.
        deploy.atomic_link(self.root / "current", "releases/" + release)
        self.mutate("restore", backup)
        self.assert_originals()
        self.assertIsNone(self.deployment.current())

    def test_legacy_backup_pointer_state_is_not_guessed(self):
        release, backup = self.first()
        journal = self.journal(backup)
        journal["schema"] = 1
        for name in ("current_before", "current_after", "targets"):
            del journal[name]
        deploy.atomic_json(self.root / "backups" / backup / "backup.json", journal)
        with self.assertRaisesRegex(DeployError, "Legacy backup"):
            self.mutate("restore", backup)
        self.assertTrue(self.original.is_symlink())
        self.assertEqual(self.deployment.current(), release)

    def test_restore_refuses_new_user_edits_and_tampered_backups(self):
        _, backup = self.first()
        saved = self.root / "backups" / backup / "files/.tmux.conf"
        saved.write_text("tampered")
        with self.assertRaisesRegex(DeployError, "Backup content"):
            self.mutate("restore", backup)
        self.assertTrue(self.original.is_symlink())
        saved.write_bytes(b"original config\n")
        self.original.unlink()
        self.original.write_text("new user content")
        with self.assertRaisesRegex(DeployError, "drift"):
            self.mutate("restore", backup)
        self.assertEqual(self.original.read_text(), "new user content")

    def test_dependency_and_override_checks_fail_closed(self):
        self.manifest["dependencies"] = [{"home_path": ".missing-dependency", "executable": True}]
        self.write_manifest()
        with self.assertRaisesRegex(DeployError, "Missing required"):
            self.mutate("stage")
        self.manifest["dependencies"] = []
        self.manifest["empty_guards"] = [".override"]
        self.write_manifest()
        (self.home / ".override").write_text("private override withheld")
        with self.assertRaisesRegex(DeployError, "override needs inspection"):
            self.mutate("stage")
        self.assertEqual(list((self.root / "releases").iterdir()), [])

    def test_sources_and_release_trees_cannot_be_symlinks(self):
        source = self.repo / "configs/main"
        source.unlink()
        source.symlink_to(self.original)
        with self.assertRaisesRegex(DeployError, "symlink"):
            self.mutate("stage")
        source.unlink()
        source.write_text("regular")
        release = self.mutate("stage")
        path = self.deployment.release_dir(release) / "tmux/main"
        path.unlink()
        path.symlink_to(source)
        with self.assertRaisesRegex(DeployError, "symlink"):
            self.deployment.receipt(release)

    def test_live_parent_and_unknown_symlinks_are_rejected(self):
        first = self.mutate("stage")
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        (self.home / ".config").symlink_to(elsewhere, target_is_directory=True)
        with self.assertRaisesRegex(DeployError, "symlink"):
            self.mutate("migrate", first, "tmux")
        self.assertFalse(self.original.is_symlink())
        (self.home / ".config").unlink()
        self.original.unlink()
        self.original.symlink_to(elsewhere / "unknown")
        with self.assertRaisesRegex(DeployError, "unmanaged link"):
            self.mutate("migrate", first, "tmux")

    def test_state_cannot_overlap_checkout_or_follow_home_symlinks(self):
        with self.assertRaisesRegex(DeployError, "overlap"):
            Deployment(self.repo, self.home, self.repo / "active")
        (self.home / ".local").symlink_to(self.base)
        with self.assertRaisesRegex(DeployError, "symlink"):
            Deployment(self.repo, self.home, self.home / ".local/active")

    def test_removed_managed_mapping_is_rejected(self):
        first, _ = self.first()
        self.manifest["files"] = self.manifest["files"][1:]
        self.write_manifest()
        second = self.second()
        with self.assertRaisesRegex(DeployError, "removes or redirects"):
            self.mutate("activate", second, first)

    def test_manifest_rejects_traversal_duplicates_and_overlaps(self):
        for target in ("../escape", "/absolute", "a/../escape"):
            candidate = json.loads(json.dumps(self.manifest))
            candidate["files"][0]["target"] = target
            with self.assertRaises(DeployError):
                manifest_check(candidate)
        candidate = json.loads(json.dumps(self.manifest))
        candidate["files"][1]["target"] = ".tmux.conf"
        with self.assertRaisesRegex(DeployError, "Duplicate"):
            manifest_check(candidate)
        candidate["files"][1]["target"] = ".tmux.conf/child"
        with self.assertRaisesRegex(DeployError, "Overlapping"):
            manifest_check(candidate)
        candidate = json.loads(json.dumps(self.manifest))
        candidate["files"][0]["path"] = "release.json"
        with self.assertRaisesRegex(DeployError, "reserved"):
            manifest_check(candidate)

    def test_validation_failure_does_not_publish_a_release(self):
        with patch.object(deploy, "syntax_checks", side_effect=deploy.ValidationError("injected parser error")):
            with self.assertRaises(deploy.ValidationError):
                self.mutate("stage")
        self.assertEqual(list((self.root / "releases").iterdir()), [])
        self.assertIsNone(self.deployment.current())
        self.assertEqual(self.original.read_bytes(), b"original config\n")

    def test_lock_excludes_another_deployment_writer(self):
        code = ("import fcntl,sys; f=open(sys.argv[1],'a'); "
                "fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)")
        with self.deployment.locked():
            result = subprocess.run([sys.executable, "-c", code, str(self.root / ".lock")],
                                    text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BlockingIOError", result.stderr)

    @unittest.skipUnless(sys.platform == "darwin", "The documented emergency mv -h is macOS-specific")
    def test_terminal_recovery_without_python_tmux_or_ghostty(self):
        first, _ = self.first()
        original = self.original.read_bytes()
        second = self.second()
        self.mutate("activate", second, first)
        temporary = self.root / ".current-recovery-test"
        subprocess.run(["/bin/ln", "-s", "releases/" + first, str(temporary)], check=True)
        subprocess.run(["/bin/mv", "-fh", str(temporary), str(self.root / "current")], check=True)
        self.assertEqual(self.deployment.current(), first)
        self.assertEqual(self.original.read_bytes(), original)
        self.assertFalse(temporary.exists())
