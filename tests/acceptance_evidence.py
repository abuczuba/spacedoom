"""Metadata-only diagnostics and a real, private approval-policy fixture."""
import json
from pathlib import Path
import re
import uuid


APPROVAL_COMMAND = ("/bin/echo", "dotfiles-approval-probe")
APPROVAL_RULE = '''prefix_rule(
    pattern = ["/bin/echo", "dotfiles-approval-probe"],
    decision = "prompt",
    justification = "Disposable dashboard approval check; cancel without approval",
)
'''


def owned_turn_metadata(root, identity):
    """Read only our exact disposable session; never return message/tool contents."""
    root = Path(root).resolve()
    assert str(uuid.UUID(identity)) == identity
    paths = list((root / "codex/sessions").rglob("*" + identity + "*.jsonl"))
    assert len(paths) == 1 and not paths[0].is_symlink()
    assert paths[0].resolve().is_relative_to(root)
    turns, current = {}, None

    def turn():
        return turns.setdefault(current, {"tool_calls": [], "started": False, "stopped": False})

    with paths[0].open() as stream:
        header = json.loads(stream.readline())
        assert header.get("type") == "session_meta"
        assert header["payload"]["id"] == identity
        assert header["payload"]["cwd"] == str(root / "project")
        for line in stream:
            row = json.loads(line)
            payload = row.get("payload", {})
            if row.get("type") == "turn_context":
                current = payload.get("turn_id")
                turn().update(approval_policy=payload.get("approval_policy"),
                              sandbox_type=payload.get("sandbox_policy", {}).get("type"))
            elif row.get("type") == "event_msg":
                if payload.get("type") == "task_started":
                    current = payload.get("turn_id")
                    turn()["started"] = True
                elif payload.get("type") in {"task_complete", "turn_aborted"}:
                    turn()["stopped"] = True
            elif row.get("type") == "response_item" and payload.get("type") in {"function_call", "custom_tool_call"}:
                name = payload.get("name", "")
                assert re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", name)
                turn()["tool_calls"].append(name)
    return {"session": identity, "turns": turns}


def require_approval_attempt(metadata, turn):
    """A no-op model reply is a fixture failure, never proof of lost hooks."""
    evidence = metadata["turns"][turn]
    if evidence["stopped"] and not evidence["tool_calls"]:
        raise AssertionError("approval fixture stopped without a tool call; no permission request was exercised")
