#!/usr/bin/env python3
"""Tests for the stable builder. Run: python -m unittest discover -s scripts"""
import io
import os
import shutil
import subprocess
import sys
import contextlib
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_stable  # noqa: E402
from build_stable import build, plugin_tree, problems, tree_files  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid")


class Repo:
    """A throwaway repo: a full-tree `stable` like today's, then a main with the plugin folder."""

    def __init__(self):
        self.dir = tempfile.mkdtemp()
        self.git("init", "-q", "-b", "main")
        self.put("README.md", "root")
        self.put("scripts/tool.py", "print(1)")
        self.put(".claude-plugin/plugin.json", "{}")
        self.commit("old layout")
        self.git("branch", "stable")
        self.git("rm", "-q", ".claude-plugin/plugin.json")
        self.put("plugins/dax-for-agents/.claude-plugin/plugin.json", '{"name": "dax"}')
        self.put("plugins/dax-for-agents/skills/a/SKILL.md", "---\nname: a\n---\n")
        self.put("plugins/dax-for-agents/LICENSE.md", "MIT")
        self.commit("move")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.dir, capture_output=True, text=True,
                              check=True, env=ENV).stdout.strip()

    def put(self, rel, text):
        path = os.path.join(self.dir, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def commit(self, msg):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)


def with_env(fn):
    def run(self):
        old = {k: os.environ.get(k) for k in ENV if k.startswith("GIT_")}
        os.environ.update({k: v for k, v in ENV.items() if k.startswith("GIT_")})
        try:
            fn(self)
        finally:
            for k, v in old.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    return run


class TheReleaseCommit(unittest.TestCase):
    @with_env
    def test_its_root_is_the_plugin_folder_and_nothing_else(self):
        with Repo() as r:
            sha, tree, created = build("main", r.git("rev-parse", "stable"), "release", cwd=r.dir)
            self.assertTrue(created)
            self.assertEqual(tree_files(tree, cwd=r.dir), [".claude-plugin/plugin.json",
                                                           "LICENSE.md", "skills/a/SKILL.md"])

    @with_env
    def test_it_fast_forwards_stable_whatever_its_history(self):
        # Today's stable is the whole repo; a subtree split would not descend from it.
        with Repo() as r:
            old = r.git("rev-parse", "stable")
            sha, _, _ = build("main", old, "release", cwd=r.dir)
            self.assertEqual(r.git("rev-list", "--parents", "-n", "1", sha).split()[1:], [old])
            r.git("merge-base", "--is-ancestor", old, sha)  # raises if not a fast-forward

    @with_env
    def test_a_second_build_of_the_same_tree_creates_nothing(self):
        with Repo() as r:
            first, _, _ = build("main", r.git("rev-parse", "stable"), "release", cwd=r.dir)
            again, _, created = build("main", first, "release", cwd=r.dir)
            self.assertFalse(created)
            self.assertEqual(again, first)

    def test_a_rev_without_the_plugin_folder_fails_loudly(self):
        with Repo() as r:
            with self.assertRaises(RuntimeError):
                plugin_tree("stable", cwd=r.dir)


class TheCheck(unittest.TestCase):
    def test_a_clean_plugin_tree_passes(self):
        self.assertEqual(problems([".claude-plugin/plugin.json", "README.md",
                                   "skills/a/SKILL.md", "skills/a/x.json"]), [])

    def test_a_script_or_a_missing_manifest_fails(self):
        self.assertEqual(len(problems([".claude-plugin/plugin.json", "skills/a/run.py"])), 1)
        self.assertTrue(any("plugin.json" in e for e in problems(["README.md"])))


class TheRealRepo(unittest.TestCase):
    def test_head_builds_a_tree_the_directory_accepts(self):
        tree = plugin_tree("HEAD")
        files = tree_files(tree)
        self.assertEqual(problems(files), [], files)
        self.assertIn("LICENSE.md", files)
        self.assertFalse([f for f in files if f.startswith((".git", "scripts/", "lab/"))])

    def test_a_bad_rev_fails_in_one_line(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = build_stable.main(["--rev", "no-such-rev", "--parent", ""])
        self.assertEqual(code, 1)
        self.assertTrue(out.getvalue().startswith("FAIL: "), out.getvalue())

    def test_the_dry_run_lists_the_files_and_pushes_nothing(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = build_stable.main(["--rev", "HEAD", "--parent", ""])
        self.assertEqual(code, 0)
        self.assertIn(".claude-plugin/plugin.json", out.getvalue())
        self.assertNotIn("Pushed", out.getvalue())


if __name__ == "__main__":
    unittest.main()
