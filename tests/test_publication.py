"""Private Git fixtures prove full-history coverage without exposing findings."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from publication_audit import audit, findings, sensitive_path


class PublicationTests(unittest.TestCase):
    def test_deleted_secret_is_still_found_and_value_is_not_reported(self):
        with tempfile.TemporaryDirectory(prefix="df-audit-") as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-c", "user.name=Fixture",
                    "-c", "user.email=fixture@example.org", "-c", "commit.gpgsign=false",
                    *args], cwd=root, stderr=subprocess.DEVNULL)
            git("init", "-q", "--template=")
            secret = "ghp_" + "x" * 32
            (root / "temporary.txt").write_text(secret)
            git("add", "temporary.txt")
            git("commit", "-qm", "fixture secret")
            git("rm", "-q", "temporary.txt")
            git("commit", "-qm", "remove fixture secret")
            result = audit(root)
            self.assertEqual(result["commits"], 2)
            self.assertTrue(any(row["kind"] == "github-token" and row["reachable"]
                                for row in result["findings"]))
            self.assertNotIn(secret, json.dumps(result))

    def test_unreachable_blob_is_distinguished_from_publication_surface(self):
        with tempfile.TemporaryDirectory(prefix="df-audit-") as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "--template=", str(root)], check=True)
            subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=root,
                           input=b"sk-" + b"x" * 32, check=True, capture_output=True)
            # No commit exists yet: create an empty one without touching global config.
            subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.org",
                "-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "fixture"],
                cwd=root, check=True)
            result = audit(root)
            self.assertEqual(len(result["findings"]), 1)
            self.assertFalse(result["findings"][0]["reachable"])

    def test_known_credential_formats_and_sensitive_state_paths(self):
        self.assertEqual(findings(("https://ntfy.sh/" + "a" * 48).encode())[0]["kind"], "notification-topic")
        self.assertTrue(sensitive_path("old/.codex/auth.json"))
        self.assertTrue(sensitive_path("state/pins.json"))
        self.assertFalse(sensitive_path("configs/doom/org.el"))
        self.assertFalse(sensitive_path("configs/codex/config.example.toml"))
        self.assertFalse(findings(b"ssh-ed25519 public signing key reference; token = example"))

    def test_staged_private_identity_is_blocked_but_template_is_allowed(self):
        with tempfile.TemporaryDirectory(prefix="df-audit-index-") as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "--template=", str(root)], check=True)
            script = Path(__file__).resolve().parents[1] / "scripts/preflight.py"
            p = root / "identity.example.el"
            p.write_text('(setq user-mail-address "you@example.org")\n')
            subprocess.run(["git", "add", p.name], cwd=root, check=True)
            self.assertEqual(subprocess.run(["python3", str(script)], cwd=root, capture_output=True).returncode, 0)
            private = root / "identity.el"
            private.write_text('private fixture, not a real identity\n')
            subprocess.run(["git", "add", private.name], cwd=root, check=True)
            result = subprocess.run(["python3", str(script)], cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("identity.el", result.stderr)
