#!/usr/bin/env python3
"""Bounded native title-format benchmark on a fresh private tmux socket."""
from __future__ import annotations

import importlib.util
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time

from validation import private_tmux

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dashboard", REPO / "configs/tmux/agent-dashboard.py")
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)


def main():
    count = 2000
    result = dict(iterations_per_sample=count, samples=3, title_characters=24, external_processes_per_animation_tick=0)
    with tempfile.TemporaryDirectory(prefix="df-title-benchmark-") as folder, private_tmux() as tm:
        file = Path(folder) / "formats.conf"
        file.write_text(("display-message -p '#{E:window-status-format}'\n") * count)
        for state in ["idle", "working", "done", "waiting"]:
            tm("set-option", "-g", "window-status-format", dashboard.TITLE_SLOT)
            tm("set-option", "-w", "@dotfiles-agent-ts", str(int(time.time())))
            tm("set-option", "-w", "@dotfiles-agent", "" if state == "idle" else dashboard.title_format("industrial-forge-project", state))
            samples = []
            for _ in range(3):
                start = time.perf_counter()
                tm("source-file", str(file))
                samples.append((time.perf_counter() - start) * 1000 / count)
            result[state + "_milliseconds_per_expansion"] = round(statistics.median(samples), 4)
        # One no-op monitor format covering ordinary windows. No callbacks,
        # Python jobs or title subprocesses are created by these expansions.
        file.write_text(("display-message -p '" + dashboard.SIGNATURE + "'\n") * count)
        for index in range(19):
            tm("new-window", "-d", "-n", "ordinary-" + str(index), "/bin/sleep 120")
        tm("set-option", "-w", "@dotfiles-agent", "")
        start = time.perf_counter()
        tm("source-file", str(file))
        result["twenty_idle_window_monitor_ms"] = round((time.perf_counter() - start) * 1000 / count, 4)
        state_root = Path(folder) / "state"
        records = state_root / "dotfiles-dashboard"
        records.mkdir(mode=0o700, parents=True)
        agents = []
        boot = tm("display-message", "-p", "#{start_time}:#{pid}").strip()
        for index in range(3):
            pane = tm("new-window", "-d", "-P", "-F", "#{pane_id}", "-n", "industrial-forge-agent-" + str(index),
                      sys.executable, "-c", "import time; time.sleep(120)").strip()
            pid = int(tm("display-message", "-p", "-t", pane, "#{pane_pid}"))
            socket = tm("display-message", "-p", "#{socket_path}").strip()
            name = hashlib.sha256(socket.encode()).hexdigest() + "-" + pane[1:] + ".json"
            data = dict(socket=socket, pane=pane, boot=boot, pid=pid, token="benchmark",
                        session="benchmark", turn="one", state="working", stamp=int(time.time()),
                        sequence=1, ended=False, settled=False, pending=[])
            tm("set-option", "-p", "-t", pane, "@dotfiles-agent-evidence", "benchmark:1")
            agents.append((records / name, data))
        samples = []
        env = os.environ.copy()
        env.pop("TMUX", None)
        env.pop("TMUX_PANE", None)
        for state in ["working", "waiting", "done", "idle", "working"]:
            for path, data in agents:
                data["state"] = state
                path.write_text(json.dumps(data))
                path.chmod(0o600)
            start = time.perf_counter()
            subprocess.run([sys.executable, "-B", str(REPO / "configs/tmux/agent-dashboard.py"),
                            "refresh", "--socket", socket, "--state", str(state_root)],
                           env=env, check=True, capture_output=True, timeout=10)
            samples.append((time.perf_counter() - start) * 1000)
        result["refresh_three_agents_wall_ms"] = round(statistics.median(samples), 2)
        samples = []
        for _ in range(5):
            start = time.perf_counter()
            subprocess.run([sys.executable, "-B", str(REPO / "configs/cdev/activity.py"), "event", "--state", str(state_root),
                            "--socket", socket, "--pane", agents[0][1]["pane"], "--token", "benchmark"],
                           env=env, input=json.dumps(dict(hook_event_name="PostToolUse", session_id="benchmark", turn_id="one", tool_name="Bash")),
                           text=True, check=True, capture_output=True, timeout=10)
            samples.append((time.perf_counter() - start) * 1000)
        assert json.loads(agents[0][0].read_text())["sequence"] == 1
        result["unchanged_working_hook_wall_ms"] = round(statistics.median(samples), 2)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
