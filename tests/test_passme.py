"""Exercise the actual Fish function with real randomness and an isolated clipboard."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
FISH = shutil.which('fish')
OPENSSL = shutil.which('openssl')


@unittest.skipUnless(FISH and OPENSSL, 'Fish and OpenSSL required')
class PassmeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='df-passme-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.capture = self.root / 'clipboard'
        config = (REPO / 'configs/fish/config.fish').read_text()
        start = config.index('function passme')
        end = config.index('\nend', start) + len('\nend')
        self.function = self.root / 'passme.fish'
        self.function.write_text(config[start:end] + '\n')
        (self.bin / 'openssl').symlink_to(OPENSSL)
        self.script('pbcopy', '/bin/cat >> "$PASSME_CAPTURE"')
        self.env = dict(HOME=str(self.root), XDG_CONFIG_HOME=str(self.root / 'config'),
                        PATH=str(self.bin), PASSME_CAPTURE=str(self.capture),
                        TERM='xterm-256color')

    def script(self, name, body):
        path = self.bin / name
        path.unlink(missing_ok=True)
        path.write_text('#!/bin/sh\n' + body + '\n')
        path.chmod(0o700)

    def run_passme(self, count=1):
        command = 'source "$argv[1]"; ' + 'passme; or exit $status; ' * count
        return subprocess.run([FISH, '--no-config', '-c', command, str(self.function)],
                              env=self.env, capture_output=True, text=True, timeout=15)

    def test_real_randomness_has_exact_length_required_classes_and_no_output_leak(self):
        result = self.run_passme(64)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = self.capture.read_bytes()
        self.assertEqual(len(data), 64 * 48)  # No clipboard newline or trailing spaces.
        values = [data[i:i + 48] for i in range(0, len(data), 48)]
        self.assertEqual(len(set(values)), 64)
        for value in values:
            # Never include generated credentials in assertion diagnostics.
            self.assertTrue(value.isalnum())
            self.assertTrue(any(97 <= c <= 122 for c in value))
            self.assertTrue(any(65 <= c <= 90 for c in value))
            self.assertTrue(any(48 <= c <= 57 for c in value))
            self.assertFalse(value.decode() in result.stdout + result.stderr)
        self.assertEqual(result.stdout.count('copied to clipboard'), 64)

    def test_generator_failure_preserves_clipboard_and_never_reports_success(self):
        self.capture.write_bytes(b'previous clipboard')
        self.script('openssl', 'exit 42')
        result = self.run_passme()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('random generation failed', result.stderr)
        self.assertNotIn('copied', result.stdout)
        self.assertEqual(self.capture.read_bytes(), b'previous clipboard')

    def test_malformed_generator_output_is_rejected_before_copy(self):
        self.script('openssl', 'printf "bad-output\\n"')
        result = self.run_passme()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unexpected generator output', result.stderr)
        self.assertFalse(self.capture.exists())

    def test_noncompliant_candidates_are_retried_with_a_bound(self):
        self.script('openssl', 'printf "%s\\n" ' + 'a' * 64)
        result = self.run_passme()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('could not generate a compliant password', result.stderr)
        self.assertFalse(self.capture.exists())

    def test_filtering_discards_punctuation_without_mapping_or_short_output(self):
        sample = 'aB1+' * 16
        self.script('openssl', 'printf "%s\\n" ' + sample)
        result = self.run_passme()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.capture.read_bytes(), b'aB1' * 16)

    def test_clipboard_failure_returns_nonzero_without_success(self):
        self.script('pbcopy', 'exit 7')
        result = self.run_passme()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('clipboard copy failed', result.stderr)
        self.assertNotIn('copied', result.stdout)

    def test_missing_dependency_is_actionable_and_does_not_copy(self):
        (self.bin / 'openssl').unlink()
        result = self.run_passme()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('openssl and pbcopy are required', result.stderr)
        self.assertFalse(self.capture.exists())
