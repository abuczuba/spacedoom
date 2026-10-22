"""Synthetic event controls for owned cdev fixtures, not real hook delivery."""
import json
from pathlib import Path
import time

REPO = Path(__file__).resolve().parents[1]


def wait_for(function):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        value = function()
        if value:
            return value
        time.sleep(.02)
    raise AssertionError("Owned activity fixture did not become ready")


def enable_driver(h):
    directory = h.root / "synthetic-events"
    directory.mkdir(mode=0o700)
    h.tm("set-environment", "-g", "CDEV_TEST_DRIVER", str(REPO / "tests/fixtures/activity_driver.py"))
    h.tm("set-environment", "-g", "CDEV_TEST_EVENTS", str(directory))


def context(h, pane):
    path = h.root / "synthetic-events" / (pane[1:] + ".context")
    return wait_for(lambda: json.loads(path.read_text()) if path.exists() else None)


def dispatch(h, pane, event="UserPromptSubmit", session="fixture-session", turn="one", **overrides):
    directory = h.root / "synthetic-events"
    reply = directory / (pane[1:] + ".reply")
    reply.unlink(missing_ok=True)
    data = {"payload": dict(hook_event_name=event, session_id=session, turn_id=turn, tool_name="Bash")}
    data.update(overrides)
    temporary = directory / (pane[1:] + ".pending")
    temporary.write_text(json.dumps(data))
    temporary.replace(directory / (pane[1:] + ".request"))
    return wait_for(lambda: json.loads(reply.read_text()) if reply.exists() else None)
