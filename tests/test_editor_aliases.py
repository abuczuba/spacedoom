"""Fish terminal-client shortcuts, without launching editors or touching user state."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
FISH = shutil.which('fish')


@unittest.skipUnless(FISH, 'Fish required')
class EditorAliasTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='df-editor-alias-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.config = self.root / 'config with spaces'
        (self.config / 'cdev').mkdir(parents=True)
        source = (REPO / 'configs/fish/config.fish').read_text()
        functions = []
        for name in ['emacs', 'emax']:
            start = source.index('function ' + name + ' --description')
            end = source.index('\nend', start) + len('\nend')
            functions.append(source[start:end])
        functions.append(next(line for line in source.splitlines() if line.startswith('alias enw=')))
        self.functions = self.root / 'clients.fish'
        self.functions.write_text('\n'.join(functions))
        stub = ('import json, os, sys\nfrom pathlib import Path\n'
                'Path(os.environ["EDITOR_CAPTURE"]).write_text(json.dumps('
                '{"tool": Path(sys.argv[0]).name, "args": sys.argv[1:]}))\n'
                'sys.exit(int(os.environ.get("EDITOR_EXIT", "0")))\n')
        for name in ['emacs', 'emacsclient']:
            p = self.bin / name
            p.write_text('#!' + sys.executable + '\n' + stub)
            p.chmod(0o700)
        (self.config / 'cdev/doom-server.py').write_text(stub)
        self.capture = self.root / 'capture.json'
        self.env = os.environ.copy() | dict(HOME=str(self.root), PATH=str(self.bin),
            XDG_CONFIG_HOME=str(self.config), XDG_STATE_HOME=str(self.root / 'state with spaces'),
            EDITOR_CAPTURE=str(self.capture))

    def run_alias(self, command):
        return subprocess.run([FISH, '--no-config', '-c', 'source "$argv[1]"; ' + command,
                               str(self.functions)], env=self.env, cwd=self.root,
                              capture_output=True, text=True, timeout=10)

    def test_emacs_uses_named_terminal_client_and_preserves_file_arguments(self):
        result = self.run_alias('emacs "file with spaces.txt"')
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(self.capture.read_text())
        self.assertEqual(record['tool'], 'emacsclient')
        self.assertEqual(record['args'], ['--socket-name=' + str(self.root / 'state with spaces/cdev-emacs/server'),
            '--alternate-editor=/usr/bin/false', '-t', 'file with spaces.txt'])

    def test_emax_uses_current_folder_and_requests_dashboard_only_for_new_workspaces(self):
        result = self.run_alias('emax')
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(self.capture.read_text())
        self.assertEqual(record['tool'], 'doom-server.py')
        self.assertEqual(record['args'], ['client', '--project=' + str(self.root), '--dashboard-if-new'])

    def test_emax_accepts_one_explicit_directory_and_rejects_extra_arguments(self):
        result = self.run_alias('emax "another folder"')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--project=another folder', json.loads(self.capture.read_text())['args'])
        self.capture.unlink()
        result = self.run_alias('emax first second')
        self.assertEqual(result.returncode, 2)
        self.assertIn('Usage: emax', result.stderr)
        self.assertFalse(self.capture.exists())

    def test_enw_still_invokes_real_emacs_instead_of_recursing_into_client_alias(self):
        result = self.run_alias('enw "file with spaces.txt"')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.capture.read_text()), {'tool': 'emacs', 'args': ['-nw', 'file with spaces.txt']})

    def test_missing_server_error_is_returned_without_starting_another_editor(self):
        self.env['EDITOR_EXIT'] = '9'
        self.assertEqual(self.run_alias('emacs').returncode, 9)
