#!/usr/bin/env python3
"""Tests for the Learn fetch.

Run: python -m unittest discover -s skills/dax-reference/scripts

Offline. The fixtures are cut down from real pages — the exact markup each of the five
applies-to variants renders, verified against `bredeespelid/PBIP_SemLin`'s copy of the
upstream source, which still carries the `[!INCLUDE]` shortcodes those renderings came
from. A test that invented the markup would pass against nothing.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import fetch_from_learn as learn                                  # noqa: E402
import sync_query_docs as sync                                    # noqa: E402


def icons(*states):
    """The applies-to paragraph as Learn renders it, bold and linked."""
    labels = ["Calculated column", "Calculated table", "Measure", "Visual calculation"]
    parts = "".join(
        f'<img src="media/icons/{s}.png" role="presentation" '
        f'data-linktype="relative-path">\n<a href="/en-us/power-bi/x">{lab}</a> '
        for s, lab in zip(states, labels))
    return f"<p><strong>Applies to:</strong> {parts}</p>"


# The INFO.* pages, copied from a real one. Two things differ from every other variant
# and both were got wrong first time: there is no bold and no links, and there is a FIFTH
# entry, "DAX query", which is the only one set to yes.
_ICON_HTML = '<img src="media/icons/{}.png" role="presentation" data-linktype="relative-path">'
QUERY_ONLY = "<p>Applies to: " + " ".join(
    _ICON_HTML.format(state) + "\n" + label
    for state, label in (("no", "Calculated column"), ("no", "Calculated table"),
                         ("no", "Measure"), ("no", "Visual calculation"),
                         ("yes", "DAX query"))) + "</p>"


class AppliesTo(unittest.TestCase):
    def test_the_four_yes_form(self):
        self.assertEqual(learn.applies_to_include(icons("yes", "yes", "yes", "yes")),
                         "applies-to-measures-columns-tables-visual-calculations")

    def test_the_discouraged_icon_is_not_a_yes(self):
        """`discouraged.png` is its own icon and it is the ONLY thing separating the
        discouraged variant from the plain one — both show three yeses and a fourth
        entry. Reading the fourth as a boolean puts 49 functions in the wrong include and
        drops the warning Microsoft prints right underneath it."""
        self.assertEqual(
            learn.applies_to_include(icons("yes", "yes", "yes", "discouraged")),
            "applies-to-measures-columns-tables-visual-calculations-discouraged")

    def test_a_no_on_the_fourth_is_the_three_context_form(self):
        self.assertEqual(learn.applies_to_include(icons("yes", "yes", "yes", "no")),
                         "applies-to-measures-columns-tables")

    def test_visual_calculations_only(self):
        self.assertEqual(learn.applies_to_include(icons("no", "no", "no", "yes")),
                         "applies-to-visual-calculations")

    def test_the_query_only_form_has_no_bold_no_links_and_a_fifth_icon(self):
        """Two separate traps in one variant, and both were live.

        Matching only the bold-and-linked form found four of the five variants. And the
        fifth entry, "DAX query", makes this key five icons long — a four-icon key looked
        right against the top of the page and left all 68 INFO.* functions declaring
        nothing about where they are legal. Caught by checking all 479 pages, not a
        sample; the fixture is copied from a real one for the same reason."""
        self.assertEqual(learn.applies_to_include(QUERY_ONLY), "applies-to-query-only")
        self.assertEqual(len([k for k in learn.APPLIES_TO_BY_ICONS if len(k) == 5]), 1)

    def test_an_unknown_combination_is_None_and_not_a_default(self):
        """The same rule `parse_applies_to` follows: no fallback. The permissive default
        would have a card assert a function is legal in measures, columns and tables
        because the fetch could not read the page."""
        self.assertIsNone(learn.applies_to_include(icons("no", "yes", "no", "yes")))

    def test_a_page_with_no_block_at_all_is_None(self):
        self.assertIsNone(learn.applies_to_include("<p>Some prose.</p>"))

    def test_every_include_it_can_emit_is_one_the_sync_understands(self):
        """The contract between the two modules, and the reason this file exists beside
        the sync rather than somewhere else. An include the sync does not know maps to
        `_NO_CLAIM`, so the mismatch would not crash — it would publish 479 cards
        claiming nothing about where their function is legal."""
        for stem in learn.APPLIES_TO_BY_ICONS.values():
            self.assertIn(stem, sync.APPLIES_TO_MAP,
                          f"the fetch can emit '{stem}' and the sync does not know it")

    def test_the_map_covers_every_function_and_covers_it_once(self):
        """Read off all 479 pages: 312 + 49 + 36 + 14 + 68. The sum is the assertion —
        a key that stops matching sends its functions to `None`, and `None` stops the run
        rather than publishing a permissive default, but it should fail here first with a
        number that says how many pages moved."""
        self.assertEqual(len(learn.APPLIES_TO_BY_ICONS), 5)
        self.assertEqual(len(set(learn.APPLIES_TO_BY_ICONS.values())), 5)

    def test_the_sync_knows_no_variant_the_fetch_cannot_produce(self):
        """The other direction. A variant the sync handles and Learn renders somehow means
        this fetch would return None on those pages and the run would stop — which is the
        safe failure, but it should be a known gap rather than a surprise."""
        self.assertEqual(set(sync.APPLIES_TO_MAP), set(learn.APPLIES_TO_BY_ICONS.values()))


class Toc(unittest.TestCase):
    TOC = json.dumps({"items": [{"href": "dax-overview", "children": [
        {"href": "abs-function-dax"},
        {"href": "https://aka.ms/learndax"},
        {"href": "../power-bi/something"},
        {"href": "/en-us/absolute"},
        {"href": "best-practices/dax-divide-function-operator"},
        {"href": "abs-function-dax#syntax"},
        {"href": "./"},
    ]}]})

    def test_it_keeps_only_same_area_relative_pages(self):
        """`https://aka.ms/learndax`, `../power-bi/...` and `/en-us/...` are all real
        entries in the live toc and none of them is a DAX page."""
        self.assertEqual(learn.toc_slugs(self.TOC),
                         ["dax-overview", "abs-function-dax",
                          "best-practices/dax-divide-function-operator"])

    def test_an_anchor_is_the_same_page(self):
        """`abs-function-dax#syntax` appears in the toc beside `abs-function-dax`.
        Fetching it twice would double the crawl and write the page over itself."""
        self.assertEqual(learn.toc_slugs(self.TOC).count("abs-function-dax"), 1)


class Article(unittest.TestCase):
    PAGE = ('<div class="content">' + icons("yes", "yes", "yes", "yes") +
            "<p>Returns the absolute value.</p>"
            '<h2 id="syntax">Syntax</h2><pre><code class="lang-dax">ABS(x)</code></pre>'
            '<h2 id="feedback"> Feedback </h2><p>Was this page helpful?</p></div>')

    def test_learns_own_furniture_is_not_part_of_the_document(self):
        """Everything from the Feedback heading down is the site, not Microsoft's prose.
        Carrying it into a card would put a feedback widget in the reference."""
        out = learn.article(self.PAGE)
        self.assertIn("Returns the absolute value.", out)
        self.assertNotIn("Was this page helpful?", out)

    def test_the_applies_to_paragraph_is_removed(self):
        """It becomes the [!INCLUDE] line. Leaving it would also leave it as prose, and
        the card would state the same thing twice in two formats."""
        self.assertNotIn("Applies to:", learn.article(self.PAGE))

    def test_a_page_it_cannot_parse_returns_empty_rather_than_half(self):
        self.assertEqual(learn.article("<html><body>nothing</body></html>"), "")


class Meta(unittest.TestCase):
    def test_entities_are_unescaped(self):
        meta = learn.page_meta('<meta name="description" content="Learn &amp; more">')
        self.assertEqual(meta["description"], "Learn & more")

    def test_the_dates_are_read(self):
        meta = learn.page_meta('<meta name="ms.date" content="2023-10-20T00:00:00Z">'
                               '<meta name="updated_at" content="2026-01-22T22:02:00Z">')
        self.assertEqual(meta["ms.date"][:10], "2023-10-20")
        self.assertEqual(meta["updated_at"][:10], "2026-01-22")


if __name__ == "__main__":
    unittest.main()
