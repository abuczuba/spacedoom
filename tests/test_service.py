from __future__ import annotations

from contextlib import redirect_stdout, redirect_stderr
import io
import json
import os
from pathlib import Path
import plistlib
import tempfile
import unittest
from unittest.mock import patch

import doom_service

REPO = Path(__file__).resolve().parents[1]


class ServiceTests(unittest.TestCase):
    def test_plan_and_missing_approval_never_write_or_invoke_launchctl(self):
        with tempfile.TemporaryDirectory(prefix="df-service-") as directory:
            root = Path(directory).resolve()
            with patch.object(doom_service.Path, "home", return_value=root), patch.object(doom_service.subprocess, "run") as run:
                with redirect_stdout(io.StringIO()) as output:
                    self.assertEqual(doom_service.main(["plan"]), 0)
                self.assertIn("bootstrap", json.loads(output.getvalue()))
                for action in ["bootstrap", "kickstart", "bootout"]:
                    with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
                        doom_service.main([action])
                run.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])

    def test_bootstrap_prepares_private_logs_only_after_guard_and_kickstart_never_kills(self):
        with tempfile.TemporaryDirectory(prefix="df-service-") as directory:
            root = Path(directory).resolve()
            with patch.object(doom_service.Path, "home", return_value=root), patch.object(doom_service, "verified_plist"), \
                    patch.object(doom_service.subprocess, "run") as run:
                run.return_value.returncode = 0
                self.assertEqual(doom_service.main(["bootstrap", "--approve"]), 0)
                self.assertEqual((root / ".local/state/cdev-emacs").stat().st_mode & 0o777, 0o700)
                self.assertEqual((root / ".local/state/cdev-emacs/server.log").stat().st_mode & 0o777, 0o600)
                self.assertEqual(doom_service.main(["kickstart", "--approve"]), 0)
                self.assertNotIn("-k", run.call_args.args[0])

    def test_launchagent_has_no_restart_loop_and_pins_complete_release(self):
        value = plistlib.loads((REPO / "configs/launchd/local.dotfiles.doom.plist").read_bytes())
        self.assertFalse(value["KeepAlive"])
        self.assertTrue(value["RunAtLoad"])
        self.assertEqual(value["Umask"], 0o077)
        self.assertEqual(value["ProgramArguments"][2], "@RELEASE@/cdev/doom-server.py")
        self.assertEqual(value["EnvironmentVariables"]["MACOSX_DEPLOYMENT_TARGET"], "27.0")
