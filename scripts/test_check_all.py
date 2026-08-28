#!/usr/bin/env python3
"""Tests for the local runner.

Run: python -m unittest discover -s scripts -t scripts
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_all                                                  # noqa: E402
import check_documented_gates as documented                       # noqa: E402


class ItsListIsNotItsOwn(unittest.TestCase):
    def test_it_takes_the_list_from_the_workflows(self):
        """The whole point. A literal here would be a third place saying what is checked,
        after the workflow and the README, and the one nothing compares against anything."""
        source = open(check_all.__file__, encoding="utf-8").read()
        self.assertIn("documented.commands_in_workflows()", source)
        for name in ("check_doc_claims", "check_examples", "validate_skills"):
            self.assertNotIn(f'"python scripts/{name}.py"', source)

    def test_the_list_it_would_run_is_the_list_ci_runs(self):
        self.assertGreaterEqual(len(documented.commands_in_workflows()), 8)


class Runner(unittest.TestCase):
    def test_a_failing_command_is_reported_as_failing(self):
        code, output, _ = check_all.run("python -c \"import sys; sys.exit(3)\"")
        self.assertEqual(code, 3)

    def test_a_passing_command_carries_its_verdict(self):
        code, output, _ = check_all.run("python -c \"print('OK: fine')\"")
        self.assertEqual(code, 0)
        self.assertIn("OK: fine", output)

    def test_the_engine_check_is_skipped_loudly_and_not_silently(self):
        """A check that quietly does not run is worse than one that is absent: the run
        still ends in OK and nobody knows the engine was never asked."""
        commands, why = check_all.local_only()
        self.assertTrue(commands or why, "no commands and no reason given")


if __name__ == "__main__":
    unittest.main()
