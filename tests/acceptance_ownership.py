"""Live topology assertions for the private native acceptance driver, not a detector."""
from pathlib import Path


def connected_pairs(rows, client, server, endpoint):
    path = str(Path(endpoint).resolve())
    return [{"client_fd": left["fd"], "server_fd": right["fd"],
             "client_socket": left["socket"], "server_socket": right["socket"]}
            for left in rows for right in rows
            if left["pid"] == client and right["pid"] == server
            and left["state"] & 2 and right["state"] & 2
            and left["peer_socket"] != "0"
            and left["peer_socket"] == right["socket"] and right["peer_socket"] == left["socket"]
            and left["connected_to"] == right["bound"] == path]


def prove_topology(argv, record, identities, backend, sockets, loaded, uuid, endpoint):
    """Require current process generations AND kernel connections, never history alone."""
    launcher, child, server = record["pid"], record["child"], backend["pid"]
    assert identities[server] == backend["identity"], "shared server generation changed"
    assert identities[launcher]["started"] == record["started"], "launcher generation changed"
    assert identities[child]["started"] == record["child_started"], "client generation changed"
    assert identities[child]["parent"] == launcher and identities[child]["command"] == "codex", "client is not this launcher's live child"
    assert record.get("session") in (None, uuid), "event session differs from selected UUID"
    remote = "--remote" in argv
    tui = connected_pairs(sockets, child, server, endpoint)
    setup = connected_pairs(sockets, launcher, server, endpoint)
    listener = any(row["pid"] == server and row["bound"] == str(Path(endpoint).resolve())
                   and row["peer_socket"] == "0" for row in sockets)
    assert listener, "expected native listener is absent"
    if remote:
        assert argv[1:3] == ["resume", uuid], "resume UUID differs"
        target = argv[argv.index("--remote") + 1]
        assert target.startswith("unix://") and Path(target.removeprefix("unix://")).resolve() == Path(endpoint).resolve(), "remote endpoint differs"
        assert record.get("remote_session") == uuid and record.get("backend") == server, "registration has another remote owner"
        assert record.get("backend_started") == identities[server]["started"], "registered backend generation differs"
        assert uuid in loaded, "UUID is not loaded by the connected backend"
        assert tui, "live TUI is not connected to the registered backend"
        assert setup, "invocation hook setup connection was retired before client exit"
    else:
        assert "resume" not in argv, "local fallback during resume is forbidden"
        assert record.get("remote_session") is None and record.get("backend") is None, "local launch has remote identity"
        assert not tui and not setup and uuid not in loaded, "local classification conflicts with live shared ownership"
    return {"mode": "remote-resume" if remote else "local-fresh", "uuid": uuid,
            "client_pid": child, "launcher_pid": launcher, "backend_pid": server,
            "live_tui_pairs": tui, "retained_setup_pairs": setup, "loaded_by_backend": uuid in loaded,
            "ownership_from_stored_metadata": False}
