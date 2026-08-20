#!/usr/bin/env python3
"""Tests for the examples file format. Run: python -m unittest discover -s scripts"""
import datetime
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import examples_io as exio  # noqa: E402


class RenderValue(unittest.TestCase):
    def test_blank_and_empty_string_are_told_apart(self):
        """En DAX no son lo mismo, y una celda vacia en el fichero no se distingue de nada."""
        self.assertEqual(exio.render_value(None), "(blank)")
        self.assertEqual(exio.render_value(""), "(empty)")

    def test_booleans_do_not_render_as_numbers(self):
        self.assertEqual(exio.render_value(True), "True")
        self.assertEqual(exio.render_value(False), "False")

    def test_float_noise_is_rounded_away(self):
        """El motor devuelve 744415.2800000007; eso no puede entrar en un fichero."""
        self.assertEqual(exio.render_value(744415.2800000007), "744415.28")

    def test_whole_floats_lose_the_decimal_point(self):
        self.assertEqual(exio.render_value(5.0), "5")

    def test_dates_at_midnight_drop_the_time(self):
        self.assertEqual(exio.render_value(datetime.datetime(2024, 3, 1)), "2024-03-01")
        self.assertEqual(exio.render_value(datetime.datetime(2024, 3, 1, 13, 5, 2)),
                         "2024-03-01 13:05:02")


class RenderError(unittest.TestCase):
    def test_the_query_position_is_dropped(self):
        """`Query (3, 12)` cambia al reindentar la consulta sin que cambie nada real."""
        got = exio.render_error("Query (3, 12) Cannot find table 'X'.\nen Microsoft...")
        self.assertEqual(got, "ERROR: Cannot find table 'X'.")

    def test_only_the_first_line_survives(self):
        got = exio.render_error("Boom\n  at frame one\n  at frame two")
        self.assertNotIn("frame", got)


class ParseBlocks(unittest.TestCase):
    def test_a_dax_block_pairs_with_the_result_that_follows(self):
        text = "```dax\nEVALUATE 1\n```\n\n```result\nx\n1\n```\n"
        self.assertEqual(exio.parse_blocks(text), [("EVALUATE 1", "x\n1")])

    def test_a_dax_block_with_no_result_is_reported_as_missing(self):
        """Es justo lo que el gate tiene que cazar: un ejemplo sin numero medido."""
        text = "```dax\nEVALUATE 1\n```\n\ntexto\n\n```dax\nEVALUATE 2\n```\n"
        self.assertEqual(exio.parse_blocks(text),
                         [("EVALUATE 1", None), ("EVALUATE 2", None)])

    def test_two_queries_with_the_same_text_keep_their_own_results(self):
        """Se emparejan por POSICION. Emparejar por texto pisaria el segundo par."""
        text = ("```dax\nQ\n```\n\n```result\na\n```\n"
                "```dax\nQ\n```\n\n```result\nb\n```\n")
        self.assertEqual(exio.parse_blocks(text), [("Q", "a"), ("Q", "b")])

    def test_a_result_with_no_query_before_it_is_ignored(self):
        self.assertEqual(exio.parse_blocks("```result\nhuerfano\n```\n"), [])


class Frontmatter(unittest.TestCase):
    def test_reads_function_and_model(self):
        fm = exio.parse_frontmatter("---\nfunction: IF\nmodel: ninguno\n---\n# IF\n")
        self.assertEqual(fm, {"function": "IF", "model": "ninguno"})

    def test_no_frontmatter_is_empty_not_an_error(self):
        self.assertEqual(exio.parse_frontmatter("# IF\n"), {})


class RoundTrip(unittest.TestCase):
    def test_what_render_writes_is_what_parse_reads_back(self):
        """Sin esto el runner comparara siempre distinto y nadie sabra por que."""
        body = exio.render_result(["[a]", "[b]"], [(None, 1.5), ("", True)])
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "x.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"---\nfunction: X\nmodel: ninguno\n---\n"
                        f"```dax\nQ\n```\n\n```result\n{body}\n```\n")
            _, pairs = exio.parse(path)
        self.assertEqual(pairs, [("Q", body)])
        self.assertEqual(body, "a | b\n(blank) | 1.5\n(empty) | True")


if __name__ == "__main__":
    unittest.main()
