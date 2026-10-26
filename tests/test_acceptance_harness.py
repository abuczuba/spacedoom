"""Real private tmux/process environment regressions; no native Codex or credentials."""
import hashlib
import json
import os
import subprocess
import unittest
import uuid
import time
from unittest.mock import patch

from acceptance_harness import AcceptanceHarness, UTF8_LOCALE, verify_utf8

INTEGRATION = os.environ.get("DOTFILES_INTEGRATION") == "1"


@unittest.skipUnless(INTEGRATION, "Use --integration for isolated acceptance-harness checks")
class AcceptanceEnvironmentTests(unittest.TestCase):
    def harness(self, **kwargs):
        harness = AcceptanceHarness(**kwargs)
        self.addCleanup(harness.close)
        return harness

    def test_old_control_only_environment_is_rejected_before_launcher_or_pins(self):
        h = self.harness(propagate=False)
        h.open()
        h.wait(lambda: h.proofs("launcher"))
        self.assertTrue(h.proofs("control")[0]["ok"])
        self.assertTrue(h.proofs("plan")[0]["ok"])
        launcher = h.proofs("launcher")[0]
        self.assertFalse(launcher["ok"])
        self.assertIn("XDG_STATE_HOME", launcher["wrong_keys"])
        with self.assertRaisesRegex(AssertionError, "unverified"):
            h.allow_launcher()
        self.assertFalse(h.proofs("agent"))
        self.assertFalse((h.root / "state/cdev/pins.json").exists())
        self.assertFalse((h.server_home / ".local/state/cdev/pins.json").exists())

    def test_environment_on_the_tmux_client_does_not_reach_a_new_pane(self):
        h = self.harness()
        result = subprocess.run([h.tmux, "-N", "-S", str(h.socket), "new-window", "-d", "-n", "old-client-env",
                                 "/usr/bin/python3", "-B", str(h.root / "probe.py"), "editor"],
                                env=h.env, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0)
        row = h.wait(lambda: h.proofs("editor"))[0]
        self.assertFalse(row["ok"])
        self.assertIn("XDG_STATE_HOME", row["wrong_keys"])
        self.assertEqual(h.server_markers(), h.server_before)
        self.assertFalse((h.root / "state/cdev/pins.json").exists())

    def test_explicit_environment_reaches_every_actual_descendant_before_state(self):
        h = self.harness()
        payloads = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in (h.root / "payload").rglob("*") if p.is_file()}
        h.open()
        for role in ("control", "plan", "editor", "launcher"):
            h.wait(lambda role=role: h.proofs(role))
        self.assertFalse((h.root / "state/cdev").exists())
        self.assertFalse(h.proofs("agent"))
        h.allow_launcher()
        h.wait(lambda: h.proofs("hook"))
        h.start_backend_probe()
        required = {"control", "plan", "editor", "launcher", "agent", "hook", "backend"}
        self.assertTrue(required.issubset({row["role"] for row in h.proofs()}))
        for row in h.proofs():
            self.assertTrue(row["ok"], row)
            self.assertEqual(row["codex_home"], h.env["CODEX_HOME"])
            self.assertEqual(row["pins"], str(h.root / "state/cdev/pins.json"))
            self.assertEqual(row["auth_store"], "file")
            self.assertEqual(row["auth_file"], str(h.root / "codex/auth.json"))
            self.assertEqual(row["socket"], str(h.socket))
        launcher, agent, hook = [h.proofs(role)[0] for role in ("launcher", "agent", "hook")]
        self.assertEqual(agent["parent"], launcher["pid"])
        self.assertEqual(hook["parent"], agent["pid"])
        self.assertEqual(launcher["pane"], agent["pane"])
        self.assertEqual(agent["pane"], hook["pane"])
        self.assertEqual(launcher["pid"], launcher["pane_root"])
        self.assertNotEqual(h.proofs("editor")[0]["pane"], agent["pane"])
        self.assertEqual(h.server_markers(), h.server_before)
        self.assertNotEqual(h.server_before["HOME"], h.env["HOME"])
        self.assertIsNone(h.server_before["XDG_STATE_HOME"])
        self.assertFalse((h.root / "state/cdev/pins.json").exists())
        # Only now create synthetic metadata and exercise the UNCHANGED pin writer.
        identity = str(uuid.uuid4())
        sessions = h.root / "codex/sessions"
        sessions.mkdir()
        (sessions / (identity + ".jsonl")).write_text(json.dumps({
            "type": "session_meta", "payload": {"id": identity, "cwd": str(h.project), "source": "cli"}}) + "\n")
        result = h.run_probe("pin", identity)
        self.assertEqual(result.returncode, 0, result.stderr)
        path = h.root / "state/cdev/pins.json"
        self.assertEqual(json.loads(path.read_text())["pins"], {str(h.project): identity})
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        result = h.run_probe("paths", identity)
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in [h.root / "runtime/registry" / (identity + ".json"),
                     h.root / "cache/fixture-cache", h.root / "tmp/fixture-temporary",
                     h.root / "codex/app-server-control/app-server-control.sock"]:
            self.assertTrue(path.exists())
            self.assertTrue(path.resolve().is_relative_to(h.root))
        self.assertFalse((h.root / "codex/auth.json").exists())
        self.assertEqual(payloads, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in payloads})

    def test_environment_is_an_allowlist_and_wrappers_refuse_another_socket(self):
        h = self.harness()
        self.assertFalse(set(h.env) & {"OPENAI_API_KEY", "CODEX_ACCESS_TOKEN", "CDEV_ACTIVITY_CONTEXT", "TMUX", "TMUX_PANE"})
        for socket_option in ("-S", "-L"):
            result = h.run_probe("tmux", socket_option, str(h.root / "wrong.sock"), "display-message", "-p", "x")
            self.assertNotEqual(result.returncode, 0)
        self.assertFalse((h.root / "wrong.sock").exists())

    def test_fixing_only_new_window_still_rejects_the_nested_agent_pane(self):
        h = self.harness()
        h.spec["propagate_commands"] = ["new-window"]
        h.config.write_text(json.dumps(h.spec))
        h.open()
        h.wait(lambda: h.proofs("launcher"))
        self.assertTrue(h.proofs("editor")[0]["ok"])
        self.assertFalse(h.proofs("launcher")[0]["ok"])
        with self.assertRaisesRegex(AssertionError, "unverified launcher"):
            h.allow_launcher()
        self.assertFalse(h.proofs("agent"))
        self.assertFalse((h.root / "state/cdev/pins.json").exists())

    def test_concurrent_fixtures_keep_identical_pane_numbers_in_separate_namespaces(self):
        fixtures = [self.harness(), self.harness()]
        for h in fixtures:
            h.open()
        for h in fixtures:
            h.wait(lambda h=h: h.proofs("launcher") and h.proofs("editor"))
            h.allow_launcher()
        for h in fixtures:
            h.wait(lambda h=h: h.proofs("hook"))
            records = list((h.root / "state/dotfiles-dashboard").glob("*.json"))
            self.assertEqual(len(records), 1)
            record = json.loads(records[0].read_text())
            self.assertEqual(record["socket"], str(h.socket))
            self.assertEqual(record["pid"], h.proofs("launcher")[0]["pid"])
        first, second = fixtures
        self.assertEqual(first.proofs("agent")[0]["pane"], second.proofs("agent")[0]["pane"])
        for key in ("HOME", "CODEX_HOME", "XDG_STATE_HOME", "XDG_RUNTIME_DIR"):
            self.assertNotEqual(first.env[key], second.env[key])
        self.assertNotEqual(first.socket, second.socket)

    def test_private_hook_probe_allows_stale_backend_pane_markers(self):
        h = self.harness()
        shims = h.root / "codex/executable-shims"
        shims.mkdir()
        env = h.env | {"TMUX": str(h.socket) + ",0,0", "TMUX_PANE": "%9999",
                       "PATH": str(shims) + ":" + h.env["PATH"]}
        result = h.run_probe("event", "event", env=env, input="{}")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(h.proofs("hook")[0]["ok"])
        # Invalid event input remains unlabelled; the fixture never fabricates
        # a session/pane match or bypasses the source identity checks.
        self.assertFalse((h.root / "state/dotfiles-dashboard").exists())

    def test_native_profile_sections_preserve_the_file_credential_guard(self):
        h = self.harness()
        config = h.root / "codex/config.toml"
        config.write_text('cli_auth_credentials_store = "file"\n[features]\nhooks = true\n'
                          '[projects."' + str(h.project) + '"]\ntrust_level = "trusted"\n')
        self.assertEqual(h.run_probe("event", "event", input="{}").returncode, 0)
        config.write_text(config.read_text().replace('store = "file"', 'store = "keyring"'))
        self.assertNotEqual(h.run_probe("event", "event", input="{}").returncode, 0)

    def synthetic_state(self, h, state, sequence):
        """Controlled cache input for offline rendering tests, never native proof."""
        path = next((h.root / "state/dotfiles-dashboard").glob("*.json"))
        row = json.loads(path.read_text())
        row.update(session="00000000-0000-0000-0000-000000000001", turn="synthetic-turn",
                   state=state, stamp=int(time.time()), sequence=sequence)
        temporary = path.with_suffix(".pending")
        temporary.write_text(json.dumps(row)); temporary.chmod(0o600); temporary.replace(path)
        h.tm("set-option", "-p", "-t", row["pane"], "@dotfiles-agent-evidence", row["token"] + ":" + str(sequence))
        return row

    def callback_fixture(self, **kwargs):
        h = self.harness(**kwargs)
        h.install_renderer_callback()
        h.open()
        h.wait(lambda: h.proofs("launcher") and h.proofs("editor"))
        h.allow_launcher()
        h.wait(lambda: h.proofs("hook"))
        return h

    def test_real_background_callback_receives_utf8_metadata_and_renders_all_states(self):
        h = self.callback_fixture()
        self.assertEqual(h.server_env["LC_ALL"], UTF8_LOCALE)
        self.assertEqual(h.env["LANG"], UTF8_LOCALE)
        for sequence, state in enumerate(("working", "done", "waiting", "idle"), 1):
            row = self.synthetic_state(h, state, sequence)
            window = h.tm("display-message", "-p", "-t", row["pane"], "#{window_id}")
            expected = "" if state == "idle" else state
            h.wait(lambda: h.tm("show-options", "-wqv", "-t", window, "@dotfiles-agent-state") == expected)
            frame = h.tm("display-message", "-p", "-t", row["pane"], "#{E:window-status-current-format}")
            if state == "working":
                time.sleep(1.1)
                self.assertNotEqual(frame, h.tm("display-message", "-p", "-t", row["pane"], "#{E:window-status-current-format}"))
            elif state == "done":
                self.assertIn("●", frame)
            elif state == "waiting":
                self.assertIn("!", frame); self.assertIn("bg=#a50021", frame)
        audits = h.wait(lambda: h.callback_audits())
        self.assertTrue(all(row["ok"] for row in audits))
        self.assertTrue(all(row["locale"] == row["lang"] == UTF8_LOCALE for row in audits))
        self.assertTrue(all(row["codeset"].replace("-", "").lower() == "utf8" for row in audits))
        self.assertTrue(any(item["tabs"] > 0 for row in audits for item in row["metadata"]))
        self.assertTrue(all(row["home"] == str(h.server_home) for row in audits))

    def test_old_c_locale_breaks_the_actual_background_callback(self):
        # Deliberately bypass only the new locale preflight for the old-fixture
        # reproduction; no native Codex or credential access occurs.
        with patch("acceptance_harness.verify_utf8"):
            h = self.callback_fixture(locale_name="C")
        state = self.synthetic_state(h, "working", 1)
        audits = h.wait(lambda: [row for row in h.callback_audits() if not row["ok"]])
        row = audits[-1]
        self.assertEqual(row["locale"], "C")
        self.assertEqual(row["error_type"], "ValueError")
        self.assertIn("expected 4, got 1", row["error"])
        tables = [item for item in row["metadata"] if item["command"] == "list-windows"]
        self.assertTrue(tables); self.assertEqual(tables[-1]["tabs"], 0)
        self.assertIn("___", tables[-1]["text"])
        window = h.tm("display-message", "-p", "-t", state["pane"], "#{window_id}")
        self.assertEqual(h.tm("show-options", "-wqv", "-t", window, "@dotfiles-agent-state"), "")

    def test_non_utf8_locale_is_rejected_before_server_start(self):
        with self.assertRaisesRegex(RuntimeError, "verified UTF-8"):
            verify_utf8({"PATH": "/usr/bin:/bin", "LC_ALL": "C", "LANG": "C"})

    def test_utf8_cdev_reuse_keeps_the_existing_nested_agent(self):
        h = self.callback_fixture()
        row = self.synthetic_state(h, "done", 1)
        window = h.tm("display-message", "-p", "-t", row["pane"], "#{window_id}")
        before = h.tm("list-panes", "-t", window, "-F", "#{pane_id}|#{pane_pid}")
        (h.root / "open-status").unlink(missing_ok=True)
        h.open()
        h.wait(lambda: (h.root / "open-status").exists())
        self.assertEqual((h.root / "open-status").read_text().strip(), "0")
        self.assertEqual(h.tm("list-panes", "-t", window, "-F", "#{pane_id}|#{pane_pid}"), before)
        self.assertEqual(len(h.proofs("agent")), 1)
        self.assertEqual(h.server_markers(), h.server_before)

    def test_actual_callback_keeps_rendering_without_a_phone_transport(self):
        h = self.callback_fixture()
        for sequence, state in enumerate(("working", "done", "waiting"), 1):
            row = self.synthetic_state(h, state, sequence)
            window = h.tm("display-message", "-p", "-t", row["pane"], "#{window_id}")
            h.wait(lambda: h.tm("show-options", "-wqv", "-t", window, "@dotfiles-agent-state") == state)
        self.assertTrue(all(row["ok"] for row in h.callback_audits()))
        self.assertFalse((h.root / "state/dotfiles-pager").exists())


if __name__ == "__main__":
    unittest.main()
