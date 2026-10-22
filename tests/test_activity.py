from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest

from validation import private_tmux

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
                self.assertIn("%42", value)
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


@unittest.skipUnless(INTEGRATION, "Use --integration for private hook dispatch")
class ActivityIntegration(unittest.TestCase):
    def test_pinned_hook_survives_wrong_environment_and_old_nonce_cannot_clobber(self):
        with tempfile.TemporaryDirectory(prefix="df-events-") as directory, private_tmux() as tm:
            root = Path(directory).resolve()
            socket = tm("display-message", "-p", "#{socket_path}").strip()
            pane = tm("display-message", "-p", "#{pane_id}").strip()
            boot = tm("display-message", "-p", "#{start_time}:#{pid}").strip()
            pid = int(tm("display-message", "-p", "#{pane_pid}"))
            path = activity.record_path(root, socket, pane)
            activity.save(path, dict(socket=socket, pane=pane, boot=boot, pid=pid, token="new-launch",
                                     session=None, turn=None, state="idle", ended=False, sequence=0))
            tm("set-option", "-p", "@dotfiles-agent-evidence", "new-launch:0")
            env = os.environ.copy() | {"TMUX": "/invalid/not-the-socket,0,0", "TMUX_PANE": "%9999"}
            payload = dict(hook_event_name="UserPromptSubmit", session_id="ordinary-cdev", turn_id="one")
            command = ["python3", "-B", str(REPO / "configs/cdev/activity.py"), "event", "--state", str(root),
                       "--socket", socket, "--pane", pane, "--token", "new-launch"]
            result = subprocess.run(command, input=json.dumps(payload), text=True, env=env, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(path.read_text())["state"], "working")
            marker = tm("show-options", "-pqv", "@dotfiles-agent-evidence")
            activity.event(root, socket, pane, "old-launch", payload | {"hook_event_name": "Stop"})
            activity.mark(socket, pane, "old-launch", "")
            self.assertEqual(tm("show-options", "-pqv", "@dotfiles-agent-evidence"), marker)
            self.assertEqual(json.loads(path.read_text())["state"], "working")
            with activity.lock(root, socket):
                start = time.monotonic()
                busy = subprocess.run(command, input=json.dumps(payload), text=True, env=env, capture_output=True, timeout=3)
                self.assertEqual(busy.returncode, 0, busy.stderr)
                self.assertLess(time.monotonic() - start, 2)
                self.assertIn("evidence unavailable", busy.stderr)
            path.write_text("[]")
            result = subprocess.run(command, input=json.dumps(payload), text=True, env=env, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run(command, input="[]", text=True, env=env, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
