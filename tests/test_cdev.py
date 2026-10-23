from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import subprocess
import time
import unittest
import uuid

from cdev_harness import CdevHarness
from activity_harness import context, dispatch, enable_driver

INTEGRATION = os.environ.get("DOTFILES_INTEGRATION") == "1"


@unittest.skipUnless(INTEGRATION, "Use --integration for isolated Fish/cdev/native-process tests")
class CdevIntegration(unittest.TestCase):
    def setUp(self):
        self.h = CdevHarness()
        self.addCleanup(self.h.close)

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def reject_unchanged(self, root, message):
        before = self.h.snapshot(), self.h.log()
        result = self.h.cdev(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertEqual((self.h.snapshot(), self.h.log()), before)

    def test_project_reuse_naming_layout_and_no_duplicate_agents(self):
        h = self.h
        root = h.repo("space and quote's project")
        (root / "nested").mkdir()
        self.assertNotEqual(h.cdev(root, inside=False).returncode, 0)
        self.reject_unchanged(h.root, "not a Git")
        self.assert_ok(h.cdev(root / "nested"))
        window = h.window(root)
        rows = h.tm("list-panes", "-t", window, "-F", "#{pane_left}|#{pane_width}|#{pane_current_path}|#{pane_dead}").splitlines()
        data = [row.split("|") for row in rows]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0][0], "0")
        self.assertLessEqual(abs(int(data[0][1]) - int(data[1][1])), 1)
        self.assertTrue(all(row[2] == str(root) and row[3] == "0" for row in data))
        before = h.snapshot(), h.log()
        link = h.root / "project-link"
        link.symlink_to(root)
        for target in [root, link]:
            result = h.cdev(target)
            self.assert_ok(result)
            self.assertIn("reused", result.stdout)
        self.assert_ok(h.cdev(cwd=root / "nested"))
        h.tm("rename-window", "-t", window, "renamed-project")
        self.assert_ok(h.cdev(root))
        self.assertEqual((h.snapshot(), h.log()), before)
        # Reuse precedes future launch preflight, even with an invalid saved pin.
        pinfile = Path(h.env["XDG_STATE_HOME"]) / "cdev/pins.json"
        pinfile.parent.mkdir(parents=True, exist_ok=True)
        pinfile.write_text(json.dumps(dict(version=1, pins={str(root): str(uuid.uuid4())})))
        self.assert_ok(h.cdev(root))
        self.assertEqual((h.snapshot(), h.log()), before)
        self.assertFalse(list(h.release.rglob("*.pyc")))

    def test_concurrent_calls_and_same_name_collision(self):
        h = self.h
        root = h.repo("concurrent")
        code = "source " + shlex.quote(str(h.release / "fish/functions/cdev.fish")) + "; cdev " + shlex.quote(str(root))
        jobs = [subprocess.Popen(["fish", "--no-config", "-c", code], env=h.env, cwd=h.root,
                                 text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
        for job in jobs:
            out, err = job.communicate(timeout=15)
            self.assertEqual(job.returncode, 0, out + err)
        self.assertEqual(len(h.log()), 1)
        other = h.repo("other")
        collision = h.repo("collision")
        h.tm("new-window", "-d", "-n", "collision", "-c", str(other), "/bin/sleep 120")
        self.reject_unchanged(collision, "different or unverifiable")

    def test_generic_agent_and_mixed_or_unverifiable_roots_never_duplicate(self):
        h = self.h
        root = h.repo("generic")
        window = h.tm("new-window", "-d", "-P", "-F", "#{window_id}", "-n", "codex", "-c", str(root), str(h.bin / "codex")).strip()
        time.sleep(.1)
        before = h.snapshot(), h.log()
        result = h.cdev(root)
        self.assert_ok(result)
        self.assertIn("reused", result.stdout)
        self.assertEqual((h.snapshot(), h.log()), before)
        h.tm("kill-window", "-t", window)
        other = h.repo("other")
        window = h.tm("new-window", "-d", "-P", "-F", "#{window_id}", "-n", "mixed", "-c", str(root), "/bin/sleep 120").strip()
        h.tm("set-option", "-w", "-t", window, "@cdev_root", str(root))
        h.tm("split-window", "-d", "-h", "-t", window, "-c", str(other), "/bin/sleep 120")
        self.reject_unchanged(root, "mixed or unverifiable")
        h.tm("kill-window", "-t", window)
        window = h.tm("new-window", "-d", "-P", "-F", "#{window_id}", "-n", "recorded", "-c", str(other), "/bin/sleep 120").strip()
        h.tm("set-option", "-w", "-t", window, "@cdev_root", str(root))
        self.reject_unchanged(root, "mixed or unverifiable")

    def test_exact_conversation_pin_and_fail_closed_metadata(self):
        h = self.h
        root = h.repo("restore")
        first = h.saved(root)
        self.assert_ok(h.cdev(root))
        self.assertEqual(h.log()[-1][1:5], ["resume", first, "--cd", str(root)])
        h.tm("kill-window", "-t", h.window(root))
        h.saved(root)
        # Once selected, a newer conversation cannot change the project's pin.
        self.assert_ok(h.cdev(root))
        self.assertEqual(h.log()[-1][2], first)
        h.tm("kill-window", "-t", h.window(root))
        self.assert_ok(h.fish("cdev-pin " + first + " " + shlex.quote(str(root))))
        pinfile = Path(h.env["XDG_STATE_HOME"]) / "cdev/pins.json"
        self.assertEqual(pinfile.stat().st_mode & 0o777, 0o600)
        self.assert_ok(h.cdev(root))
        self.assertEqual(h.log()[-1][1:5], ["resume", first, "--cd", str(root)])
        h.tm("kill-window", "-t", h.window(root))
        other = h.repo("unrelated")
        wrong = h.saved(other)
        for identity in [wrong, str(uuid.uuid4()), "not-a-uuid"]:
            result = h.fish("cdev-pin " + identity + " " + shlex.quote(str(root)))
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(pinfile.read_text())["pins"][str(root)], first)
        self.assert_ok(h.fish("cdev-pin --remove " + shlex.quote(str(root))))
        pinfile.write_text("{broken")
        self.reject_unchanged(root, "cannot read pin metadata")
        pinfile.write_text(json.dumps(dict(version=1, pins={})))
        nested = h.repo("nested-history")
        (nested / "inside").mkdir()
        identity = h.saved(nested, nested / "inside")
        self.assert_ok(h.cdev(nested))
        self.assertEqual(h.log()[-1][2], identity)
        ambiguous = h.repo("ambiguous-history")
        h.saved(ambiguous)
        h.saved(ambiguous)
        self.reject_unchanged(ambiguous, "ambiguous project history")
        for launch in h.log():
            self.assertFalse(set(launch) & {"--last", "--all", "--sandbox", "--ask-for-approval", "--no-daemon",
                                          "--dangerously-bypass-hook-trust", "--dangerously-bypass-approvals-and-sandbox"})

    def test_unavailable_daemon_and_explicit_standalone_fallback(self):
        h = self.h
        root = h.repo("unavailable")
        env = h.env | {"CDEV_TEST_FAIL": "unavailable"}
        before = h.snapshot(), h.log()
        result = h.cdev(root, env=env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no fallback", result.stderr)
        self.assertEqual(before, (h.snapshot(), h.log()))
        self.assert_ok(h.fish("CDEV_EDITOR_MODE=standalone cdev " + shlex.quote(str(root)), env=env))
        self.assertIn("|27.0|-nw", Path(h.env["CDEV_TEST_EDITOR_LOG"]).read_text())

    def test_failed_agent_is_visible_never_retried_and_existing_panes_survive(self):
        h = self.h
        root = h.repo("failing-resume")
        identity = h.saved(root)
        self.assert_ok(h.fish("cdev-pin " + identity + " " + shlex.quote(str(root))))
        previous = h.snapshot()
        h.tm("set-environment", "-g", "CDEV_TEST_FAIL", "pinned")
        result = h.cdev(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("retained", result.stderr)
        self.assertIn(previous.strip(), h.snapshot())
        self.assertEqual(len(h.log()), 1)
        self.assertIn("1", h.tm("list-panes", "-t", h.window(root), "-F", "#{pane_dead}").splitlines())
        again = h.cdev(root)
        self.assertEqual(len(h.log()), 1)

    def test_scoped_dashboard_hook_targets_plain_cdev_pane_and_can_be_disabled(self):
        h = self.h
        enable_driver(h)
        root = h.repo("ordinary-no-worktree")
        self.assert_ok(h.cdev(root))
        args = h.log()[-1]
        self.assertEqual(args[1:3], ["--cd", str(root)])
        self.assertIn("hooks.UserPromptSubmit=", " ".join(args))
        right = h.tm("list-panes", "-t", h.window(root), "-F", "#{pane_id}").splitlines()[1]
        marker = h.tm("show-options", "-pqv", "-t", right, "@dotfiles-agent-evidence").strip()
        self.assertTrue(marker)
        self.assertNotIn("--token", context(h, right)["command"])
        for event in ["UserPromptSubmit", "PermissionRequest", "PostToolUse", "Stop"]:
            result = dispatch(h, right, event=event)
            self.assertEqual(result["code"], 0, result["stderr"])
        records = list((Path(h.env["XDG_STATE_HOME"]) / "dotfiles-dashboard").glob("*.json"))
        self.assertEqual(json.loads(records[0].read_text())["state"], "done")
        other = h.repo("dashboard-off")
        h.tm("set-environment", "-gu", "CDEV_TEST_DRIVER")
        self.assert_ok(h.fish("CDEV_DASHBOARD=0 cdev " + shlex.quote(str(other))))
        self.assertEqual(h.log()[-1][1:], ["--cd", str(other)])

    def test_unchanged_live_standalone_function_uses_stable_installed_adapter_path(self):
        h = self.h
        source = Path.home() / ".config/fish/functions/cdev.fish"
        if not source.is_file():
            self.skipTest("Inspected standalone launcher is not available")
        # A read-only copy of this one inspected public function. No Fish startup
        # or other live configs run; editor and agent are owned inert stand-ins.
        fixture = h.root / "standalone.fish"
        fixture.write_bytes(source.read_bytes())
        installed = h.home / ".config/cdev"
        installed.mkdir(parents=True)
        for name in ["codex_session.py", "activity.py"]:
            (installed / name).symlink_to(h.release / "cdev" / name)
        root = h.repo("legacy-standalone")
        identity = h.saved(root)
        self.assert_ok(h.fish("source " + shlex.quote(str(fixture)) + "; cdev " + shlex.quote(str(root))))
        self.assertIn("|27.0|-nw", Path(h.env["CDEV_TEST_EDITOR_LOG"]).read_text())
        args = h.log()[-1]
        self.assertEqual(args[1:5], ["resume", identity, "--cd", str(root)])
        hook = next(value for value in args if value.startswith("hooks.UserPromptSubmit="))
        command = json.JSONDecoder().raw_decode(hook.split("command=", 1)[1])[0]
        self.assertIn(str(installed / "activity.py"), command)
        self.assertNotIn(str(h.release), command)
        before = h.snapshot(), h.log()
        self.assert_ok(h.fish("source " + shlex.quote(str(fixture)) + "; cdev " + shlex.quote(str(root))))
        self.assertEqual((h.snapshot(), h.log()), before)
