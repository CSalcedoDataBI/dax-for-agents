#!/usr/bin/env python3
"""Tests for the typeable-name gate.

Run: python -m unittest discover -s scripts -t scripts
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_function_names as gate                               # noqa: E402


def catalog(*names):
    return {"functions": [{"name": n, "file": n.lower()} for n in names]}


class Pattern(unittest.TestCase):
    def test_a_plain_name_passes(self):
        self.assertEqual(gate.offenders(catalog("CALCULATE", "SUMX")), [])

    def test_a_dotted_name_passes(self):
        self.assertEqual(gate.offenders(catalog("INFO.VIEW.TABLES", "ISO.CEILING")), [])

    def test_a_space_is_the_finding(self):
        """`DISTINCT column` is what shipped. It is Microsoft's label for one of two pages
        of the same function, and no engine will accept it."""
        self.assertEqual(gate.offenders(catalog("DISTINCT column")), ["DISTINCT column"])

    def test_a_lower_case_character_is_the_finding_too(self):
        """`T.INV.2t`, from a typo in Microsoft's own statistical index. DAX does not care
        about case, so this one would still run — but the reference states it wrong, and
        stating things right is the only product here."""
        self.assertEqual(gate.offenders(catalog("T.INV.2t")), ["T.INV.2t"])

    def test_a_name_starting_with_a_digit_is_not_a_name(self):
        self.assertEqual(gate.offenders(catalog("2FAST")), ["2FAST"])


class Repository(unittest.TestCase):
    def test_the_shipped_catalogue_is_clean(self):
        with open(os.path.join(gate.GENERATED, "catalog.json"), encoding="utf-8") as f:
            self.assertEqual(gate.offenders(json.load(f)), [])

    def test_the_two_distinct_pages_are_still_two_cards(self):
        """The repair renames; it does not merge. Microsoft publishes two pages and the
        overloads behave differently, so collapsing them would lose a card — the fix for a
        wrong name must not become a smaller library."""
        with open(os.path.join(gate.GENERATED, "catalog.json"), encoding="utf-8") as f:
            functions = json.load(f)["functions"]
        distinct = [f for f in functions if f["name"] == "DISTINCT"]
        self.assertEqual(len(distinct), 2)
        self.assertEqual(sorted(f["file"] for f in distinct), ["distinct", "distinct-table"])
        self.assertNotEqual(distinct[0]["summary"], distinct[1]["summary"])

    def test_the_normalisation_is_the_syncs_own(self):
        """One definition. A second opinion here and the repair would drift away from what
        the next regeneration produces, which is how the tree got two names it could not
        use in the first place."""
        self.assertEqual(gate.sync.function_name("DISTINCT column"), "DISTINCT")


if __name__ == "__main__":
    unittest.main()
