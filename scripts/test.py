#!/usr/bin/env python3
"""Run temporary-directory unit tests; --integration adds private tmux/PTY tests."""
import argparse
import os
from pathlib import Path
import sys
import unittest

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--integration", action="store_true")
parser.add_argument("--match", action="append", help="Only run test names matching this glob")
args = parser.parse_args()
if args.integration:
    os.environ["DOTFILES_INTEGRATION"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parent))
if args.match:
    unittest.defaultTestLoader.testNamePatterns = args.match
suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parents[1] / "tests"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
