#!/usr/bin/env python3
"""Tests for the bundle layout of generated/. Run: python -m unittest discover -s skills/dax-reference/scripts

The property that matters is the round trip: a card comes back out of its bundle as the
exact bytes that went in. Everything else -- the validators, refresh, the catalog's line
ranges -- reads the tree through `split`, so a lossy split would corrupt all of it quietly.
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import card_bundles as cb                                         # noqa: E402

GENERATED = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "generated")


def card(name, category, body=""):
    return (f"---\nname: {name.upper()}\nprimaryCategory: {category}\n---\n"
            f"# {name.upper()}\n\n{body}\n")


TREES = {
    "library": {
        "abs": card("abs", "math-and-trig", "See [SIGN](./sign.md) and [IF](./if.md#examples)."),
        "sign": card("sign", "math-and-trig", "Glossary: [x](../concepts/dax-glossary.md)."),
        "if": card("if", "logical", "Runnable: [here](../../examples/logical/if.md)."),
        "blank": "---\nname: BLANK\nprimaryCategory:\n---\nno final newline",
    },
    "concepts": {
        "dax-glossary": "# Glossary\n\nSee [ABS](../library/abs.md).\n",
    },
}


class RoundTrip(unittest.TestCase):
    def test_every_card_comes_back_byte_for_byte(self):
        files, _ = cb.layout(TREES)
        self.assertEqual(cb.split(files), TREES)

    def test_a_card_without_a_final_newline_keeps_it_missing(self):
        files, _ = cb.layout(TREES)
        self.assertFalse(cb.split(files)["library"]["blank"].endswith("\n"))

    def test_the_real_tree_round_trips(self):
        """The 513 cards on disk, split and rebuilt: the same bytes as the bundles."""
        self.assertEqual(cb.check(GENERATED), [])


class Grouping(unittest.TestCase):
    def test_a_function_goes_with_its_primary_category(self):
        groups = cb.group(TREES)
        self.assertEqual(groups["functions-math-and-trig"],
                         [("library", "abs"), ("library", "sign")])
        self.assertEqual(groups["functions-logical"], [("library", "if")])
        self.assertEqual(groups["functions-uncategorized"], [("library", "blank")])
        self.assertEqual(groups["concepts"], [("concepts", "dax-glossary")])

    def test_a_group_over_the_target_splits_into_numbered_parts_under_it(self):
        big = {"library": {f"f{i:02}": card(f"f{i:02}", "text", "x" * 40_000)
                           for i in range(12)}, "concepts": {}}
        files, _ = cb.layout(big)
        self.assertEqual(sorted(files), ["functions-text-1.md", "functions-text-2.md",
                                         "functions-text-3.md"])
        for text in files.values():
            self.assertLessEqual(len(text.encode("utf-8")), cb.TARGET + 1024)
        self.assertEqual(cb.split(files), big)


class Links(unittest.TestCase):
    def setUp(self):
        self.files, _ = cb.layout(TREES)

    def test_a_link_to_another_card_points_at_its_bundle_and_anchor(self):
        self.assertIn("[SIGN](./functions-math-and-trig.md#sign)",
                      self.files["functions-math-and-trig.md"])
        self.assertIn("[x](./concepts.md#dax-glossary)", self.files["functions-math-and-trig.md"])
        self.assertIn("[ABS](./functions-math-and-trig.md#abs)", self.files["concepts.md"])

    def test_a_section_anchor_rides_along_as_the_title(self):
        self.assertIn('[IF](./functions-logical.md#if "section:examples")',
                      self.files["functions-math-and-trig.md"])

    def test_a_link_outside_generated_is_untouched(self):
        self.assertIn("(../../examples/logical/if.md)", self.files["functions-logical.md"])

    def test_every_card_has_an_anchor_for_those_links(self):
        self.assertIn('<a id="sign"></a>', self.files["functions-math-and-trig.md"])


class Pointers(unittest.TestCase):
    def test_the_range_starts_at_the_card_and_ends_at_its_end_marker(self):
        files, pointers = cb.layout(TREES)
        for (sub, stem), ptr in pointers.items():
            name, lines = ptr.split(":")
            first, last = map(int, lines.split("-"))
            text = files[f"{name}.md"].split("\n")
            self.assertEqual(text[first - 1], f'<a id="{stem}"></a>')
            self.assertEqual(text[first], f"<!-- card: {sub}/{stem}"
                             + (" no-final-newline" if stem == "blank" else "") + " -->")
            self.assertEqual(text[last - 1], "<!-- /card -->")

    def test_pointers_for_keeps_one_subtree(self):
        _, pointers = cb.layout(TREES)
        self.assertEqual(sorted(cb.pointers_for(pointers, "concepts")), ["dax-glossary"])


class Check(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        cb.save(self.dir, TREES)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_a_clean_tree_passes(self):
        self.assertEqual(cb.check(self.dir), [])
        self.assertEqual(cb.read(self.dir), TREES)

    def test_a_hand_edit_to_a_bundle_fails(self):
        path = os.path.join(self.dir, cb.BUNDLES, "functions-logical.md")
        with open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write("a stray line\n")
        self.assertTrue(cb.check(self.dir))

    def test_the_old_one_file_per_card_layout_fails(self):
        """A stale library/ beside the bundles would be read by an agent and never updated."""
        os.makedirs(os.path.join(self.dir, "library"))
        self.assertTrue(any("library/" in p for p in cb.check(self.dir)))

    def test_a_stale_bundle_is_removed_on_save(self):
        cb.save(self.dir, {"library": {"if": TREES["library"]["if"]}, "concepts": {}})
        self.assertEqual(sorted(cb.read_files(self.dir)), ["functions-logical.md"])


if __name__ == "__main__":
    unittest.main()
