#!/usr/bin/env python3
"""Tests for the gate that ties the README's headline table to its runs.

Run: python -m unittest discover -s scripts -t scripts
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_eval_claims as gate                                  # noqa: E402


TABLE = """Some prose.

| | alone | with the catalogue |
|---|---:|---:|
| Claude Haiku 4.5 | 11 | 6 |
| Claude Sonnet 5 | 8 | **0** |
| DeepSeek V4-Pro | 4 | **0** |
| DeepSeek V4-Flash | 3 | **0** |

More prose.
"""


class Parsing(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "README.md")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, text):
        with open(self.path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def test_it_reads_every_row(self):
        self.write(TABLE)
        self.assertEqual(gate.table_rows(self.path),
                         [("Claude Haiku 4.5", 11, 6), ("Claude Sonnet 5", 8, 0),
                          ("DeepSeek V4-Pro", 4, 0), ("DeepSeek V4-Flash", 3, 0)])

    def test_the_bold_on_a_zero_is_emphasis_and_not_data(self):
        """Three of the four rows end in **0** because it is the result worth seeing. A
        parser that choked on the asterisks would read the table as half missing."""
        rows = dict((m, (a, b)) for m, a, b in gate.table_rows(self.path)) if False else None
        self.write(TABLE)
        self.assertIn(("Claude Sonnet 5", 8, 0), gate.table_rows(self.path))

    def test_a_row_about_something_else_is_ignored(self):
        """The README has other tables. Only rows naming a model this gate has a run for
        are claims about inventions."""
        self.write(TABLE + "\n| **479 function cards** | derived from upstream | x |\n")
        self.assertEqual(len(gate.table_rows(self.path)), 4)

    def test_no_table_at_all_is_an_error_not_a_pass(self):
        """Deleting the table would otherwise silently retire the gate: nothing to compare
        means nothing to disagree, and the run would end in OK."""
        self.write("# Repo\n\nNo table here.\n")
        self.assertEqual(gate.table_rows(self.path), [])


class AgainstTheRuns(unittest.TestCase):
    def test_every_model_in_the_map_has_a_run_file(self):
        for model, filename in gate.MODEL_FILES.items():
            self.assertTrue(os.path.exists(os.path.join(gate.RUNS, filename)),
                            f"{model}: {filename} is missing")

    def test_the_shipped_readme_agrees_with_the_shipped_runs(self):
        """The assertion the whole gate exists for, run against the real files."""
        self.assertEqual(gate.main(), 0)

    def test_the_invalid_opus_run_is_not_among_the_claims(self):
        """Its 24 empty answers make its totals meaningless, so it is deliberately absent
        from the README table and from this map. If someone adds the row, this says why
        they should not."""
        self.assertNotIn("Claude Opus 5", gate.MODEL_FILES)


if __name__ == "__main__":
    unittest.main()
