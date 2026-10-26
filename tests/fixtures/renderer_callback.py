"""Audit the ACTUAL background renderer callback on private synthetic fixtures."""
import importlib.util
import json
import locale
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audited_renderer", ROOT / "payload/agent-dashboard.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.__file__ = __file__
original_tm, original_refresh = module.Dashboard.tm, module.Dashboard.refresh
data = {"pid": os.getpid(), "parent": os.getppid(), "locale": os.environ.get("LC_ALL"),
        "lang": os.environ.get("LANG"), "home": os.environ.get("HOME"),
        "codeset": locale.nl_langinfo(locale.CODESET), "argv": sys.argv[1:], "metadata": []}


def tm(self, *args):
    result = original_tm(self, *args)
    if args[0] in {"list-panes", "list-windows"} and "-F" in args:
        data["metadata"].append({"command": args[0], "text": result, "tabs": result.count("\t")})
    return result


def refresh(self):
    try:
        original_refresh(self)  # Real locks, source validation and tmux writes.
        data["ok"] = True
    except Exception as error:
        data.update(ok=False, error_type=type(error).__name__, error=str(error))
        raise
    finally:
        fd = os.open(ROOT / "callback.jsonl", os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.write(fd, (json.dumps(data) + "\n").encode())
        finally:
            os.close(fd)


module.Dashboard.tm = tm
module.Dashboard.refresh = refresh
module.main()
