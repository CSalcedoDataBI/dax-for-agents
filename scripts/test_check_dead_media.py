#!/usr/bin/env python3
"""Tests for the dead-image gate.

Run: python -m unittest discover -s scripts -t scripts
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import check_dead_media as gate                                   # noqa: E402


DEAD = gate.DEAD_PREFIX + "media/dax-queries/collapse.png"
LIVE = gate.LIVE_PREFIX + "media/dax-queries/collapse.png"


class Tree(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "concepts"))

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, rel, text):
        path = os.path.join(self.dir, rel)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    def read(self, rel):
        with open(os.path.join(self.dir, rel), encoding="utf-8") as f:
            return f.read()

    def test_it_finds_a_dead_image(self):
        self.write("concepts/a.md", f"text\n\n![shot]({DEAD})\n")
        urls, files = gate.scan(self.dir)
        self.assertEqual(len(urls), 1)
        self.assertEqual(files, {"concepts/a.md": 1})

    def test_it_counts_every_occurrence_not_every_file(self):
        """dax-copilot.md alone carried 32. A per-file count would have called that one
        problem and hidden how much of the page was pictures."""
        self.write("concepts/a.md", f"![1]({DEAD})\n![2]({DEAD})\n![3]({DEAD})\n")
        urls, _ = gate.scan(self.dir)
        self.assertEqual(len(urls), 3)

    def test_the_docfx_directive_form_is_found_too(self):
        """Half the images upstream are `:::image source=...:::`, not markdown. A checker
        that only knew `](...)` missed 16 of them once already, in this repository."""
        self.write("concepts/a.md", f':::image type="content" source="{DEAD}" alt-text="x":::')
        urls, _ = gate.scan(self.dir)
        self.assertEqual(len(urls), 1)

    def test_a_live_url_is_not_a_finding(self):
        self.write("concepts/a.md", f"![shot]({LIVE})\n")
        self.assertEqual(gate.scan(self.dir), ([], {}))

    def test_fix_rewrites_the_prefix_and_keeps_the_path(self):
        self.write("concepts/a.md", f"![shot]({DEAD})\n")
        gate.fix(self.dir)
        self.assertIn(LIVE, self.read("concepts/a.md"))
        self.assertEqual(gate.scan(self.dir), ([], {}))

    def test_fix_touches_nothing_else_in_the_file(self):
        """It rewrites a URL prefix, not prose. The tree is frozen and Microsoft's half is
        not ours to edit — see the decision record."""
        body = f"# Title\n\nSome prose with a `CALCULATE` call.\n\n![shot]({DEAD})\n\nMore.\n"
        self.write("concepts/a.md", body)
        gate.fix(self.dir)
        self.assertEqual(self.read("concepts/a.md"), body.replace(DEAD, LIVE))

    def test_fix_is_idempotent(self):
        self.write("concepts/a.md", f"![shot]({DEAD})\n")
        gate.fix(self.dir)
        self.assertEqual(gate.fix(self.dir), [])

    def test_a_url_under_another_upstream_path_is_left_alone(self):
        """The prefix is narrow on purpose. This gate knows about one host that is known
        to be gone; a general is-every-URL-alive check needs the network and is --online."""
        other = "https://raw.githubusercontent.com/MicrosoftDocs/other-repo/main/x.png"
        self.write("concepts/a.md", f"![shot]({other})\n")
        self.assertEqual(gate.scan(self.dir), ([], {}))


class Repository(unittest.TestCase):
    def test_the_shipped_tree_has_no_dead_image_host(self):
        urls, files = gate.scan()
        self.assertEqual((urls, files), ([], {}))

    def test_the_live_prefix_is_learn_and_not_an_archive(self):
        """Wayback was the obvious answer and it is not this one: sampled six of the 87 and
        only two were archived at all, and it would tie the content to a third party. Learn
        is the publisher, it is alive, and it served all 87."""
        self.assertTrue(gate.LIVE_PREFIX.startswith("https://learn.microsoft.com/"))


if __name__ == "__main__":
    unittest.main()
