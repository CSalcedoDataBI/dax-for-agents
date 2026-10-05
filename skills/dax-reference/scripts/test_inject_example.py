#!/usr/bin/env python3
"""Tests for the example injector.

Run: python -m unittest discover -s skills/dax-reference/scripts

Offline: the master is the repo's own lab/contoso, never the release download. What these
prove is the shape — the measure lands in TMDL, the page opens first, a bad reference is
refused before anything is written. That the numbers are right was measured once by opening
the result in Power BI Desktop (CALCULATE vs KEEPFILTERS, 2026-10-05); no test here can.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "inject_example.py")
MASTER = os.path.normpath(os.path.join(HERE, "..", "..", "..", "lab", "contoso"))

GOOD = {
    "title": "CALCULATE vs KEEPFILTERS",
    "note": "Red replaces the Color filter in one column and intersects with it in the other.",
    "rows": "DimProduct[Color]",
    "measures": [
        {"name": "Red (CALCULATE)",
         "expression": 'CALCULATE([Total Sales], DimProduct[Color] = "Red")',
         "formatString": "\\$#,0", "description": "Overwrites the Color filter."},
        {"name": "Red (KEEPFILTERS)",
         "expression": 'CALCULATE(\n    [Total Sales],\n    KEEPFILTERS(DimProduct[Color] = "Red")\n)'},
    ],
}


def run(spec, tmp):
    path = os.path.join(tmp, "spec.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(spec, f)
    return subprocess.run([sys.executable, SCRIPT, path, "--out", os.path.join(tmp, "out"),
                           "--master", MASTER], capture_output=True, text=True, encoding="utf-8")


@unittest.skipUnless(os.path.isdir(MASTER), "lab/contoso not present (installed plugin)")
class InjectTest(unittest.TestCase):
    def test_good_spec_produces_a_zip_with_measures_and_first_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = run(GOOD, tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with zipfile.ZipFile(os.path.join(tmp, "out", "dax-example-calculate-vs-keepfilters.zip")) as z:
                self.check_zip(z)

    def check_zip(self, z):
        names = z.namelist()
        self.assertIn("contoso/Contoso.pbip", names)
        self.assertFalse(any("/.pbi/" in n for n in names), "Desktop cache leaked into the zip")

        tmdl = z.read("contoso/Contoso.SemanticModel/definition/tables/_Measures.tmdl").decode()
        self.assertIn("\tmeasure 'Red (CALCULATE)' = CALCULATE([Total Sales]", tmdl)
        self.assertIn("\tmeasure 'Red (KEEPFILTERS)' =\n\t\t\tCALCULATE(", tmdl)
        self.assertLess(tmdl.index("Red (KEEPFILTERS)"), tmdl.index("\tpartition "))

        pages = json.loads(z.read("contoso/Contoso.Report/definition/pages/pages.json"))
        self.assertEqual(pages["pageOrder"][0], "ejemplo-calculate-vs-keepfilters")
        self.assertEqual(pages["activePageName"], "ejemplo-calculate-vs-keepfilters")
        visual = json.loads(z.read("contoso/Contoso.Report/definition/pages/"
                                   "ejemplo-calculate-vs-keepfilters/visuals/matriz/visual.json"))
        props = [p["field"]["Measure"]["Property"]
                 for p in visual["visual"]["query"]["queryState"]["Values"]["projections"]]
        self.assertEqual(props, ["Red (CALCULATE)", "Red (KEEPFILTERS)"])

    def test_bad_references_are_refused_before_writing(self):
        bad = {"title": "bad", "measures": [
            {"name": "Total Sales", "expression": "SUM(DimProduct[Colour]) + [Nope] + (1"}]}
        with tempfile.TemporaryDirectory() as tmp:
            r = run(bad, tmp)
            self.assertNotEqual(r.returncode, 0)
            for expected in ("already exists", "DimProduct[Colour] does not exist",
                             "[Nope] is neither", "unbalanced parentheses"):
                self.assertIn(expected, r.stderr)
            self.assertFalse(os.path.exists(os.path.join(tmp, "out")))

    def test_strings_are_not_read_as_references(self):
        spec = {"title": "strings", "measures": [
            {"name": "Label", "expression": '"[not a measure] (" & FORMAT([Total Sales], "#,0")'}]}
        with tempfile.TemporaryDirectory() as tmp:
            r = run(spec, tmp)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
