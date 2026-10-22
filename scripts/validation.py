"""Local parsers only: no live sockets, user plugins, config reloads or GUI."""
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import tempfile
from contextlib import contextmanager


class ValidationError(RuntimeError):
    def __init__(self, message: str, diagnostics: str = ""):
        super().__init__(message)
        self.diagnostics = diagnostics


def run(argv: list[str], *, env: dict[str, str] | None = None) -> str:
    try:
        result = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValidationError(f"{Path(argv[0]).name} could not complete local validation") from exc
    if result.returncode:
        # Configuration diagnostics can contain private values. Do not echo them.
        raise ValidationError(f"{Path(argv[0]).name} validation failed (exit {result.returncode}); diagnostics withheld",
                              result.stdout + result.stderr)
    return result.stdout


@contextmanager
def private_tmux():
    """An empty private server with an inert pane; never inherit a live socket."""
    with tempfile.TemporaryDirectory(prefix="dotfiles-tmux-") as folder:
        socket = str(Path(folder) / "server.sock")
        env = os.environ.copy()
        env.pop("TMUX", None)
        env.pop("TMUX_PANE", None)

        def tmux(*args: str) -> str:
            return run(["tmux", "-S", socket, *args], env=env)

        tmux("-f", "/dev/null", "new-session", "-d", "-s", "dotfiles-test",
             "-n", "one", "/bin/sleep 120")
        try:
            yield tmux
        finally:
            # The socket and exact session name are ours, even after test failure.
            subprocess.run(["tmux", "-S", socket, "kill-session", "-t", "=dotfiles-test"],
                           env=env, capture_output=True, timeout=10)


def syntax_checks(directory: Path, manifest: dict) -> list[str]:
    results = []
    tmux_files = []
    if manifest.get("tmux_min_version"):
        match = re.search(r"tmux (\d+)\.(\d+)", run(["tmux", "-V"]))
        minimum = tuple(map(int, manifest["tmux_min_version"].split(".")))
        if not match or tuple(map(int, match.groups())) < minimum:
            raise ValidationError(f"This configuration requires tmux >= {manifest['tmux_min_version']}")
    for item in manifest["files"]:
        path = directory / item["path"]
        kind = item["syntax"]
        if kind == "sh":
            run(["/bin/sh", "-n", str(path)])
            results.append(f"sh syntax: {item['path']}")
        elif kind == "tmux":
            tmux_files.append(path)
        elif kind == "ghostty":
            # This action accepts --config-file=PATH, but not the general
            # --config-default-files flag. An explicit file bypasses defaults.
            run(["ghostty", "+validate-config", f"--config-file={path}"])
            results.append(f"Ghostty syntax: {item['path']}")
        elif kind != "text":
            raise ValidationError(f"Unknown syntax validator: {kind}")
    if tmux_files:
        with private_tmux() as tmux:
            for path in tmux_files:
                tmux("source-file", "-n", str(path))
                results.append(f"tmux parse only: {path.name}")
    minimum = manifest.get("less_min_version")
    if minimum:
        version = run(["/usr/bin/less", "--version"])
        match = re.search(r"less (\d+)", version)
        if not match or int(match[1]) < minimum:
            raise ValidationError(f"This pager configuration requires less >= {minimum}")
        results.append(f"less version >= {minimum}")
    return results
