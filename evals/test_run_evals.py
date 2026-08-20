#!/usr/bin/env python3
"""Tests for the accuracy evals. Run: python -m unittest discover -s evals"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run_evals  # noqa: E402
from run_evals import accuracy_eval, find_function, retrieval_rank  # noqa: E402


CATALOG = {
    "functions": [
        {"name": "CALCULATE", "file": "calculate", "primaryCategory": "filter",
         "returns": "scalar", "appliesTo": ["measure", "column", "table"],
         "discouragedInVisualCalculations": False, "notes": True,
         "summary": "Evaluates an expression in a modified filter context."},
        {"name": "DATEADD", "file": "dateadd", "primaryCategory": "time-intelligence",
         "returns": "table", "appliesTo": ["measure", "column", "table"],
         "discouragedInVisualCalculations": True, "notes": False,
         "summary": "Returns a table of dates shifted forward or backward in time."},
    ]
}


class FindFunction(unittest.TestCase):
    def test_it_finds_by_name(self):
        self.assertEqual(find_function(CATALOG, "CALCULATE")["file"], "calculate")

    def test_it_is_case_insensitive(self):
        self.assertIsNotNone(find_function(CATALOG, "calculate"))

    def test_an_unknown_name_is_none(self):
        self.assertIsNone(find_function(CATALOG, "NOSUCHFUNCTION"))


class RetrievalRank(unittest.TestCase):
    """The catalog summary is what an agent scans. If it loses the words a user would
    actually type, the function stops being findable even though the card is perfect."""

    def test_the_right_function_ranks_first(self):
        self.assertEqual(
            retrieval_rank(CATALOG, "evaluate an expression in a modified filter context",
                           "CALCULATE"), 1)

    def test_a_function_whose_summary_shares_nothing_ranks_last(self):
        self.assertGreater(
            retrieval_rank(CATALOG, "shifted forward or backward in time", "CALCULATE"), 1)

    def test_an_unknown_function_has_no_rank(self):
        self.assertIsNone(retrieval_rank(CATALOG, "anything", "NOSUCHFUNCTION"))

    def test_a_tie_does_not_push_a_function_down_the_list(self):
        # Puesto por competicion: las que empatan comparten posicion. Con desempate
        # alfabetico, DIVIDE caia al 4 empatada con BITAND/BITOR/BITXOR y el eval
        # reportaba un fallo de recuperacion que no existia.
        tied = {"functions": [
            {"name": "AAA", "summary": "shared word"},
            {"name": "ZZZ", "summary": "shared word"},
        ]}
        self.assertEqual(retrieval_rank(tied, "shared word", "ZZZ"), 1)
        self.assertEqual(retrieval_rank(tied, "shared word", "AAA"), 1)


class AccuracyEval(unittest.TestCase):
    def run_cases(self, cases, top_n=3):
        # El catalogo de prueba tiene dos funciones, asi que el umbral real (3) no puede
        # dispararse nunca aqui. Los casos que prueban el ranking pasan top_n=1.
        return accuracy_eval(CATALOG, cases, top_n=top_n)

    def test_a_case_that_matches_passes(self):
        code, fails = self.run_cases([{
            "prompt": "evaluate an expression in a modified filter context",
            "expectFunction": "CALCULATE",
            "expectFlag": {"notes": True, "discouragedInVisualCalculations": False},
        }])
        self.assertEqual((code, fails), (0, []))

    def test_a_missing_function_fails(self):
        code, fails = self.run_cases([{"prompt": "x", "expectFunction": "GHOST"}])
        self.assertEqual(code, 1)
        self.assertIn("GHOST", fails[0])

    def test_a_wrong_flag_fails(self):
        code, fails = self.run_cases([{
            "prompt": "evaluate an expression in a modified filter context",
            "expectFunction": "CALCULATE",
            "expectFlag": {"discouragedInVisualCalculations": True},
        }])
        self.assertEqual(code, 1)
        self.assertIn("discouragedInVisualCalculations", fails[0])

    def test_an_unknown_flag_name_fails_rather_than_passing_silently(self):
        # A typo in the case file must not read as "nothing to check".
        code, fails = self.run_cases([{
            "prompt": "evaluate an expression in a modified filter context",
            "expectFunction": "CALCULATE",
            "expectFlag": {"discourage": True},
        }])
        self.assertEqual(code, 1)
        self.assertIn("discourage", fails[0])

    def test_a_function_that_cannot_be_retrieved_fails(self):
        # The card can be perfect and still be unreachable: this is the summary rotting.
        code, fails = self.run_cases([{
            "prompt": "shifted forward or backward in time",
            "expectFunction": "CALCULATE",
        }], top_n=1)
        self.assertEqual(code, 1)
        self.assertIn("CALCULATE", fails[0])

    def test_no_accuracy_cases_is_not_a_failure(self):
        self.assertEqual(self.run_cases([]), (0, []))

    def test_a_prompt_that_matches_nothing_fails(self):
        # retrieval_rank cuenta las que puntuan MAS, asi que si nadie puntua, todas empatan
        # a cero y la esperada sale "primera". Sin esta comprobacion, un prompt que no
        # comparte una sola palabra con el catalogo pasaba como recuperacion perfecta.
        code, fails = self.run_cases([{
            "prompt": "zzzz qqqq xxxx",
            "expectFunction": "CALCULATE",
        }])
        self.assertEqual(code, 1)
        self.assertIn("CALCULATE", fails[0])

    def test_a_case_without_expectFunction_is_malformed_not_skipped(self):
        # Dentro de accuracy: no hay casos "de otro tipo". Un expectFuncton mal escrito
        # dejaba la entrada sin comprobar y el conjunto decia OK.
        code, fails = self.run_cases([{"prompt": "x", "expectFuncton": "CALCULATE"}])
        self.assertEqual(code, 1)
        self.assertIn("expectFunction", fails[0])


class MissingCatalog(unittest.TestCase):
    """Con casos escritos y sin catalogo, decir OK es afirmar que se comprobo algo. Un PR
    que borre o no genere el catalogo tiene que ponerse rojo, no verde."""

    def test_no_catalog_with_cases_fails(self):
        code, fails = accuracy_eval(None, [{"prompt": "x", "expectFunction": "CALCULATE"}])
        self.assertEqual(code, 1)
        self.assertIn("catalog", fails[0].lower())

    def test_no_catalog_without_cases_is_fine(self):
        self.assertEqual(accuracy_eval(None, []), (0, []))


if __name__ == "__main__":
    unittest.main()
