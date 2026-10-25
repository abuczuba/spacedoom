from __future__ import annotations

import importlib.util
import hashlib
import json
import os
from pathlib import Path
import pty
import re
import shlex
import select
import signal
import subprocess
import tempfile
import threading
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

    def test_stopped_workmux_attention_outlives_lease_with_identity_checks(self):
        record = self.record | dict(status="done")
        pane = self.pane | dict(raw="✅")
        def check(change=None, pane_change=None, now=1000 + 86400):
            return dashboard.observable(record | (change or {}), pane | (pane_change or {}),
                                        "/tmp/private", "100:222", now)
        self.assertEqual(check(), "done")
        self.assertIsNone(check(now=999))  # A future timestamp is never evidence.
        for change in [dict(boot_id="old:222"), dict(pane_pid=456), dict(agent_session_id=None)]:
            self.assertIsNone(check(change))
        for change in [dict(dead="1"), dict(command="fish"), dict(raw="🤖")]:
            self.assertIsNone(check(pane_change=change))
        for state in ["working", "waiting"]:
            self.assertIsNone(check(dict(status=state), dict(raw=dashboard.STATES[state])))

    def test_stopped_cdev_attention_outlives_lease_with_identity_checks(self):
        record = dict(socket="/tmp/private", pane="%2", boot="100:222", pid=123,
                      token="launch-one", session="session", turn="turn", state="done", stamp=1000)
        pane = self.pane | dict(command="Python", own="launch-one:2")
        def check(change=None, pane_change=None, now=1000 + 86400):
            return dashboard.own_observable(record | (change or {}), pane | (pane_change or {}),
                                            "/tmp/private", "100:222", now)
        self.assertEqual(check(), "done")
        self.assertIsNone(check(now=999))
        for change in [dict(ended=True), dict(boot="old:222"), dict(pid=456), dict(token="new-launch"),
                       dict(session=None), dict(turn=None), dict(state="working"), dict(state="waiting")]:
            self.assertIsNone(check(change))
        for change in [dict(dead="1"), dict(command="fish"), dict(own="new-launch:2")]:
            self.assertIsNone(check(pane_change=change))

    def test_config_uses_same_native_title_expiry_as_renderer(self):
        config = (REPO / "configs/tmux/agent-dashboard.conf").read_text()
        self.assertIn("set -g @tmux-dotbar-window-status-format '" + dashboard.TITLE_SLOT + "'", config)

    def test_phone_transport_is_absent_from_active_code_and_manifest(self):
        self.assertFalse(hasattr(dashboard.Dashboard, "notify"))
        self.assertFalse((REPO / "configs/tmux/pager.py").exists())
        manifest = json.loads((REPO / "deploy/manifest.json").read_text())
        self.assertNotIn("tmux/pager.py", {item["path"] for item in manifest["files"]})
        for path in [REPO / "configs/tmux/tmux.conf", REPO / "configs/tmux/agent-dashboard.py"]:
            self.assertNotIn("--pager-config", path.read_text())
            self.assertNotIn("pager.json", path.read_text())

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

    def test_preview_matches_readable_stone_and_blood_palette(self):
        preview = (REPO / "docs/previews/dashboard.html").read_text()
        palette = json.loads(re.search(r'id="working-palette">(.*?)</script>', preview).group(1))
        self.assertEqual(palette, dict(base=list(dashboard.WORKING_BASE),
                                      wave=[list(colors) for colors in dashboard.WORKING_WAVE]))
        def luminance(color):
            rgb = [int(color[i:i+2], 16) / 255 for i in [1, 3, 5]]
            values = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
            return sum(a*b for a, b in zip(values, [.2126, .7152, .0722]))
        for fg, bg in [dashboard.WORKING_BASE, *dashboard.WORKING_WAVE]:
            self.assertGreaterEqual((luminance(fg) + .05) / (luminance(bg) + .05), 4.5, (fg, bg))


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

    def test_forwarded_keys_cross_safe_rollout_phases_in_real_tmux_client(self):
        candidate = self.ghostty.read_text()
        legacy = subprocess.check_output(["git", "show", "ec518f0:configs/ghostty/config.ghostty"], cwd=REPO, text=True)
        env = self.view.env | {"HOME": str(self.root / "home"), "XDG_CONFIG_HOME": str(self.root / "home/.config"),
                               "TERM": "xterm-256color"}
        def ghostty_bytes(source):
            self.ghostty.write_text(source)
            # This action has no --config-file flag. Use the isolated HOME/XDG
            # config path, and assert below that both snapshots really loaded.
            result = subprocess.run(["ghostty", "+show-config"],
                                    env=env, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, "Ghostty configuration parsing failed")
            keys = {}
            for line in result.stdout.splitlines():
                match = re.fullmatch(r"keybind = ([^=]+)=text:(.*)", line)
                if match:
                    # show-config escapes the text action's backslashes for
                    # serialization; the action then interprets its escapes.
                    text = bytes(match[2], "ascii").decode("unicode_escape")
                    keys[match[1]] = bytes(text, "ascii").decode("unicode_escape").encode("ascii")
            return keys
        old_keys = ghostty_bytes(legacy)
        new_keys = ghostty_bytes(candidate)
        self.assertEqual(old_keys["super+shift+n"], b"\x06n")
        self.assertEqual(new_keys["super+shift+n"], b"\x06c")
        self.assertEqual({k:v for k,v in old_keys.items() if k != "super+shift+n"},
                         {k:v for k,v in new_keys.items() if k != "super+shift+n"})
        self.ghostty.write_text(legacy)
        navigation = self.root / "navigation.conf"
        navigation.write_text((REPO / "configs/tmux/czuba-navigation.conf").read_text().replace("@RELEASE@", str(REPO / "configs")))
        self.tm("source-file", str(navigation))
        self.tm("set-option", "-g", "prefix", "C-f")
        self.tm("set-option", "-g", "base-index", "1")
        self.tm("move-window", "-r")
        self.tm("set-option", "-g", "renumber-windows", "on")
        self.tm("set-option", "-g", "default-command", "/bin/sleep 120")
        self.tm("bind-key", "Tab", "run-shell", "workmux last-agent")
        protected = {k:v for k,v in self.view.prefix_bindings().items() if k not in {"a", "n", "c", "N"}}
        directory = self.root / "project with spaces"
        directory.mkdir()
        start = self.tm("new-window", "-P", "-F", "#{window_id}", "-c", str(directory), "/bin/sleep", "120").strip()
        self.view.install()  # Legacy bridge: n and c both create in the directory.

        child, fd = pty.fork()
        if child == 0:
            os.execvpe("tmux", ["tmux", "-N", "-S", self.socket, "attach-session", "-t", "=dotfiles-test"], env)
        stopped = threading.Event()
        def drain():
            while not stopped.is_set():
                try:
                    if select.select([fd], [], [], .05)[0]:
                        if not os.read(fd, 65536):
                            return
                except OSError:
                    return
        reader = threading.Thread(target=drain, daemon=True)
        reader.start()
        def close_client():
            stopped.set()
            reader.join(timeout=1)
            os.close(fd)
            until = time.monotonic() + 2
            while time.monotonic() < until:
                if os.waitpid(child, os.WNOHANG)[0]:
                    return
                time.sleep(.02)
            os.kill(child, signal.SIGTERM)  # Only this owned private test client.
            os.waitpid(child, 0)
        self.addCleanup(close_client)
        def wait_for(condition):
            until = time.monotonic() + 4
            while time.monotonic() < until:
                if condition():
                    return
                time.sleep(.02)
            self.fail("forwarded bytes did not produce the expected private tmux state")
        wait_for(lambda: str(child) in self.tm("list-clients", "-F", "#{client_pid}").splitlines())
        def windows():
            return self.tm("list-windows", "-F", "#{window_id}").splitlines()
        def create(keys):
            before = windows()
            os.write(fd, keys)
            wait_for(lambda: len(windows()) == len(before) + 1)
            self.assertEqual(self.tm("display-message", "-p", "#{pane_current_path}").strip(), str(directory))
        self.tm("select-window", "-t", start)
        create(old_keys["super+shift+n"])
        self.ghostty.write_text(candidate)  # Migration may become visible at once.
        self.view.watch()  # File changes/new sessions cannot rebind attention.
        create(old_keys["super+shift+n"])
        create(new_keys["super+shift+n"])
        self.view.install()  # Only after separately approved GUI reload/key check.
        create(new_keys["super+shift+n"])
        create(b"\x06c")

        # A real Python pane gives the adapter its actual stable identity.
        agent = self.tm("new-window", "-d", "-P", "-F", "#{pane_id}", "-c", str(directory),
                        "/usr/bin/python3", "-c", "import time; time.sleep(120)").strip()
        record = dict(socket=self.socket, pane=agent, pid=int(self.tm("display-message", "-p", "-t", agent, "#{pane_pid}")),
                      boot=self.tm("display-message", "-p", "#{start_time}:#{pid}").strip(),
                      token="forward-chain", session="synthetic", turn="one", sequence=1, state="waiting", stamp=int(time.time()))
        path = self.root / "state/dotfiles-dashboard" / (hashlib.sha256(self.socket.encode()).hexdigest() + "-" + agent[1:] + ".json")
        path.write_text(json.dumps(record))
        path.chmod(0o600)
        self.tm("set-option", "-p", "-t", agent, "@dotfiles-agent-evidence", "forward-chain:1")
        self.assertEqual([row["pane"] for row in self.view.snapshot()], [agent],
                         self.tm("list-panes", "-a", "-F", "#{pane_id}:#{pane_current_command}"))
        count = len(windows())
        os.write(fd, b"\x06n")
        wait_for(lambda: self.tm("display-message", "-p", "#{pane_id}").strip() == agent)
        self.assertEqual(len(windows()), count)
        create(new_keys["super+shift+n"])
        while len(windows()) < 9:
            self.tm("new-window", "-d", "/bin/sleep", "120")
        for number in range(1, 10):
            os.write(fd, new_keys["super+digit_" + str(number)])
            wait_for(lambda: self.tm("display-message", "-p", "#{window_index}").strip() == str(number))
        order = windows()
        self.tm("select-window", "-t", order[0])
        os.write(fd, b"\x06N")
        wait_for(lambda: self.tm("display-message", "-p", "#{window_id}").strip() == order[1])
        os.write(fd, b"\x06\x1bl")  # Prefix, then Option+l moves this owned window.
        wait_for(lambda: windows()[2] == order[1])
        self.assertEqual(self.tm("display-message", "-p", "#{window_id}").strip(), order[1])
        left = self.tm("display-message", "-p", "#{pane_id}").strip()
        right = self.tm("split-window", "-d", "-h", "-P", "-F", "#{pane_id}", "/bin/sleep", "120").strip()
        os.write(fd, new_keys["super+shift+l"])
        wait_for(lambda: self.tm("display-message", "-p", "#{pane_id}").strip() == right)
        os.write(fd, new_keys["super+shift+h"])
        wait_for(lambda: self.tm("display-message", "-p", "#{pane_id}").strip() == left)
        self.assertEqual({k:v for k,v in self.view.prefix_bindings().items() if k not in {"a", "n", "c", "N"}}, protected)

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
        self.view.bootstrap()  # tmux.conf activates after theme/navigation setup.
        after = {line.split()[3]: line for line in self.tm("list-keys", "-T", "prefix").splitlines()}
        self.assertEqual({key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}, {"a", "n", "c", "N"})
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
                colors = re.findall(r"#\[fg=(#[0-9a-f]{6}),bg=(#[0-9a-f]{6})\]", value)
                self.assertEqual(len(colors), 4)
                self.assertTrue(all(pair in [dashboard.WORKING_BASE, *dashboard.WORKING_WAVE] for pair in colors))
                time.sleep(1.05)
                second = self.tm("display-message", "-p", dashboard.TITLE_SLOT)
                self.assertNotEqual(value, second)
            else:
                self.assertIn("●" if state == "done" else "!", value)

    def test_native_title_and_monitor_expiry_preserve_only_stopped_state(self):
        self.tm("set-option", "-w", "@dotfiles-agent-ts", str(int(time.time())))
        clock = "#{t/d:@dotfiles-agent-ts}"
        title = dashboard.TITLE_SLOT.replace(clock, "#{@test-evidence-age}")
        signature = dashboard.SIGNATURE.replace(clock, "#{@test-evidence-age}")
        for state in ["working", "waiting", "done"]:
            self.tm("set-option", "-w", "@dotfiles-agent-state", state)
            self.tm("set-option", "-w", "@dotfiles-agent", dashboard.title_format("agent-title", state))
            self.tm("set-option", "-w", "@test-evidence-age", str(dashboard.TTL - 1))
            before = self.tm("display-message", "-p", signature)
            self.assertIn("agent-title", re.sub(r"#\[[^]]*\]", "", self.tm("display-message", "-p", title)))
            self.tm("set-option", "-w", "@test-evidence-age", str(dashboard.TTL))
            after = self.tm("display-message", "-p", signature)
            output = re.sub(r"#\[[^]]*\]", "", self.tm("display-message", "-p", title))
            self.assertEqual(before == after, state == "done")
            self.assertEqual("agent-title" in output, state == "done")
            self.tm("set-option", "-w", "@test-evidence-age", "-1")
            self.assertNotIn("agent-title", self.tm("display-message", "-p", title))

    def test_stopped_attention_survives_delay_splits_movement_and_visits(self):
        # These are synthetic lifecycle records in real, inert Python panes;
        # no Codex CLI, global hooks, application startup or network is invoked.
        def agent(name, age):
            pane = self.tm("new-window", "-d", "-P", "-F", "#{pane_id}", "-n", name,
                           "/usr/bin/python3", "-c", "import time; time.sleep(120)").strip()
            window = self.tm("display-message", "-p", "-t", pane, "#{window_id}").strip()
            record = dict(socket=self.socket, pane=pane,
                          pid=int(self.tm("display-message", "-p", "-t", pane, "#{pane_pid}")),
                          boot=self.tm("display-message", "-p", "#{start_time}:#{pid}").strip(),
                          token="stopped-" + pane[1:], session="synthetic-" + pane, turn="one", sequence=1,
                          state="done", ended=False, stamp=int(time.time()) - age)
            folder = self.root / "state/dotfiles-dashboard"
            folder.mkdir(mode=0o700, parents=True, exist_ok=True)
            path = folder / (hashlib.sha256(self.socket.encode()).hexdigest() + "-" + pane[1:] + ".json")
            path.write_text(json.dumps(record))
            path.chmod(0o600)
            self.tm("set-option", "-p", "-t", pane, "@dotfiles-agent-evidence", record["token"] + ":1")
            return window, pane, path
        a, ap, ar = agent("stopped-a", dashboard.TTL + 1)
        b, bp, br = agent("stopped-b", 86400)
        splits = [self.tm("split-window", "-d", "-v", "-t", a, "-P", "-F", "#{pane_id}",
                          "/bin/sleep", "120").strip() for _ in range(2)]
        self.view.install()
        for window in [a, b]:
            self.assertIn("●", self.tm("display-message", "-p", "-t", window, dashboard.TITLE_SLOT))
            self.assertEqual(self.tm("show-options", "-wqv", "-t", window, "@dotfiles-agent-state").strip(), "done")
        self.tm("select-window", "-t", a)
        self.tm("select-pane", "-t", splits[0])
        # Execute the actual installed callback in its real private-server
        # context. The existing PTY test also covers delivery of Ctrl+F n bytes.
        binding = self.view.prefix_bindings()["n"]
        self.assertEqual(binding[0], "run-shell")
        window_count = self.tm("list-windows", "-a", "-F", "#{window_id}")
        originals = {path: path.read_bytes() for path in [ar, br]}
        def next_attention(expected):
            self.tm("run-shell", "-t", splits[0], binding[1])
            self.assertEqual(self.tm("display-message", "-p", "#{pane_id}").strip(), expected)
        for pane in [ap, bp, ap, bp]:
            next_attention(pane)
        self.assertEqual(self.tm("list-windows", "-a", "-F", "#{window_id}"), window_count)
        self.assertTrue(all(path.read_bytes() == data for path, data in originals.items()),
                        "Visiting a pane is not an acknowledgement or a new lifecycle event")
        self.tm("swap-window", "-s", a, "-t", b)
        self.tm("move-window", "-r")
        self.tm("rename-window", "-t", b, "renamed-stopped")
        self.view.refresh()
        self.tm("select-window", "-t", b)
        self.tm("select-pane", "-t", bp)
        next_attention(ap)  # Now b precedes a; stable pane identity still wins.
        self.assertIn("●", self.tm("display-message", "-p", "-t", b, dashboard.TITLE_SLOT))
        self.assertIn("renamed-stopped", self.tm("display-message", "-p", "-t", b, dashboard.TITLE_SLOT))

        # A new turn consumes the stopped signal, and a terminal event clears
        # attention even when the pane/process itself continues to exist.
        data = json.loads(ar.read_text())
        data.update(state="working", stamp=int(time.time()))
        ar.write_text(json.dumps(data))
        self.tm("set-option", "-p", "-t", ap, "@dotfiles-agent-evidence", data["token"] + ":2")
        self.view.refresh()
        next_attention(bp)
        data = json.loads(br.read_text())
        data.update(ended=True)
        br.write_text(json.dumps(data))
        self.view.refresh()
        before = self.tm("display-message", "-p", "#{window_id}:#{pane_id}")
        self.tm("run-shell", "-t", splits[0], binding[1])
        self.assertEqual(before, self.tm("display-message", "-p", "#{window_id}:#{pane_id}"))
        self.assertEqual(self.tm("show-options", "-wqv", "-t", b, "@dotfiles-agent").strip(), "")
        self.assertEqual(self.tm("show-options", "-wqv", "-t", b, "@dotfiles-agent-state").strip(), "")

        # Even an orphaned old Stop record cannot label a pane once its Python
        # process exits (the other inert splits keep this window alive).
        data = json.loads(ar.read_text())
        data.update(state="done", stamp=int(time.time()) - 86400)
        ar.write_text(json.dumps(data))
        self.view.refresh()
        self.assertIn("●", self.tm("display-message", "-p", "-t", a, dashboard.TITLE_SLOT))
        self.tm("kill-pane", "-t", ap)  # Only the owned private test process.
        self.view.refresh()
        self.assertEqual(self.view.snapshot(), [])
        self.assertEqual(self.tm("show-options", "-wqv", "-t", a, "@dotfiles-agent").strip(), "")

    def test_one_cohesive_wave_moves_right_and_exits_before_wrapping(self):
        # Inject only the clock value; exercise the actual cached native format
        # at every phase, including short titles, punctuation and the wrap.
        for title in ["A", "AB", "stone-agent", "a#,'{}z"]:
            rendered = dashboard.title_format(title, "working").replace("#{t/d:start_time}", "#{@test-age}")
            period = len(title) + len(dashboard.WORKING_WAVE) - 1
            for phase in range(period + 1):
                self.tm("set-option", "-w", "@test-age", str(phase))
                value = self.tm("display-message", "-p", rendered).strip()
                self.assertEqual(re.sub(r"#\[[^]]*\]", "", value), title)
                colors = re.findall(r"#\[fg=(#[0-9a-f]{6}),bg=(#[0-9a-f]{6})\]", value)
                expected = [dashboard.WORKING_WAVE[phase % period - index]
                            if 0 <= phase % period - index < len(dashboard.WORKING_WAVE)
                            else dashboard.WORKING_BASE for index in range(len(title))]
                self.assertEqual(colors, expected, (title, phase, value))
                lit = [index for index, pair in enumerate(colors) if pair != dashboard.WORKING_BASE]
                self.assertLessEqual(len(lit), 3)
                self.assertEqual(lit, list(range(min(lit), max(lit) + 1)))

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
