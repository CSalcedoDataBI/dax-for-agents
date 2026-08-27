#!/usr/bin/env python3
"""Fail when the README's list of checks and the checks CI runs disagree.

The README has a section called "Checking it yourself" whose whole argument is that
nothing here asks to be taken on trust. It listed four gates while CI ran seven, and the
two it omitted — the credential sweep and the Actions cost rules — are the two a reader is
most likely to care about. That is the one paragraph in the repository that cannot be
approximately right.

It had already cost something outside the repo: the session that wrote the long-form
article quoted the README's four and published the wrong number, because it read prose
where it should have read the workflow.

`check_doc_claims.py` does not catch this and should not: there is no number beside a noun
here, and stretching that gate to parse fenced blocks would make it argue with prose it has
no business reading. So this is its own check, and it compares two lists rather than a
count.

Which commands count:

  Every `python ...` line in a step of a job with no `if:`, in a workflow triggered by
  `pull_request`.

That rule, rather than naming validate-skills.yml, so a new unconditional gate anywhere is
picked up on its own. A step or a job behind an `if:` is conditional by definition — the
LLM-judge eval job is manual and costs tokens — and a list that promised it would be
promising something that does not run.

Run: python scripts/check_documented_gates.py
"""
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed (pip install pyyaml)")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(ROOT, ".github", "workflows")
README = os.path.join(ROOT, "README.md")

HEADING = "## Checking it yourself"
_PYTHON_LINE = re.compile(r"^\s*(python\s+\S.*?)\s*(?:#.*)?$")


def _normalise(command):
    """One spelling per command, so formatting is never the finding.

    Arguments stay: `--check` is the difference between a gate and a tool that rewrites the
    tree, and a list that dropped it would be describing something else.

    `-v` is the exception, and it is the only one. It changes how much unittest prints, not
    what it runs, and CI wants the noise while a person reading the README does not. A gate
    that failed over it would be arguing about verbosity in the name of trust, which is the
    cry-wolf failure the other gates in this repository are careful to avoid.
    """
    words = [w for w in command.split() if w not in ("-v", "--verbose")]
    return " ".join(words)


def commands_in_workflows(directory=WORKFLOWS):
    """Every python command CI runs unconditionally on a pull request."""
    found = {}
    for path in sorted(glob.glob(os.path.join(directory, "*.yml"))):
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
        # PyYAML reads the bare key `on:` as the boolean True. Reading only "on" is how a
        # checker silently passes on every workflow in the repository.
        triggers = doc.get("on", doc.get(True)) or {}
        if isinstance(triggers, str):
            triggers = {triggers: None}
        if isinstance(triggers, list):
            triggers = {t: None for t in triggers}
        if "pull_request" not in triggers:
            continue
        for job in (doc.get("jobs") or {}).values():
            if not isinstance(job, dict) or job.get("if") is not None:
                continue
            for step in job.get("steps") or []:
                if not isinstance(step, dict) or step.get("if") is not None:
                    continue
                for line in str(step.get("run", "")).splitlines():
                    m = _PYTHON_LINE.match(line)
                    if m:
                        found[_normalise(m.group(1))] = os.path.basename(path)
    return found


def commands_in_readme(path=README):
    """The python commands inside the fenced blocks under "Checking it yourself"."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    at = text.find(HEADING)
    if at == -1:
        return None
    # To the next section of the same level, so a later `## Licensing` block cannot be
    # read as part of the promise.
    end = text.find("\n## ", at + len(HEADING))
    section = text[at:end if end != -1 else len(text)]

    commands, inside = [], False
    for line in section.splitlines():
        if line.startswith("```"):
            inside = not inside
            continue
        if inside:
            m = _PYTHON_LINE.match(line)
            if m:
                commands.append(_normalise(m.group(1)))
    return commands


def main():
    ci = commands_in_workflows()
    documented = commands_in_readme()
    if documented is None:
        print(f"ERROR: README.md has no '{HEADING}' section to check.")
        return 1

    missing = [c for c in ci if c not in documented]
    extra = [c for c in documented if c not in ci]
    if not missing and not extra:
        print(f"OK: the README lists the {len(ci)} check(s) CI runs on every pull request.")
        return 0

    print("ERROR: the README and CI disagree about what is checked.")
    for c in sorted(missing):
        print(f"  - CI runs it, the README does not list it: {c}   ({ci[c]})")
    for c in sorted(extra):
        print(f"  - the README lists it, CI does not run it on a pull request: {c}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
