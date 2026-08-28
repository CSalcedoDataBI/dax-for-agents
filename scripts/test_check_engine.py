#!/usr/bin/env python3
"""Tests for the catalogue-against-engine comparison.

Run: python -m unittest discover -s scripts -t scripts

The comparison itself is offline and pure, so it is tested here and runs in CI. Only the
one query that reads the engine needs Power BI Desktop, and that is why `check_engine.py`
lives in `lab/` beside `check_lab.py` rather than in `scripts/`.
"""
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "lab"))

import check_engine                                               # noqa: E402


BASE = {"documented_not_in_engine": {"SHADOWCLUSTER": "preview"},
        "in_engine_not_documented": {"NATURALJOINUSAGE": "no page upstream"}}


class Compare(unittest.TestCase):
    def test_the_recorded_differences_are_not_problems(self):
        """The two lists never match exactly, and that is not a defect. A gate that failed
        on the known differences would fail every run and be switched off."""
        problems, only_docs, only_engine = check_engine.compare(
            engine={"ABS", "NATURALJOINUSAGE"},
            documented={"ABS", "SHADOWCLUSTER"},
            baseline=BASE)
        self.assertEqual(problems, [])
        self.assertEqual(only_docs, {"SHADOWCLUSTER"})
        self.assertEqual(only_engine, {"NATURALJOINUSAGE"})

    def test_a_new_undocumented_engine_function_is_a_problem(self):
        """The library missing a function the engine has is the gap this exists to find."""
        problems, _, _ = check_engine.compare(
            engine={"ABS", "NATURALJOINUSAGE", "BRANDNEW"},
            documented={"ABS", "SHADOWCLUSTER"},
            baseline=BASE)
        self.assertEqual(len(problems), 1)
        self.assertIn("BRANDNEW", problems[0])

    def test_a_new_documented_function_the_engine_lacks_is_a_problem(self):
        problems, _, _ = check_engine.compare(
            engine={"ABS", "NATURALJOINUSAGE"},
            documented={"ABS", "SHADOWCLUSTER", "GHOST"},
            baseline=BASE)
        self.assertEqual(len(problems), 1)
        self.assertIn("GHOST", problems[0])

    def test_good_news_fails_too(self):
        """A baseline entry that has resolved is good news, and good news nobody records
        rots into folklore — the next reader believes a file that is describing last year."""
        problems, _, _ = check_engine.compare(
            engine={"ABS", "NATURALJOINUSAGE", "SHADOWCLUSTER"},
            documented={"ABS", "SHADOWCLUSTER"},
            baseline=BASE)
        self.assertEqual(len(problems), 1)
        self.assertIn("good news", problems[0])

    def test_a_card_appearing_for_an_undocumented_function_fails_too(self):
        problems, _, _ = check_engine.compare(
            engine={"ABS", "NATURALJOINUSAGE"},
            documented={"ABS", "SHADOWCLUSTER", "NATURALJOINUSAGE"},
            baseline=BASE)
        self.assertEqual(len(problems), 1)
        self.assertIn("good news", problems[0])


class Baseline(unittest.TestCase):
    def setUp(self):
        self.baseline = check_engine.load_baseline()

    def test_every_recorded_difference_carries_a_reason(self):
        """`--record` writes 'TODO: say why' for anything new. A list of names with no
        reasons is a list nobody can review, which is the same as no baseline at all."""
        for side in ("documented_not_in_engine", "in_engine_not_documented"):
            for name, reason in self.baseline[side].items():
                self.assertNotIn("TODO", reason, f"{name} has no reason yet")
                self.assertGreater(len(reason), 20, f"{name}'s reason says nothing")

    def test_the_nine_are_the_uncategorised_ones(self):
        """The correlation the baseline claims, asserted against the tree rather than
        trusted. If a future sync gives one of them a category, this goes red and the note
        gets re-read instead of surviving as a story."""
        path = os.path.join(ROOT, "skills", "dax-reference", "generated", "catalog.json")
        with open(path, encoding="utf-8") as f:
            catalog = json.load(f)
        uncategorised = {f["name"] for f in catalog["functions"]
                         if not f["primaryCategory"]}
        missing = set(self.baseline["documented_not_in_engine"])
        self.assertTrue(missing <= uncategorised,
                        f"no longer uncategorised: {sorted(missing - uncategorised)}")


if __name__ == "__main__":
    unittest.main()
