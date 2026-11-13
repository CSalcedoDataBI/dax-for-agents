#!/usr/bin/env python3
"""Build the commit that `stable` moves to on a release: the plugin folder alone, at its root.

The plugin directory listing reads `stable` with its plugin path set to the repository root,
and a submission's repository and path cannot change -- only its branch. So the root of
`stable` has to BE the plugin: `.claude-plugin/plugin.json`, `skills/`, the README and the
license, and nothing the directory refuses from an organization that is not Verified.

`main` keeps the plugin in `plugins/dax-for-agents/`. For each release this script takes the
tree of that folder at the release commit and wraps it in a new commit whose single parent is
the current `stable`:

    git commit-tree <rev>:plugins/dax-for-agents -p <stable> -m "release vX.Y.Z"

That is always a fast-forward of `stable`, whatever its history, so nothing is ever
force-pushed and what a reviewer already read is never rewritten. A plain `git subtree split`
is not: its history does not descend from today's `stable`.

    python scripts/build_stable.py --rev v0.10.0                 # dry run: build, list, check
    python scripts/build_stable.py --rev HEAD --label v0.10.0 --push   # CI, on release_created
    python scripts/build_stable.py --rev HEAD --export <dir>     # write the tree, to measure it

The dry run prints every file of the resulting tree and fails when one is a refused type or
the root has no `.claude-plugin/plugin.json`. --push runs the same check first.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_plugin_manifest import PLUGIN_DIR, type_errors  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANCH = "stable"


def git(*args, cwd=ROOT, env=None):
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                         encoding="utf-8", env=env)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout.strip()


def plugin_tree(rev, cwd=ROOT):
    return git("rev-parse", f"{rev}^{{commit}}:{PLUGIN_DIR}", cwd=cwd)


def tree_files(tree, cwd=ROOT):
    return sorted(git("ls-tree", "-r", "--name-only", tree, cwd=cwd).splitlines())


def problems(files):
    errors = [e.replace(f"{PLUGIN_DIR}/", "") for e in type_errors(files)]
    if ".claude-plugin/plugin.json" not in files:
        errors.append("the tree has no .claude-plugin/plugin.json at its root")
    return errors


def build(rev, parent, message, cwd=ROOT):
    """(sha, tree, created). Reuses `parent` when its tree is already the plugin's."""
    tree = plugin_tree(rev, cwd)
    if parent and git("rev-parse", f"{parent}^{{tree}}", cwd=cwd) == tree:
        return parent, tree, False
    args = ["commit-tree", tree, "-m", message]
    if parent:
        args[2:2] = ["-p", parent]
    return git(*args, cwd=cwd), tree, True


def export(tree, out, cwd=ROOT):
    """Write `tree` under `out`, for measure_plugin.py."""
    os.makedirs(out, exist_ok=True)
    for rel in tree_files(tree, cwd):
        path = os.path.join(out, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = subprocess.run(["git", "cat-file", "blob", f"{tree}:{rel}"], cwd=cwd,
                              capture_output=True, check=True).stdout
        with open(path, "wb") as f:
            f.write(data)


def current_stable(remote="origin", cwd=ROOT):
    try:
        return git("rev-parse", "--verify", "--quiet", f"refs/remotes/{remote}/{BRANCH}", cwd=cwd)
    except RuntimeError:
        return ""


def main(argv=None):
    try:
        return _main(argv)
    except RuntimeError as exc:
        # One line, not a traceback: the usual causes are a --rev without the plugin
        # folder, or a push refused because stable moved since the fetch (nothing forced).
        print(f"FAIL: {exc}")
        return 1


def _main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--rev", required=True, help="the release tag or commit")
    ap.add_argument("--parent", help="the commit stable is at (default: origin/stable)")
    ap.add_argument("--push", action="store_true", help="push to refs/heads/stable")
    ap.add_argument("--export", metavar="DIR", help="write the resulting tree to DIR")
    ap.add_argument("--label", help="name for the commit message (default: --rev)")
    ap.add_argument("--remote", default="origin")
    a = ap.parse_args(argv)

    parent = a.parent if a.parent is not None else current_stable(a.remote)
    sha, tree, created = build(a.rev, parent, f"release {a.label or a.rev}\n\nThe tree of {PLUGIN_DIR}/ "
                               f"at {git('rev-parse', a.rev)}.")
    files = tree_files(tree)
    for rel in files:
        print(f"  {rel}")
    print(f"{len(files)} files in the tree of {PLUGIN_DIR}/ at {a.rev}"
          f" -> {'new commit' if created else 'stable already holds it'} {sha[:7]}"
          f" (parent {parent[:7] if parent else 'none'})")
    errors = problems(files)
    for e in errors:
        print(f"FAIL: {e}")
    if errors:
        return 1
    if a.export:
        export(tree, a.export)
        print(f"Wrote the tree to {a.export}")
    if a.push:
        if not created:
            print("Nothing to push.")
            return 0
        # No force, ever: the new commit's parent is the remote stable, so this is a
        # fast-forward, and if stable moved in between the push fails instead of rewriting it.
        git("push", a.remote, f"{sha}:refs/heads/{BRANCH}")
        print(f"Pushed {sha[:7]} to {BRANCH}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
