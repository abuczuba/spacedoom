"""Private tmux, inert agents and synthetic lifecycle caches; no ntfy traffic."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time
import unittest
from unittest.mock import Mock

import test_dashboard as fixtures

dashboard, REPO = fixtures.dashboard, fixtures.REPO

spec = importlib.util.spec_from_file_location("ack_pager", REPO / "configs/tmux/pager.py")
pager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pager)


@unittest.skipUnless(os.environ.get("DOTFILES_INTEGRATION") == "1", "private tmux tests")
class AcknowledgeTests(unittest.TestCase):
    setUp = fixtures.DashboardIntegration.setUp

    def agent(self, name):
        pane = self.tm("new-window", "-d", "-P", "-F", "#{pane_id}", "-n", name,
                       "/usr/bin/python3", "-c", "import time; time.sleep(120)").strip()
        data = dict(socket=self.socket, pane=pane,
                    pid=int(self.tm("display-message", "-p", "-t", pane, "#{pane_pid}")),
                    boot=self.tm("display-message", "-p", "#{start_time}:#{pid}").strip(),
                    token="owned-" + pane, session="synthetic-" + pane, turn="turn-one", sequence=2,
                    state="done", stamp=int(time.time()), ended=False)
        folder = self.root / "state/dotfiles-dashboard"
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        path = folder / (hashlib.sha256(self.socket.encode()).hexdigest() + "-" + pane[1:] + ".json")
        path.write_text(json.dumps(data))
        path.chmod(0o600)
        self.tm("set-option", "-p", "-t", pane, "@dotfiles-agent-evidence", data["token"] + ":2")
        return pane, path

    def event(self, pane):
        return self.tm("show-options", "-pqv", "-t", pane, "@dotfiles-agent-event").strip()

    def test_binding_acknowledges_only_selected_turn_without_mutating_agent(self):
        a, ar = self.agent("a")
        b, br = self.agent("b")
        self.view.install()
        originals = [ar.read_bytes(), br.read_bytes()]
        pids = self.tm("list-panes", "-a", "-F", "#{pane_id}:#{pane_pid}")
        # Exercise the installed callback with the same format expansion as a
        # prefix key. No private record is edited by acknowledgment.
        self.tm("run-shell", "-t", a, self.view.prefix_bindings()["a"][1])
        self.assertEqual([ar.read_bytes(), br.read_bytes()], originals)
        self.assertEqual(self.tm("list-panes", "-a", "-F", "#{pane_id}:#{pane_pid}"), pids)
        self.assertEqual({p["pane"] for p in dashboard.actionable(self.view.snapshot())}, {b})
        self.assertNotIn("●", self.tm("display-message", "-p", "-t", a, dashboard.TITLE_SLOT))
        self.assertIn("●", self.tm("display-message", "-p", "-t", b, dashboard.TITLE_SLOT))
        self.view.attention("$0")
        self.assertEqual(self.tm("display-message", "-p", "#{pane_id}").strip(), b)
        self.view.acknowledge(b, self.event(b))
        before = self.tm("display-message", "-p", "#{window_id}:#{pane_id}")
        self.view.attention("$0")
        self.assertEqual(before, self.tm("display-message", "-p", "#{window_id}:#{pane_id}"))

    def test_stale_key_new_turn_movement_and_process_exit(self):
        pane, path = self.agent("old-title")
        self.view.install()
        old = self.event(pane)
        self.view.acknowledge(pane, old)
        self.tm("rename-window", "-t", pane, "renamed")
        self.tm("move-window", "-r")
        self.view.refresh()
        self.assertEqual(dashboard.actionable(self.view.snapshot()), [])
        data = json.loads(path.read_text())
        data.update(turn="turn-two", sequence=4)
        path.write_text(json.dumps(data))
        self.view.acknowledge(pane, old)  # queued key from the previous turn
        self.assertEqual(len(dashboard.actionable(self.view.snapshot())), 1)
        self.view.refresh()
        new = self.event(pane)
        self.assertNotEqual(new, old)
        self.assertIn("●", self.tm("display-message", "-p", "-t", pane, dashboard.TITLE_SLOT))
        self.view.acknowledge(pane, new)
        self.assertEqual(dashboard.actionable(self.view.snapshot()), [])
        data.update(state="waiting", sequence=5)
        path.write_text(json.dumps(data))
        self.view.refresh()
        self.view.acknowledge(pane, new)
        self.assertEqual([p["state"] for p in dashboard.actionable(self.view.snapshot())], ["waiting"])
        data.update(ended=True)
        path.write_text(json.dumps(data))
        self.view.acknowledge(pane, new)
        self.assertEqual(self.view.snapshot(), [])

    def test_conflicting_a_is_preserved_and_shell_is_noop(self):
        self.tm("bind-key", "a", "display-message", "existing")
        with self.assertRaisesRegex(ValueError, "a is already bound"):
            self.view.install()
        self.assertEqual(self.view.prefix_bindings()["a"], ["display-message", "existing"])
        self.tm("unbind-key", "a")
        self.view.install()
        pane = self.tm("display-message", "-p", "#{pane_id}").strip()
        self.tm("run-shell", "-t", pane, self.view.prefix_bindings()["a"][1])
        self.assertEqual(self.tm("show-options", "-pqv", "-t", pane, "@dotfiles-agent-ack").strip(), "")
        self.view.disable()
        self.assertNotIn("a", self.view.prefix_bindings())

    def test_other_stopped_pane_in_same_window_keeps_attention(self):
        a, _ = self.agent("a")
        b, _ = self.agent("b")
        self.tm("join-pane", "-d", "-h", "-s", b, "-t", a)
        self.view.install()
        self.view.acknowledge(a, self.event(a))
        self.assertIn("●", self.tm("display-message", "-p", "-t", a, dashboard.TITLE_SLOT))
        self.assertEqual([p["pane"] for p in dashboard.actionable(self.view.snapshot())], [b])

    def test_ack_refresh_and_monitor_restart_do_not_replay_ntfy(self):
        pane, path = self.agent("agent")
        config = self.root / "pager.json"
        config.write_text('{"url":"https://ntfy.invalid/test-only"}')
        config.chmod(0o600)
        publisher = pager.Publisher(self.root / "state", self.socket, config)
        now = int(time.time())
        publisher.observe([], now=now - 5, spawn=False)
        self.view.notify = lambda observed: publisher.observe(observed, now=now + 1, spawn=False)
        self.view.install()
        transport = Mock()
        transport.publish.return_value = ("sent", False)
        publisher.drain(snapshot=self.view.snapshot, transport=transport, now=lambda: now + 2)
        self.view.acknowledge(pane, self.event(pane))
        self.view.acknowledge(pane, self.event(pane))
        self.view.refresh()
        publisher.drain(snapshot=self.view.snapshot, transport=transport, now=lambda: now + 3)
        ledger = pager.private_json(publisher.path)
        self.assertEqual(transport.publish.call_count, 1)
        self.assertEqual(len(ledger["alerts"]), 1)
        self.assertEqual(next(iter(ledger["alerts"].values()))["status"], "sent")
        self.assertEqual(self.view.snapshot()[0]["state"], "done")
