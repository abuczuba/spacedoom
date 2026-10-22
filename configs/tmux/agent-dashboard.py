#!/usr/bin/env python3
"""Render validated cdev/workmux event caches; never read transcripts or hooks.

Only explicit tmux sockets are accepted. Refresh is called by a native tmux
format monitor when evidence changes; animation itself launches no processes.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import shlex
import subprocess
import time
from urllib.parse import quote

TTL = 900
STATES = {"working": "🤖", "waiting": "💬", "done": "✅"}
MONITOR = "@dotfiles-agents"
# Foreground/background pairs. Deep reds form the contiguous glow; adjusted
# steel reflections keep every letter above 4.5:1 contrast, even in its wake.
WORKING_BASE = ("#85868c", "#111214")
WORKING_WAVE = (("#cc4650", "#000000"),  # Red light at the leading edge.
                ("#d4d4d6", "#a42a36"),  # One cold reflection in blood red.
                ("#b1b2b8", "#751b25"))  # Dark crimson fading into stone.
# Untracked windows contribute nothing, including their titles. A cache being
# cleared contributes until the refresh observes its now-empty workmux status.
SIGNATURE = ("#{W:#{?#{||:#{||:#{@workmux_status},#{P:#{@workmux_pane_status}#{@dotfiles-agent-evidence}}},#{@dotfiles-agent}},"
             "#{window_id}|#{window_name}|#{P:#{pane_id}/#{pane_pid}/#{pane_dead}/"
             "#{pane_current_command}/#{@workmux_pane_status}/#{@dotfiles-agent-evidence};}"
             "#{?@dotfiles-agent,#{>=:#{t/d:@dotfiles-agent-ts},900},},}}")
TITLE_SLOT = (" #{?#{&&:#{@dotfiles-agent},#{&&:#{>=:#{t/d:@dotfiles-agent-ts},0},#{<:#{t/d:@dotfiles-agent-ts},900}}},"
              "#{E:@dotfiles-agent},#W}#{?@workmux_status,,} ")


def literal(text):
    """A title is data, including tmux/shell metacharacters; never re-evaluate it."""
    return "".join(c for c in text if c.isprintable()).replace("#", "##")


def title_format(title, state):
    text = literal(title)
    restore = "#[nobold,fg=#{?window_active,#{@tmux-dotbar-fg-current},#{@tmux-dotbar-fg}},bg=#{@tmux-dotbar-bg}]"
    if state == "waiting":
        return "#[bold,fg=#ffffff,bg=#a50021] ! " + restore + " " + text
    if state == "done":
        return "#[fg=#ffffff]●" + restore + " " + text
    if state == "working":
        # Server age advances once per second. Avoid the A: modifier, which
        # redraws at 10Hz even for A/10. No date/sh/Python process per frame.
        chars = [c for c in title if c.isprintable()]
        # The wake exits the right edge before the next pass starts at the
        # left. Never split the band across opposite ends of the title.
        count = max(1, len(chars) + len(WORKING_WAVE) - 1)
        clock = ("#{e|-:#{t/d:start_time},#{e|*:#{e|/:#{t/d:start_time},"
                 + str(count) + "}," + str(count) + "}}")
        parts = []
        for i, char in enumerate(chars):
            # Escape style commas inside conditional branches. Select a whole
            # style once, rather than repeating the clock for fg and bg.
            style = "#[fg=" + WORKING_BASE[0] + "#,bg=" + WORKING_BASE[1] + "]"
            for offset, (fg, bg) in reversed(list(enumerate(WORKING_WAVE))):
                position = "#{==:" + clock + "," + str(i + offset) + "}"
                style = "#{?" + position + ",#[fg=" + fg + "#,bg=" + bg + "]," + style + "}"
            parts.append(style + literal(char))
        return "".join(parts) + restore
    return text


def private_json(path):
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
            or info.st_mode & 0o022 or info.st_size > 65536):
        raise ValueError("untrusted event cache")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError("event cache must be an object")
    return value


def observable(record, pane, socket, boot, now):
    """Fail closed on old server/PID/pane identity, unknown/expired evidence."""
    state = record.get("status")
    stamp = record.get("status_ts")
    if (record.get("pane_key") != {"backend": "tmux", "instance": socket, "pane_id": pane["pane"]}
            or record.get("boot_id") != boot or record.get("pane_pid") != int(pane["pid"])
            or not record.get("agent_session_id") or pane["dead"] != "0"
            or pane["command"] not in {"codex", "codex-cli"}
            or state not in STATES or pane["raw"] != STATES[state]
            or not isinstance(stamp, int) or not 0 <= now - stamp < TTL):
        return None
    return state


def own_observable(record, pane, socket, boot, now):
    stamp = record.get("stamp")
    if (record.get("socket") != socket or record.get("pane") != pane["pane"]
            or record.get("boot") != boot or record.get("pid") != int(pane["pid"])
            or record.get("ended") or not record.get("session") or not record.get("turn")
            or pane["dead"] != "0" or pane["command"] not in {"Python", "python3", "codex", "codex-cli"}
            or not pane.get("own", "").startswith(str(record.get("token")) + ":")
            or record.get("state") not in STATES
            or not isinstance(stamp, int) or not 0 <= now - stamp < TTL):
        return None
    return record["state"]


class Dashboard:
    def __init__(self, socket, state=None, ghostty_config=None):
        if not Path(socket).is_absolute():
            raise ValueError("an absolute, explicit tmux socket is required")
        self.socket = socket
        self.state = Path(state or os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
        self.ghostty = Path(ghostty_config or Path.home() / ".config/ghostty/config.ghostty")
        self.env = os.environ.copy()
        self.env.pop("TMUX", None)
        self.env.pop("TMUX_PANE", None)

    def tm(self, *args):
        result = subprocess.run(["tmux", "-N", "-S", self.socket, *args], env=self.env,
                                capture_output=True, text=True, timeout=10)
        if result.returncode:
            raise RuntimeError("dashboard: tmux command failed: " + args[0])
        return result.stdout.removesuffix("\n")

    @contextmanager
    def locked(self):
        folder = self.state / "dotfiles-dashboard"
        if folder.is_symlink():
            raise ValueError("dashboard state cannot be a symlink")
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = folder.stat()
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("dashboard state must be private")
        name = hashlib.sha256(self.socket.encode()).hexdigest() + ".lock"
        fd = os.open(folder / name, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "a") as handle:
            deadline = time.monotonic() + 1
            while True:
                try:
                    fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError("dashboard cache is busy; retry attention navigation")
                    time.sleep(.02)
            yield

    def snapshot(self, now=None):
        now = int(time.time()) if now is None else now
        boot = self.tm("display-message", "-p", "#{start_time}:#{pid}")
        fields = ["session_id", "window_id", "window_index", "pane_id", "pane_pid",
                  "pane_dead", "pane_current_command", "@workmux_pane_status", "@dotfiles-agent-evidence"]
        rows = self.tm("list-panes", "-a", "-F", "\t".join("#{" + x + "}" for x in fields))
        result = []
        for row in rows.splitlines():
            values = row.split("\t")
            if len(values) != len(fields):
                continue
            pane = dict(zip(["session", "window", "index", "pane", "pid", "dead", "command", "raw", "own"], values))
            if pane["own"]:
                name = hashlib.sha256(self.socket.encode()).hexdigest() + "-" + pane["pane"][1:] + ".json"
                try:
                    record = private_json(self.state / "dotfiles-dashboard" / name)
                    state = own_observable(record, pane, self.socket, boot, now)
                    if state:
                        result.append(pane | {"state": state, "stamp": record["stamp"]})
                    continue  # A registered cdev launch owns its own evidence.
                except (OSError, ValueError, TypeError, KeyError):
                    continue
            if pane["raw"] not in STATES.values():
                continue
            name = "tmux__" + quote(self.socket, safe="") + "__" + quote(pane["pane"], safe="") + ".json"
            try:
                record = private_json(self.state / "workmux/agents" / name)
                state = observable(record, pane, self.socket, boot, now)
            except (OSError, ValueError, TypeError, KeyError):
                continue
            if state:
                result.append(pane | {"state": state, "stamp": record["status_ts"]})
        return result

    def refresh(self):
        with self.locked():
            if self.tm("show-options", "-gqv", "@dotfiles-dashboard-enabled") == "off":
                return
            observed = self.snapshot()
            by_window = {}
            priority = {"waiting": 3, "done": 2, "working": 1}
            for pane in observed:
                old = by_window.get(pane["window"])
                if old is None or priority[pane["state"]] > priority[old["state"]]:
                    by_window[pane["window"]] = pane
            windows = self.tm("list-windows", "-a", "-F", "#{window_id}\t#{@dotfiles-agent}\t#{@dotfiles-agent-ts}").splitlines()
            seen = set()
            writes = []
            for row in windows:
                window, old, old_stamp = row.split("\t", 2)
                if window in seen:
                    continue
                seen.add(window)
                pane = by_window.get(window)
                value = title_format(self.tm("display-message", "-p", "-t", window, "#{window_name}"), pane["state"]) if pane else ""
                if value != old:
                    writes += ["set-option", "-w", "-t", window, "@dotfiles-agent", value, ";"]
                stamp = str(pane["stamp"]) if pane else "0"
                if stamp != old_stamp and (pane or old_stamp):
                    writes += ["set-option", "-w", "-t", window, "@dotfiles-agent-ts", stamp, ";"]
            if writes:
                self.tm(*writes[:-1])
            previous = self.tm("show-options", "-gqv", "@dotfiles-status-interval-before")
            if previous:
                interval = "1" if any(p["state"] == "working" for p in observed) else previous
                if interval != self.tm("show-options", "-gqv", "status-interval"):
                    self.tm("set-option", "-g", "status-interval", interval)

    def navigation_ready(self):
        try:
            mappings = []
            for line in self.ghostty.read_text().splitlines():
                fields = [field.strip() for field in line.split("=", 2)]
                if len(fields) == 3 and fields[:2] == ["keybind", "super+shift+n"]:
                    mappings.append(fields[2])
            return mappings == [r"text:\x06\x63"]
        except OSError:
            return False

    def install(self, navigation=True):
        if self.tm("show-options", "-gqv", "@dotfiles-dashboard-enabled") == "off":
            return
        self.preflight(require_navigation=False)
        if navigation and "N" not in self.prefix_bindings():
            self.tm("set-option", "-g", "@dotfiles-dashboard-owned-N", "1")
        script = str(Path(__file__).resolve())
        # These paths are generated by the deployment validator. No title,
        # project path or hook payload is interpolated into shell commands.
        command = ("python3 -B " + shlex.quote(script) + " refresh --socket " + shlex.quote(self.socket)
                   + " --state " + shlex.quote(str(self.state)) + " --quiet")
        installer = ("python3 -B " + shlex.quote(script) + " watch --socket " + shlex.quote(self.socket)
                     + " --state " + shlex.quote(str(self.state)) + " --ghostty-config " + shlex.quote(str(self.ghostty)) + " --quiet")
        self.tm("set-hook", "-g", "session-created[882]", "run-shell -b " + shlex.quote(installer))
        if not self.tm("show-options", "-gqv", "@dotfiles-status-interval-before"):
            self.tm("set-option", "-g", "@dotfiles-status-interval-before", self.tm("show-options", "-gqv", "status-interval"))
        for session in self.tm("list-sessions", "-F", "#{session_id}").splitlines():
            self.tm("set-hook", "-t", session + ":", "-B", MONITOR + "::" + SIGNATURE,
                    "run-shell -b " + shlex.quote(command))
        self.refresh()
        # A monitor's first tick establishes its comparison value without firing.
        # Cover events arriving between this initial refresh and that first tick.
        self.tm("run-shell", "-b", "-d", "2", command)
        if navigation:
            self.tm("bind-key", "c", "new-window", "-c", "#{pane_current_path}")
            self.tm("bind-key", "N", "next-window")
            if self.navigation_ready():
                attention = ("python3 -B " + shlex.quote(script) + " attention --socket " + shlex.quote(self.socket)
                             + " --state " + shlex.quote(str(self.state)) + " --session #{q:session_id}")
                self.tm("bind-key", "n", "run-shell", attention)
                self.tm("set-option", "-g", "@dotfiles-attention-installed", "on")
            else:
                self.tm("bind-key", "n", "new-window", "-c", "#{pane_current_path}")
                self.tm("set-option", "-g", "@dotfiles-attention-installed", "off")

    def watch(self):
        self.install(navigation=False)  # New sessions must never rebind live keys.

    def preflight(self, check_formats=True, require_navigation=True):
        hooks = self.tm("show-hooks", "-g").splitlines()
        for line in hooks:
            if line.startswith("session-created[882]") and "agent-dashboard.py" not in line:
                raise ValueError("session-created hook slot 882 is occupied; review the conflict")
        keys = self.prefix_bindings()
        if "N" in keys and keys["N"] != ["next-window"]:
            raise ValueError("Shift+N is already bound; review the navigation conflict")
        if check_formats:
            if keys.get("c") not in (["new-window"], ["new-window", "-c", "#{pane_current_path}"]):
                raise ValueError("c has a custom binding; review before relocating window creation")
            if keys.get("n") not in (["next-window"], ["new-window", "-c", "#{pane_current_path}"]):
                if not any("agent-dashboard.py" in item and "attention" in item for item in keys.get("n", [])):
                    raise ValueError("n has a custom binding; review before installing attention navigation")
        if require_navigation and not self.navigation_ready():
            raise ValueError("Ghostty Cmd+Shift+N requires the companion Ctrl+F c mapping and approved reload before attention activation")
        for window in dict.fromkeys(self.tm("list-windows", "-a", "-F", "#{window_id}").splitlines()) if check_formats else []:
            for option in ["window-status-format", "window-status-current-format"]:
                value = self.tm("show-options", "-wqv", "-t", window, option)
                if value and "@dotfiles-agent" not in value:
                    raise ValueError("a local window title override conflicts with Dotbar; review it first")

    def prefix_bindings(self):
        result = {}
        for line in self.tm("list-keys", "-T", "prefix").splitlines():
            words = shlex.split(line)
            index = words.index("-T") + 2
            result[words[index]] = words[index + 1:] + (["repeat"] if "-r" in words[:index] else [])
        return result

    def attention(self, session):
        if not re.fullmatch(r"\$\d+", session):
            raise ValueError("a stable session ID is required")
        with self.locked():
            if self.tm("show-options", "-gqv", "@dotfiles-dashboard-enabled") == "off":
                return
            queue = sorted((p for p in self.snapshot() if p["session"] == session and p["state"] in {"done", "waiting"}),
                           key=lambda p: (int(p["index"]), int(p["pane"][1:])))
            if not queue:
                return  # Explicitly no working/idle fallback and no focus change.
            current = self.tm("display-message", "-p", "-t", session + ":", "#{pane_id}")
            ids = [p["pane"] for p in queue]
            next_pane = queue[(ids.index(current) + 1) % len(queue)] if current in ids else queue[0]
            self.tm("select-window", "-t", session + ":" + next_pane["window"])
            self.tm("select-pane", "-t", next_pane["pane"])

    def disable(self):
        """Explicit feature recovery, never called by Git/deployment/tests on live."""
        with self.locked():
            self.preflight(check_formats=False, require_navigation=False)
            # Refuse to overwrite a user's subsequent n binding.
            binding = self.tm("list-keys", "-T", "prefix", "n")
            keys = self.prefix_bindings()
            own_attention = "agent-dashboard.py" in binding and "attention" in binding
            own_legacy = (self.tm("show-options", "-gqv", "@dotfiles-attention-installed") == "off"
                          and keys.get("n") == ["new-window", "-c", "#{pane_current_path}"])
            if not own_attention and not own_legacy:
                raise ValueError("attention binding changed; review before disabling")
            if keys.get("c") not in (["new-window"], ["new-window", "-c", "#{pane_current_path}"]):
                raise ValueError("window creation binding changed; review before disabling")
            self.tm("set-option", "-g", "@dotfiles-dashboard-enabled", "off")
            self.tm("set-option", "-g", "@dotfiles-attention-installed", "off")
            for session in self.tm("list-sessions", "-F", "#{session_id}").splitlines():
                self.tm("set-hook", "-t", session + ":", "-u", "-B", MONITOR)
            self.tm("set-hook", "-gu", "session-created[882]")
            for window in dict.fromkeys(self.tm("list-windows", "-a", "-F", "#{window_id}").splitlines()):
                self.tm("set-option", "-w", "-t", window, "@dotfiles-agent", "")
            interval = self.tm("show-options", "-gqv", "@dotfiles-status-interval-before")
            if interval:
                self.tm("set-option", "-g", "status-interval", interval)
            self.tm("bind-key", "n", "new-window", "-c", "#{pane_current_path}")
            # Preserve Cmd+Shift+N's directory semantics while Ghostty forwards c.
            # Full Ghostty rollback/reload precedes restoring c's former default.
            if not self.navigation_ready():
                self.tm("bind-key", "c", "new-window")
            if self.tm("show-options", "-gqv", "@dotfiles-dashboard-owned-N") == "1":
                self.tm("unbind-key", "N")
                self.tm("set-option", "-gu", "@dotfiles-dashboard-owned-N")
            self.tm("set-option", "-gu", "@dotfiles-status-interval-before")
            # Remove only our exact slot from Dotbar's constructed formats;
            # preserve its wrappers/SSH/styles. This also restores workmux's
            # original format auto-detection after the dashboard is disabled.
            for option in ["window-status-format", "window-status-current-format"]:
                value = self.tm("show-options", "-gqv", option)
                if TITLE_SLOT in value:
                    self.tm("set-option", "-g", option, value.replace(TITLE_SLOT, " #W "))
            if self.tm("show-options", "-gqv", "@tmux-dotbar-window-status-format") == TITLE_SLOT:
                self.tm("set-option", "-g", "@tmux-dotbar-window-status-format", " #W ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "watch", "refresh", "attention", "preview", "disable", "preflight"])
    parser.add_argument("--socket")
    parser.add_argument("--session")
    parser.add_argument("--state")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--ghostty-config")
    parser.add_argument("--display-only", action="store_true", help="Preflight display/legacy navigation without enabling attention")
    args = parser.parse_args()
    if args.action == "preview":
        for state in ["working", "done", "waiting", "idle"]:
            print(state + ": " + title_format("project-codex", state))
        return
    try:
        dashboard = Dashboard(args.socket or "", args.state, args.ghostty_config)
        if args.action == "attention":
            dashboard.attention(args.session or "")
        elif args.action == "preflight":
            dashboard.preflight(require_navigation=not args.display_only)
        else:
            getattr(dashboard, args.action)()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired):
        if not args.quiet:
            raise


if __name__ == "__main__":
    main()
