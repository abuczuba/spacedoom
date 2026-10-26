"""Ownership must fail closed even when stored UUID metadata looks correct."""
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest

from acceptance_ownership import prove_topology, connected_pairs


class AcceptanceOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.uuid = "00000000-0000-0000-0000-000000000001"
        self.endpoint = "/private/tmp/acceptance-owner.sock"
        self.ids = {10: {"started": "launcher", "command": "Python", "parent": 1},
                    11: {"started": "client", "command": "codex", "parent": 10},
                    12: {"started": "server", "command": "codex", "parent": 1}}
        self.backend = {"pid": 12, "identity": self.ids[12].copy()}
        self.record = dict(pid=10, started="launcher", child=11, child_started="client", session=self.uuid,
                           remote_session=self.uuid, backend=12, backend_started="server")
        self.argv = ["codex", "resume", self.uuid, "--remote", "unix://" + self.endpoint]
        self.sockets = [dict(pid=12, fd=3, socket="listener", peer_socket="0", bound=self.endpoint, connected_to="", state=128)]
        for pid, label in ((11, "tui"), (10, "setup")):
            self.sockets += [dict(pid=pid, fd=4, socket=label, peer_socket=label+"-server", bound="", connected_to=self.endpoint, state=2),
                             dict(pid=12, fd=pid, socket=label+"-server", peer_socket=label, bound=self.endpoint, connected_to="", state=2)]

    def prove(self, **changes):
        values = dict(argv=self.argv, record=self.record, identities=self.ids, backend=self.backend,
                      sockets=self.sockets, loaded={self.uuid}, uuid=self.uuid, endpoint=self.endpoint)
        values.update(changes)
        return prove_topology(**values)

    def test_remote_requires_both_actual_connections_and_loaded_uuid(self):
        proof = self.prove()
        self.assertEqual(proof["mode"], "remote-resume")
        self.assertTrue(proof["live_tui_pairs"] and proof["retained_setup_pairs"])
        with self.assertRaisesRegex(AssertionError, "not loaded"):
            self.prove(loaded=set())

    def test_old_premature_connection_close_fails_despite_live_tui_and_history(self):
        rows = [row for row in self.sockets if row["socket"] not in {"setup", "setup-server"}]
        with self.assertRaisesRegex(AssertionError, "retired"):
            self.prove(sockets=rows)

    def test_stored_uuid_listener_and_registration_do_not_prove_client_connection(self):
        rows = [row for row in self.sockets if row["socket"] not in {"tui", "tui-server"}]
        with self.assertRaisesRegex(AssertionError, "TUI is not connected"):
            self.prove(sockets=rows)

    def test_wrong_generation_endpoint_and_nonreciprocal_handles_fail(self):
        for change in (dict(identities=self.ids | {11: self.ids[11] | {"started": "reused"}}),
                       dict(argv=self.argv[:-1]+["unix:///private/tmp/wrong.sock"]),
                       dict(sockets=[row | {"peer_socket": "wrong"} if row["socket"] == "tui-server" else row for row in self.sockets])):
            with self.subTest(change=change), self.assertRaises(AssertionError):
                self.prove(**change)

    def test_local_fresh_is_explicitly_local_and_cannot_claim_shared_runtime(self):
        record = self.record | {"remote_session": None, "backend": None, "backend_started": None}
        proof = self.prove(argv=["codex", "--cd", "/private/tmp/project"], record=record,
                           sockets=self.sockets[:1], loaded=set())
        self.assertEqual(proof["mode"], "local-fresh")
        with self.assertRaisesRegex(AssertionError, "local classification"):
            self.prove(argv=["codex", "--cd", "/private/tmp/project"], record=record)

    @unittest.skipUnless(os.environ.get("DOTFILES_INTEGRATION") == "1", "Private kernel socket test")
    def test_actual_kernel_probe_matches_only_the_connected_same_account_peer(self):
        with tempfile.TemporaryDirectory(prefix="df-peer-", dir="/private/tmp") as directory:
            root = Path(directory); binary = root / "probe"; endpoint = root / "peer.sock"
            source = Path(__file__).with_name("fixtures") / "proc_unix.c"
            subprocess.run(["/usr/bin/cc", "-Wall", "-Wextra", "-Werror", str(source), "-o", str(binary)], check=True, capture_output=True)
            code = "import socket,sys;s=socket.socket(socket.AF_UNIX);s.bind(sys.argv[1]);s.listen();print('ready',flush=True);c,_=s.accept();print('connected',flush=True);sys.stdin.readline()"
            child = subprocess.Popen(["/usr/bin/python3", "-c", code, str(endpoint)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            try:
                self.assertEqual(child.stdout.readline().strip(), "ready")
                with socket.socket(socket.AF_UNIX) as client:
                    client.connect(str(endpoint)); self.assertEqual(child.stdout.readline().strip(), "connected")
                    rows = json.loads(subprocess.check_output([str(binary), str(os.getpid()), str(child.pid)], text=True))
                    self.assertTrue(connected_pairs(rows, os.getpid(), child.pid, endpoint))
                    self.assertFalse(connected_pairs(rows, os.getpid(), child.pid, root / "wrong.sock"))
            finally:
                child.stdin.close(); child.wait(timeout=5); child.stdout.close()
