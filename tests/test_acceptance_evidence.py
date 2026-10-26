"""Prevent the missing-tool-call fixture from masquerading as a hook failure."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid

from acceptance_evidence import APPROVAL_COMMAND, APPROVAL_RULE, owned_turn_metadata, require_approval_attempt


class AcceptanceEvidenceTests(unittest.TestCase):
    def fixture(self, *, call=False, cwd=None):
        temp = tempfile.TemporaryDirectory(prefix="df-evidence-", dir="/private/tmp")
        self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve()
        identity, turn = str(uuid.uuid4()), str(uuid.uuid4())
        folder = root / "codex/sessions"
        folder.mkdir(parents=True)
        rows = [dict(type="session_meta", payload=dict(id=identity, cwd=cwd or str(root / "project"))),
                dict(type="event_msg", payload=dict(type="task_started", turn_id=turn)),
                dict(type="turn_context", payload=dict(turn_id=turn, approval_policy="on-request", sandbox_policy=dict(type="workspace-write"))),
                dict(type="response_item", payload=dict(type="message", content="PRIVATE MESSAGE MUST NOT ESCAPE"))]
        if call:
            rows.append(dict(type="response_item", payload=dict(type="function_call", name="exec", arguments="PRIVATE ARGUMENTS MUST NOT ESCAPE")))
        rows.append(dict(type="event_msg", payload=dict(type="task_complete", last_agent_message="PRIVATE RESPONSE MUST NOT ESCAPE")))
        (folder / (identity + ".jsonl")).write_text("".join(json.dumps(row) + "\n" for row in rows))
        return root, identity, turn

    def test_actual_no_tool_failure_is_classified_as_fixture_failure(self):
        root, identity, turn = self.fixture()
        result = owned_turn_metadata(root, identity)
        with self.assertRaisesRegex(AssertionError, "without a tool call"):
            require_approval_attempt(result, turn)
        self.assertNotIn("PRIVATE", json.dumps(result))

    def test_tool_attempt_is_not_mistaken_for_proof_of_permission_delivery(self):
        root, identity, turn = self.fixture(call=True)
        result = owned_turn_metadata(root, identity)
        require_approval_attempt(result, turn)
        self.assertEqual(result["turns"][turn]["tool_calls"], ["exec"])
        self.assertNotIn("PRIVATE", json.dumps(result))
        self.assertNotIn("approval_pass", result)

    def test_reader_refuses_an_unrelated_project(self):
        root, identity, _ = self.fixture(cwd="/unrelated/project")
        with self.assertRaises(AssertionError):
            owned_turn_metadata(root, identity)

    @unittest.skipUnless(os.environ.get("DOTFILES_INTEGRATION") == "1", "Native policy parser, private profile only")
    def test_native_prompt_rule_requires_approval_only_for_harmless_probe(self):
        with tempfile.TemporaryDirectory(prefix="df-rule-", dir="/private/tmp") as directory:
            root = Path(directory)
            (root / "codex").mkdir(mode=0o700)
            path = root / "approval.rules"
            path.write_text(APPROVAL_RULE)
            native = "/opt/homebrew/Caskroom/codex/0.164.0/bin/codex"
            env = {"HOME": str(root), "CODEX_HOME": str(root / "codex"), "PATH": "/usr/bin:/bin", "LC_ALL": "en_US.UTF-8"}
            def check(command):
                return json.loads(subprocess.check_output([native, "execpolicy", "check", "--rules", str(path), "--", *command], env=env, text=True))
            self.assertEqual(check(APPROVAL_COMMAND)["decision"], "prompt")
            self.assertFalse(check(["/bin/sleep", "3"])["matchedRules"])
