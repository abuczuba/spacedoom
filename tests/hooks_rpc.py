"""Read native hook metadata in an owned stdio server; never run or trust hooks."""
import json
import os
import queue
import subprocess
import threading


def hook_metadata(home, cwd, args=()):
    env = os.environ.copy() | {"HOME": str(home), "CODEX_HOME": str(home / ".codex"),
                              "XDG_CONFIG_HOME": str(home / ".config"),
                              "XDG_STATE_HOME": str(home / ".local/state"),
                              "XDG_CACHE_HOME": str(home / ".cache")}
    proc = subprocess.Popen(["codex", *args, "app-server", "--stdio"], env=env, cwd=cwd,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, text=True)
    lines = queue.Queue()

    def read():
        for line in proc.stdout:
            lines.put(json.loads(line))

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    try:
        for message in [
            {"id": 0, "method": "initialize", "params": {
                "clientInfo": {"name": "dotfiles_hook_audit", "version": "1"},
                "capabilities": {"experimentalApi": True}}},
            {"method": "initialized", "params": {}},
            {"id": 1, "method": "hooks/list", "params": {"cwds": [str(cwd)]}},
        ]:
            proc.stdin.write(json.dumps(message) + "\n")
        proc.stdin.flush()
        for _ in range(100):
            value = lines.get(timeout=15)
            if value.get("id") == 1:
                if "error" in value:
                    raise AssertionError(value["error"])
                entry = value["result"]["data"][0]
                if entry["errors"]:
                    raise AssertionError(entry["errors"])
                return entry["hooks"]
        raise AssertionError("No hooks/list response")
    finally:
        proc.stdin.close()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.terminate()  # Only the subprocess this fixture created.
            proc.wait(timeout=5)
        reader.join(timeout=2)
        proc.stdout.close()
