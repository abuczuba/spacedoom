from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import shlex
import tempfile
import time
import unittest
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor

from cdev_harness import CdevHarness
from activity_harness import context, dispatch, enable_driver, wait_for
from hooks_rpc import hook_metadata

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("activity", REPO / "configs/cdev/activity.py")
activity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(activity)
INTEGRATION = os.environ.get("DOTFILES_INTEGRATION") == "1"


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(token="launch-one", state="idle", session=None, turn=None,
                           ended=False, sequence=0, stamp=0)

    def send(self, event, turn="turn-a", **extra):
        result = activity.transition(self.record, dict(hook_event_name=event, session_id="session-a", turn_id=turn) | extra, 1000)
        if result is not None:
            self.record = result
        return result

    def test_lifecycle_and_approval_evidence_without_conversation_storage(self):
        self.send("SessionStart")
        self.assertEqual(self.record["state"], "idle")
        self.send("UserPromptSubmit", prompt="PRIVATE TEST PROMPT")
        self.assertEqual(self.record["state"], "working")
        self.send("PermissionRequest", tool_name="Bash", tool_input={"command": "PRIVATE TEST COMMAND"})
        self.assertEqual(self.record["state"], "waiting")
        self.send("PostToolUse", tool_name="mcp__else")
        self.assertEqual(self.record["state"], "waiting")
        self.send("PostToolUse", tool_name="Bash")
        self.assertEqual(self.record["state"], "working")
        self.send("Stop")
        self.assertEqual(self.record["state"], "done")
        self.assertIsNone(self.send("PostToolUse", tool_name="Bash"))
        self.assertNotIn("PRIVATE", json.dumps(self.record))
        self.send("UserPromptSubmit", turn="turn-b")
        self.assertIsNone(self.send("Stop", turn="turn-a"))
        self.assertEqual(self.record["state"], "working")
        self.send("Interrupt", turn="turn-b")
        self.assertEqual(self.record["state"], "idle")
        self.assertIsNone(self.send("UserPromptSubmit", turn="turn-b"))

    def test_session_end_stale_unknown_events_and_missing_turn_are_conservative(self):
        self.send("UserPromptSubmit")
        self.assertIsNone(self.send("Stop", session_id="old-session"))
        self.assertIsNone(self.send("Stop", turn=None))
        self.assertIsNone(self.send("Notification"))
        self.send("SessionEnd", turn=None)
        self.assertEqual(self.record["state"], "idle")
        self.assertIsNone(self.send("UserPromptSubmit", turn="new"))

    def test_invocation_config_has_no_policy_or_global_hook_overrides(self):
        with tempfile.TemporaryDirectory(prefix="df-hooks-") as folder:
            launch = activity.Launch(Path(folder).resolve(), "/private/tmp/test.sock", "%42")
            args = launch.config_args()
            self.assertEqual(args[::2], ["-c"] * len(activity.EVENTS))
            for event, value in zip(activity.EVENTS, args[1::2]):
                self.assertTrue(value.startswith("hooks." + event + "="))
                self.assertNotIn("%42", value)
                self.assertNotIn(launch.token, value)
                self.assertNotIn(str(folder), value)
                for forbidden in ["bypass", "approval_policy", "notify=", "sandbox", "features.hooks=false"]:
                    self.assertNotIn(forbidden, value)
            home = Path(folder).resolve() / "home"
            home.mkdir()
            (home / ".codex").mkdir()
            env = os.environ.copy() | {"HOME": str(home), "CODEX_HOME": str(home / ".codex")}
            # Config parsing only: no conversations, authentication, tools,
            # network, daemon or trust bypass. The CLI validates inline hooks.
            result = subprocess.run(["codex", *args, "features", "list"],
                                    env=env, text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_native_definition_hashes_stable_and_workmux_source_untouched(self):
        with tempfile.TemporaryDirectory(prefix="df-hook-hash-") as directory:
            home = Path(directory).resolve()
            config = home / ".codex"
            config.mkdir(mode=0o700)
            (config / "config.toml").write_text('[features]\nhooks = true\n')
            # Inspect only the already relevant public hook definitions. No
            # auth, trust state or other user configuration is copied or edited.
            source = Path.home() / ".codex/hooks.json"
            hooks = json.loads(source.read_text())
            self.assertTrue(all("workmux " in h["command"] for groups in hooks["hooks"].values()
                                for group in groups for h in group["hooks"]))
            (config / "hooks.json").write_text(json.dumps(hooks))
            original = hook_metadata(home, home)
            launches = [activity.Launch(home / "one", "/private/tmp/one.sock", "%42"),
                        activity.Launch(home / "two", "/private/tmp/two.sock", "%99")]
            self.assertNotEqual(launches[0].token, launches[1].token)
            self.assertEqual(launches[0].config_args(), launches[1].config_args())
            first, second = [hook_metadata(home, home, launch.config_args()) for launch in launches]
            extract = lambda rows: {h["key"]: h["currentHash"] for h in rows}
            self.assertEqual(extract(first), extract(second))
            self.assertEqual({k: v for k, v in extract(first).items() if k in extract(original)}, extract(original))
            new = [h for h in first if h["source"] == "sessionFlags"]
            self.assertEqual(len(new), 8)
            self.assertTrue(all(h["trustStatus"] == "untrusted" and not h["isManaged"] for h in new))
            self.assertEqual(len(first), len(original) + 8)
            self.assertNotIn("state", (config / "config.toml").read_text())

    def test_runtime_input_and_record_permissions_fail_closed(self):
        for raw in ['[]', '{}', '{"version":1}', 'x' * 4097]:
            with patch.dict(os.environ, {activity.CONTEXT_ENV: raw}):
                with self.assertRaises(ValueError):
                    activity.runtime_context()
        with tempfile.TemporaryDirectory(prefix="df-private-context-") as directory:
            root = Path(directory).resolve()
            path = activity.folder(root) / "record.json"
            activity.save(path, {"only": "metadata"})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)
            self.assertEqual(activity.private_record(path), {"only": "metadata"})
            path.chmod(0o644)
            with self.assertRaises(ValueError):
                activity.private_record(path)
            alias = root / "alias"
            alias.symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                activity.folder(alias)

    def test_managed_symlink_keeps_definition_path_stable(self):
        with tempfile.TemporaryDirectory(prefix="df-hook-path-") as directory:
            root = Path(directory).resolve()
            link = root / "activity.py"
            targets = [root / "release-a.py", root / "release-b.py"]
            for target in targets:
                target.write_text("# owned fixture\n")
            link.symlink_to(targets[0])
            with patch.object(activity, "__file__", str(link)):
                first = activity.Launch(root, "/private/tmp/one.sock", "%1").config_args()
                link.unlink()
                link.symlink_to(targets[1])
                second = activity.Launch(root, "/private/tmp/two.sock", "%2").config_args()
            self.assertEqual(first, second)
            self.assertIn(str(link), str(first))
            self.assertNotIn("release-a", str(first))

    def test_failed_adapter_is_advisory_with_no_shell_or_policy_output(self):
        command = ["python3", "-B", str(REPO / "configs/cdev/activity.py"), "event"]
        for raw in ['', 'bad-json', '{"version":1}']:
            result = subprocess.run(command, input='{"hook_event_name":"Stop"}',
                                    env=os.environ.copy() | {activity.CONTEXT_ENV: raw},
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


@unittest.skipUnless(INTEGRATION, "Use --integration for private hook dispatch")
class ActivityIntegration(unittest.TestCase):
    def setUp(self):
        self.h = CdevHarness()
        self.addCleanup(self.h.close)
        enable_driver(self.h)
        self.root = self.h.repo("ordinary-project")
        result = self.h.fish("CDEV_EDITOR_MODE=standalone cdev " + shlex.quote(str(self.root)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.pane = self.h.tm("list-panes", "-t", self.h.window(self.root), "-F", "#{pane_id}").splitlines()[1]
        self.first = context(self.h, self.pane)
        self.runtime = json.loads(self.first["runtime"])
        self.path = activity.record_path(self.runtime["state"], self.h.socket, self.pane)
        wait_for(lambda: activity.private_record(self.path).get("child"))

    def test_concurrent_same_cwd_wrong_environment_reordering_and_no_cross_pane_events(self):
        h = self.h
        other = h.tm("new-window", "-P", "-F", "#{pane_id}", "/usr/bin/python3", "-B",
                     str(h.home / ".config/cdev/codex_session.py"), "launch", "--root", str(self.root),
                     "--codex", str(h.bin / "codex")).strip()
        second = context(h, other)
        other_runtime = json.loads(second["runtime"])
        other_path = activity.record_path(other_runtime["state"], h.socket, other)
        wait_for(lambda: activity.private_record(other_path).get("child"))
        self.assertEqual(self.first["command"], second["command"])
        self.assertNotEqual(self.runtime["token"], other_runtime["token"])
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(lambda row: dispatch(h, row[0], session=row[1]),
                                    [(self.pane, "session-a"), (other, "session-b")]))
        self.assertTrue(all(r["code"] == 0 for r in results))
        self.assertEqual(activity.private_record(self.path)["session"], "session-a")
        self.assertEqual(activity.private_record(other_path)["session"], "session-b")
        before = self.path.read_bytes()
        dispatch(h, other, event="Stop", session="session-a", runtime=self.first["runtime"])
        self.assertEqual(self.path.read_bytes(), before)
        h.tm("set-option", "-g", "renumber-windows", "on")
        h.tm("swap-window", "-s", h.window(self.root), "-t", "0", "-d")
        h.tm("rename-window", "-t", other, "moved-title")
        dispatch(h, self.pane, event="PermissionRequest", session="session-a")
        dispatch(h, other, event="Stop", session="session-b")
        self.assertEqual(activity.private_record(self.path)["state"], "waiting")
        self.assertEqual(activity.private_record(other_path)["state"], "done")
        dispatch(h, self.pane, event="PostToolUse", session="session-a")
        self.assertEqual(activity.private_record(self.path)["state"], "working")
        self.assertIn("|27.0|-nw", Path(h.env["CDEV_TEST_EDITOR_LOG"]).read_text())

    def test_stale_nonce_process_reuse_session_and_turn_fail_closed(self):
        h = self.h
        dispatch(h, self.pane)
        before = self.path.read_bytes()
        for change in [{"token": "0" * 32}, {"started": "previous process"}, {"pid": 1}]:
            dispatch(h, self.pane, event="Stop", runtime=json.dumps(self.runtime | change))
            self.assertEqual(self.path.read_bytes(), before)
        dispatch(h, self.pane, event="Stop", session="wrong-session")
        dispatch(h, self.pane, event="Stop", turn="old-turn")
        self.assertEqual(self.path.read_bytes(), before)
        # Even stolen valid runtime data cannot attribute a sibling process to
        # the registered CLI: this test runner is outside its ancestry.
        result = subprocess.run(shlex.split(self.first["command"]),
                                input=json.dumps(dict(hook_event_name="Stop", session_id="fixture-session", turn_id="one")),
                                env=h.env | {activity.CONTEXT_ENV: self.first["runtime"]},
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
        dispatch(h, self.pane, event="Stop")
        dispatch(h, self.pane, turn="two")
        dispatch(h, self.pane, event="Stop", turn="one")
        self.assertEqual(activity.private_record(self.path)["state"], "working")
        dispatch(h, self.pane, event="SessionEnd", turn=None)
        self.assertTrue(activity.private_record(self.path)["ended"])
        self.assertEqual(activity.private_record(self.path)["state"], "idle")
        ended = self.path.read_bytes()
        dispatch(h, self.pane, turn="three")
        self.assertEqual(self.path.read_bytes(), ended)

    def test_missing_failed_untrusted_or_busy_hook_leaves_cli_usable_and_unlabelled(self):
        h = self.h
        self.assertEqual(activity.private_record(self.path)["state"], "idle")
        for raw in ["", "{}", "bad-json"]:
            result = dispatch(h, self.pane, runtime=raw)
            self.assertEqual(result["code"], 0)
            self.assertEqual(activity.private_record(self.path)["state"], "idle")
        with activity.lock(self.runtime["state"], h.socket):
            start = time.monotonic()
            result = dispatch(h, self.pane)
            self.assertLess(time.monotonic() - start, 2)
            self.assertEqual(result["code"], 0)
            self.assertIn("evidence unavailable", result["stderr"])
        self.assertEqual(h.tm("display-message", "-p", "-t", self.pane, "#{pane_dead}").strip(), "0")
        # Bad cache permissions refuse an update; they never change CLI policy.
        self.path.chmod(0o644)
        result = dispatch(h, self.pane)
        self.assertEqual(result["code"], 0)
        self.assertEqual(json.loads(self.path.read_text())["state"], "idle")

    def test_child_exit_clears_working_evidence_and_late_events_cannot_revive_it(self):
        h = self.h
        dispatch(h, self.pane)
        self.assertEqual(activity.private_record(self.path)["state"], "working")
        request = h.root / "synthetic-events" / (self.pane[1:] + ".request")
        request.write_text(json.dumps({"exit": True}))
        wait_for(lambda: activity.private_record(self.path).get("ended"))
        self.assertEqual(activity.private_record(self.path)["state"], "idle")
        # Record and marker are separate writes; wait for the finalizer, rather
        # than treating its safe intermediate ended record as completed cleanup.
        wait_for(lambda: h.tm("show-options", "-pqv", "-t", self.pane,
                              "@dotfiles-agent-evidence").strip() == "")
        marker = h.tm("show-options", "-pqv", "-t", self.pane, "@dotfiles-agent-evidence").strip()
        self.assertEqual(marker, "")
        before = self.path.read_bytes()
        result = subprocess.run(shlex.split(self.first["command"]), input=json.dumps({
            "hook_event_name": "UserPromptSubmit", "session_id": "fixture-session", "turn_id": "late"}),
            env=h.env | {activity.CONTEXT_ENV: self.first["runtime"]},
            capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.path.read_bytes(), before)
