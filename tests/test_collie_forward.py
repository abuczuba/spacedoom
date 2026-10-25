"""Isolated candidate checks; native hook delivery and phone use remain live tests."""
import contextlib
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


activity = load("candidate_activity", "configs/cdev/activity.py")
SID = "019a1234-1111-7222-8333-123456789abc"


class ForwardingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="collie-forward-", dir="/private/tmp")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.config = self.root / "collie.json"
        self.record = dict(socket="/private/tmp/owned.sock", pane="%1", boot="100:200",
                           pid=300, started="launcher-birth", child=301, child_started="client-birth",
                           remote_session=SID, state="idle", session=SID, turn=None,
                           ended=False, token="private-launch-token", sequence=0, stamp=0)
        self.binding = {key: self.record[key] for key in
                        ("socket", "pane", "boot", "pid", "started", "child", "child_started", "remote_session")}
        self.policy = dict(enabled=True, binding=self.binding, binary="/private/tmp/export/bin/collie",
                           profile=str(self.root / "profile"))
        self.payload = dict(hook_event_name="UserPromptSubmit", session_id=SID, turn_id="turn-one",
                            prompt="DO-NOT-FORWARD", transcript_path="/DO-NOT-FORWARD",
                            tool_input={"command": "DO-NOT-FORWARD"})
        self.write_policy()
        self.config_patch = patch.object(activity, "COLLIE_CONFIG", self.config)
        self.config_patch.start()
        self.addCleanup(self.config_patch.stop)

    def write_policy(self):
        self.config.write_text(json.dumps(self.policy))
        self.config.chmod(0o600)

    def test_only_metadata_and_an_isolated_environment_reach_the_existing_emitter(self):
        original_record, original_payload = copy.deepcopy(self.record), copy.deepcopy(self.payload)
        with patch.dict(os.environ, {"HOME": "/production", "CODEX_HOME": "/production/.codex",
                                     "OPENAI_API_KEY": "DO-NOT-FORWARD", "COLLIE_VAPID_PRIVATE": "DO-NOT-FORWARD"}), \
                patch.object(activity.subprocess, "run") as run:
            activity.collie_event(self.record, self.payload)
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0], [self.policy["binary"], "beacon", "emit", "codex-native"])
        kwargs = run.call_args.kwargs
        self.assertEqual(json.loads(kwargs["input"]),
                         dict(hook_event_name="UserPromptSubmit", session_id=SID, turn_id="turn-one"))
        self.assertNotIn("DO-NOT-FORWARD", json.dumps(kwargs["env"]) + kwargs["input"])
        self.assertNotIn("private-launch-token", kwargs["input"])
        self.assertEqual(kwargs["env"]["HOME"], str(self.root / "profile/home"))
        self.assertEqual(kwargs["env"]["CODEX_HOME"], str(self.root / "profile/codex"))
        self.assertEqual(kwargs["env"]["COLLIE_MUX_ENDPOINT_TMUX"], self.binding["socket"])
        self.assertNotIn("TMUX_PANE", kwargs["env"])
        self.assertEqual(kwargs["timeout"], .5)
        self.assertEqual(kwargs["stdout"], subprocess.DEVNULL)
        self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
        self.assertEqual(self.record, original_record)
        self.assertEqual(self.payload, original_payload)

    def test_every_frozen_identity_field_is_required(self):
        for field in self.binding:
            with self.subTest(field=field), patch.object(activity.subprocess, "run") as run:
                changed = self.record | {field: "different-generation"}
                activity.collie_event(changed, self.payload)
                run.assert_not_called()
        with patch.object(activity.subprocess, "run") as run:
            activity.collie_event(self.record, self.payload | {"session_id": "another-session"})
            run.assert_not_called()

    def test_auxiliary_unknown_and_pretool_events_are_absent(self):
        for key in ("agent_id", "subagent_id", "parent_session_id"):
            with patch.object(activity.subprocess, "run") as run:
                activity.collie_event(self.record, self.payload | {key: "auxiliary"})
                run.assert_not_called()
        for event in ("SubagentStop", "PreToolUse", "Notification", "Interrupt"):
            with patch.object(activity.subprocess, "run") as run:
                activity.collie_event(self.record, self.payload | {"hook_event_name": event})
                run.assert_not_called()

    def test_missing_disabled_loose_symlink_and_invalid_config_fail_closed(self):
        for change in ("disabled", "loose", "missing", "symlink", "invalid"):
            with self.subTest(change=change), patch.object(activity.subprocess, "run") as run:
                self.config.unlink(missing_ok=True)
                self.policy["enabled"] = change != "disabled"
                if change != "missing":
                    self.write_policy()
                if change == "loose":
                    self.config.chmod(0o644)
                if change == "invalid":
                    self.config.write_text("[]")
                if change == "symlink":
                    target = self.root / "other.json"
                    target.write_text(self.config.read_text())
                    self.config.unlink()
                    self.config.symlink_to(target)
                activity.collie_event(self.record, self.payload)
                run.assert_not_called()

    def test_failed_emission_preserves_the_existing_dashboard_update(self):
        context = dict(state=str(self.root), socket=self.record["socket"], pane="%1", token=self.record["token"])
        def read(path):
            return self.policy if path == self.config else self.record
        with patch.object(activity, "lock", return_value=contextlib.nullcontext()), \
                patch.object(activity, "private_record", side_effect=read), \
                patch.object(activity, "verified_origin", return_value=True), \
                patch.object(activity, "tmux", return_value="100:200|300"), \
                patch.object(activity.subprocess, "run", side_effect=subprocess.TimeoutExpired("owned-emitter", .5)), \
                patch.object(activity, "save") as save, patch.object(activity, "mark") as mark, \
                patch.object(activity, "remember_remote"):
            activity.event(context, self.payload)
        self.assertEqual(save.call_args.args[1]["state"], "working")
        mark.assert_called_once()

    def test_origin_failure_cannot_invoke_collie(self):
        context = dict(state=str(self.root), socket=self.record["socket"], pane="%1", token=self.record["token"])
        with patch.object(activity, "lock", return_value=contextlib.nullcontext()), \
                patch.object(activity, "private_record", return_value=self.record), \
                patch.object(activity, "verified_origin", return_value=False), \
                patch.object(activity, "collie_event") as forward:
            activity.event(context, self.payload)
        forward.assert_not_called()



if __name__ == "__main__":
    unittest.main()
