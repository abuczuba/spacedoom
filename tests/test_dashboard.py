from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch
from urllib.parse import quote

from validation import private_tmux

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dashboard", REPO / "configs/tmux/agent-dashboard.py")
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)
INTEGRATION = os.environ.get("DOTFILES_INTEGRATION") == "1"


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.pane = dict(pane="%2", pid="123", dead="0", command="codex", raw="🤖")
        self.record = dict(pane_key=dict(backend="tmux", instance="/tmp/private", pane_id="%2"),
                           boot_id="100:222", pane_pid=123, agent_session_id="synthetic-session",
                           status="working", status_ts=1000)

    def test_evidence_identity_expiry_and_unknowns_fail_closed(self):
        def check(record=None, pane=None, now=1001):
            return dashboard.observable(record or self.record, pane or self.pane, "/tmp/private", "100:222", now)
        self.assertEqual(check(), "working")
        for change in [dict(boot_id="old:222"), dict(pane_pid=456), dict(status_ts=0),
                       dict(status_ts=2000), dict(agent_session_id=None), dict(status="unknown"),
                       dict(pane_key=dict(backend="tmux", instance="/tmp/other", pane_id="%2"))]:
            self.assertIsNone(check(self.record | change))
        for change in [dict(raw="✅"), dict(dead="1"), dict(command="fish")]:
            self.assertIsNone(check(pane=self.pane | change))
        self.assertIsNone(check(now=1900))

    def test_preview_palette_title_escaping_and_one_second_clock(self):
        for state in ["working", "done", "waiting", "idle"]:
            output = dashboard.title_format("a#{evil}\n'b", state)
            self.assertIn("##", output)
            self.assertNotIn("\n", output)
        self.assertIn("#a50021", dashboard.title_format("title", "waiting"))
        self.assertIn("●", dashboard.title_format("title", "done"))
        output = dashboard.title_format("title", "working")
        self.assertIn("t/d:start_time", output)
        self.assertNotIn("#{A", output)
        self.assertNotIn("#(", output)


@unittest.skipUnless(INTEGRATION, "Use --integration for private tmux/workmux tests")
class DashboardIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="dotfiles-dashboard-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.server = private_tmux()
        self.tm = self.server.__enter__()
        self.addCleanup(lambda: self.server.__exit__(None, None, None))
        self.socket = self.tm("display-message", "-p", "#{socket_path}").strip()
        self.ghostty = self.root / "home/.config/ghostty/config.ghostty"
        self.ghostty.parent.mkdir(parents=True)
        self.ghostty.write_bytes((REPO / "configs/ghostty/config.ghostty").read_bytes())
        self.tm("set-environment", "-g", "HOME", str(self.root / "home"))
        self.view = dashboard.Dashboard(self.socket, self.root / "state", self.ghostty)
        self.tm("set-option", "-g", "@tmux-dotbar-fg", "#e0def4")
        self.tm("set-option", "-g", "@tmux-dotbar-fg-current", "#f6c177")
        self.tm("set-option", "-g", "@tmux-dotbar-bg", "#1f1d2e")
        self.tm("set-option", "-g", "window-status-format", dashboard.TITLE_SLOT)
        self.tm("set-option", "-g", "window-status-current-format", dashboard.TITLE_SLOT)

    def agent(self, name, state="working"):
        # exec -a makes the private process a Codex stand-in without invoking
        # Codex, authentication, conversation history, hooks or the network.
        window = self.tm("new-window", "-d", "-P", "-F", "#{window_id}", "-n", name,
                         "/bin/sleep 120").strip()
        pane = self.tm("display-message", "-p", "-t", window, "#{pane_id}").strip()
        pid = int(self.tm("display-message", "-p", "-t", pane, "#{pane_pid}"))
        self.tm("set-option", "-p", "-t", pane, "@workmux_pane_status", dashboard.STATES[state])
        self.tm("set-option", "-w", "-t", window, "@workmux_status", dashboard.STATES[state])
        self.record(pane, pid, state)
        return window, pane

    def record(self, pane, pid, state):
        folder = self.root / "state/workmux/agents"
        folder.mkdir(parents=True, exist_ok=True)
        name = "tmux__" + quote(self.socket, safe="") + "__" + quote(pane, safe="") + ".json"
        path = folder / name
        data = dict(pane_key=dict(backend="tmux", instance=self.socket, pane_id=pane),
                    pane_pid=pid, boot_id=self.tm("display-message", "-p", "#{start_time}:#{pid}").strip(),
                    agent_session_id="synthetic-" + pane, status=state, status_ts=int(time.time()))
        path.write_text(json.dumps(data))
        return path

    def test_native_monitor_disconnected_clients_and_idle_fast_path(self):
        session = self.tm("display-message", "-p", "#{session_id}").strip()
        self.tm("set-hook", "-t", session + ":", "-B", "@test:%*:#{@workmux_pane_status}",
                "set-option -g @observed yes")
        # tmux's monitor establishes its initial comparison value on its first
        # tick; installation explicitly refreshes once for that initial state.
        time.sleep(1.2)
        self.tm("set-option", "-p", "@workmux_pane_status", "🤖")
        deadline = time.monotonic() + 4
        while time.monotonic() < deadline:
            if self.tm("show-options", "-gqv", "@observed").strip() == "yes":
                break
            time.sleep(0.1)
        self.assertEqual(self.tm("show-options", "-gqv", "@observed").strip(), "yes")
        self.tm("set-option", "-p", "-u", "@workmux_pane_status")
        self.assertEqual(self.tm("display-message", "-p", dashboard.SIGNATURE).strip(), "")
        self.assertNotIn("#(", dashboard.TITLE_SLOT)

    def test_disable_refuses_binding_drift_and_blocks_late_refreshes(self):
        window, pane = self.agent("agent-to-disable", "working")
        self.view.install()
        self.tm("bind-key", "n", "display-message", "user-custom-binding")
        with self.assertRaises(ValueError):
            self.view.disable()
        self.tm("bind-key", "n", "run-shell", "python3 agent-dashboard.py attention")
        self.view.disable()
        self.view.refresh()
        self.assertEqual(self.tm("show-options", "-wqv", "-t", window, "@dotfiles-agent").strip(), "")
        self.assertEqual(self.tm("show-options", "-gqv", "@dotfiles-dashboard-enabled").strip(), "off")
        self.assertNotIn(dashboard.MONITOR, self.tm("show-hooks", "-B", "-t", "$0:"))
        self.assertIn("new-window", self.tm("list-keys", "-T", "prefix", "n"))
        self.assertEqual(self.tm("show-options", "-gqv", "window-status-format").rstrip("\n"), " #W ")

    def test_ghostty_new_window_forwarding_is_preserved_and_attention_is_gated(self):
        candidate = (REPO / "configs/ghostty/config.ghostty").read_text()
        legacy = subprocess.check_output(["git", "show", "ec518f0c6246a8e24b97627aecb74aad7b2d5f16:configs/ghostty/config.ghostty"],
                                         cwd=REPO, text=True)
        self.ghostty.write_text(legacy)
        with self.assertRaises(ValueError):
            self.view.preflight()
        self.view.preflight(require_navigation=False)
        self.view.install()
        original_new_window = self.view.prefix_bindings()["n"]
        self.assertEqual(original_new_window, ["new-window", "-c", "#{pane_current_path}"])
        self.assertEqual(self.tm("show-options", "-gqv", "@dotfiles-attention-installed").strip(), "off")
        self.ghostty.write_text(candidate)
        self.view.watch()  # A new session/file change cannot silently rebind n.
        self.assertEqual(self.view.prefix_bindings()["n"], original_new_window)
        self.view.install()  # Explicit candidate reload after companion adoption.
        self.assertEqual(self.view.prefix_bindings()["c"], original_new_window)
        self.assertIn("attention", " ".join(self.view.prefix_bindings()["n"]))
        self.assertEqual(self.tm("show-options", "-gqv", "@dotfiles-attention-installed").strip(), "on")
        self.assertIn(r"super+shift+n=text:\x06\x63", candidate)
        # Every other Command forwarding sequence remains byte-for-byte intact.
        before = [line for line in legacy.splitlines() if line.startswith("keybind") and "super+shift+n=" not in line]
        after = [line for line in candidate.splitlines() if line.startswith("keybind") and "super+shift+n=" not in line]
        self.assertEqual(before, after)
        self.assertEqual(bytes(r"\x06\x63", "ascii").decode("unicode_escape"), "\x06c")

    def test_title_and_hook_conflicts_are_refused_without_overwrite(self):
        self.tm("set-option", "-w", "window-status-format", "custom-title")
        with self.assertRaises(ValueError):
            self.view.install()
        self.assertEqual(self.tm("show-options", "-wqv", "window-status-format").strip(), "custom-title")
        self.tm("set-option", "-wu", "window-status-format")
        self.tm("set-hook", "-g", "session-created[882]", "display-message existing")
        with self.assertRaises(ValueError):
            self.view.install()
        self.assertIn("existing", self.tm("show-hooks", "-g", "session-created"))

    def test_two_attention_panes_and_pane_movement_use_stable_ids(self):
        window, ap = self.agent("two-agents", "waiting")
        bp = self.tm("split-window", "-d", "-h", "-P", "-F", "#{pane_id}", "-t", window, "/bin/sleep 120").strip()
        self.tm("set-option", "-p", "-t", bp, "@workmux_pane_status", "✅")
        self.record(bp, int(self.tm("display-message", "-p", "-t", bp, "#{pane_pid}")), "done")
        original = dashboard.observable
        def fixture(record, pane, *args):
            return original(record, pane | {"command": "codex"}, *args)
        session = self.tm("display-message", "-p", "#{session_id}").strip()
        with patch.object(dashboard, "observable", side_effect=fixture):
            self.view.install()
            self.tm("select-window", "-t", window)
            self.tm("select-pane", "-t", ap)
            self.view.attention(session)
            self.assertEqual(self.tm("display-message", "-p", "#{pane_id}").strip(), bp)
            self.view.attention(session)
            self.assertEqual(self.tm("display-message", "-p", "#{pane_id}").strip(), ap)
            self.tm("join-pane", "-d", "-s", ap, "-t", "@0")
            signature = self.tm("display-message", "-p", dashboard.SIGNATURE)
            self.assertIn(ap, signature)
            self.view.refresh()
            self.assertIn("!", self.tm("show-options", "-wqv", "-t", "@0", "@dotfiles-agent"))

    def test_only_documented_window_bindings_change_and_existing_navigation_survives(self):
        navigation = self.root / "navigation.conf"
        navigation.write_text((REPO / "configs/tmux/czuba-navigation.conf").read_text().replace("@RELEASE@", str(REPO / "configs")))
        self.tm("source-file", str(navigation))
        before = {line.split()[3]: line for line in self.tm("list-keys", "-T", "prefix").splitlines()}
        self.tm("set-option", "-g", "@dotfiles-dashboard-enabled", "on")
        overlay = self.root / "dashboard.conf"
        # Pin the test state explicitly for the installed helper callback.
        self.tm("set-environment", "-g", "XDG_STATE_HOME", str(self.root / "state"))
        overlay.write_text((REPO / "configs/tmux/agent-dashboard.conf").read_text().replace("@RELEASE@", str(REPO / "configs")))
        self.tm("source-file", str(overlay))
        after = {line.split()[3]: line for line in self.tm("list-keys", "-T", "prefix").splitlines()}
        self.assertEqual({key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}, {"n", "c", "N"})
        for key in ["h", "j", "k", "l", "M-h", "M-l", "1", "9", "?", "Q", "L"]:
            self.assertEqual(before[key], after[key])
        self.assertIn("next-window", self.tm("list-keys", "-T", "prefix", "N"))
        self.assertIn("next-layout", self.tm("list-keys", "-T", "prefix", "Space"))

    def test_clock_shimmer_on_actual_title_and_static_states(self):
        window = self.tm("display-message", "-p", "#{window_id}").strip()
        self.tm("set-option", "-w", "@dotfiles-agent-ts", str(int(time.time())))
        for state in ["working", "done", "waiting"]:
            self.tm("set-option", "-w", "@dotfiles-agent", dashboard.title_format("ABCD", state))
            value = self.tm("display-message", "-p", dashboard.TITLE_SLOT)
            self.assertIn("ABCD", re.sub(r"#\[[^]]*\]", "", value))
            if state == "working":
                self.assertEqual(value.count("fg=#e3e6e8"), 1, value)
                def luminance(color):
                    rgb = [int(color[i:i+2], 16) / 255 for i in [1, 3, 5]]
                    values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
                    return sum(a*b for a, b in zip(values, [.2126, .7152, .0722]))
                colors = re.findall(r"#\[fg=(#[0-9a-f]{6}),bg=(#[0-9a-f]{6})\]", value)
                self.assertEqual(len(colors), 4)
                self.assertTrue(all((luminance(fg) + .05) / (luminance(bg) + .05) >= 4.5 for fg, bg in colors))
                time.sleep(1.05)
                second = self.tm("display-message", "-p", dashboard.TITLE_SLOT)
                self.assertNotEqual(value, second)
            else:
                self.assertIn("●" if state == "done" else "!", value)

    def test_concurrent_transitions_movement_titles_termination_and_attention(self):
        a, ap = self.agent("agent-a", "waiting")
        b, bp = self.agent("agent-b", "done")
        c, cp = self.agent("agent-c", "working")
        # Synthetic fixtures use sleep instead of a real agent; map only that
        # command in the test, retaining every other production validation.
        original = dashboard.observable
        def fixture(record, pane, *args):
            return original(record, pane | {"command": "codex"}, *args)
        with patch.object(dashboard, "observable", side_effect=fixture):
            self.view.install()
            self.assertIn("!", self.tm("show-options", "-wqv", "-t", a, "@dotfiles-agent"))
            self.assertIn("●", self.tm("show-options", "-wqv", "-t", b, "@dotfiles-agent"))
            self.assertEqual(self.tm("show-options", "-gqv", "status-interval").strip(), "1")
            session = self.tm("display-message", "-p", "#{session_id}").strip()
            self.tm("select-window", "-t", c)
            for expected in [ap, bp, ap]:
                self.view.attention(session)
                self.assertEqual(self.tm("display-message", "-p", "#{pane_id}").strip(), expected)
            self.tm("swap-window", "-s", a, "-t", b)
            self.tm("rename-window", "-t", a, "renamed '##{evil}")
            self.view.refresh()
            title = self.tm("display-message", "-p", "-t", a, dashboard.TITLE_SLOT)
            self.assertIn("renamed '#{evil}", title)
            self.tm("kill-window", "-t", a)  # This window belongs to the fixture.
            self.tm("set-option", "-p", "-t", bp, "@workmux_pane_status", "")
            self.tm("set-option", "-p", "-t", cp, "@workmux_pane_status", "")
            self.view.refresh()
            before = self.tm("display-message", "-p", "#{window_id}:#{pane_id}")
            self.view.attention(session)
            self.assertEqual(before, self.tm("display-message", "-p", "#{window_id}:#{pane_id}"))
            self.assertEqual(self.tm("show-options", "-gqv", "status-interval").strip(), "15")

    def test_installed_workmux_tracks_plain_pane_without_replacing_format(self):
        env = self.view.env | {"HOME": str(self.root), "XDG_CONFIG_HOME": str(self.root / "config"),
                               "XDG_STATE_HOME": str(self.root / "state"), "XDG_CACHE_HOME": str(self.root / "cache"),
                               "TMUX": self.socket + ",0,0", "TMUX_PANE": self.tm("display-message", "-p", "#{pane_id}").strip()}
        for command in [["register-agent"], ["set-window-status", "working"],
                        ["set-window-status", "waiting"], ["set-window-status", "done"]]:
            result = subprocess.run(["workmux", *command], input=json.dumps({"session_id": "test-ordinary-cdev"}),
                                    text=True, capture_output=True, env=env, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(self.tm("show-options", "-Awqv", "window-status-format").strip(), dashboard.TITLE_SLOT.strip())
        records = list((self.root / "state/workmux/agents").glob("*.json"))
        self.assertEqual(len(records), 1)
        record = json.loads(records[0].read_text())
        self.assertEqual(record["agent_session_id"], "test-ordinary-cdev")
        self.assertEqual(record["status"], "done")
        self.tm("bind-key", "n", "run-shell", "python3 agent-dashboard.py attention")
        self.view.install()
        self.view.disable()
        result = subprocess.run(["workmux", "set-window-status", "working"], input="{}",
                                text=True, capture_output=True, env=env, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("@workmux_status", self.tm("show-options", "-wqv", "window-status-format"))
        self.assertNotIn("@dotfiles-agent", self.tm("show-options", "-wqv", "window-status-format"))
