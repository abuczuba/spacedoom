"""Inert process/environment probes. Never launches native Codex or reads credentials."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
SPEC = json.loads((ROOT / "fixture.json").read_text())
ROLE, ARGS = sys.argv[1], sys.argv[2:]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def probe(role):
    expected = SPEC["env"]
    # Codex may prepend its executable shims. A shared backend may also retain
    # an old pane marker. Those are not lifecycle identities; the source adapter
    # resolves session UUIDs and verifies process generations itself.
    exempt = {"TERM", "PATH"} if role == "hook" else {"TERM"}
    wrong = [key for key, value in expected.items() if key not in exempt and os.environ.get(key) != value]
    if role == "hook" and shutil.which("tmux") != str(ROOT / "bin/tmux"):
        wrong.append("PATH")
    path_keys = ("HOME", "XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME", "XDG_DATA_HOME",
                 "XDG_RUNTIME_DIR", "CODEX_HOME", "TMPDIR", "TMP", "TEMP", "TMUX_TMPDIR")
    for key in path_keys:
        path = Path(os.environ.get(key, "/"))
        if not path.is_absolute() or not path.resolve().is_relative_to(ROOT):
            wrong.append(key)
        elif any(parent.is_symlink() for parent in (path, *path.parents) if parent.is_relative_to(ROOT)):
            wrong.append(key)
    # The allowlist, not a copied environment, must be the credential boundary.
    forbidden = [key for key in os.environ if key.startswith(("OPENAI_", "CHATGPT_"))
                 or key in {"CODEX_ACCESS_TOKEN", "CODEX_API_KEY", "CODEX_APP_SERVER_URL"}]
    row = dict(role=role, pid=os.getpid(), parent=os.getppid(), pane=os.environ.get("TMUX_PANE"),
               ok=not wrong and not forbidden, wrong_keys=wrong, forbidden_keys=forbidden)
    if role in {"control", "plan", "editor", "launcher", "agent"} and not row["pane"]:
        row["ok"] = False
        row["wrong_keys"].append("TMUX_PANE")
    if row["pane"] and not os.environ.get("TMUX", "").startswith(SPEC["socket"] + ","):
        row["ok"] = False
        row["wrong_keys"].append("TMUX")
    if row["ok"]:
        session = load("probe_session", ROOT / "payload/cdev/codex_session.py")
        assert session.codex_home() == ROOT / "codex" and session.state_dir() == ROOT / "state/cdev"
        # Native login/project trust may append normal TOML sections. Keep the
        # root credential-store guard without requiring an otherwise empty file.
        header = (ROOT / "codex/config.toml").read_text().split("[", 1)[0]
        stores = [line.strip() for line in header.splitlines()
                  if line.strip().startswith("cli_auth_credentials_store")]
        assert stores == ['cli_auth_credentials_store = "file"']
        row.update(codex_home=str(session.codex_home()), pins=str(session.state_dir() / "pins.json"),
                   auth_store="file", auth_file=str(session.codex_home() / "auth.json"),
                   temporary=str(Path(os.environ["TMPDIR"])), socket=SPEC["socket"])
        if row["pane"] and role != "hook":
            actual = subprocess.check_output([SPEC["tmux"], "-N", "-S", SPEC["socket"], "display-message",
                                              "-p", "-t", row["pane"], "#{socket_path}|#{pane_pid}"], text=True).strip()
            row["pane_root"] = int(actual.split("|")[1])
            assert actual.split("|")[0] == SPEC["socket"]
            if role in {"editor", "launcher"}:
                assert row["pane_root"] == os.getpid()
    path = ROOT / "proofs" / (role + "-" + str(os.getpid()) + ".json")
    temporary = path.with_suffix(".pending")
    temporary.write_text(json.dumps(row))
    temporary.chmod(0o600)
    temporary.replace(path)
    if not row["ok"]:
        if role == "editor":
            # Keep this inert probe pane long enough to inspect the independent
            # nested-pane boundary too; never run an editor after a failed guard.
            wait_for("stop")
        raise SystemExit(91)
    return row


def wait_for(name):
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        if (ROOT / "stop").exists():
            raise SystemExit(0)
        if (ROOT / name).exists():
            return
        time.sleep(.04)
    raise SystemExit(92)


if ROLE == "tmux":
    # cdev and activity may pass an explicit socket. Refuse any other server.
    while ARGS and ARGS[0].startswith("-"):
        if ARGS[0] == "-N":
            ARGS.pop(0)
        elif ARGS[0] == "-S" and len(ARGS) > 1 and ARGS[1] == SPEC["socket"]:
            del ARGS[:2]
        else:
            raise SystemExit("fixture refuses alternate tmux connection options")
    assert ARGS
    if ARGS[0] in SPEC["propagate_commands"]:
        # This is the correction: creation-time argv, never set-environment -g.
        extra = [arg for key, value in SPEC["env"].items() for arg in ("-e", key + "=" + value)]
        ARGS[1:1] = extra
    os.execv(SPEC["tmux"], [SPEC["tmux"], "-N", "-S", SPEC["socket"], *ARGS])
elif ROLE == "helper":
    action = ARGS[0]
    probe("launcher" if action == "launch" else "plan")
    if action == "plan":
        # Stage one is strictly preflight: no source plan(), locks or pin writes.
        print("fresh")
    elif action == "launch":
        wait_for("allow-launcher")
        activity = load("activity", ROOT / "payload/cdev/activity.py")
        # Fixed production registry is deliberately rebased in THIS test process
        # and the private adapter. No production module/file is edited.
        activity.REMOTE_DIRECTORY = ROOT / "runtime/registry"
        sys.modules["activity"] = activity
        session = load("acceptance_session", ROOT / "payload/cdev/codex_session.py")
        session.__file__ = str(ROOT / "config/cdev/codex_session.py")
        sys.argv = [session.__file__, *ARGS]
        raise SystemExit(session.main())
    else:
        raise SystemExit("fixture helper supports plan/launch only")
elif ROLE == "agent":
    row = probe("agent")
    context = json.loads(os.environ["CDEV_ACTIVITY_CONTEXT"])
    assert context["state"] == str(ROOT / "state") and context["socket"] == SPEC["socket"]
    assert context["pane"] == row["pane"] and context["pid"] == os.getppid()
    subprocess.run(["/usr/bin/python3", "-B", str(ROOT / "config/cdev/activity.py"), "event"],
                   input=b"{}", check=True)
    wait_for("stop")
elif ROLE == "backend":
    path = ROOT / "codex/app-server-control/app-server-control.sock"
    path.parent.mkdir(mode=0o700, parents=True)
    with socket.socket(socket.AF_UNIX) as backend:
        backend.bind(str(path))
        probe("backend")
        wait_for("stop")
elif ROLE == "event":
    probe("hook")
    activity = load("private_adapter", ROOT / "payload/cdev/activity.py")
    activity.REMOTE_DIRECTORY = ROOT / "runtime/registry"
    sys.argv = [str(ROOT / "config/cdev/activity.py"), *ARGS]
    raise SystemExit(activity.main())
elif ROLE == "pin":
    probe("pin")
    session = load("pin_session", ROOT / "payload/cdev/codex_session.py")
    session.update_pin(Path(SPEC["project"]), ARGS[0])
elif ROLE == "paths":
    probe("paths")
    session = load("path_session", ROOT / "payload/cdev/codex_session.py")
    assert session.shared_endpoint() == ROOT / "codex/app-server-control/app-server-control.sock"
    activity = load("private_activity", ROOT / "payload/cdev/activity.py")
    activity.REMOTE_DIRECTORY = ROOT / "runtime/registry"
    with activity.remote_lock():
        activity.save(activity.remote_path(ARGS[0]), {"fixture": True})
    (ROOT / "cache/fixture-cache").touch()
    (ROOT / "tmp/fixture-temporary").touch()
elif ROLE in {"control", "editor"}:
    probe(ROLE)
    if ROLE == "editor":
        wait_for("stop")
else:
    raise SystemExit("unknown fixture role")
