#!/usr/bin/env python3
"""Tests for the gate that keeps the README's list of checks honest.

Run: python -m unittest discover -s scripts -t scripts
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_documented_gates as gate                             # noqa: E402


WORKFLOW = """name: Validate
on:
  pull_request:
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - name: A gate
        run: python scripts/check_one.py
      - name: Another
        run: python scripts/check_two.py --check
"""


def readme(*commands):
    body = "\n".join(commands)
    return (f"# Repo\n\nIntro.\n\n{gate.HEADING}\n\nWords.\n\n"
            f"```bash\n{body}\n```\n\n## Licensing\n\npython scripts/not_a_gate.py\n")


class Workflows(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, name, text):
        with open(os.path.join(self.dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def test_it_finds_the_commands_a_pull_request_runs(self):
        self.write("validate.yml", WORKFLOW)
        found = gate.commands_in_workflows(self.dir)
        self.assertEqual(set(found),
                         {"python scripts/check_one.py",
                          "python scripts/check_two.py --check"})

    def test_the_bare_on_key_is_not_read_as_the_boolean_true(self):
        """PyYAML parses `on:` as True. Reading only the string key finds nothing, in every
        workflow, and the gate passes on an empty set — green while checking nothing."""
        self.write("validate.yml", WORKFLOW)
        self.assertTrue(gate.commands_in_workflows(self.dir))

    def test_a_workflow_without_a_pull_request_trigger_is_ignored(self):
        """The weekly sync also runs python. It is not something a reader can run to check
        this repository, and promising it in that list would be promising a cron."""
        self.write("weekly.yml", WORKFLOW.replace("  pull_request:", "  schedule:\n"
                                                  "    - cron: '17 6 * * 1'"))
        self.assertEqual(gate.commands_in_workflows(self.dir), {})

    def test_a_conditional_job_is_ignored(self):
        """The LLM-judge eval job is manual and spends tokens."""
        self.write("evals.yml", WORKFLOW.replace(
            "    runs-on: ubuntu-latest",
            "    if: github.event_name == 'workflow_dispatch'\n    runs-on: ubuntu-latest"))
        self.assertEqual(gate.commands_in_workflows(self.dir), {})

    def test_a_conditional_step_is_ignored(self):
        self.write("validate.yml", WORKFLOW.replace(
            "      - name: Another\n",
            "      - name: Another\n        if: always()\n"))
        self.assertEqual(set(gate.commands_in_workflows(self.dir)),
                         {"python scripts/check_one.py"})


class Readme(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "README.md")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, text):
        with open(self.path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def test_it_reads_only_the_section_it_is_about(self):
        """A python line under a later heading is not a promise about checking."""
        self.write(readme("python scripts/check_one.py"))
        self.assertEqual(gate.commands_in_readme(self.path),
                         ["python scripts/check_one.py"])

    def test_a_trailing_comment_is_not_part_of_the_command(self):
        """Every line in that block carries one, and comparing them would make the gate
        fail over a reworded explanation."""
        self.write(readme("python scripts/check_one.py   # what it does"))
        self.assertEqual(gate.commands_in_readme(self.path),
                         ["python scripts/check_one.py"])

    def test_verbosity_is_not_a_disagreement(self):
        """CI wants unittest's -v and a reader does not. The two lists still describe the
        same run, and a gate that cried wolf here is a gate someone switches off."""
        self.assertEqual(gate._normalise("python -m unittest discover -s x -t x -v"),
                         gate._normalise("python -m unittest discover -s x -t x"))

    def test_an_argument_that_changes_the_behaviour_is_a_disagreement(self):
        """`--check` is the difference between a gate and a tool that rewrites the tree."""
        self.assertNotEqual(gate._normalise("python scripts/refresh.py --check"),
                            gate._normalise("python scripts/refresh.py"))

    def test_a_missing_section_is_an_error_not_a_pass(self):
        self.write("# Repo\n\nNo such section.\n")
        self.assertIsNone(gate.commands_in_readme(self.path))


class Repository(unittest.TestCase):
    def test_the_real_readme_and_the_real_workflows_agree(self):
        """The gate against the tree it ships with. This is the assertion the issue asked
        for: the section promising the repository can be checked was itself wrong."""
        ci = gate.commands_in_workflows()
        documented = gate.commands_in_readme()
        self.assertIsNotNone(documented)
        self.assertEqual(sorted(ci), sorted(documented))

    def test_it_is_watching_a_real_number_of_checks(self):
        """A rule that quietly matched nothing would pass forever. Twelve today; the floor
        is what stops an empty set from reading as agreement."""
        self.assertGreaterEqual(len(gate.commands_in_workflows()), 8)


if __name__ == "__main__":
    unittest.main()
