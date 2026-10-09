#!/usr/bin/env python3
"""Tests for the query-docs sync pipeline. Run: python -m unittest discover -s dax-reference/scripts"""
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sync_query_docs  # noqa: E402
from sync_query_docs import (  # noqa: E402
    apply_filename_rules,
    apply_toc,
    broken_local_links,
    build_category_map,
    build_concept_card,
    broken_local_links,
    build_library_card,
    count_deviation,
    determine_returns,
    discover_concept_docs,
    discover_function_docs,
    discover_indexes,
    main,
    parse_applies_to,
    parse_category_index,
    parse_ms_date,
    parse_return_value,
    parse_summary,
    parse_title,
    parse_toc,
    parse_syntax,
    _learn_url,
    absolutise_links,
    resolve_includes,
    read_toc,
    rewrite_links,
    stale_uncategorized,
    uncategorized_gate,
    unlisted_content_dirs,
    write_library,
)


FILTER_INDEX = """---
description: "Learn more about: Filter functions"
title: "Filter functions (DAX)"
ms.topic: reference
---
# Filter functions

The filter and value functions in DAX are some of the most complex and powerful.

## In this category

|Function  |Description  |
|---------|---------|
|[ALL](all-function-dax.md)      |  Returns all the rows in a table, ignoring any filters.       |
|[CALCULATE](calculate-function-dax.md)      |  Evaluates an expression in a modified filter context.      |
"""

CALCULATE_DOC = """---
description: "Learn more about: CALCULATE"
title: "CALCULATE function (DAX)"
ms.topic: reference
ms.date: 06/29/2026
---
# CALCULATE

[!INCLUDE[applies-to-measures-columns-tables-visual-calculations](includes/applies-to-measures-columns-tables-visual-calculations.md)]

Evaluates an expression in a modified filter context.

## Syntax

```dax
CALCULATE(<expression>[, <filter1> [, <filter2> [, ...]]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|The expression to evaluate.|
|`filter1, filter2,...`|(Optional) Boolean expressions or table expressions that defines filters.|

## Return value

The value that results from the expression.

## Remarks

- When you provide filter expressions, the CALCULATE function modifies the filter context.

- [CALCULATETABLE](calculatetable-function-dax.md) performs exactly the same functionality.

## Related content

- [CALCULATETABLE function](calculatetable-function-dax.md)
- [Filter functions](filter-functions-dax.md)
"""

DISCOURAGED_DOC = """---
description: "Learn more about: EARLIER"
title: "EARLIER function (DAX)"
ms.topic: reference
---
# EARLIER

[!INCLUDE[applies-to-measures-columns-tables-visual-calculations-discouraged](includes/applies-to-measures-columns-tables-visual-calculations-discouraged.md)]

Returns the current value of the specified column in an outer evaluation pass.

## Syntax

```dax
EARLIER(<column>, <number>)
```

## Return value

The current value of row, from column, at number of outer evaluation passes.
"""

QUERY_ONLY_DOC = """---
description: "Learn more about: EVALUATE"
title: "EVALUATE keyword (DAX)"
ms.topic: reference
---
# EVALUATE

[!INCLUDE[applies-to-query-only](includes/applies-to-query-only.md)]

Required statement in a DAX query.

## Syntax

```dax
EVALUATE <table>
```
"""

VISUAL_CALC_DOC = """---
description: "Learn more about: COLLAPSE"
title: "COLLAPSE function (DAX)"
ms.topic: reference
---
# COLLAPSE

[!INCLUDE[applies-to-visual-calculations](includes/applies-to-visual-calculations.md)]

Returns a value from the parent level in the visual hierarchy.

## Syntax

```dax
COLLAPSE(<expression>[, <axis>])
```
"""

MEASURES_COLUMNS_TABLES_DOC = """---
description: "Learn more about: SUMX"
title: "SUMX function (DAX)"
ms.topic: reference
ms.date: 01/15/2026
---
# SUMX

[!INCLUDE[applies-to-measures-columns-tables](includes/applies-to-measures-columns-tables.md)]

Returns the sum of an expression evaluated for each row in a table.

## Syntax

```dax
SUMX(<table>, <expression>)
```
"""

TABLE_INDEX = """# Table manipulation functions

## In this category

|Function  |Description  |
|---------|---------|
|[INDEX](index-function-dax.md)      |  Returns a row at an absolute position.       |
|[SUMMARIZE](summarize-function-dax.md)      |  Returns a summary table.      |
"""


# ---- Pass 1 tests (unchanged) ----

class ParseCategoryIndex(unittest.TestCase):

    def test_extracts_one_entry_per_table_row(self):
        entries = parse_category_index(FILTER_INDEX, "filter-functions-dax.md")
        self.assertEqual([e["name"] for e in entries], ["ALL", "CALCULATE"])

    def test_captures_the_target_file_of_each_link(self):
        entries = parse_category_index(FILTER_INDEX, "filter-functions-dax.md")
        self.assertEqual(entries[0]["file"], "all-function-dax.md")
        self.assertEqual(entries[1]["file"], "calculate-function-dax.md")

    def test_captures_the_summary_stripped_of_padding(self):
        entries = parse_category_index(FILTER_INDEX, "filter-functions-dax.md")
        self.assertEqual(
            entries[1]["summary"],
            "Evaluates an expression in a modified filter context.",
        )

    def test_derives_the_category_from_the_index_filename(self):
        entries = parse_category_index(FILTER_INDEX, "filter-functions-dax.md")
        self.assertTrue(all(e["category"] == "filter" for e in entries))

    def test_ignores_link_tables_outside_the_in_this_category_section(self):
        text = FILTER_INDEX + (
            "\n## Related content\n\n"
            "|Topic  |Description  |\n"
            "|---------|---------|\n"
            "|[DAX overview](dax-overview.md)  |  Not a function.  |\n"
        )
        entries = parse_category_index(text, "filter-functions-dax.md")
        self.assertEqual([e["name"] for e in entries], ["ALL", "CALCULATE"])

    def test_takes_only_the_description_column_when_a_row_has_extras(self):
        text = (
            "## In this category\n\n"
            "|Function  |Description  |Since  |\n"
            "|---------|---------|---------|\n"
            "|[ALL](all-function-dax.md)  |  Returns all the rows.  |  2015  |\n"
        )
        entries = parse_category_index(text, "filter-functions-dax.md")
        self.assertEqual(entries[0]["summary"], "Returns all the rows.")


class BuildCategoryMap(unittest.TestCase):

    def indexes(self):
        return [
            (FILTER_INDEX, "filter-functions-dax.md"),
            (TABLE_INDEX, "table-manipulation-functions-dax.md"),
        ]

    def test_keys_the_map_by_the_function_document(self):
        m = build_category_map(self.indexes())
        self.assertEqual(
            sorted(m),
            ["all-function-dax.md", "calculate-function-dax.md",
             "index-function-dax.md", "summarize-function-dax.md"],
        )

    def test_carries_name_and_summary_through(self):
        m = build_category_map(self.indexes())
        entry = m["calculate-function-dax.md"]
        self.assertEqual(entry["name"], "CALCULATE")
        self.assertEqual(entry["summary"],
                         "Evaluates an expression in a modified filter context.")

    def test_a_function_listed_once_still_gets_a_category_list(self):
        m = build_category_map(self.indexes())
        self.assertEqual(m["all-function-dax.md"]["category"], ["filter"])
        self.assertEqual(m["all-function-dax.md"]["primaryCategory"], "filter")

    def test_a_function_in_two_indexes_collects_both_categories(self):
        indexes = self.indexes() + [(
            "## In this category\n\n"
            "|Function  |Description  |\n"
            "|---------|---------|\n"
            "|[INDEX](index-function-dax.md)  |  Returns a row at an absolute position.  |\n",
            "other-functions-dax.md",
        )]
        entry = build_category_map(indexes)["index-function-dax.md"]
        self.assertEqual(entry["category"], ["table-manipulation", "other"])

    def test_primary_category_is_the_first_index_that_listed_it(self):
        indexes = self.indexes() + [(
            "## In this category\n\n"
            "|Function  |Description  |\n"
            "|---------|---------|\n"
            "|[INDEX](index-function-dax.md)  |  Returns a row at an absolute position.  |\n",
            "other-functions-dax.md",
        )]
        entry = build_category_map(indexes)["index-function-dax.md"]
        self.assertEqual(entry["primaryCategory"], "table-manipulation")

    def test_a_duplicate_listing_does_not_repeat_the_category(self):
        indexes = self.indexes() + [(FILTER_INDEX, "filter-functions-dax.md")]
        self.assertEqual(build_category_map(indexes)["all-function-dax.md"]["category"],
                         ["filter"])


class DiscoverIndexes(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        filter_with_overlap = FILTER_INDEX + (
            "|[INDEX](index-function-dax.md)      |  Returns a row at an absolute position.       |\n"
        )
        for fn, body in [
            ("filter-functions-dax.md", filter_with_overlap),
            ("table-manipulation-functions-dax.md", TABLE_INDEX),
            ("calculate-function-dax.md", "# CALCULATE\n"),
            ("dax-overview.md", "# DAX overview\n"),
        ]:
            with open(os.path.join(self.dir, fn), "w", encoding="utf-8") as f:
                f.write(body)

    def test_picks_up_only_the_category_index_files(self):
        found = [fn for _, fn in discover_indexes(self.dir)]
        self.assertEqual(found,
                         ["filter-functions-dax.md", "table-manipulation-functions-dax.md"])

    def test_does_not_mistake_a_function_doc_for_an_index(self):
        found = [fn for _, fn in discover_indexes(self.dir)]
        self.assertNotIn("calculate-function-dax.md", found)

    def test_reads_the_file_contents(self):
        text, _ = discover_indexes(self.dir)[0]
        self.assertIn("[CALCULATE](calculate-function-dax.md)", text)

    def test_function_docs_are_found_without_swallowing_the_indexes(self):
        # '-functions-dax.md' (index) vs '-function-dax.md' (function): one letter apart.
        self.assertEqual(discover_function_docs(self.dir), ["calculate-function-dax.md"])

    def test_order_is_alphabetical_so_primary_category_is_deterministic(self):
        # INDEX is deliberately listed by BOTH fixtures. Asserting on a function that
        # only one index lists would pass whatever the discovery order was.
        m = build_category_map(discover_indexes(self.dir))
        entry = m["index-function-dax.md"]
        self.assertEqual(entry["primaryCategory"], "filter",
                         "'filter' sorts before 'table-manipulation' and must win")
        self.assertEqual(entry["category"], ["filter", "table-manipulation"])


class ApplyFilenameRules(unittest.TestCase):
    """info-functions-dax.md is prose, not a table, so the 72 INFO.* docs are listed by
    no index at all. Their filename is the only signal available in pass 1."""

    def test_an_info_doc_no_index_listed_gets_the_info_category(self):
        mapping = {}
        apply_filename_rules(mapping, ["info-calcdependency-function-dax.md"])
        entry = mapping["info-calcdependency-function-dax.md"]
        self.assertEqual(entry["category"], ["info"])
        self.assertEqual(entry["primaryCategory"], "info")

    def test_derives_the_dotted_function_name_from_the_filename(self):
        mapping = {}
        apply_filename_rules(mapping, ["info-view-tables-function-dax.md"])
        self.assertEqual(mapping["info-view-tables-function-dax.md"]["name"],
                         "INFO.VIEW.TABLES")

    def test_leaves_the_summary_empty_for_pass_two_to_fill(self):
        mapping = {}
        apply_filename_rules(mapping, ["info-annotations-function-dax.md"])
        self.assertEqual(mapping["info-annotations-function-dax.md"]["summary"], "")

    def test_never_overwrites_what_an_index_already_supplied(self):
        mapping = build_category_map([(FILTER_INDEX, "filter-functions-dax.md")])
        apply_filename_rules(mapping, ["calculate-function-dax.md"])
        self.assertEqual(mapping["calculate-function-dax.md"]["primaryCategory"], "filter")

    def test_returns_the_docs_that_still_have_no_category(self):
        mapping = {}
        left = apply_filename_rules(
            mapping, ["info-annotations-function-dax.md", "collapse-function-dax.md"])
        self.assertEqual(left, ["collapse-function-dax.md"])


class MainFixture:
    """Shared setup for the tests that drive main() over a synthetic corpus.

    Two things a real corpus has that a temp directory does not. toc.yml, because the sync
    refuses to run without upstream's table of contents rather than quietly losing the
    fourth route to a category. And its own overrides.json: load_overrides() reads the
    repo's real one, so a synthetic corpus where the 16 declared functions do not exist
    would trip the stale-declaration gate — correctly, which is why it is patched here
    rather than weakened there.
    """

    def set_up_corpus(self):
        self.dir = tempfile.mkdtemp()
        self.write("toc.yml", "items:\n- name: DAX\n  items: []\n")
        self._real_load = sync_query_docs.load_overrides
        sync_query_docs.load_overrides = lambda *a, **k: {}
        self.addCleanup(setattr, sync_query_docs, "load_overrides", self._real_load)


class CoverageFloor(MainFixture, unittest.TestCase):
    """Silent parser drift is the failure mode the whole pipeline exists to prevent."""

    def setUp(self):
        self.set_up_corpus()

    def write(self, fn, body):
        with open(os.path.join(self.dir, fn), "w", encoding="utf-8") as f:
            f.write(body)

    def run_main(self):
        with io.StringIO() as out, io.StringIO() as err:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                return main(["sync_query_docs.py", self.dir])

    def test_exits_non_zero_when_almost_nothing_got_categorized(self):
        self.write("filter-functions-dax.md", FILTER_INDEX)
        for i in range(40):
            self.write(f"orphan{i}-function-dax.md", "# ORPHAN\n")
        self.assertEqual(self.run_main(), 1)

    def test_exits_zero_when_coverage_is_healthy(self):
        self.write("filter-functions-dax.md", FILTER_INDEX)
        self.write("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL"))
        self.write("calculate-function-dax.md", GOOD_DOC)
        self.assertEqual(self.run_main(), 0)

    def test_exits_non_zero_when_the_directory_holds_no_index_at_all(self):
        self.write("calculate-function-dax.md", "# CALCULATE\n")
        self.assertEqual(self.run_main(), 1)

    def test_exits_non_zero_when_there_are_no_function_docs_to_cover(self):
        self.write("filter-functions-dax.md", FILTER_INDEX)
        self.assertEqual(self.run_main(), 1)

    def build(self, listed, orphans):
        rows = "".join(
            f"|[FN{i}](fn{i}-function-dax.md)  |  Does thing {i}.  |\n" for i in range(listed))
        self.write("filter-functions-dax.md",
                   "# Filter functions\n\n## In this category\n\n"
                   "|Function  |Description  |\n|---------|---------|\n" + rows)
        for i in range(listed):
            self.write(f"fn{i}-function-dax.md", GOOD_DOC.replace("CALCULATE", f"FN{i}"))
        for i in range(orphans):
            self.write(f"orphan{i}-function-dax.md",
                       GOOD_DOC.replace("CALCULATE", f"ORPHAN{i}"))

    def declare(self, *names):
        sync_query_docs.load_overrides = lambda *a, **k: {
            "uncategorized": {"functions": list(names)}}

    def test_the_toc_cannot_cover_for_a_collapsed_index_parser(self):
        # The floor exists to catch the category-index parser breaking. Measured after the
        # TOC filled the gaps, it stopped doing that: on the real corpus the TOC alone
        # classifies 459 of 479 (95.8%), so an index parser that matched NOTHING would
        # still clear a 90% floor and publish. The floor is measured on the index and
        # filename routes, before the TOC gets a turn.
        rows = "".join(f"|[FN{i}](fn{i}-function-dax.md)  |  Does thing {i}.  |\n"
                       for i in range(50))
        self.write("filter-functions-dax.md",
                   "# Filter functions\n\n"          # no "## In this category" heading:
                   f"|Function  |Description  |\n|---------|---------|\n{rows}")
        for i in range(50):
            self.write(f"fn{i}-function-dax.md", GOOD_DOC.replace("CALCULATE", f"FN{i}"))
        self.write("toc.yml", "items:\n- name: DAX\n  items:\n  - name: Filter functions\n"
                   "    items:\n" + "".join(
                       f"    - name: FN{i}\n      href: fn{i}-function-dax.md\n"
                       for i in range(50)))
        self.assertEqual(self.run_main(), 1)

    def test_a_drift_that_stays_above_the_ratio_floor_still_fails(self):
        # 289/320 = 90.3%, above the coarse floor. The ratio was never the sharp signal;
        # an undeclared uncategorized function is, however many there are.
        self.build(listed=289, orphans=31)
        self.assertEqual(self.run_main(), 1)

    def test_the_known_orphan_set_stays_green_once_it_is_declared(self):
        # These two tests used to read "21 orphans pass, 31 fail" against a ceiling of 30.
        # That ceiling is gone: it left nine slots a regression could sit in unnoticed, and
        # it could not tell a swap (one gains a category, one loses it) from no change at
        # all. The exceptions are named now, so the number stopped being the question.
        self.build(listed=458, orphans=3)
        self.declare("ORPHAN0", "ORPHAN1", "ORPHAN2")
        self.assertEqual(self.run_main(), 0)

    def test_one_undeclared_orphan_is_enough_to_fail(self):
        self.build(listed=458, orphans=3)
        self.declare("ORPHAN0", "ORPHAN1")
        self.assertEqual(self.run_main(), 1)

    def test_a_declaration_that_is_no_longer_true_fails(self):
        self.build(listed=458, orphans=3)
        self.declare("ORPHAN0", "ORPHAN1", "ORPHAN2", "GONEUPSTREAM")
        self.assertEqual(self.run_main(), 1)


# ---- Pass 2 tests ----

class ParseAppliesTo(unittest.TestCase):
    """parse_applies_to() reads the [!INCLUDE] line to determine context and discouraged flag."""

    def test_measures_columns_tables_visual_calculations_not_discouraged(self):
        applies_to, discouraged = parse_applies_to(CALCULATE_DOC)
        self.assertEqual(applies_to, ["measure", "column", "table", "visual-calculation"])
        self.assertFalse(discouraged)

    def test_measures_columns_tables_visual_calculations_discouraged(self):
        applies_to, discouraged = parse_applies_to(DISCOURAGED_DOC)
        self.assertEqual(applies_to, ["measure", "column", "table", "visual-calculation"])
        self.assertTrue(discouraged)

    def test_measures_columns_tables_not_discouraged(self):
        applies_to, discouraged = parse_applies_to(MEASURES_COLUMNS_TABLES_DOC)
        self.assertEqual(applies_to, ["measure", "column", "table"])
        self.assertFalse(discouraged)

    def test_query_only(self):
        applies_to, discouraged = parse_applies_to(QUERY_ONLY_DOC)
        self.assertEqual(applies_to, ["query"])
        self.assertFalse(discouraged)

    def test_visual_calculations_only(self):
        applies_to, discouraged = parse_applies_to(VISUAL_CALC_DOC)
        self.assertEqual(applies_to, ["visual-calculation"])
        self.assertFalse(discouraged)

    def test_no_include_falls_back_to_safe_default(self):
        applies_to, discouraged = parse_applies_to("# UNKNOWN\n\nSome text.\n")
        self.assertIsInstance(applies_to, list)
        self.assertFalse(discouraged)

    def test_discouraged_is_false_when_only_the_word_discouraged_appears_in_prose(self):
        doc = (
            "# FN\n\n"
            "[!INCLUDE[applies-to-measures-columns-tables-visual-calculations]"
            "(includes/applies-to-measures-columns-tables-visual-calculations.md)]\n\n"
            "This function is discouraged for large datasets.\n"
        )
        _, discouraged = parse_applies_to(doc)
        self.assertFalse(discouraged)


class ParseSummary(unittest.TestCase):
    """parse_summary() finds the short description paragraph after [!INCLUDE]."""

    def test_extracts_first_non_empty_paragraph_after_include(self):
        summary = parse_summary(CALCULATE_DOC)
        self.assertEqual(summary, "Evaluates an expression in a modified filter context.")

    def test_skips_note_blocks_that_immediately_follow_the_include(self):
        doc = (
            "# FN\n\n"
            "[!INCLUDE[applies-to-measures-columns-tables](includes/applies-to-measures-columns-tables.md)]\n\n"
            "> [!NOTE]\n> Some note about this function.\n\n"
            "The actual description.\n"
        )
        summary = parse_summary(doc)
        self.assertEqual(summary, "The actual description.")

    def test_returns_empty_string_when_no_include_found(self):
        summary = parse_summary("# FN\n\nSome text.\n")
        self.assertEqual(summary, "")

    def test_strips_leading_and_trailing_whitespace_from_the_result(self):
        doc = (
            "[!INCLUDE[applies-to-measures-columns-tables](includes/applies-to-measures-columns-tables.md)]\n\n"
            "   Trimmed summary.   \n"
        )
        summary = parse_summary(doc)
        self.assertEqual(summary, "Trimmed summary.")


class ParseSyntax(unittest.TestCase):
    """parse_syntax() extracts the first ```dax code block."""

    def test_extracts_the_dax_syntax_block(self):
        syntax = parse_syntax(CALCULATE_DOC)
        self.assertIn("CALCULATE(<expression>", syntax)

    def test_strips_surrounding_whitespace(self):
        syntax = parse_syntax(CALCULATE_DOC)
        self.assertEqual(syntax, syntax.strip())

    def test_returns_empty_string_when_no_dax_block(self):
        self.assertEqual(parse_syntax("# FN\n\nNo code block.\n"), "")

    def test_takes_the_first_block_when_multiple_exist(self):
        doc = (
            "## Syntax\n\n```dax\nFIRST()\n```\n\n"
            "## Examples\n\n```dax\nSECOND()\n```\n"
        )
        self.assertEqual(parse_syntax(doc), "FIRST()")


class ParseMsDate(unittest.TestCase):
    """parse_ms_date() extracts the ms.date field from YAML frontmatter."""

    def test_extracts_date_from_calculate_doc(self):
        self.assertEqual(parse_ms_date(CALCULATE_DOC), "06/29/2026")

    def test_returns_empty_string_when_no_date(self):
        self.assertEqual(parse_ms_date(DISCOURAGED_DOC), "")

    def test_strips_whitespace(self):
        doc = "---\nms.date:  01/01/2026  \n---\n"
        self.assertEqual(parse_ms_date(doc), "01/01/2026")


class RewriteLinks(unittest.TestCase):
    """rewrite_links() rewrites cross-links from query-docs paths to local library paths."""

    def test_rewrites_function_doc_link(self):
        text = "See [CALCULATETABLE](calculatetable-function-dax.md) for details."
        result = rewrite_links(text)
        self.assertIn("(./calculatetable.md)", result)
        self.assertNotIn("function-dax.md", result)

    def test_preserves_the_link_label(self):
        text = "[CALCULATETABLE function](calculatetable-function-dax.md)"
        result = rewrite_links(text)
        self.assertIn("[CALCULATETABLE function]", result)

    def test_preserves_in_text_anchors(self):
        text = "[filter context](dax-overview.md#filter-context)"
        result = rewrite_links(text)
        self.assertEqual(text, result,
                         "Concept links (non-function) must not be rewritten")

    def test_rewrites_anchor_on_function_link(self):
        text = "[remarks](calculate-function-dax.md#remarks)"
        result = rewrite_links(text)
        self.assertIn("(./calculate.md#remarks)", result)

    def test_multiple_links_in_one_text(self):
        text = (
            "- [ALL](all-function-dax.md)\n"
            "- [FILTER](filter-function-dax.md)\n"
            "- [DAX overview](dax-overview.md)\n"
        )
        result = rewrite_links(text)
        self.assertIn("(./all.md)", result)
        self.assertIn("(./filter.md)", result)
        self.assertIn("(dax-overview.md)", result)

    def test_does_not_rewrite_external_urls(self):
        text = "[Power BI](https://powerbi.microsoft.com/some-path)"
        result = rewrite_links(text)
        self.assertEqual(text, result)

    def test_does_not_rewrite_category_index_links(self):
        text = "[Filter functions](filter-functions-dax.md)"
        result = rewrite_links(text)
        self.assertEqual(text, result,
                         "Category index links end in -functions-dax.md, not -function-dax.md")


class BuildLibraryCard(unittest.TestCase):
    """build_library_card() produces the full markdown content for library/<fn>.md."""

    def category_map(self):
        return {
            "calculate-function-dax.md": {
                "name": "CALCULATE",
                "summary": "Evaluates an expression in a modified filter context.",
                "category": ["filter"],
                "primaryCategory": "filter",
            }
        }

    def test_frontmatter_contains_name(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("name: CALCULATE", card)

    def test_frontmatter_contains_applies_to(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("appliesTo:", card)
        self.assertIn("measure", card)

    def test_frontmatter_contains_discouraged_false(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("discouragedInVisualCalculations: false", card)

    def test_frontmatter_contains_discouraged_true_for_discouraged_doc(self):
        category_map = {
            "earlier-function-dax.md": {
                "name": "EARLIER",
                "summary": "Returns the current value.",
                "category": ["filter"],
                "primaryCategory": "filter",
            }
        }
        card = build_library_card(DISCOURAGED_DOC, "earlier-function-dax.md",
                                  category_map, {}, set())
        self.assertIn("discouragedInVisualCalculations: true", card)

    def test_frontmatter_contains_source(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("source: query-languages/dax/calculate-function-dax.md", card)

    def test_frontmatter_contains_source_date(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("sourceDate: 06/29/2026", card)

    def test_notes_is_false_when_not_in_notes_set(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("notes: false", card)

    def test_notes_is_true_when_in_notes_set(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, {"calculate"})
        self.assertIn("notes: true", card)

    def test_body_contains_syntax_section(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("## Syntax", card)
        self.assertIn("CALCULATE(<expression>", card)

    def test_body_has_cross_links_rewritten(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("./calculatetable.md", card)
        self.assertNotIn("calculatetable-function-dax.md", card)

    def test_ms_frontmatter_is_stripped_from_body(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertNotIn("ms.topic: reference", card)

    def test_include_line_is_stripped_from_body(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertNotIn("[!INCLUDE", card)

    def test_returns_scalar_for_filter_category(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertIn("returns: scalar", card)

    def test_the_return_type_comes_from_the_document_not_the_category(self):
        # This used to assert 'table' purely because primaryCategory was
        # table-manipulation, on a fixture whose own '## Return value' says
        # "The value that results from the expression" — i.e. scalar. Guessing from the
        # category stamped 'scalar' on 123 of 458 real functions that return a table, so
        # the category no longer decides: the page does.
        category_map = {
            "summarize-function-dax.md": {
                "name": "SUMMARIZE",
                "summary": "Returns a summary table.",
                "category": ["table-manipulation"],
                "primaryCategory": "table-manipulation",
            }
        }
        doc = CALCULATE_DOC.replace("calculate-function-dax.md", "summarize-function-dax.md")
        card = build_library_card(doc, "summarize-function-dax.md", category_map, {}, set())
        self.assertIn("returns: scalar", card)

    def test_a_document_that_returns_a_table_is_stamped_table(self):
        category_map = {
            "filter-function-dax.md": {
                "name": "FILTER", "summary": "", "category": ["filter"],
                "primaryCategory": "filter",   # NOT table-manipulation
            }
        }
        card = build_library_card(RETVAL_TABLE, "filter-function-dax.md",
                                  category_map, {}, set())
        self.assertIn("returns: table", card)

    def test_category_sha_stamped_when_provided(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set(), source_sha="abc1234")
        self.assertIn("abc1234", card)

    def test_card_starts_with_yaml_frontmatter_delimiter(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md",
                                  self.category_map(), {}, set())
        self.assertTrue(card.startswith("---\n"))


RETVAL_TABLE = """# FILTER

[!INCLUDE[applies-to-measures-columns-tables](includes/applies-to-measures-columns-tables.md)]

Returns a table.

## Return value

A table containing only the filtered rows.

## Remarks
"""

RETVAL_SCALAR = """# COUNTROWS

## Return value

The number of rows in the table.

## Remarks
"""

RETVAL_NONE = """# DEGREES

## Remarks

No return-value section at all.
"""


class ParseReturnValue(unittest.TestCase):
    """Pass 2 must READ the return type. Guessing it from the category stamped
    'scalar' on 123 of 458 real functions whose own docs say table."""

    def test_reads_table_from_the_return_value_section(self):
        self.assertEqual(parse_return_value(RETVAL_TABLE), "table")

    def test_a_table_mentioned_after_a_preposition_is_not_the_return(self):
        # COUNTROWS: "The number of rows in the table" — scalar despite the word.
        self.assertEqual(parse_return_value(RETVAL_SCALAR), "scalar")

    def test_a_leading_clause_does_not_hide_the_table(self):
        # DATEADD: "For date column input, a table containing a single column..."
        text = "## Return value\n\nFor date column input, a table containing dates.\n"
        self.assertEqual(parse_return_value(text), "table")

    def test_a_single_column_result_counts_as_a_table(self):
        # DISTINCT describes its one-column table as "A column of unique values".
        text = "## Return value\n\nA column of unique values.\n"
        self.assertEqual(parse_return_value(text), "table")

    def test_returns_none_when_the_document_has_no_return_value_section(self):
        self.assertIsNone(parse_return_value(RETVAL_NONE))


class DetermineReturnsFromText(unittest.TestCase):

    def test_an_override_wins_over_the_parsed_value(self):
        ovr = {"returns": {"FILTER": "scalar"}}
        cmap = {"filter-function-dax.md": {"name": "FILTER"}}
        self.assertEqual(
            determine_returns("filter-function-dax.md", RETVAL_TABLE, cmap, ovr), "scalar")

    def test_falls_back_to_the_parsed_value(self):
        cmap = {"filter-function-dax.md": {"name": "FILTER"}}
        self.assertEqual(
            determine_returns("filter-function-dax.md", RETVAL_TABLE, cmap, {}), "table")

    def test_unresolvable_returns_empty_rather_than_guessing_scalar(self):
        cmap = {"degrees-function-dax.md": {"name": "DEGREES"}}
        self.assertEqual(
            determine_returns("degrees-function-dax.md", RETVAL_NONE, cmap, {}), "")


class AppliesToDoesNotFabricate(unittest.TestCase):
    """Asserting a permission the document never granted is the worst failure a
    reference can have: the agent stops inventing and starts trusting the invention."""

    def test_a_missing_include_yields_no_claim(self):
        self.assertEqual(parse_applies_to("# ABS\n\nNo include here.\n"), ([], None))

    def test_an_unknown_include_variant_yields_no_claim(self):
        text = "[!INCLUDE[x](includes/applies-to-something-new.md)]\n"
        self.assertEqual(parse_applies_to(text), ([], None))

    def test_a_known_include_is_still_read_normally(self):
        self.assertEqual(parse_applies_to(RETVAL_TABLE),
                         (["measure", "column", "table"], False))


GOOD_DOC = """---
ms.date: 06/29/2026
---
# CALCULATE

[!INCLUDE[applies-to-measures-columns-tables](includes/applies-to-measures-columns-tables.md)]

Evaluates an expression.

## Return value

A decimal number.

## Remarks

Notes.
"""


class Pass2Gates(MainFixture, unittest.TestCase):
    """main() has to RUN pass 2, not just ship its parsers. Measured on the real corpus:
    every one of the 479 docs carries a recognisable applies-to include, and exactly 3
    (DATEVALUE, DEGREES, RADIANS) lack a Return value section - those live in overrides.
    So both ceilings are zero, and anything above it means upstream moved."""

    def setUp(self):
        self.set_up_corpus()
        self.write("filter-functions-dax.md", FILTER_INDEX)
        self.write("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL"))
        self.write("calculate-function-dax.md", GOOD_DOC)

    def write(self, fn, body):
        with open(os.path.join(self.dir, fn), "w", encoding="utf-8") as f:
            f.write(body)

    def run_main(self):
        with io.StringIO() as out, io.StringIO() as err:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["sync_query_docs.py", self.dir])
            return code, err.getvalue()

    def test_a_clean_corpus_passes(self):
        code, _ = self.run_main()
        self.assertEqual(code, 0)

    def test_an_unknown_applies_to_variant_fails_the_build(self):
        self.write("calculate-function-dax.md",
                   GOOD_DOC.replace("applies-to-measures-columns-tables",
                                    "applies-to-something-microsoft-just-added"))
        code, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("applies-to", err)

    def test_a_document_with_no_return_value_section_fails_the_build(self):
        self.write("calculate-function-dax.md", GOOD_DOC.split("## Return value")[0])
        code, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("return", err.lower())

    def test_pass_2_reports_how_many_cards_it_could_build(self):
        _, err = self.run_main()
        self.assertIn("pass 2", err.lower())


class OrphanCardNaming(unittest.TestCase):

    def test_an_uncategorized_doc_takes_its_name_from_its_own_heading(self):
        card = build_library_card(GOOD_DOC.replace("CALCULATE", "COLLAPSE"),
                                  "collapse-function-dax.md", {}, {}, set())
        self.assertIn("name: COLLAPSE", card)

    def test_the_name_is_not_derived_from_the_filename(self):
        # filename says one thing, the heading says another: the heading wins.
        card = build_library_card(GOOD_DOC.replace("CALCULATE", "INFO.VIEW.TABLES"),
                                  "some-other-name-function-dax.md", {}, {}, set())
        self.assertIn("name: INFO.VIEW.TABLES", card)
        self.assertNotIn("SOME.OTHER.NAME", card)


class WriteLibrary(unittest.TestCase):
    """The catalog and the cards are one deliverable: validate_skills requires every
    catalog row to have a card and every card to have a row, so a catalog written
    without cards breaks the build by construction."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        self.write(self.src, "filter-functions-dax.md", FILTER_INDEX)
        self.write(self.src, "all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL"))
        self.write(self.src, "calculate-function-dax.md", GOOD_DOC)

    def write(self, d, fn, body):
        os.makedirs(os.path.dirname(os.path.join(d, fn)) or d, exist_ok=True)
        with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
            f.write(body)

    def run_write(self, notes=()):
        notes_dir = os.path.join(self.out, "notes")
        os.makedirs(notes_dir, exist_ok=True)
        for stem in notes:
            self.write(notes_dir, f"{stem}.md", "## Trampa\n\nAlgo.\n")
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="abc1234", source_date="2026-08-10T00:00:00Z")

    def read(self, rel):
        """Relative to the skill root — for the hand-written files, which stay outside."""
        with open(os.path.join(self.out, rel), encoding="utf-8") as f:
            return f.read()

    def gen(self, rel):
        """Relative to generated/ — everything the sync produces."""
        return self.read(os.path.join("generated", rel))

    def test_writes_one_card_per_function_named_after_its_stem(self):
        self.run_write()
        self.assertEqual(sorted(os.listdir(os.path.join(self.out, "generated", "library"))),
                         ["all.md", "calculate.md"])

    def test_the_catalog_row_count_matches_the_cards(self):
        self.run_write()
        cat = json.loads(self.gen("catalog.json"))
        self.assertEqual(cat["functionCount"], 2)
        self.assertEqual({f["file"] for f in cat["functions"]}, {"all", "calculate"})

    def test_stamps_the_upstream_repo_sha_and_date(self):
        self.run_write()
        cat = json.loads(self.gen("catalog.json"))
        self.assertEqual(cat["source"], "MicrosoftDocs/query-docs@abc1234")
        self.assertEqual(cat["sourceCommitDate"], "2026-08-10T00:00:00Z")

    def test_the_human_catalog_has_a_row_per_function(self):
        self.run_write()
        md = self.gen("catalog.md")
        self.assertIn("| CALCULATE |", md)
        self.assertIn("| ALL |", md)

    def test_a_function_with_a_hand_written_note_is_flagged_in_both_catalogs(self):
        self.run_write(notes=["calculate"])
        cat = json.loads(self.gen("catalog.json"))
        flagged = {f["file"] for f in cat["functions"] if f["notes"]}
        self.assertEqual(flagged, {"calculate"})
        row = [l for l in self.gen("catalog.md").splitlines() if "| CALCULATE |" in l][0]
        self.assertIn("★", row)

    def test_notes_are_never_touched_by_the_write(self):
        self.run_write(notes=["calculate"])
        self.assertEqual(self.read("notes/calculate.md"), "## Trampa\n\nAlgo.\n")

    def test_rerunning_produces_the_same_tree(self):
        self.run_write()
        first = {p: self.gen(os.path.join("library", p))
                 for p in os.listdir(os.path.join(self.out, "generated", "library"))}
        self.run_write()
        second = {p: self.gen(os.path.join("library", p))
                  for p in os.listdir(os.path.join(self.out, "generated", "library"))}
        self.assertEqual(first, second)

    def test_a_card_removed_upstream_does_not_survive_the_next_write(self):
        self.run_write()
        self.write(self.out, "generated/library/ghost.md", "---\nname: GHOST\n---\n")
        self.run_write()
        self.assertNotIn("ghost.md", os.listdir(os.path.join(self.out, "generated", "library")))


class PublishedTreeLayout(unittest.TestCase):
    """Everything the sync generates lives under one directory, so installing it is a
    single rename. Spread across three paths at the skill root it needed a hand-written
    rollback to undo a half-finished install, and that rollback was where every review
    finding landed. The hand-written files stay outside it."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)

    def _run(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="abc1234", source_date="2026-08-10T00:00:00Z")

    def test_the_catalogs_and_the_cards_land_under_one_directory(self):
        self._run()
        gen = os.path.join(self.out, "generated")
        self.assertTrue(os.path.isfile(os.path.join(gen, "catalog.json")))
        self.assertTrue(os.path.isfile(os.path.join(gen, "catalog.md")))
        self.assertEqual(sorted(os.listdir(os.path.join(gen, "library"))),
                         ["all.md", "calculate.md"])

    def test_nothing_generated_is_left_at_the_skill_root(self):
        self._run()
        # A stale copy at the old path would be read by an agent and never refreshed,
        # because the swap no longer touches it.
        for stale in ("catalog.json", "catalog.md", "library"):
            self.assertFalse(os.path.exists(os.path.join(self.out, stale)),
                             f"{stale} must live inside generated/, not beside it")

    def test_a_first_publish_that_fails_leaves_no_half_built_tree(self):
        # Nothing existed before, so there is nothing to restore and the recovery path is
        # skipped entirely. What must still hold is that the run leaves no trace: a
        # generated/ that only got part-way through is worse than no generated/ at all.
        import sync_query_docs as mod
        real = os.replace

        def explode(a, b):
            raise OSError("volume went away installing the first generation")

        mod.os.replace = explode
        try:
            with self.assertRaises(OSError):
                self._run()
        finally:
            mod.os.replace = real
        self.assertFalse(os.path.exists(os.path.join(self.out, "generated")))
        self.assertEqual([d for d in os.listdir(self.out) if d.startswith(".publish-")], [])

    def test_the_hand_written_files_stay_outside_the_swapped_directory(self):
        notes = os.path.join(self.out, "notes")
        os.makedirs(notes, exist_ok=True)
        with open(os.path.join(notes, "calculate.md"), "w", encoding="utf-8") as f:
            f.write("## Trampa\n\nAlgo.\n")
        self._run()
        # notes/ is authored by hand. Inside generated/ the swap would delete it.
        with open(os.path.join(notes, "calculate.md"), encoding="utf-8") as f:
            self.assertEqual(f.read(), "## Trampa\n\nAlgo.\n")
        self.assertFalse(os.path.exists(os.path.join(self.out, "generated", "notes")))


IDEMPOTENCE_TOC = """items:
- name: DAX
  items:
  - name: DAX functions
    items:
    - name: Filter functions
      items:
      - name: Filter functions
        href: filter-functions-dax.md
      - name: CALCULATE
        href: calculate-function-dax.md
      - name: ALL
        href: all-function-dax.md
"""


class Idempotence(unittest.TestCase):
    """Two runs against the same upstream produce the same tree, byte for byte.

    It is in the plan's definition of done and was only ever checked by hand. Without it
    the weekly sync would open a pull request every Monday whose diff was the generator
    disagreeing with itself, and a diff that always exists is a diff nobody reads.
    """

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        # Written in an order that is not alphabetical on purpose: if anything downstream
        # took the order it found on disk, the two runs could still agree while CI and a
        # laptop disagreed. Sorting is what makes the tree portable, not just repeatable.
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("calculate-function-dax.md", GOOD_DOC),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         # Two concept pages, written in reverse alphabetical order for
                         # the same reason as the functions.
                         ("zeta-tema.md", "---\ntitle: Zeta\nms.date: 01/01/2026\n---\n# Zeta\n\nAlgo.\n"),
                         ("alfa-tema.md", "---\ntitle: Alfa\nms.date: 01/01/2026\n---\n# Alfa\n\nAlgo.\n"),
                         # The CLI refuses to run without upstream's own table of contents,
                         # so the subprocess test needs one even though write_library does not.
                         ("toc.yml", IDEMPOTENCE_TOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)

    def _run(self, docs=None):
        mapping = build_category_map(discover_indexes(self.src))
        use = discover_function_docs(self.src) if docs is None else docs
        # Applied to the docs actually being published. Deriving the categories from one
        # list and publishing another works only while the two hold the same names.
        apply_filename_rules(mapping, use)
        return write_library(self.src, self.out, mapping, use, {},
                             source_sha="abc1234", source_date="2026-08-10T00:00:00Z")

    def _snapshot(self):
        """Every generated file as {relative path: bytes}."""
        gen = os.path.join(self.out, "generated")
        tree = {}
        for dirpath, _, filenames in os.walk(gen):
            for name in filenames:
                path = os.path.join(dirpath, name)
                with open(path, "rb") as f:
                    tree[os.path.relpath(path, gen).replace("\\", "/")] = f.read()
        return tree

    def test_two_runs_produce_the_same_tree(self):
        self._run()
        first = self._snapshot()
        self._run()
        second = self._snapshot()
        self.assertEqual(sorted(first), sorted(second), "the second run changed the file list")
        differing = sorted(k for k in first if first[k] != second[k])
        self.assertEqual(differing, [], f"the second run changed: {differing}")
        self.assertTrue(first, "nothing was generated, so the comparison proved nothing")

    def test_two_runs_under_different_hash_seeds_produce_the_same_tree(self):
        """Same tree from two separate processes, seeded differently.

        The test above runs both generations inside one interpreter, which shares one
        PYTHONHASHSEED. Iterating a set or a dict keyed by strings would come out in the
        same order both times and the comparison would prove nothing about CI, where the
        seed is different every run. Two subprocesses with the seed pinned to different
        values is what actually tests it.
        """
        import shutil
        import subprocess
        # Run a COPY of the script from a bare skill root. `load_overrides` reads
        # overrides.json from the script's own parent, so the real one would come along
        # and its declared exceptions — none of which exist in this three-file fixture —
        # would trip the stale-uncategorized gate before anything got written.
        root = tempfile.mkdtemp()
        os.makedirs(os.path.join(root, "scripts"))
        script = os.path.join(root, "scripts", "sync_query_docs.py")
        shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "sync_query_docs.py"), script)
        trees = []
        for seed in ("0", "1"):
            out = tempfile.mkdtemp()
            env = dict(os.environ, PYTHONHASHSEED=seed)
            run = subprocess.run([sys.executable, script, self.src, "--write", "--out", out],
                                 capture_output=True, text=True, env=env)
            self.assertEqual(run.returncode, 0, run.stderr)
            gen = os.path.join(out, "generated")
            tree = {}
            for dirpath, _, filenames in os.walk(gen):
                for name in filenames:
                    path = os.path.join(dirpath, name)
                    with open(path, "rb") as f:
                        tree[os.path.relpath(path, gen).replace("\\", "/")] = f.read()
            trees.append(tree)

        self.assertTrue(trees[0], "nothing was generated, so the comparison proved nothing")
        self.assertEqual(sorted(trees[0]), sorted(trees[1]))
        differing = sorted(k for k in trees[0] if trees[0][k] != trees[1][k])
        self.assertEqual(differing, [], f"the two seeds disagreed on: {differing}")

    def test_the_catalog_is_sorted_rather_than_in_the_order_it_was_handed(self):
        # Handed in reverse on purpose. Reading them off disk would not test this:
        # discover_function_docs already sorts, so the catalog would come out alphabetical
        # whether or not anything sorted it, and the test would pass over a removed sort.
        reversed_docs = sorted(discover_function_docs(self.src), reverse=True)
        self._run(docs=reversed_docs)
        with open(os.path.join(self.out, "generated", "catalog.json"), encoding="utf-8") as f:
            catalog = json.load(f)
        names = [fn["name"] for fn in catalog["functions"]]
        self.assertEqual(names, sorted(names))
        self.assertIn("ALL", names)   # handed last, and first alphabetically

        # The concept index too. This one pins the PUBLISHED order and nothing more:
        # concepts are discovered inside write_library and arrive sorted already, so
        # removing `concepts.sort` does not fail this — checked with the mutation. What it
        # does guarantee is what a consumer reads, whichever line ends up producing it.
        concepts = [c["file"] for c in catalog["concepts"]]
        self.assertEqual(concepts, sorted(concepts))
        self.assertEqual(concepts[0], "alfa-tema")   # written second, listed first


TOC_YML = """items:
- name: DAX
  items:
  - name: DAX functions
    items:
    - name: Filter functions
      items:
      - name: Filter functions
        href: filter-functions-dax.md
      - name: CALCULATE
        href: calculate-function-dax.md
      - name: FIRSTNONBLANK
        href: firstnonblank-function-dax.md
    - name: Statistical functions
      items:
      - name: SAMPLECARTESIANPOINTSBYCOVER
        href: samplecartesianpointsbycover-function-dax.md
    - name: Best practices
      items:
      - name: Use variables
        href: best-practices/dax-variables.md
"""


class TocIsAFourthRouteToACategory(unittest.TestCase):
    """The 15 category indexes leave 21 of 479 functions unclassified, but Learn's own
    navigation places 5 of them. toc.yml is upstream's authoritative table of contents, so
    reading it assigns a category Microsoft actually gave rather than one this pipeline
    guessed. Its 15 section names derive to exactly the 15 index slugs — verified against
    the real file, not assumed."""

    KNOWN = {"filter", "statistical"}

    def test_a_function_takes_the_category_of_its_section(self):
        self.assertEqual(parse_toc(TOC_YML, self.KNOWN)["firstnonblank-function-dax.md"],
                         "filter")

    def test_sections_derive_to_the_index_slugs(self):
        self.assertEqual(parse_toc(TOC_YML, self.KNOWN)["samplecartesianpointsbycover-function-dax.md"],
                         "statistical")

    def test_the_index_page_itself_is_not_a_function(self):
        self.assertNotIn("filter-functions-dax.md", parse_toc(TOC_YML, self.KNOWN))

    def test_a_page_outside_the_function_sections_is_ignored(self):
        # best-practices/dax-variables.md is a concept; it has no category and must not
        # acquire one from the section it happens to sit under.
        self.assertNotIn("best-practices/dax-variables.md", parse_toc(TOC_YML, self.KNOWN))

    def test_it_only_fills_gaps_and_never_overrides_an_index(self):
        # The indexes are the primary source; the TOC is the fallback. A function the
        # indexes DID classify keeps their answer.
        mapping = build_category_map(discover_indexes_from([(FILTER_INDEX,
                                                             "filter-functions-dax.md")]))
        before = mapping["calculate-function-dax.md"]["primaryCategory"]
        apply_toc(mapping, parse_toc(TOC_YML, self.KNOWN), ["calculate-function-dax.md",
                                                "firstnonblank-function-dax.md"])
        self.assertEqual(mapping["calculate-function-dax.md"]["primaryCategory"], before)

    def test_it_categorizes_what_the_indexes_missed(self):
        mapping = build_category_map(discover_indexes_from([(FILTER_INDEX,
                                                             "filter-functions-dax.md")]))
        added = apply_toc(mapping, parse_toc(TOC_YML, self.KNOWN),
                          ["firstnonblank-function-dax.md"])
        self.assertEqual(added, ["firstnonblank-function-dax.md"])
        self.assertEqual(mapping["firstnonblank-function-dax.md"]["primaryCategory"],
                         "filter")

    def test_a_section_that_is_not_a_real_category_is_refused(self):
        # The TOC's section name is a display string, not a category. Deriving a slug from
        # it and stamping it on a card would put a category in the library that no index
        # backs — this repo's one unforgivable failure, since a reader cannot tell an
        # invented classification from a real one.
        toc = TOC_YML.replace("Statistical functions", "Handy shortcuts")
        with self.assertRaises(ValueError) as caught:
            parse_toc(toc, {"filter", "statistical"})
        self.assertIn("Handy shortcuts", str(caught.exception))

    def test_a_function_under_two_different_sections_is_refused(self):
        # Last-write-wins would pick one silently, and which one depends on TOC order.
        toc = TOC_YML + """    - name: Text functions
      items:
      - name: FIRSTNONBLANK
        href: firstnonblank-function-dax.md
"""
        with self.assertRaises(ValueError) as caught:
            parse_toc(toc, {"filter", "statistical", "text"})
        self.assertIn("firstnonblank-function-dax.md", str(caught.exception))

    def test_the_same_function_twice_under_one_section_is_fine(self):
        toc = TOC_YML + """    - name: Filter functions
      items:
      - name: FIRSTNONBLANK
        href: firstnonblank-function-dax.md
"""
        self.assertEqual(parse_toc(toc, {"filter", "statistical"})
                         ["firstnonblank-function-dax.md"], "filter")

    def test_the_known_categories_come_from_the_indexes_themselves(self):
        # So a genuinely new category — which arrives as a new '*-functions-dax.md' — is
        # accepted without anyone editing a list here.
        toc = TOC_YML.replace("Statistical functions", "Quantum functions")
        self.assertEqual(parse_toc(toc, {"filter", "quantum"})
                         ["samplecartesianpointsbycover-function-dax.md"], "quantum")

    def test_a_missing_toc_is_not_a_silent_zero(self):
        # No toc.yml means the fourth route is simply absent; the caller must be able to
        # tell that from "the toc classified nothing".
        with self.assertRaises(OSError):
            read_toc(tempfile.mkdtemp())


def discover_indexes_from(pairs):
    """The (text, filename) shape discover_indexes returns, without touching disk."""
    return list(pairs)


class UncategorizedGate(unittest.TestCase):
    """MAX_UNCATEGORIZED was an anonymous ceiling: 30 slots, 21 in use, and nine spare in
    which a real regression could hide unnoticed. The gate now names the exceptions, so a
    function that loses its category fails the run even though the total did not move."""

    def test_a_new_uncategorized_function_fails(self):
        bad = uncategorized_gate(["topnskip-function-dax.md", "brandnew-function-dax.md"],
                                 {"TOPNSKIP"})
        self.assertEqual(bad, ["BRANDNEW"])

    def test_the_declared_exceptions_pass(self):
        self.assertEqual(uncategorized_gate(["topnskip-function-dax.md"], {"TOPNSKIP"}), [])

    def test_a_swap_that_keeps_the_count_still_fails(self):
        # The exact hole in a ceiling: one function gains a category, another loses it, the
        # total is unchanged and nothing looks wrong.
        self.assertEqual(uncategorized_gate(["other-function-dax.md"], {"TOPNSKIP"}),
                         ["OTHER"])

    def test_a_stale_exception_is_reported(self):
        # Upstream classifying one of them is good news, but leaving the name behind rots
        # the list into a set of claims nobody has checked.
        self.assertEqual(stale_uncategorized([], {"TOPNSKIP"}), ["TOPNSKIP"])

    def test_nothing_stale_when_it_is_still_uncategorized(self):
        self.assertEqual(stale_uncategorized(["topnskip-function-dax.md"], {"TOPNSKIP"}), [])


class BrokenLinkGate(unittest.TestCase):
    """Gate 3, and the one with the most evidence behind it: the first run of this pipeline
    produced 637 broken relative links out of 1755 and nothing failed. Checked in memory,
    before the swap, so a bad generation never reaches disk."""

    def trees(self, library=None, concepts=None):
        return {"library": library or {}, "concepts": concepts or {}}

    def test_a_card_linking_to_a_missing_card_is_caught(self):
        bad = broken_local_links(self.trees(library={
            "calculate": "see [ALL](./all.md)",
        }))
        self.assertEqual(bad, [("library/calculate.md", "./all.md")])

    def test_a_link_that_resolves_is_not_reported(self):
        self.assertEqual(broken_local_links(self.trees(library={
            "calculate": "see [ALL](./all.md)", "all": "x",
        })), [])

    def test_a_concept_reaching_the_library_is_resolved_across_directories(self):
        self.assertEqual(broken_local_links(self.trees(
            library={"calculate": "x"},
            concepts={"dax-glossary": "see [CALCULATE](../library/calculate.md)"})), [])

    def test_a_concept_pointing_at_a_card_that_does_not_exist_is_caught(self):
        bad = broken_local_links(self.trees(
            concepts={"dax-glossary": "see [GHOST](../library/ghost.md)"}))
        self.assertEqual(bad, [("concepts/dax-glossary.md", "../library/ghost.md")])

    def test_an_anchor_does_not_make_a_good_link_look_broken(self):
        self.assertEqual(broken_local_links(self.trees(library={
            "calculate": "see [ALL](./all.md#remarks)", "all": "x"})), [])

    def test_absolute_urls_are_not_this_gate_s_business(self):
        self.assertEqual(broken_local_links(self.trees(library={
            "calculate": "see [docs](https://learn.microsoft.com/en-us/dax/all)"})), [])


class OrphanNoteGate(unittest.TestCase):
    """Gate 2. A note written for a function that upstream later renamed or removed points
    at a card that is not there, and the ★ flag in the catalog promises a page that cannot
    be opened. validate_skills catches it in CI; the sync must not build it in the first
    place."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.out, "notes"))
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)

    def note(self, stem):
        with open(os.path.join(self.out, "notes", f"{stem}.md"), "w",
                  encoding="utf-8") as f:
            f.write("## Trampa\n\nAlgo.\n")

    def _run(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="a", source_date="d")

    def test_a_note_with_no_card_fails_the_run(self):
        self.note("ghost")
        with self.assertRaises(ValueError) as caught:
            self._run()
        self.assertIn("ghost", str(caught.exception))

    def test_a_note_with_its_card_is_fine(self):
        self.note("calculate")
        self._run()
        self.assertTrue(os.path.exists(
            os.path.join(self.out, "generated", "library", "calculate.md")))

    def test_nothing_is_published_when_a_note_is_orphaned(self):
        self.note("ghost")
        with self.assertRaises(ValueError):
            self._run()
        self.assertFalse(os.path.exists(os.path.join(self.out, "generated")))


class CountDeviationGate(unittest.TestCase):
    """Gate 4. The previous catalog.json is already on disk, so 'compared with the last
    sync' needs no state file of its own."""

    def test_a_small_move_passes(self):
        self.assertIsNone(count_deviation(479, 480, "functionCount"))

    def test_a_collapse_is_reported(self):
        msg = count_deviation(479, 300, "functionCount")
        self.assertIn("functionCount", msg)
        self.assertIn("479", msg)
        self.assertIn("300", msg)

    def test_a_jump_is_reported_too(self):
        # Upwards matters as much: a parser that starts counting index pages as functions
        # inflates the library just as silently as one that drops them.
        self.assertIsNotNone(count_deviation(479, 900, "functionCount"))

    def read_counts(self, body):
        out = tempfile.mkdtemp()
        os.makedirs(os.path.join(out, "generated"))
        with open(os.path.join(out, "generated", "catalog.json"), "w",
                  encoding="utf-8") as f:
            f.write(body)
        return sync_query_docs._previous_counts(out)

    def test_a_catalog_that_is_not_an_object_is_treated_as_absent(self):
        # A catalog nobody can read must not be able to block the sync that would replace
        # it. json.load succeeds on these — it is .get that then explodes.
        for body in ("[]", "null", '"a string"', "not json at all"):
            with self.subTest(body=body):
                self.assertEqual(self.read_counts(body), {})

    def test_a_non_numeric_count_is_treated_as_absent(self):
        self.assertEqual(self.read_counts('{"functionCount": "a"}'), {})

    def test_a_readable_catalog_is_used(self):
        self.assertEqual(self.read_counts('{"functionCount": 479, "conceptCount": 34}'),
                         {"functionCount": 479, "conceptCount": 34})

    def test_the_first_ever_sync_has_nothing_to_compare(self):
        self.assertIsNone(count_deviation(None, 479, "functionCount"))

    def test_growing_from_zero_is_not_a_deviation(self):
        self.assertIsNone(count_deviation(0, 479, "functionCount"))


class DiscoverConceptDocs(unittest.TestCase):
    """A page that is neither a function doc nor a category index is a concept. The rule is
    mechanical on purpose: a curated list of 34 filenames goes stale the first time
    Microsoft adds a page, and going stale silently is the failure this repo exists to
    avoid. includes/ holds transclusion fragments and media/ holds images — neither is a
    page, so the descent is limited to directories known to carry content."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        for d in ("best-practices", "includes", "media"):
            os.makedirs(os.path.join(self.src, d))
        for rel in ("dax-glossary.md", "dax-overview.md",
                    "calculate-function-dax.md", "filter-functions-dax.md",
                    "best-practices/dax-variables.md",
                    "includes/applies-to-measures.md",
                    "media/not-a-page.md"):
            with open(os.path.join(self.src, rel), "w", encoding="utf-8") as f:
                f.write("---\ntitle: x\ndescription: y\n---\n# x\n")

    def test_the_pages_that_are_neither_functions_nor_indexes(self):
        self.assertEqual(discover_concept_docs(self.src),
                         ["best-practices/dax-variables.md",
                          "dax-glossary.md", "dax-overview.md"])

    def test_transclusion_fragments_and_media_are_not_pages(self):
        found = discover_concept_docs(self.src)
        self.assertNotIn("includes/applies-to-measures.md", found)
        self.assertNotIn("media/not-a-page.md", found)

    def test_a_nested_directory_inside_a_known_content_dir_is_reported(self):
        # The worst blind spot of the two checks put together: best-practices/ is read, so
        # the drift guard skipped it wholesale, and the read only goes one level — so
        # best-practices/advanced/foo.md was neither generated nor reported.
        os.makedirs(os.path.join(self.src, "best-practices", "advanced"))
        with open(os.path.join(self.src, "best-practices", "advanced", "foo.md"), "w",
                  encoding="utf-8") as f:
            f.write("# nested\n")
        self.assertEqual(unlisted_content_dirs(self.src), ["best-practices/advanced"])

    def test_media_inside_a_known_content_dir_is_not_reported(self):
        os.makedirs(os.path.join(self.src, "best-practices", "media"))
        self.assertEqual(unlisted_content_dirs(self.src), [])

    def test_a_nested_content_directory_is_reported_too(self):
        # Looking one level down saw only the subfolder, not the pages inside it, so a
        # nested docs area produced no warning at all — the silent case this exists to
        # prevent, dressed up as a check.
        os.makedirs(os.path.join(self.src, "guidance", "advanced"))
        with open(os.path.join(self.src, "guidance", "advanced", "page.md"), "w",
                  encoding="utf-8") as f:
            f.write("# nested\n")
        self.assertEqual(unlisted_content_dirs(self.src), ["guidance"])

    def test_a_new_content_directory_is_reported_rather_than_silently_dropped(self):
        # The cost of limiting the descent is missing a directory Microsoft adds later.
        # That has to be loud: silence here is indistinguishable from "there was nothing".
        os.makedirs(os.path.join(self.src, "guidance"))
        with open(os.path.join(self.src, "guidance", "new-page.md"), "w",
                  encoding="utf-8") as f:
            f.write("# new\n")
        self.assertEqual(unlisted_content_dirs(self.src), ["guidance"])

    def test_the_known_directories_are_not_reported(self):
        self.assertEqual(unlisted_content_dirs(self.src), [])


CONCEPT_DOC = """---
title: "Use variables to improve your DAX formulas"
description: "Learn more about: DAX variables"
ms.topic: best-practice
ms.date: 08/25/2021
---

# Use variables to improve your DAX formulas

Variables can improve performance. See [CALCULATE](../calculate-function-dax.md) and the
[filter functions](../filter-functions-dax.md).
"""


class BuildConceptCard(unittest.TestCase):
    """A concept card is the upstream page with Microsoft's frontmatter replaced by ours.
    Its slug is the upstream stem, so a reader can always get back to the source."""

    def card(self, text=CONCEPT_DOC, rel="best-practices/dax-variables.md", **kw):
        return build_concept_card(text, rel, source_sha="abc1234", **kw)

    def test_the_frontmatter_carries_title_topic_and_summary(self):
        import yaml
        fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", self.card(), re.S).group(1))
        self.assertEqual(fm["title"], "Use variables to improve your DAX formulas")
        self.assertEqual(fm["topic"], "best-practice")
        self.assertEqual(fm["summary"], "Learn more about: DAX variables")
        self.assertEqual(fm["sourceDate"], "08/25/2021")

    def test_it_stamps_the_upstream_path_and_sha(self):
        import yaml
        fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", self.card(), re.S).group(1))
        self.assertEqual(fm["source"],
                         "query-languages/dax/best-practices/dax-variables.md@abc1234")

    def test_microsofts_own_frontmatter_is_replaced_not_kept(self):
        card = self.card()
        self.assertNotIn("ms.topic:", card)
        self.assertEqual(card.count("---\n"), 2)

    def test_a_link_to_a_function_points_at_the_library(self):
        # A concept sits in concepts/, one directory away from the cards. Reusing the
        # library's own './<fn>.md' would resolve to concepts/<fn>.md, which is nothing.
        self.assertIn("(../library/calculate.md)", self.card())

    def test_a_link_to_a_category_index_becomes_an_upstream_url(self):
        # There are no local index pages — catalog.md replaced them.
        self.assertIn("learn.microsoft.com/en-us/dax/filter-functions-dax", self.card())


class RewriteLinksFromASubdirectory(unittest.TestCase):
    """Pages in best-practices/ reach the function docs with '../calculate-function-dax.md'.
    The rewrite only matched bare siblings, so those links fell through to the upstream-URL
    pass and left the local library — sitting right there — unused."""

    def test_a_parent_relative_function_link_is_rewritten_too(self):
        self.assertEqual(rewrite_links("[CALCULATE](../calculate-function-dax.md)"),
                         "[CALCULATE](./calculate.md)")

    def test_the_prefix_is_the_callers_to_choose(self):
        self.assertEqual(
            rewrite_links("[CALCULATE](calculate-function-dax.md)", prefix="../library/"),
            "[CALCULATE](../library/calculate.md)")

    def test_the_default_prefix_is_unchanged(self):
        # The 479 cards link to each other with './'; changing that would churn them all.
        self.assertEqual(rewrite_links("[ALL](all-function-dax.md)"), "[ALL](./all.md)")

    def test_an_anchor_survives_the_parent_relative_form(self):
        self.assertEqual(rewrite_links("[x](../all-function-dax.md#remarks)"),
                         "[x](./all.md#remarks)")


class ConceptsIndex(unittest.TestCase):
    """Concepts get their own index rather than rows in catalog.md. A conceptual question
    would otherwise have to pay 14k tokens of function rows to find a page about evaluation
    context, which is the opposite of the one-hop the library is built for."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.src, "best-practices"))
        self.out = tempfile.mkdtemp()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)
        with open(os.path.join(self.src, "dax-glossary.md"), "w", encoding="utf-8") as f:
            f.write('---\ntitle: "DAX glossary"\ndescription: "Common terms"\n'
                    'ms.topic: glossary\n---\n# DAX glossary\n\nTerms.\n')
        with open(os.path.join(self.src, "best-practices", "dax-variables.md"), "w",
                  encoding="utf-8") as f:
            f.write(CONCEPT_DOC)

    def _run(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="abc1234", source_date="d")

    def gen(self, rel):
        with open(os.path.join(self.out, "generated", rel), encoding="utf-8") as f:
            return f.read()

    def test_a_card_per_concept_named_after_its_upstream_stem(self):
        self._run()
        self.assertEqual(
            sorted(os.listdir(os.path.join(self.out, "generated", "concepts"))),
            ["dax-glossary.md", "dax-variables.md"])

    def test_the_human_index_has_a_row_per_concept(self):
        self._run()
        md = self.gen("concepts.md")
        self.assertIn("| dax-glossary |", md)
        self.assertIn("| dax-variables |", md)
        self.assertIn("Common terms", md)

    def test_the_machine_index_lives_beside_the_functions(self):
        self._run()
        cat = json.loads(self.gen("catalog.json"))
        self.assertEqual(cat["conceptCount"], 2)
        self.assertEqual({c["file"] for c in cat["concepts"]},
                         {"dax-glossary", "dax-variables"})
        self.assertEqual([c["topic"] for c in cat["concepts"] if c["file"] == "dax-glossary"],
                         ["glossary"])

    def test_the_function_catalog_does_not_carry_concept_rows(self):
        # The whole point of the split: catalog.md stays the function index.
        self._run()
        self.assertNotIn("dax-glossary", self.gen("catalog.md"))

    def test_rerunning_produces_the_same_concepts(self):
        self._run()
        first = self.gen("concepts/dax-variables.md")
        self._run()
        self.assertEqual(self.gen("concepts/dax-variables.md"), first)

    def test_a_concept_removed_upstream_does_not_survive(self):
        self._run()
        os.remove(os.path.join(self.src, "dax-glossary.md"))
        self._run()
        self.assertNotIn("dax-glossary.md",
                         os.listdir(os.path.join(self.out, "generated", "concepts")))


class LinksAreRelativeToTheirOwnPage(unittest.TestCase):
    """A page in best-practices/ links to its neighbours by bare filename, and its images
    live in best-practices/media/. Resolving those as if every page sat in dax/ produced
    URLs to pages and images that do not exist — an invented URL, which is the one failure
    this library must never produce."""

    def test_a_sibling_page_keeps_its_directory(self):
        # dax-error-functions.md really does link to this one, and it really does live
        # under best-practices/.
        self.assertEqual(_learn_url("dax-divide-function-operator.md", base="best-practices"),
                         "https://learn.microsoft.com/en-us/dax/best-practices/"
                         "dax-divide-function-operator")

    def test_a_parent_relative_link_climbs_out_of_the_directory(self):
        self.assertEqual(_learn_url("../filter-functions-dax.md", base="best-practices"),
                         "https://learn.microsoft.com/en-us/dax/filter-functions-dax")

    def test_a_page_at_the_root_is_unaffected(self):
        self.assertEqual(_learn_url("filter-functions-dax.md"),
                         "https://learn.microsoft.com/en-us/dax/filter-functions-dax")

    def test_a_sibling_link_in_a_body_is_absolutised_under_the_base(self):
        out = absolutise_links("[DIVIDE](dax-divide-function-operator.md)",
                               base="best-practices")
        self.assertIn("/dax/best-practices/dax-divide-function-operator", out)

    def test_an_image_resolves_under_the_base_too(self):
        out = absolutise_links("![x](media/dax-understand-orderby/offset.png)",
                               base="best-practices")
        self.assertIn("/dax/best-practices/media/dax-understand-orderby/offset.png", out)

    def test_a_docfx_image_directive_resolves_under_the_base_too(self):
        out = absolutise_links(':::image type="content" source="media/x/y.png":::',
                               base="best-practices")
        self.assertIn("/dax/best-practices/media/x/y.png", out)

    def test_an_unknown_sibling_area_is_still_refused(self):
        with self.assertRaises(ValueError):
            _learn_url("../power-query-m/some-page.md", base="best-practices")

    def test_a_link_that_climbs_out_of_dax_is_refused(self):
        # '../foo.md' from a root page is query-languages/foo.md — outside dax/ entirely.
        # Dropping every '..' and then asking only whether an AREA name was left mapped it
        # to /dax/foo: an invented URL, from the guard meant to prevent exactly that.
        for target, base in (("../foo.md", ""),
                             ("../../foo.md", "best-practices"),
                             ("best-practices/../../power-query-m/page.md", "")):
            with self.subTest(target=target, base=base):
                with self.assertRaises(ValueError):
                    _learn_url(target, base=base)

    def test_the_upstream_parent_relative_quirk_still_resolves(self):
        # best-practices/ IS inside dax/, yet root pages reach it with '../'. That one is
        # real and must keep working — it is why the '..' is dropped at all.
        self.assertEqual(_learn_url("../best-practices/dax-variables.md"),
                         "https://learn.microsoft.com/en-us/dax/best-practices/dax-variables")


class ConceptsIndexIsWellFormed(unittest.TestCase):
    """Two upstream titles end in '| Microsoft Docs'. Emitted raw into a markdown table they
    add columns, and the index stops being a table — the summary column was escaped and the
    title column was not."""

    def rows(self, concepts):
        md = sync_query_docs._concepts_md(concepts, "src", "date")
        return [l for l in md.splitlines() if l.startswith("| ") and "---" not in l]

    def columns(self, row):
        """Column separators only. An escaped '\\|' is a literal pipe, not a new column."""
        return row.replace("\\|", "").count("|")

    def concept(self, **kw):
        base = {"file": "f", "title": "t", "topic": "reference", "summary": "s"}
        base.update(kw)
        return base

    def test_a_pipe_in_the_title_does_not_add_a_column(self):
        header, row = self.rows([self.concept(title="Virtual Column (DAX) | Microsoft Docs")])
        self.assertEqual(self.columns(row), self.columns(header))
        self.assertIn("Virtual Column (DAX) \\| Microsoft Docs", row)

    def test_a_pipe_in_any_cell_is_escaped(self):
        for field in ("file", "title", "topic", "summary"):
            with self.subTest(field=field):
                header, row = self.rows([self.concept(**{field: "a | b"})])
                self.assertEqual(self.columns(row), self.columns(header))


class ConceptSlugsMustBeUnique(unittest.TestCase):
    """Cards are keyed by the upstream stem. Two pages with the same stem in different
    directories would overwrite each other's card while both still emit a catalog row —
    one page missing, and nothing about the output looking wrong."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.src, "best-practices"))
        with open(os.path.join(self.src, "filter-functions-dax.md"), "w",
                  encoding="utf-8") as f:
            f.write(FILTER_INDEX)
        for rel in ("dax-variables.md", "best-practices/dax-variables.md"):
            with open(os.path.join(self.src, rel), "w", encoding="utf-8") as f:
                f.write(CONCEPT_DOC)

    def test_a_collision_fails_the_run_instead_of_overwriting(self):
        with self.assertRaises(ValueError) as caught:
            write_library(self.src, self.out, {}, [], {}, source_sha="a", source_date="d")
        self.assertIn("dax-variables", str(caught.exception))


class DiscouragedIsScopedToVisualCalculations(unittest.TestCase):
    """The upstream include that raises this flag says the function is discouraged *in
    visual calculations*, "as it likely returns meaningless results" — not deprecated, not
    discouraged in a measure. There is exactly one such include in the corpus. A card that
    says only "discouraged" invites an agent to warn a user off a function that is fine
    where they are using it, which is a wrong answer stated with confidence."""

    def test_the_field_names_the_context_it_applies_to(self):
        card = build_library_card(CALCULATE_DOC.replace(
            "applies-to-measures-columns-tables-visual-calculations",
            "applies-to-measures-columns-tables-visual-calculations-discouraged"),
            "calculate-function-dax.md", {}, {}, set())
        self.assertIn("discouragedInVisualCalculations: true", card)
        self.assertNotIn("\ndiscouraged: ", card)

    def test_a_function_that_is_not_discouraged_says_so(self):
        card = build_library_card(CALCULATE_DOC, "calculate-function-dax.md", {}, {}, set())
        self.assertIn("discouragedInVisualCalculations: false", card)

    def test_the_catalog_legend_scopes_the_symbol(self):
        md = sync_query_docs._catalog_md([], "src", "date")
        self.assertIn("cálculos visuales", md)


class FrontmatterQuoting(unittest.TestCase):
    """Concept summaries are prose straight from Microsoft's `description`, and 17 of the
    34 begin "Learn more about: ...". Written unquoted that colon starts a mapping and the
    frontmatter stops being YAML. Function cards never hit this — every value they carry is
    a bare token — so the renderer had no reason to quote until now."""

    def render(self, fm):
        import yaml
        block = sync_query_docs._format_frontmatter(fm)
        return yaml.safe_load(block)

    def test_a_colon_in_a_value_survives_as_one_string(self):
        got = self.render({"summary": "Learn more about: DAX syntax"})
        self.assertEqual(got, {"summary": "Learn more about: DAX syntax"})

    def test_a_hash_does_not_start_a_comment(self):
        # YAML starts a comment at a '#' PRECEDED by whitespace, whatever follows it. The
        # first version of this rule looked for '#' followed by a space, so "See #123" went
        # out bare and the value silently truncated to "See" — and this very test masked it
        # by picking a string that happened to have a space after the hash.
        for value in ("Use # for comments", "See #123", "a #b"):
            with self.subTest(value=value):
                self.assertEqual(self.render({"summary": value})["summary"], value)

    def test_a_hash_with_no_space_before_it_is_not_a_comment(self):
        # 'C#' is part of the word. Quoting it would be harmless but wrong, and the point
        # of the rule is to quote only what would otherwise change.
        self.assertNotIn('"', sync_query_docs._format_frontmatter({"summary": "a#b"}))

    def test_a_quote_inside_the_value_is_escaped(self):
        got = self.render({"title": 'The "DAX" language'})
        self.assertEqual(got["title"], 'The "DAX" language')

    def test_a_leading_quote_is_not_read_as_a_quoted_scalar(self):
        # Bare, YAML reads the opening quote as the start of a quoted scalar and then
        # chokes on the text after the closing one.
        for value in ('"DAX" overview', "'DAX' overview"):
            with self.subTest(value=value):
                self.assertEqual(self.render({"title": value})["title"], value)

    def test_a_leading_indicator_character_is_not_read_as_syntax(self):
        for value in ("[not a list]", "{not a map}", "*not an alias", "&not an anchor",
                      ">not a block", "|not a literal", "!not a tag", "%not a directive"):
            with self.subTest(value=value):
                self.assertEqual(self.render({"summary": value})["summary"], value)

    def test_an_empty_value_stays_bare(self):
        # Bare it parses as null, which is what an absent ms.date means. Quoting it
        # rewrote the frontmatter of 458 of the 479 cards for no gain — caught by
        # regenerating and finding a diff that should not have existed.
        self.assertIn("sourceDate: \n",
                      sync_query_docs._format_frontmatter({"sourceDate": ""}))

    def test_plain_values_are_left_unquoted(self):
        # The 479 function cards already on disk must not all churn on the next sync.
        block = sync_query_docs._format_frontmatter({"returns": "scalar", "notes": False,
                                                     "category": ["filter", "table"]})
        self.assertIn("returns: scalar\n", block)
        self.assertIn("notes: false\n", block)
        self.assertIn("category: [filter, table]\n", block)


class ResolveIncludes(unittest.TestCase):
    """[!INCLUDE[x](includes/x.md)] is a transclusion, not a link. Left raw it becomes a
    dangling link where a real constraint should be — 266 of the 479 docs carry the
    DirectQuery one, which states the function does not work in calculated columns or RLS
    under DirectQuery."""

    def setUp(self):
        self.inc = tempfile.mkdtemp()
        with open(os.path.join(self.inc, "dq.md"), "w", encoding="utf-8") as f:
            f.write("---\nms.topic: include\n---\n\nThis function is not supported in "
                    "DirectQuery mode.")

    def test_inlines_the_include_body(self):
        out = resolve_includes("- [!INCLUDE [dq](includes/dq.md)]\n", self.inc)
        self.assertIn("This function is not supported in DirectQuery mode.", out)

    def test_strips_the_includes_own_frontmatter(self):
        out = resolve_includes("[!INCLUDE [dq](includes/dq.md)]\n", self.inc)
        self.assertNotIn("ms.topic", out)

    def test_leaves_no_dangling_include_link_behind(self):
        out = resolve_includes("- [!INCLUDE [dq](includes/dq.md)]\n", self.inc)
        self.assertNotIn("includes/dq.md", out)

    def test_an_include_that_does_not_exist_is_dropped_not_left_broken(self):
        out = resolve_includes("[!INCLUDE [gone](includes/gone.md)]\n", self.inc)
        self.assertNotIn("includes/gone.md", out)


class AbsolutiseLinks(unittest.TestCase):
    """A link to a query-docs page this repo does not carry must resolve for the reader,
    not point at a file that is not there."""

    def test_a_category_index_link_becomes_an_upstream_url(self):
        out = absolutise_links("- [Filter functions](filter-functions-dax.md)\n")
        self.assertIn("https://learn.microsoft.com/en-us/dax/filter-functions-dax", out)

    def test_an_anchor_survives(self):
        out = absolutise_links("[filter context](dax-overview.md#filter-context)\n")
        self.assertIn("dax-overview#filter-context", out)

    def test_a_local_card_link_is_left_alone(self):
        text = "[CALCULATETABLE](./calculatetable.md)\n"
        self.assertEqual(absolutise_links(text), text)

    def test_an_already_absolute_link_is_left_alone(self):
        text = "[docs](https://learn.microsoft.com/en-us/dax/x)\n"
        self.assertEqual(absolutise_links(text), text)

    def test_a_site_absolute_learn_path_becomes_a_full_url(self):
        out = absolutise_links("[DAX query view](/power-bi/transform-model/dax-query-view)\n")
        self.assertIn("https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view",
                      out)

    def test_a_media_image_points_at_a_host_that_answers(self):
        """It pointed at the upstream raw host, which was right until that host started
        returning 404 and left 87 dead images across 33 cards. Learn serves the same file
        at the same path behind a different prefix; all 87 were fetched and answered 200
        before this moved."""
        out = absolutise_links("![shot](media/dax-queries/collapse.png)\n")
        self.assertIn(
            "https://learn.microsoft.com/en-us/dax/media/dax-queries/collapse.png", out)
        self.assertNotIn("raw.githubusercontent.com", out)

    def test_a_media_image_with_a_title_attribute_is_still_rewritten(self):
        out = absolutise_links('![x](media/crossfilter/diag.png "CROSSFILTER_DiagView")\n')
        self.assertIn("learn.microsoft.com/en-us/dax/media/crossfilter/diag.png", out)
        self.assertIn('"CROSSFILTER_DiagView"', out)

    def test_an_in_page_anchor_is_left_alone(self):
        text = "[see below](#remarks)\n"
        self.assertEqual(absolutise_links(text), text)


class WriteMode(MainFixture, unittest.TestCase):
    """A generation only reachable from an ad-hoc snippet is not reproducible. The weekly
    sync workflow invokes this CLI."""

    def setUp(self):
        self.set_up_corpus()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            self.write(fn, body)
        self.out = tempfile.mkdtemp()

    def write(self, fn, body):
        with open(os.path.join(self.dir, fn), "w", encoding="utf-8") as f:
            f.write(body)

    def run_main(self, *args):
        with io.StringIO() as o, io.StringIO() as e:
            with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
                code = main(["sync_query_docs.py", self.dir, *args])
            return code, e.getvalue()

    def test_without_write_nothing_is_generated(self):
        code, _ = self.run_main()
        self.assertEqual(code, 0)
        self.assertFalse(os.path.exists(os.path.join(self.out, "generated", "catalog.json")))

    def test_write_generates_the_cards_and_both_catalogs(self):
        code, _ = self.run_main("--write", "--out", self.out)
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(os.path.join(self.out, "generated", "catalog.json")))
        self.assertTrue(os.path.exists(os.path.join(self.out, "generated", "catalog.md")))
        self.assertEqual(sorted(os.listdir(os.path.join(self.out, "generated", "library"))),
                         ["all.md", "calculate.md"])

    def test_write_reports_what_it_wrote(self):
        _, err = self.run_main("--write", "--out", self.out)
        self.assertIn("wrote", err.lower())

    def test_an_unknown_flag_is_refused_rather_than_ignored(self):
        code, _ = self.run_main("--wrote")
        self.assertEqual(code, 2)


class ReturnValueBooleans(unittest.TestCase):
    """The noun-phrase match alone read "TRUE when a column of TableName is filtered" as a
    table return. ISFILTERED, ISCROSSFILTERED and ISEMPTY shipped as returns: table.
    The 27-case validation set that blessed the heuristic contained no boolean function —
    a validation set that shares the code's blind spot proves nothing."""

    def ret(self, first_line):
        return parse_return_value("## Return value\n\n" + first_line + "\n")

    def test_isfiltered_is_scalar_despite_naming_a_column(self):
        self.assertEqual(
            self.ret("`TRUE` when `ColumnName` or a column of `TableName` is being "
                     "filtered directly. Otherwise returns `FALSE`."), "scalar")

    def test_isempty_is_scalar_despite_naming_a_table(self):
        self.assertEqual(
            self.ret("True if the table is empty (has no rows), if else, False."), "scalar")

    def test_a_genuine_table_return_is_still_table(self):
        self.assertEqual(self.ret("A table containing only the filtered rows."), "table")

    def test_a_table_return_that_merely_mentions_true_is_not_downgraded(self):
        # 'true' as an adjective, not a boolean result.
        self.assertEqual(self.ret("A table of the true daily rates."), "table")


class DocFxImageDirectives(unittest.TestCase):
    """query-docs uses DocFX :::image::: as well as markdown images. Rewriting only the
    markdown form left 16 local media paths across 5 cards — and the link checker that
    blessed the run had the same blind spot, counting only ](...) syntax."""

    def test_the_source_attribute_is_absolutised(self):
        out = absolutise_links(':::image type="content" source="media/x/y.png" alt-text="a":::')
        self.assertIn("learn.microsoft.com/en-us/dax/media/x/y.png", out)
        self.assertNotIn('source="media/', out)

    def test_the_lightbox_attribute_is_absolutised_too(self):
        out = absolutise_links(':::image source="media/x/y.png" lightbox="media/x/y.png":::')
        self.assertNotIn('lightbox="media/', out)

    def test_a_directive_without_media_is_untouched(self):
        text = ':::image type="content" source="https://example.com/y.png":::'
        self.assertEqual(absolutise_links(text), text)


class WriteIsFailureAtomic(unittest.TestCase):
    """library/ is wiped before the replacements exist. A crash mid-write left a partial
    library plus catalogs that disagreed with it — the exact state this pipeline exists to
    make impossible."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)
        self._write_once()

    def _write_once(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="aaa", source_date="d")

    def test_a_failure_mid_write_leaves_the_previous_library_intact(self):
        before = sorted(os.listdir(os.path.join(self.out, "generated", "library")))
        boom = os.path.join(self.src, "aaa-function-dax.md")
        with open(boom, "w", encoding="utf-8") as f:
            f.write(GOOD_DOC.replace("CALCULATE", "ZZZ"))
        real = sync_query_docs.build_library_card

        def explode(text, filename, *a, **k):
            if filename.startswith("aaa"):
                raise RuntimeError("upstream page broke the parser")
            return real(text, filename, *a, **k)

        sync_query_docs.build_library_card = explode
        try:
            with self.assertRaises(RuntimeError):
                self._write_once()
        finally:
            sync_query_docs.build_library_card = real
        self.assertEqual(sorted(os.listdir(os.path.join(self.out, "generated", "library"))), before)

    def test_a_failure_mid_write_leaves_the_catalog_agreeing_with_the_cards(self):
        with open(os.path.join(self.out, "generated", "catalog.json"), encoding="utf-8") as f:
            before = json.load(f)
        boom = os.path.join(self.src, "aaa-function-dax.md")
        with open(boom, "w", encoding="utf-8") as f:
            f.write(GOOD_DOC.replace("CALCULATE", "ZZZ"))
        real = sync_query_docs.build_library_card

        def explode(text, filename, *a, **k):
            if filename.startswith("aaa"):
                raise RuntimeError("boom")
            return real(text, filename, *a, **k)

        sync_query_docs.build_library_card = explode
        try:
            with self.assertRaises(RuntimeError):
                self._write_once()
        finally:
            sync_query_docs.build_library_card = real
        with open(os.path.join(self.out, "generated", "catalog.json"), encoding="utf-8") as f:
            after = json.load(f)
        self.assertEqual(before, after)


class LearnRouteIsNotTheRepoLayout(unittest.TestCase):
    """All DAX content in query-docs lives under query-languages/dax/ and serves from the
    /dax/ route. Upstream links reach it with ../best-practices/... even though
    best-practices is INSIDE dax/ — the relative path is wrong in the repo and only works
    because Learn's route differs from the layout. Resolving it as a filesystem path
    dropped the /dax/ segment and produced a URL to a page that does not exist."""

    def test_a_parent_relative_target_still_lands_under_dax(self):
        out = absolutise_links("[x](../best-practices/dax-unicode-character-behavior.md)")
        self.assertIn("learn.microsoft.com/en-us/dax/best-practices/"
                      "dax-unicode-character-behavior", out)

    def test_a_dot_dot_dax_target_does_not_double_the_segment(self):
        out = absolutise_links("[x](../dax/best-practices/dax-understand-orderby.md)")
        self.assertIn("learn.microsoft.com/en-us/dax/best-practices/"
                      "dax-understand-orderby", out)
        self.assertNotIn("/dax/dax/", out)

    def test_a_plain_sibling_target_is_unaffected(self):
        out = absolutise_links("[x](filter-functions-dax.md)")
        self.assertIn("learn.microsoft.com/en-us/dax/filter-functions-dax", out)


class CatalogSummariesAreNormalised(unittest.TestCase):
    """The summary comes from the index table's description cell, which can contain
    markdown links. The card body was normalised and the catalogs were not, so
    catalog.json and catalog.md carried raw paths like islogical-function-dax.md."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        index = ("# Information functions\n\n## In this category\n\n"
                 "|Function  |Description  |\n|---------|---------|\n"
                 "|[ISBOOLEAN](isboolean-function-dax.md)  |  Checks a value; see "
                 "[ISLOGICAL](islogical-function-dax.md).  |\n")
        with open(os.path.join(self.src, "information-functions-dax.md"), "w",
                  encoding="utf-8") as f:
            f.write(index)
        with open(os.path.join(self.src, "isboolean-function-dax.md"), "w",
                  encoding="utf-8") as f:
            f.write(GOOD_DOC.replace("CALCULATE", "ISBOOLEAN"))

    def entries(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="a", source_date="d")

    def test_a_link_in_the_summary_becomes_an_upstream_url(self):
        summary = self.entries()[0]["summary"]
        self.assertNotIn("islogical-function-dax.md", summary)
        self.assertIn("learn.microsoft.com", summary)

    def test_the_human_catalog_carries_the_normalised_summary(self):
        self.entries()
        with open(os.path.join(self.out, "generated", "catalog.md"), encoding="utf-8") as f:
            md = f.read()
        self.assertNotIn("islogical-function-dax.md", md)


class WriteIsAtomicOnDisk(unittest.TestCase):
    """Building in memory protects against a parse failure. It does not protect against a
    failure DURING the writes: wiping library/ and then writing in place leaves a partial
    tree if the process dies halfway. Claiming failure-atomic means surviving that too."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)
        self._run()

    def _run(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="a", source_date="d")

    def test_a_failure_while_writing_leaves_the_previous_tree_intact(self):
        before = sorted(os.listdir(os.path.join(self.out, "generated", "library")))
        with open(os.path.join(self.out, "generated", "catalog.json"), encoding="utf-8") as f:
            cat_before = f.read()
        real = sync_query_docs._publish

        def explode(*a, **k):
            raise RuntimeError("disk died mid-publish")

        sync_query_docs._publish = explode
        try:
            with self.assertRaises(RuntimeError):
                self._run()
        finally:
            sync_query_docs._publish = real
        self.assertEqual(sorted(os.listdir(os.path.join(self.out, "generated", "library"))), before)
        with open(os.path.join(self.out, "generated", "catalog.json"), encoding="utf-8") as f:
            self.assertEqual(f.read(), cat_before)


class UnknownParentTraversalIsRefused(unittest.TestCase):
    """query-languages/ contains only dax/ today, and the corpus has exactly 3 parent-
    relative targets, all dax-internal. Discarding `..` unconditionally would silently
    misroute a sibling docs area if Microsoft ever adds one — turning upstream drift into
    an invented URL, which is the failure this whole repo exists to avoid."""

    def test_a_known_dax_internal_traversal_still_resolves(self):
        self.assertEqual(_learn_url("../dax/best-practices/x.md"),
                         "https://learn.microsoft.com/en-us/dax/best-practices/x")
        self.assertEqual(_learn_url("../best-practices/x.md"),
                         "https://learn.microsoft.com/en-us/dax/best-practices/x")

    def test_an_unknown_sibling_area_is_refused_not_guessed(self):
        with self.assertRaises(ValueError):
            _learn_url("../power-query-m/some-page.md")

    # There was a test here asserting that _learn_url("../filter-functions-dax.md") with no
    # base resolves to the dax root. It was written to make best-practices/ links work
    # before _learn_url knew which page a link came from, and it pinned the wrong answer:
    # '../x.md' from a root page is query-languages/x.md, OUTSIDE dax/, and mapping it to
    # /dax/x invents a URL. The corpus has no such link — root pages only use
    # '../dax/best-practices/...' — and the real best-practices case is now covered with a
    # base, where the '..' resolves away. Refusal is asserted in
    # LinksAreRelativeToTheirOwnPage.test_a_link_that_climbs_out_of_dax_is_refused.

    def test_a_plain_sibling_page_is_unaffected(self):
        self.assertEqual(_learn_url("filter-functions-dax.md"),
                         "https://learn.microsoft.com/en-us/dax/filter-functions-dax")


class PublishStagingHygiene(unittest.TestCase):
    """The scratch directory is per-run and must not survive the run. A fixed name would
    let two syncs against the same tree delete each other's work."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)

    def _run(self):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha="a", source_date="d")

    def test_no_staging_directory_is_left_behind(self):
        self._run()
        self.assertEqual([d for d in os.listdir(self.out) if d.startswith(".publish-")], [])

    def test_two_runs_do_not_share_a_staging_path(self):
        seen = []
        real = tempfile.mkdtemp

        def spy(*a, **k):
            p = real(*a, **k)
            seen.append(p)
            return p

        tempfile.mkdtemp = spy
        try:
            self._run()
            self._run()
        finally:
            tempfile.mkdtemp = real
        staging = [p for p in seen if ".publish-" in os.path.basename(p)]
        self.assertEqual(len(set(staging)), len(staging), "staging paths must be unique")


class PublishRollback(unittest.TestCase):
    """Installing a new generation takes two renames — the old directory moves aside, the
    new one takes its place — because os.replace cannot land a directory on an existing
    path. So there is exactly ONE recoverable state: the gap between them. Undoing it is
    putting a single directory back.

    The three-target layout this replaced needed per-file backups, an order to undo them
    in, a partial-copy window and bookkeeping for which targets the run had created. Those
    scenarios cannot arise against one directory and their tests are gone with them."""

    def setUp(self):
        self.src = tempfile.mkdtemp()
        self.out = tempfile.mkdtemp()
        for fn, body in [("filter-functions-dax.md", FILTER_INDEX),
                         ("all-function-dax.md", GOOD_DOC.replace("CALCULATE", "ALL")),
                         ("calculate-function-dax.md", GOOD_DOC)]:
            with open(os.path.join(self.src, fn), "w", encoding="utf-8") as f:
                f.write(body)
        self._run(sha="first")

    def _run(self, sha="a"):
        mapping = build_category_map(discover_indexes(self.src))
        docs = discover_function_docs(self.src)
        apply_filename_rules(mapping, docs)
        return write_library(self.src, self.out, mapping, docs, {},
                             source_sha=sha, source_date="d")

    def read(self, rel):
        with open(os.path.join(self.out, "generated", rel), encoding="utf-8") as f:
            return f.read()

    def _fail_installing(self, restore_too=False):
        """Let the retire rename through, blow up on the one that installs the new tree.

        With restore_too the rollback's own rename fails as well, which is the case that
        must NOT delete the only surviving copy of the previous generation.
        """
        real = os.replace
        state = {"retired": False, "fired": False}

        def flaky(a, b):
            if state["retired"] and (restore_too or not state["fired"]):
                state["fired"] = True
                raise OSError("volume went away installing the new generation")
            r = real(a, b)
            if os.path.basename(b) == "prev":
                state["retired"] = True
            return r

        return real, flaky

    def test_the_previous_generation_is_put_back(self):
        before_cat = self.read("catalog.json")
        before_card = self.read("library/calculate.md")
        self.assertIn("first", before_cat)
        import sync_query_docs as mod
        real, flaky = self._fail_installing()
        mod.os.replace = flaky
        try:
            with self.assertRaises(OSError):
                self._run(sha="second")
        finally:
            mod.os.replace = real
        # Cards and catalogs move as one directory, so they cannot end up describing
        # different upstream commits.
        self.assertEqual(self.read("catalog.json"), before_cat)
        self.assertEqual(self.read("library/calculate.md"), before_card)

    def test_nothing_is_left_behind_after_a_rollback(self):
        import sync_query_docs as mod
        real, flaky = self._fail_installing()
        mod.os.replace = flaky
        try:
            with self.assertRaises(OSError):
                self._run(sha="second")
        finally:
            mod.os.replace = real
        self.assertEqual([d for d in os.listdir(self.out) if d.startswith(".publish-")], [])

    def test_a_failed_rollback_keeps_the_previous_generation_instead_of_deleting_it(self):
        # If the restore cannot complete, deleting the run directory anyway would destroy
        # the only copy of the previous generation — a recovery path that eats the data it
        # exists to protect.
        import sync_query_docs as mod
        real, flaky = self._fail_installing(restore_too=True)
        mod.os.replace = flaky
        try:
            with self.assertRaises(OSError):
                self._run(sha="second")
        finally:
            mod.os.replace = real
        kept = [d for d in os.listdir(self.out) if d.startswith(".publish-")]
        self.assertEqual(len(kept), 1,
                         "the previous generation must survive a failed rollback")
        self.assertTrue(os.path.isdir(os.path.join(self.out, kept[0], "prev", "library")))

    def test_a_failure_inside_publish_reports_itself_not_an_unbound_name(self):
        # Every name the handler reads is bound before the try. Assigned inside it, an
        # early failure reached the handler with a name unbound and the UnboundLocalError
        # replaced the real error in the traceback.
        import traceback
        import sync_query_docs as mod
        real = os.makedirs

        def explode(*a, **k):
            raise RuntimeError("the real failure, which must be what surfaces")

        # Caught by hand rather than with assertRaises, which strips the traceback
        # (with_traceback(None)) to avoid a reference cycle — and the traceback is the
        # whole point of this test.
        mod.os.makedirs = explode
        try:
            self._run(sha="second")
        except RuntimeError as e:
            message, frames = str(e), [f.name for f in traceback.extract_tb(e.__traceback__)]
        else:
            self.fail("the run must fail")
        finally:
            mod.os.makedirs = real
        self.assertIn("the real failure", message)
        # The failure must happen INSIDE _publish or this proves nothing: an earlier
        # version of this test exploded in build_library_card, which runs before _publish
        # is ever entered, so it passed with the bug still present.
        self.assertIn("_publish", frames)

    def test_an_interrupt_between_the_rename_and_its_flag_still_restores(self):
        # The retire rename and the bookkeeping that records it are two bytecodes, and a
        # signal lands between bytecodes. A flag set after the call meant a Ctrl+C there
        # left the handler believing nothing had moved: no restore, and the cleanup then
        # deleted the run directory holding the only copy of the previous generation.
        # _publish catches BaseException precisely because it cares about interrupts, so
        # recovery has to read the filesystem, not a variable.
        before = self.read("catalog.json")
        import sync_query_docs as mod
        real = os.replace

        def interrupt_after_retiring(a, b):
            r = real(a, b)
            if os.path.basename(b) == "prev":
                raise KeyboardInterrupt("interrupted after the rename, before the flag")
            return r

        mod.os.replace = interrupt_after_retiring
        try:
            with self.assertRaises(KeyboardInterrupt):
                self._run(sha="second")
        finally:
            mod.os.replace = real
        self.assertEqual(self.read("catalog.json"), before,
                         "the previous generation must survive an interrupt mid-swap")

    def test_a_failure_on_the_retire_rename_leaves_the_tree_untouched(self):
        # The first rename is the step that puts the previous generation at risk. If it
        # fails, nothing moved: there is nothing to restore, and nothing of this run may
        # survive either. Failures on the SECOND rename are the covered case; this one had
        # no test after the old swap suite was folded away.
        before = self.read("catalog.json")
        import sync_query_docs as mod
        real = os.replace

        def fail_on_retire(a, b):
            if os.path.basename(b) == "prev":
                raise OSError("volume went away retiring the previous generation")
            return real(a, b)

        mod.os.replace = fail_on_retire
        try:
            with self.assertRaises(OSError):
                self._run(sha="second")
        finally:
            mod.os.replace = real
        self.assertEqual(self.read("catalog.json"), before)
        self.assertEqual([d for d in os.listdir(self.out) if d.startswith(".publish-")], [])

    def test_a_relative_symlink_target_is_still_recognised_as_the_backup(self):
        # Retiring a relative symlink moves the LINK one directory deeper, so its target
        # stops resolving. Asking isdir() about a broken link answers False, the backup
        # looks absent, and the cleanup deletes the only record of where the tree lived.
        # stranded() asks whether the path is occupied, not whether it is usable.
        real_tree = os.path.join(self.out, "elsewhere")
        os.replace(os.path.join(self.out, "generated"), real_tree)
        try:
            os.symlink("elsewhere", os.path.join(self.out, "generated"),
                       target_is_directory=True)
        except (OSError, NotImplementedError) as e:      # Windows without developer mode
            self.skipTest(f"symlinks unavailable here: {e}")
        import sync_query_docs as mod
        realr = os.replace
        state = {"retired": False, "fired": False}

        def fail_installing(a, b):
            # Once only: the restore is also an os.replace, and failing that too would be
            # testing a double failure instead of whether the backup was recognised.
            if state["retired"] and not state["fired"]:
                state["fired"] = True
                raise OSError("volume went away installing the new generation")
            r = realr(a, b)
            if os.path.basename(b) == "prev":
                state["retired"] = True
            return r

        mod.os.replace = fail_installing
        try:
            with self.assertRaises(OSError):
                self._run(sha="second")
        finally:
            mod.os.replace = realr
        self.assertTrue(os.path.lexists(os.path.join(self.out, "generated")),
                        "the symlink must be put back, broken or not")

    def test_an_interrupt_during_the_restore_keeps_the_previous_generation(self):
        # The restore's own guard caught OSError and set the keep-the-scratch-directory
        # flag inside it. A KeyboardInterrupt on the restore rename skips an `except
        # OSError` entirely, so the flag stayed false and the cleanup deleted the run
        # directory with `retired` — the only copy — inside. Same interrupt hole the
        # forward path closes, one level down: the fix is to stop using a flag at all.
        before = self.read("catalog.json")
        import sync_query_docs as mod
        real = os.replace
        state = {"retired": False}

        def flaky(a, b):
            if state["retired"]:
                raise KeyboardInterrupt("interrupted during the restore")
            r = real(a, b)
            if os.path.basename(b) == "prev":
                state["retired"] = True
            return r

        mod.os.replace = flaky
        try:
            with self.assertRaises(KeyboardInterrupt):
                self._run(sha="second")
        finally:
            mod.os.replace = real
        kept = [d for d in os.listdir(self.out) if d.startswith(".publish-")]
        self.assertEqual(len(kept), 1, "an interrupted restore must not eat the backup")
        with open(os.path.join(self.out, kept[0], "prev", "catalog.json"),
                  encoding="utf-8") as f:
            self.assertEqual(f.read(), before)

    def test_a_successful_run_installs_the_new_generation(self):
        self._run(sha="second")
        self.assertIn("second", self.read("catalog.json"))
        self.assertIn("second", self.read("library/calculate.md"))


DOC_CON_EJEMPLOS = """---
title: IF function
---
# IF

Checks a condition.

## Syntax

```dax
IF(<test>, <then>[, <else>])
```

## Examples

The following example uses Adventure Works.
"""


class ExamplesWiring(unittest.TestCase):
    """La ficha enlaza los ejemplos ejecutables y marca los de Microsoft."""

    def card(self, index=None, doc=DOC_CON_EJEMPLOS):
        return build_library_card(doc, "if-function-dax.md",
                                  {"if-function-dax.md": {"name": "IF"}}, {}, set(),
                                  examples_index=index)

    def test_a_card_with_no_examples_says_zero(self):
        self.assertIn("examples: 0", self.card())

    def test_the_count_comes_from_the_file_not_from_a_promise(self):
        self.assertIn("examples: 3", self.card({"if": ("logical", 3)}))

    def test_our_section_links_the_hand_written_file(self):
        self.assertIn("../../examples/logical/if.md", self.card({"if": ("logical", 3)}))

    def test_our_examples_go_above_the_microsoft_ones(self):
        """Un agente que deje de leer pronto tiene que toparse antes con lo ejecutable."""
        card = self.card({"if": ("logical", 3)})
        self.assertLess(card.index("Ejemplos ejecutables"), card.index("Microsoft"))

    def test_the_microsoft_heading_is_marked_even_with_no_examples_of_ours(self):
        """El problema de Adventure Works esta en las 479, no solo donde escribimos."""
        card = self.card()
        self.assertIn("Examples (Microsoft", card)
        self.assertIn("Adventure Works", card)

    def test_the_blank_line_after_the_heading_survives(self):
        """Sin ella la cita se traga el parrafo siguiente por continuacion perezosa."""
        card = self.card()
        self.assertIn("de Microsoft.\n\nThe following example", card)

    def test_a_card_with_no_upstream_examples_still_gets_ours(self):
        sin = DOC_CON_EJEMPLOS[:DOC_CON_EJEMPLOS.index("## Examples")]
        card = self.card({"if": ("logical", 3)}, doc=sin)
        self.assertIn("Ejemplos ejecutables", card)
        self.assertNotIn("Examples (Microsoft", card)


class BrokenLinksKnowsAboutExamples(unittest.TestCase):
    TREES = {"library": {"if": "see [x](../../examples/logical/if.md)"}}

    def test_a_link_to_an_examples_file_is_not_broken_when_it_exists(self):
        self.assertEqual(
            broken_local_links(self.TREES, outside={"../examples/logical/if.md"}), [])

    def test_the_same_link_is_broken_when_the_file_is_not_there(self):
        """Sin esta mitad, el de arriba pasaria con un gate que no mirase nada."""
        self.assertEqual(broken_local_links(self.TREES),
                         [("library/if.md", "../../examples/logical/if.md")])


if __name__ == "__main__":
    unittest.main()


class FunctionNameIsTypeable(unittest.TestCase):
    """A catalogue name has to be something you can put in front of a parenthesis.

    Two of the 479 were not, and it went unnoticed for as long as the catalogue was only
    ever compared against documentation. Asking the engine settled it in one query:
    `INFO.FUNCTIONS()` returns 470 names and exactly one of them is DISTINCT.
    """

    def test_a_plain_name_is_untouched(self):
        self.assertEqual(sync_query_docs.function_name("CALCULATE"), "CALCULATE")

    def test_a_dotted_name_is_untouched(self):
        self.assertEqual(sync_query_docs.function_name("INFO.VIEW.TABLES"),
                         "INFO.VIEW.TABLES")

    def test_the_index_label_loses_its_disambiguator(self):
        """`DISTINCT column` is how the table-manipulation index lists it. As a name it is
        something no engine will accept, and `catalog.md` is what an agent reads to learn
        what exists."""
        self.assertEqual(sync_query_docs.function_name("DISTINCT column"), "DISTINCT")
        self.assertEqual(sync_query_docs.function_name("DISTINCT table"), "DISTINCT")

    def test_the_parenthesised_heading_form_too(self):
        """The pages head themselves `# DISTINCT (column)`, which reaches the name by a
        different route — `parse_title`, used for the 21 docs no index lists."""
        self.assertEqual(sync_query_docs.function_name("DISTINCT (column)"), "DISTINCT")

    def test_an_empty_label_is_empty_and_not_an_exception(self):
        self.assertEqual(sync_query_docs.function_name("   "), "")

    def test_the_index_parser_applies_it(self):
        index = ("## In this category\n\n"
                 "|Function|Description|\n|---|---|\n"
                 "|[DISTINCT column](distinct-function-dax.md)|One column.|\n"
                 "|[DISTINCT table](distinct-table-function-dax.md)|A table.|\n")
        entries = sync_query_docs.parse_category_index(
            index, "table-manipulation-functions-dax.md")
        self.assertEqual([e["name"] for e in entries], ["DISTINCT", "DISTINCT"])
        # The disambiguation survives where it belongs: two files, two summaries.
        self.assertEqual([e["file"] for e in entries],
                         ["distinct-function-dax.md", "distinct-table-function-dax.md"])
        self.assertNotEqual(entries[0]["summary"], entries[1]["summary"])

    def test_parse_title_applies_it(self):
        self.assertEqual(sync_query_docs.parse_title("# DISTINCT (table)\n\nProse.\n"),
                         "DISTINCT")

    def test_no_shipped_catalogue_name_carries_a_space(self):
        """The tree, not a fixture. This is the assertion the whole change exists for."""
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "generated", "catalog.json")
        with open(path, encoding="utf-8") as f:
            catalog = json.load(f)
        bad = [f["name"] for f in catalog["functions"]
               if not re.fullmatch(r"[A-Z][A-Z0-9_]*(?:\.[A-Z0-9_]+)*", f["name"])]
        self.assertEqual(bad, [])

    def test_microsofts_own_index_typo_is_corrected(self):
        """`[T.INV.2t](t-inv-2t-function-dax.md)` is what the statistical index says. The
        page heads itself `# T.INV.2T`, its title says T.INV.2T, and the engine returns
        T.INV.2T. The sync prefers the index label, so it published the typo."""
        self.assertEqual(sync_query_docs.function_name("T.INV.2t"), "T.INV.2T")

    def test_every_shipped_name_is_upper_case(self):
        """470 of 470 names the engine returns are upper-case, and so is every page title.
        One index label was not, and it reached the catalogue."""
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "generated", "catalog.json")
        with open(path, encoding="utf-8") as f:
            catalog = json.load(f)
        self.assertEqual([f["name"] for f in catalog["functions"]
                          if f["name"] != f["name"].upper()], [])
