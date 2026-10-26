"""Personal source coverage, parser safety and backup-first disposable bootstrap."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from deploy import Deployment, manifest_check
from validation import syntax_checks, ValidationError


REPO = Path(__file__).resolve().parents[1]


class PersonalConfigurationTests(unittest.TestCase):
    def test_actual_configuration_sources_and_include_graph_are_present(self):
        manifest = manifest_check(json.loads((REPO / 'deploy/manifest.json').read_text()))
        source = {item['source']: item for item in manifest['files']}
        required = ['doom/init.el', 'doom/config.el', 'doom/packages.el', 'doom/org.el',
            'doom/simpleclip.el', 'doom/dashboard-faces.el', 'doom/clipboard.el', 'doom/cdev.el',
            'doom/snippets/org-mode/phonemic', 'doom/templates/new.org',
            'fish/config.fish', 'fish/functions/fp.fish', 'fish/functions/cdev.fish',
            'fish/functions/cdev-pin.fish', 'fish/functions/cnew.fish', 'fish/conf.d/fzf.fish',
            'aerospace/aerospace.toml', 'git/gitconfig', 'shell/zprofile', 'gh/config.yml']
        self.assertTrue(all('configs/' + path in source for path in required))
        config = (REPO / 'configs/doom/config.el').read_text()
        for name in ['org', 'clipboard', 'dashboard-faces']:
            self.assertIn('(load! "' + name + '")', config)
        self.assertNotIn('(defun dotfiles-dashboard-background-h', config)
        self.assertIn('identity.el', config)
        self.assertIn('@users.noreply.github.com', config)
        self.assertIn('spacemacs-theme-org-highlight nil', config)
        targets = {row['target'] for row in manifest['files']}
        for excluded in ['.codex/config.toml', '.codex/hooks.json', '.config/workmux/config.yaml',
                         '.config/doom/custom.el', '.config/doom/identity.el',
                         '.config/fish/fish_variables', '.local/state/cdev/pins.json']:
            self.assertNotIn(excluded, targets)

    def test_upstream_fzf_snapshot_and_required_license_notices(self):
        row = json.loads((REPO / 'deploy/provenance.json').read_text())
        self.assertEqual(len(row['files']), 10)
        for name, digest in row['files'].items():
            self.assertEqual(hashlib.sha256((REPO / name).read_bytes()).hexdigest(), digest, name)
        for name in ['LICENSE', 'THIRD_PARTY.md', 'LICENSES/Doom-MIT.txt',
                     'LICENSES/fzf-MIT.txt', 'LICENSES/GPL-2.0-only.txt']:
            self.assertTrue((REPO / name).is_file(), name)
        self.assertIn('Simplified BSD License', (REPO / 'configs/doom/simpleclip.el').read_text())

    def test_fish_startup_and_saved_color_preferences_in_an_empty_home(self):
        with tempfile.TemporaryDirectory(prefix='df-fish-personal-') as directory:
            home = Path(directory)
            shutil.copytree(REPO / 'configs/fish', home / '.config/fish')
            env = dict(HOME=str(home), XDG_CONFIG_HOME=str(home / '.config'),
                       XDG_DATA_HOME=str(home / '.local/share'),
                       PATH='/opt/homebrew/bin:/usr/bin:/bin', TERM='xterm-256color')
            command = ('functions -q cdev cnew fp la ll; or exit 81; '
                       'test "$fish_color_command" = normal; or exit 82; '
                       'test "$fish_color_error" = brred; or exit 83; '
                       'test "$EDITOR" = emacs; or exit 84')
            result = subprocess.run(['fish', '-c', command], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((home / 'org').exists())
            self.assertFalse((home / 'icloud').exists())
            self.assertFalse((home / '.local/state/cdev/pins.json').exists())

    def parse(self, root, kind, text):
        p = root / kind
        p.write_text(text)
        return syntax_checks(root, {'files': [dict(path=kind, syntax=kind)]})

    def test_new_parsers_validate_without_executing_configuration(self):
        with tempfile.TemporaryDirectory(prefix='df-parser-') as directory:
            root = Path(directory)
            self.parse(root, 'toml', 'config-version = 2\n[mode.main.binding]\nctrl-alt-h="focus left"\n')
            self.parse(root, 'json', '{"hooks":{}}')
            # Real Doom template comments contain unmatched example brackets.
            # Fundamental-mode check-parens misclassifies those as code.
            self.parse(root, 'elisp', ';; An example: (unclosed\n(setq valid t)\n')
            # Invalid included Git configuration must not be traversed by parsing.
            include = root / 'bad-include'
            include.write_text('not valid Git syntax [')
            self.parse(root, 'gitconfig', '[include]\npath = ' + str(include) + '\n')
            marker = root / 'must-not-exist'
            self.parse(root, 'zsh', 'touch ' + str(marker) + '\n')
            self.assertFalse(marker.exists())
            for kind, text in [('toml', '[broken'), ('json', '{broken'),
                               ('gitconfig', '[broken'), ('zsh', 'if then')]:
                with self.subTest(kind=kind), self.assertRaises(ValidationError):
                    self.parse(root, kind, text)

    @unittest.skipUnless(os.environ.get('DOTFILES_INTEGRATION') == '1', 'private full-manifest bootstrap')
    def test_real_manifest_bootstrap_activation_and_complete_restoration(self):
        with tempfile.TemporaryDirectory(prefix='df-bootstrap-', dir='/private/tmp') as directory:
            root = Path(directory)
            repo, home, state = root / 'checkout', root / 'home', root / 'releases'
            home.mkdir()
            shutil.copytree(REPO / 'configs', repo / 'configs')
            shutil.copytree(REPO / 'deploy', repo / 'deploy')
            d = Deployment(repo, home, state)
            manifest = d.manifest()
            # Satisfy file-presence dependencies with inert local files. Parsers
            # run for real; no dependency startup code may ever be executed.
            for dep in manifest['dependencies']:
                if 'home_path' in dep:
                    p = home / dep['home_path']
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text('#!/bin/sh\nexit 91\n')
                    p.chmod(0o755 if dep.get('executable') else 0o644)
            originals = {}
            for index, item in enumerate(manifest['files']):
                path = home / item['target']
                if item['component'] == 'tmux-dashboard':
                    continue  # Optional helper mappings deliberately remain absent.
                path.parent.mkdir(parents=True, exist_ok=True)
                if index % 3:
                    path.write_bytes(('original ' + item['target'] + '\n').encode())
                    path.chmod(0o640)
                    originals[item['target']] = path.read_bytes()
                else:
                    originals[item['target']] = None
            external = {}
            for name in ['.codex/config.toml', '.codex/hooks.json', '.config/doom/custom.el',
                         '.config/doom/identity.el', '.local/state/cdev/pins.json']:
                path = home / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('private fixture remains external\n')
                external[name] = path.read_bytes()
            with d.locked():
                first = d.stage()  # All real source payloads and parsers.
            self.assertIsNone(d.current())
            self.assertEqual(len(d.receipt(first, parse=False)['files']), len(manifest['files']))
            # Reusing the already parsed bytes avoids repeating every external
            # parser for each migration. Hash/reference/drift checks stay real.
            with patch('deploy.syntax_checks', return_value=['validated above']):
                backups = []
                components = list(dict.fromkeys(row['component'] for row in manifest['files']
                                               if row['component'] != 'tmux-dashboard'))
                for component in components:
                    with d.locked():
                        backups.append(d.migrate(first, component))
                for item in manifest['files']:
                    p = home / item['target']
                    if item['component'] == 'tmux-dashboard':
                        self.assertFalse(os.path.lexists(p))
                        continue
                    self.assertTrue(d.is_managed(item))
                    self.assertEqual(p.resolve(), d.release_dir(first) / item['path'])
                    self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o444)
                with d.locked():
                    second = d.stage()
                    d.activate(second, first)
                    self.assertEqual(d.rollback(second), first)
                for backup in reversed(backups):
                    with d.locked():
                        d.restore(backup)
                        d.restore(backup)  # Recovery is idempotent.
            self.assertIsNone(d.current())
            for name, data in originals.items():
                p = home / name
                if data is None:
                    self.assertFalse(os.path.lexists(p), name)
                else:
                    self.assertFalse(p.is_symlink())
                    self.assertEqual(p.read_bytes(), data)
                    self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o640)
            for name, data in external.items():
                self.assertEqual((home / name).read_bytes(), data)
                self.assertFalse((home / name).is_symlink())
