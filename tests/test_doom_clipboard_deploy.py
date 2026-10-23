"""Exact two-line Doom edit and schema-2 recovery, entirely in temporary homes."""
import hashlib
import json
from pathlib import Path
from unittest.mock import patch
import unittest

import deploy
import test_deploy as fixtures


class DoomClipboardDeployTests(unittest.TestCase):
    setUp = fixtures.DeploymentTests.setUp
    mutate = fixtures.DeploymentTests.mutate
    write_manifest = fixtures.DeploymentTests.write_manifest

    def prepare(self):
        (self.repo / "configs/clipboard").write_text("public clipboard fixture\n")
        self.manifest['files'].append(dict(source='configs/clipboard', path='doom/clipboard.el',
            target='.config/doom/clipboard.el', component='doom-clipboard', syntax='text', references=[]))
        (self.repo / 'deploy/manifest.json').write_text(json.dumps(self.manifest))
        self.release = self.mutate('stage')
        self.mutate('migrate', self.release, 'tmux')
        self.mutate('migrate', self.release, 'doom-clipboard')
        self.config = self.home / '.config/doom/config.el'
        self.before = b'; synthetic personal settings\n(require \'simpleclip)\n(simpleclip-mode 1)\n(setq unrelated t)\n'
        self.after = self.before.replace(b"(require 'simpleclip)\n(simpleclip-mode 1)", b'(load! "clipboard")')
        self.config.write_bytes(self.before)
        self.config.chmod(0o640)
        self.expected = hashlib.sha256(self.before).hexdigest()

    def test_exact_edit_backup_permissions_and_idempotent_restore(self):
        self.prepare()
        backup = self.mutate('configure_doom_clipboard', self.expected, self.release)
        self.assertEqual(self.config.read_bytes(), self.after)
        self.assertFalse(self.config.is_symlink())
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o640)
        saved = self.root / 'backups' / backup / 'files/.config/doom/config.el'
        self.assertEqual(saved.read_bytes(), self.before)
        self.assertEqual(saved.stat().st_mode & 0o777, 0o640)
        self.assertNotIn('.config/doom/config.el', self.deployment.adopted())
        with self.assertRaises(deploy.DeployError):
            self.mutate('configure_doom_clipboard', hashlib.sha256(self.after).hexdigest(), self.release)
        self.mutate('restore', backup)
        self.mutate('restore', backup)
        self.assertEqual(self.config.read_bytes(), self.before)
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o640)
        self.assertEqual(self.deployment.current(), self.release)

    def test_unexpected_edits_links_and_ambiguous_stanza_are_refused(self):
        self.prepare()
        with self.assertRaises(deploy.DeployError):
            self.mutate('configure_doom_clipboard', self.expected, 'unexpected-release')
        self.assertEqual(self.config.read_bytes(), self.before)
        for content in [self.before + b'; manual edit\n', self.before + self.before]:
            self.config.write_bytes(content)
            expected = hashlib.sha256(content).hexdigest() if content == self.before + self.before else self.expected
            with self.assertRaises(deploy.DeployError):
                self.mutate('configure_doom_clipboard', expected, self.release)
            self.assertEqual(self.config.read_bytes(), content)
        other_before = self.original.read_bytes()
        self.config.unlink()
        self.config.symlink_to(self.original)
        with self.assertRaises(deploy.DeployError):
            self.mutate('configure_doom_clipboard', self.expected, self.release)
        self.assertEqual(self.original.read_bytes(), other_before)

    def test_restore_refuses_later_manual_change_without_overwriting(self):
        self.prepare()
        backup = self.mutate('configure_doom_clipboard', self.expected, self.release)
        self.config.write_bytes(self.after + b'; changed after deployment\n')
        with self.assertRaises(deploy.DeployError):
            self.mutate('restore', backup)
        self.assertTrue(self.config.read_bytes().endswith(b'; changed after deployment\n'))

    def test_interruption_after_replacement_remains_recoverable(self):
        self.prepare()
        write = deploy.atomic_json
        def interrupted(path, value, *args):
            if value.get('status') == 'migrated':
                raise OSError('simulated journal failure')
            return write(path, value, *args)
        with patch.object(deploy, 'atomic_json', side_effect=interrupted):
            with self.assertRaises(OSError):
                self.mutate('configure_doom_clipboard', self.expected, self.release)
        self.assertEqual(self.config.read_bytes(), self.after)
        pending = [p for p in (self.root/'backups').glob('*/backup.json')
                   if json.loads(p.read_text())['status'] == 'prepared']
        self.assertEqual(len(pending), 1)
        self.mutate('restore', pending[0].parent.name)
        self.assertEqual(self.config.read_bytes(), self.before)

    def test_failed_restore_reports_failure_and_retry_preserves_state(self):
        self.prepare()
        backup = self.mutate('configure_doom_clipboard', self.expected, self.release)
        replace = deploy.os.replace
        def fail_once(source, target):
            if target == self.config:
                raise OSError('simulated config restore failure')
            return replace(source, target)
        with patch.object(deploy.os, 'replace', side_effect=fail_once):
            with self.assertRaises(OSError):
                self.mutate('restore', backup)
        journal = json.loads((self.root/'backups'/backup/'backup.json').read_text())
        self.assertEqual(journal['status'], 'restoring')
        self.assertEqual(self.config.read_bytes(), self.after)
        self.mutate('restore', backup)
        self.assertEqual(self.config.read_bytes(), self.before)

    def test_dashboard_inline_edit_preserves_comment_settings_and_restores(self):
        self.prepare()
        source = self.repo / 'configs/doom/dashboard-faces.el'
        source.parent.mkdir()
        source.write_bytes((Path(__file__).resolve().parents[1]/'configs/doom/dashboard-faces.el').read_bytes())
        before = b"(setq doom-theme 'spacemacs-dark) ; preserve this comment\n" + self.before
        self.config.write_bytes(before)
        expected = hashlib.sha256(before).hexdigest()
        backup = self.mutate('configure_doom_dashboard', expected, self.release)
        after = before.replace(before.splitlines(keepends=True)[0],
                               before.splitlines(keepends=True)[0] + b'\n' + source.read_bytes(), 1)
        self.assertEqual(self.config.read_bytes(), after)
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o640)
        with self.assertRaises(deploy.DeployError):
            self.mutate('configure_doom_dashboard', hashlib.sha256(after).hexdigest(), self.release)
        self.mutate('restore', backup)
        self.mutate('restore', backup)
        self.assertEqual(self.config.read_bytes(), before)
