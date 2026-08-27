#!/usr/bin/env python3
"""Tests for the local-metadata regenerator.

Run: python -m unittest discover -s skills/dax-reference/scripts

Every test here was written by breaking the thing it covers and watching it go red. The
ones that could not be made to fail were rewritten or deleted, which is the standing rule
in this repository and the reason the suite is worth its runtime.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import refresh_local_metadata as refresh                          # noqa: E402
import sync_query_docs as sync                                    # noqa: E402


CARD = """---
name: ABS
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/abs-function-dax.md@323524c
sourceDate:
notes: false
examples: 0
---
# ABS

Returns the absolute value of a number.

## Syntax

```dax
ABS(<number>)
```

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs`.

Some upstream example prose.
"""

NO_MS_EXAMPLES = """---
name: NOEX
notes: false
examples: 0
---
# NOEX

Only remarks, no examples section upstream.
"""


def fm(text, key):
    """The value of one frontmatter field, as written."""
    block = refresh._FM_RE.match(text).group(1)
    for line in block.splitlines():
        if line.startswith(key + ":"):
            return line[len(key) + 1:].strip()
    return None


class RefreshCard(unittest.TestCase):
    def test_an_example_file_stops_being_invisible(self):
        """The whole bug: three measured queries on disk, `examples: 0` on the card.

        SKILL.md step 4 routes on this field, so a card that says 0 is a file no agent has
        a reason to open. Forty-five of them were in that state.
        """
        out = refresh.refresh_card(CARD, "abs", False, ("math-and-trig", 3))
        self.assertEqual(fm(out, "examples"), "3")
        self.assertIn("examples/math-and-trig/abs.md", out)

    def test_the_block_goes_above_microsofts_own_examples(self):
        """Order is the point, not presence.

        Microsoft's examples are measured against a model this repository does not carry.
        An agent that stops reading early has to meet the reproducible ones first, so a
        block appended at the end would satisfy a presence check and still be wrong.
        """
        out = refresh.refresh_card(CARD, "abs", False, ("math-and-trig", 3))
        self.assertLess(out.index(refresh.OURS_HEADING), out.index(refresh.MS_HEADING))

    def test_a_card_without_an_upstream_examples_section_gets_it_appended(self):
        out = refresh.refresh_card(NO_MS_EXAMPLES, "noex", False, ("logical", 2))
        self.assertIn(refresh.OURS_HEADING, out)
        self.assertEqual(fm(out, "examples"), "2")
        self.assertTrue(out.rstrip().endswith("localhost:<puerto>`."))

    def test_deleting_the_example_file_removes_the_block(self):
        """The reverse direction. A card promising a file that is gone sends an agent to a
        404, which is the failure the forward check was already catching in the catalogue
        and nothing was catching on the card."""
        with_block = refresh.refresh_card(CARD, "abs", False, ("math-and-trig", 3))
        out = refresh.refresh_card(with_block, "abs", False, None)
        self.assertNotIn(refresh.OURS_HEADING, out)
        self.assertEqual(fm(out, "examples"), "0")
        self.assertIn(refresh.MS_HEADING, out)      # upstream's section is not collateral

    def test_the_count_is_rewritten_not_just_the_presence(self):
        """A card promising three when the file holds four is not a cosmetic disagreement:
        the number is printed in the block a reader is told to trust."""
        three = refresh.refresh_card(CARD, "abs", False, ("math-and-trig", 3))
        four = refresh.refresh_card(three, "abs", False, ("math-and-trig", 4))
        self.assertEqual(fm(four, "examples"), "4")
        self.assertIn("**4** consulta(s)", four)
        self.assertNotIn("**3** consulta(s)", four)

    def test_a_hand_written_note_stops_being_invisible(self):
        """WINDOW carried a note behind `notes: false` — one of the functions the
        window-functions skill exists for."""
        out = refresh.refresh_card(CARD, "abs", True, None)
        self.assertEqual(fm(out, "notes"), "true")

    def test_running_it_twice_changes_nothing(self):
        """Not a nicety: this runs as a gate. A regenerator that is not idempotent turns
        every pull request red for the crime of having run it."""
        once = refresh.refresh_card(CARD, "abs", True, ("math-and-trig", 3))
        self.assertEqual(refresh.refresh_card(once, "abs", True, ("math-and-trig", 3)), once)

    def test_microsoft_prose_is_not_touched(self):
        """The reason this script exists instead of a full regeneration: every reachable
        copy of the upstream markdown is OLDER than the tree. Anything this writes into
        Microsoft's half would be a silent downgrade."""
        out = refresh.refresh_card(CARD, "abs", True, ("math-and-trig", 3))
        self.assertIn("Returns the absolute value of a number.", out)
        self.assertIn("ABS(<number>)", out)
        self.assertIn("Some upstream example prose.", out)
        self.assertEqual(fm(out, "source"),
                         "query-languages/dax/abs-function-dax.md@323524c")

    def test_a_backslash_in_the_frontmatter_survives(self):
        """`re.sub` reads backslashes in a replacement string. Written the obvious way this
        turns a summary containing one into mojibake or a crash, and the field it mangles
        is not the field being edited — which is how it would have gone unnoticed."""
        card = CARD.replace("name: ABS", r"name: A\B")
        out = refresh.refresh_card(card, "abs", True, None)
        self.assertEqual(fm(out, "name"), r"A\B")

    def test_a_card_without_frontmatter_is_an_error_not_a_silent_skip(self):
        with self.assertRaises(ValueError):
            refresh.refresh_card("# ABS\n\nno frontmatter here\n", "abs", False, None)


class RefreshTree(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.gen = os.path.join(self.dir, "generated")
        os.makedirs(os.path.join(self.gen, "library"))
        os.makedirs(os.path.join(self.dir, "notes"))
        os.makedirs(os.path.join(self.dir, "examples", "math-and-trig"))
        with open(os.path.join(self.gen, "library", "abs.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(CARD)
        with open(os.path.join(self.dir, "examples", "math-and-trig", "abs.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write("# ABS\n\n```dax\nEVALUATE ROW(\"a\", ABS(-1))\n```\n\n"
                    "```dax\nEVALUATE ROW(\"b\", ABS(2))\n```\n")
        catalog = {"source": "MicrosoftDocs/query-docs@323524c",
                   "sourceCommitDate": "2026-08-13T16:02:28Z",
                   "functionCount": 1, "conceptCount": 0,
                   "functions": [{"name": "ABS", "file": "abs",
                                  "category": ["math-and-trig"],
                                  "primaryCategory": "math-and-trig",
                                  "returns": "scalar",
                                  "appliesTo": ["measure"],
                                  "discouragedInVisualCalculations": False,
                                  "summary": "Returns the absolute value of a number.",
                                  "notes": False, "examples": 0}],
                   "concepts": []}
        with open(os.path.join(self.gen, "catalog.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
        with open(os.path.join(self.gen, "catalog.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(sync._catalog_md(catalog["functions"], catalog["source"],
                                     catalog["sourceCommitDate"]))

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_check_mode_writes_nothing(self):
        """A gate that repairs the tree it is judging always passes, and reports a repo
        that was never in the state it claims to have verified."""
        card = os.path.join(self.gen, "library", "abs.md")
        with open(card, encoding="utf-8") as f:
            before = f.read()
        changed, _ = refresh.refresh(root=self.gen, ref=self.dir, check=True)
        self.assertIn(os.path.join("library", "abs.md"), changed)
        with open(card, encoding="utf-8") as f:
            after = f.read()
        self.assertEqual(before, after)

    def test_the_two_indexes_are_repaired_with_the_cards(self):
        """They rot from the same two directories. Fixing the card and leaving the
        catalogue is how an agent reading catalog.md keeps missing the work."""
        refresh.refresh(root=self.gen, ref=self.dir, check=False)
        with open(os.path.join(self.gen, "catalog.json"), encoding="utf-8") as f:
            catalog = json.load(f)
        self.assertEqual(catalog["functions"][0]["examples"], 2)
        with open(os.path.join(self.gen, "catalog.md"), encoding="utf-8") as f:
            md = f.read()
        self.assertIn("▶", md)

    def test_a_clean_tree_reports_nothing_to_do(self):
        refresh.refresh(root=self.gen, ref=self.dir, check=False)
        changed, reasons = refresh.refresh(root=self.gen, ref=self.dir, check=True)
        self.assertEqual(changed, [])
        self.assertEqual(reasons, [])

    def test_catalog_json_keeps_the_syncs_byte_format(self):
        """Compared as text, not as parsed objects: a second opinion on indent or key order
        would rewrite the file on every run and bury the real diff."""
        refresh.refresh(root=self.gen, ref=self.dir, check=False)
        with open(os.path.join(self.gen, "catalog.json"), encoding="utf-8") as f:
            raw = f.read()
        parsed = json.loads(raw)
        self.assertEqual(raw, json.dumps(parsed, indent=2, ensure_ascii=False) + "\n")


class CatalogFlags(unittest.TestCase):
    def test_the_catalog_marks_functions_that_have_runnable_examples(self):
        """Without ▶ the only way to know a function has measured examples was to open its
        card — 479 cards to find 99. The note flag ★ was already there; the examples one
        was not, and the examples are the larger body of work."""
        entry = {"name": "ABS", "primaryCategory": "math-and-trig", "returns": "scalar",
                 "appliesTo": ["measure"], "summary": "s",
                 "discouragedInVisualCalculations": False, "notes": False, "examples": 3}
        md = sync._catalog_md([entry], "src", "date")
        self.assertIn("▶", md.splitlines()[-1])
        entry["examples"] = 0
        self.assertNotIn("▶", sync._catalog_md([entry], "src", "date").splitlines()[-1])

    def test_the_legend_explains_every_flag_it_uses(self):
        """A glyph in a table and nothing in the legend is worse than no glyph."""
        entry = {"name": "ABS", "primaryCategory": "c", "returns": "scalar",
                 "appliesTo": ["measure"], "summary": "s",
                 "discouragedInVisualCalculations": True, "notes": True, "examples": 3}
        md = sync._catalog_md([entry], "src", "date")
        legend = [line for line in md.splitlines() if line.startswith("> **No editar")][0]
        for glyph in ("⛔", "★", "▶"):
            self.assertIn(glyph, legend)


if __name__ == "__main__":
    unittest.main()
