#!/usr/bin/env python3
"""Bounded native title-format benchmark on a private tmux socket.

This does not measure hook delivery, cache attribution or real Codex lifecycle.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import statistics
import tempfile
import time

from validation import private_tmux

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dashboard", REPO / "configs/tmux/agent-dashboard.py")
dashboard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard)


def main():
    count = 2000
    title = "industrial-forge-project"
    result = dict(iterations_per_sample=count, samples=3, title_characters=len(title), external_processes_per_animation_tick=0)
    with tempfile.TemporaryDirectory(prefix="df-title-benchmark-") as folder, private_tmux() as tm:
        file = Path(folder) / "formats.conf"
        file.write_text(("display-message -p '#{E:window-status-format}'\n") * count)
        for state in ["idle", "working", "done", "waiting"]:
            tm("set-option", "-g", "window-status-format", dashboard.TITLE_SLOT)
            tm("set-option", "-w", "@dotfiles-agent-ts", str(int(time.time())))
            tm("set-option", "-w", "@dotfiles-agent", "" if state == "idle" else dashboard.title_format(title, state))
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
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
