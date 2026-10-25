"""Project creation uses disposable homes; no shell startup or live projects run."""
from __future__ import annotations

import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "configs/fish/functions/cnew.fish"


class CnewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="df-cnew-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.home = self.root / "home with spaces"
        self.home.mkdir()
        self.env = os.environ | {"HOME": str(self.home), "XDG_CONFIG_HOME": str(self.home / ".config"),
                                 "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(self.root / "gitconfig")}
        self.env.pop("TMUX", None)
        self.env.pop("TMUX_PANE", None)
        self.base = self.home / "dev"

    def command(self, *args):
        return ["fish", "--no-config", "-c", "source " + shlex.quote(str(SOURCE)) + "; cnew " + shlex.join(args)]

    def run_cnew(self, *args):
        return subprocess.run(self.command(*args), env=self.env, cwd=self.root,
                              text=True, capture_output=True, timeout=10)

    def git(self, directory, *args):
        return subprocess.run(["git", "-C", str(directory), *args], env=self.env,
                              text=True, capture_output=True, check=True).stdout.strip()

    @staticmethod
    def snapshot(path):
        paths = [path, *sorted(path.rglob("*"))] if path.is_dir() and not path.is_symlink() else [path]
        return [(str(p), p.lstat().st_mode, os.readlink(p) if p.is_symlink() else p.read_bytes() if p.is_file() else None)
                for p in paths]

    def test_minimal_main_branch_no_commit_no_dependencies_or_application_launch(self):
        guards = self.root / "guards"
        guards.mkdir()
        for name in ["codex", "emacs", "emacsclient", "tmux", "direnv"]:
            command = guards / name
            command.write_text('#!/bin/sh\nprintf unexpected > "$HOME/unexpected-launch"\nexit 81\n')
            command.chmod(0o755)
        self.env["PATH"] = str(guards) + os.pathsep + os.environ["PATH"]
        result = self.run_cnew("small-project_v2.0")
        self.assertEqual(result.returncode, 0, result.stderr)
        project = self.base / "small-project_v2.0"
        self.assertEqual({p.name for p in project.iterdir()}, {".git", "README.md", "AGENTS.md", ".gitignore"})
        self.assertEqual(self.git(project, "symbolic-ref", "--short", "HEAD"), "main")
        head = subprocess.run(["git", "-C", str(project), "rev-parse", "--verify", "HEAD"],
                              env=self.env, capture_output=True)
        self.assertNotEqual(head.returncode, 0)
        self.assertIn("# small-project_v2.0", (project / "README.md").read_text())
        self.assertIn("No stack or setup/test commands", (project / "AGENTS.md").read_text())
        self.assertEqual(self.git(project, "check-ignore", ".env", ".env.local", ".DS_Store").splitlines(),
                         [".env", ".env.local", ".DS_Store"])
        (project / ".env.example").write_text("EXAMPLE=placeholder\n")
        self.assertIn("?? .env.example", self.git(project, "status", "--short", "--untracked-files=all"))
        self.assertIn("cdev small-project_v2.0", result.stdout)
        self.assertFalse((self.home / ".codex").exists())
        self.assertFalse((self.home / "unexpected-launch").exists())

    def test_no_global_git_template_is_copied_or_executed(self):
        template = self.root / "global-template"
        (template / "hooks").mkdir(parents=True)
        (template / "hooks/post-checkout").write_text("untrusted template fixture\n")
        (template / "unexpected").write_text("must not be copied\n")
        self.env["GIT_TEMPLATE_DIR"] = str(template)
        result = self.run_cnew("no-templates")
        self.assertEqual(result.returncode, 0, result.stderr)
        project = self.base / "no-templates"
        self.assertFalse((project / ".git/unexpected").exists())
        self.assertFalse((project / ".git/hooks").exists())

    def test_invalid_or_missing_names_never_create_the_dev_directory(self):
        for args in [(), ("one", "two"), ("",), (".",), ("..",), ("../escape",), ("/absolute",),
                     ("--option",), ("name space",), ("nested/name",), ("line\nbreak",), ("$(ignored)",)]:
            with self.subTest(args=args):
                self.assertEqual(self.run_cnew(*args).returncode, 2)
                self.assertFalse(self.base.exists())

    def test_existing_paths_and_upstream_instruction_files_are_untouched(self):
        self.base.mkdir()
        existing = self.base / "upstream"
        existing.mkdir()
        self.git(existing, "init", "--quiet", "--template=")
        (existing / "AGENTS.md").write_text("upstream agent policy\n")
        (existing / "CLAUDE.md").write_text("upstream working agreement\n")
        (existing / "CLAUDE.md").chmod(0o640)
        (self.base / "empty").mkdir()
        (self.base / "file").write_text("preserve\n")
        for path in [existing, self.base / "empty", self.base / "file"]:
            with self.subTest(path=path.name):
                before = self.snapshot(path)
                result = self.run_cnew(path.name)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("refusing existing path", result.stderr)
                self.assertEqual(self.snapshot(path), before)

    def test_existing_and_dangling_symlinks_are_not_followed_or_replaced(self):
        self.base.mkdir()
        destination = self.root / "untouched"
        destination.mkdir()
        for name, target in [("linked", destination), ("dangling", self.root / "absent")]:
            link = self.base / name
            link.symlink_to(target)
            result = self.run_cnew(name)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(os.readlink(link), str(target))
        self.assertEqual(list(destination.iterdir()), [])

    def test_nested_normal_and_bare_repositories_are_rejected(self):
        self.git(self.home, "init", "--quiet", "--template=")
        result = self.run_cnew("nested")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nested repository", result.stderr)
        self.assertFalse(self.base.exists())
        # A separate disposable home covers a bare repository at ~/dev too.
        other = self.root / "bare-home"
        other.mkdir()
        self.home, self.base = other, other / "dev"
        self.env["HOME"] = str(other)
        self.base.mkdir()
        self.git(self.base, "init", "--bare", "--quiet", "--template=")
        self.assertNotEqual(self.run_cnew("nested").returncode, 0)
        self.assertFalse((self.base / "nested").exists())

    def test_concurrent_creation_has_one_winner(self):
        jobs = [subprocess.Popen(self.command("one-winner"), env=self.env, cwd=self.root,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        for job in jobs:
            job.communicate(timeout=10)
        self.assertEqual(sorted(job.returncode for job in jobs), [0, 1])
        self.assertEqual(self.git(self.base / "one-winner", "symbolic-ref", "--short", "HEAD"), "main")
        self.assertTrue((self.base / "one-winner/AGENTS.md").is_file())

    def test_failed_initialization_is_visible_and_partial_directory_is_not_reused(self):
        binary = self.root / "bin"
        binary.mkdir()
        fake = binary / "git"
        fake.write_text('#!/bin/sh\nexit 29\n')
        fake.chmod(0o755)
        self.env["PATH"] = str(binary) + os.pathsep + os.environ["PATH"]
        result = self.run_cnew("failed")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("left", result.stderr)
        self.assertEqual(list((self.base / "failed").iterdir()), [])
        self.assertIn("refusing existing path", self.run_cnew("failed").stderr)

    def test_file_appearing_during_initialization_is_not_overwritten(self):
        binary = self.root / "bin"
        binary.mkdir()
        real_git = shutil.which("git")
        fake = binary / "git"
        fake.write_text('#!/bin/sh\n' + shlex.quote(real_git) + ' "$@" || exit $?\n'
                        'if [ "$1" = init ]; then\n  for target do :; done\n'
                        '  printf "concurrent content\\n" > "$target/README.md"\nfi\n')
        fake.chmod(0o755)
        self.env["PATH"] = str(binary) + os.pathsep + os.environ["PATH"]
        result = self.run_cnew("race")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scaffolding failed", result.stderr)
        self.assertEqual((self.base / "race/README.md").read_text(), "concurrent content\n")
        self.assertFalse((self.base / "race/AGENTS.md").exists())
