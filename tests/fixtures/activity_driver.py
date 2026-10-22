"""SYNTHETIC hook dispatcher inside an owned fake CLI's process tree.

No real Codex events or trust claims. IPC is bounded JSON, never shell commands.
"""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time

args = sys.argv[1:]
hook = next(value for value in args if value.startswith("hooks.UserPromptSubmit="))
command = json.JSONDecoder().raw_decode(hook.split("command=", 1)[1])[0]
root = Path(os.environ["CDEV_TEST_EVENTS"])
root.mkdir(mode=0o700, exist_ok=True)
context = os.environ.get("CDEV_ACTIVITY_CONTEXT", "")
pane = json.loads(context)["pane"] if context else "untracked"
metadata = root / (pane[1:] + ".context")
metadata.write_text(json.dumps({"runtime": context, "command": command, "pid": os.getpid()}))
metadata.chmod(0o600)
request = root / (pane[1:] + ".request")
reply = root / (pane[1:] + ".reply")
while True:
    if request.exists():
        data = json.loads(request.read_text())
        request.unlink()
        if data.get("exit") is True:
            break
        env = os.environ.copy() | {"TMUX": "/deliberately/wrong,0,0", "TMUX_PANE": "%99999"}
        if "runtime" in data:
            env["CDEV_ACTIVITY_CONTEXT"] = data["runtime"]
        result = subprocess.run(shlex.split(command), input=json.dumps(data["payload"]),
                                env=env, text=True, capture_output=True, timeout=5)
        reply.write_text(json.dumps({"code": result.returncode, "stderr": result.stderr}))
    time.sleep(.02)
