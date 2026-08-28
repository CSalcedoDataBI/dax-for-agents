#!/usr/bin/env python3
"""Tests for the invented-function counter.

Run: python -m unittest discover -s evals -t evals

Everything here is offline. The counter is the part of the A/B that has to be trustworthy
without a model in the loop: if it over-counts, the headline number is inflated; if it
under-counts, the whole measurement quietly reads zero — which is exactly what a broken
extractor looks like from the outside, and why `test_it_counts_the_real_functions_too`
exists.
"""
import os
import sys
import unittest

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run_ab                                                     # noqa: E402


NAMES, CATALOG = run_ab.catalog_names()


class Extractor(unittest.TestCase):
    def test_a_name_followed_by_a_paren_is_a_call(self):
        self.assertEqual(run_ab.called_functions("Use CALCULATE( ... )"), ["CALCULATE"])

    def test_a_name_without_a_paren_is_not(self):
        """`Sales[Amount]` and prose about ALL should not be read as calls."""
        self.assertEqual(run_ab.called_functions("The ALL behaviour of Sales[Amount]"), [])

    def test_a_dotted_name_stays_whole(self):
        """Splitting on the dot would report INFO, VIEW and TABLES — three inventions per
        mention of one real function."""
        self.assertEqual(run_ab.called_functions("EVALUATE INFO.VIEW.TABLES()"),
                         ["INFO.VIEW.TABLES"])

    def test_statements_are_not_counted(self):
        """A keyword written with a parenthesis would land in BOTH arms identically and
        add noise to the only number that matters, which is the difference."""
        self.assertEqual(run_ab.called_functions("EVALUATE ( ROW(\"a\", 1) )"), ["ROW"])

    def test_a_name_is_counted_once_however_often_it_appears(self):
        """The metric is distinct invented names. Counting mentions would score a model
        that repeats one wrong name in a code block worse than one that invents three."""
        self.assertEqual(run_ab.called_functions("SUM( SUM( SUM(x) ) )"), ["SUM"])

    def test_it_counts_the_real_functions_too(self):
        """The guard against a silent zero. An extractor that finds nothing reports no
        inventions and looks like a perfect score, so a run whose answers cite no function
        at all has to be distinguishable from a run that cites only real ones."""
        called = run_ab.called_functions("CALCULATE( [Sales], SAMEPERIODLASTYEAR(D[Date]) )")
        self.assertEqual(called, ["CALCULATE", "SAMEPERIODLASTYEAR"])
        self.assertEqual(run_ab.invented("CALCULATE( [Sales] )", NAMES), [])


class Invented(unittest.TestCase):
    def test_a_function_that_does_not_exist_is_reported(self):
        self.assertEqual(run_ab.invented("Use PREVIOUSYEARTOTAL([Sales])", NAMES),
                         ["PREVIOUSYEARTOTAL"])

    def test_a_function_that_exists_is_not(self):
        self.assertEqual(run_ab.invented("Use SAMEPERIODLASTYEAR(D[Date])", NAMES), [])

    def test_the_pilot_findings_are_still_findings(self):
        """The three the pilot caught, kept as a regression on the counter rather than on
        the model. `EVALUATE TMSCHEMA_MEASURES()` is a DMV table written as if it were a
        DAX function; `AXIS()` was invented outright, with a signature, inside a real
        function. If a later catalogue makes one of these real, this goes red and the
        finding gets re-read instead of quietly surviving as folklore."""
        for name in ("TMSCHEMA_MEASURES", "AXIS"):
            self.assertNotIn(name, NAMES)
            self.assertEqual(run_ab.invented(f"{name}(x)", NAMES), [name])


class Bank(unittest.TestCase):
    def setUp(self):
        with open(run_ab.QUESTIONS, encoding="utf-8") as f:
            self.questions = yaml.safe_load(f)["questions"]

    def test_every_trap_really_is_absent_from_the_catalogue(self):
        """Four of the first draft's traps were real functions — INFO.TABLES,
        INFO.MEASURES, INFO.RELATIONSHIPS and ROLLUP. Naming a real function is not
        inventing one, and a bank that says otherwise describes the wrong failure."""
        for q in self.questions:
            for trap in q.get("traps", []):
                self.assertNotIn(trap, NAMES,
                                 f"{q['id']}: '{trap}' is listed as a trap but exists")

    def test_every_question_has_a_category_that_holds_functions(self):
        """Arm B is the catalogue rows for the category. An empty category makes arm B
        identical to arm A and the question measures nothing — which is what happened
        with a `visual-calculations` category that does not exist."""
        for q in self.questions:
            rows = run_ab.category_rows(CATALOG, q["category"])
            self.assertTrue(rows.strip(), f"{q['id']}: category {q['category']!r} is empty")

    def test_both_regimes_are_represented(self):
        """The design requirement: the classic-model half is where all 31 notes and 99
        example files are, and averaging it with INFO.* and visual calculations produces a
        number that does not say which half it describes."""
        regimes = {q["regime"] for q in self.questions}
        self.assertIn("classic", regimes)
        self.assertTrue({"info", "visual"} & regimes)


if __name__ == "__main__":
    unittest.main()
