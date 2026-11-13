#!/usr/bin/env python3
"""Tests for the plugin manifest gate. Run: python -m unittest discover -s scripts"""
import io
import os
import sys
import json
import shutil
import contextlib
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_plugin_manifest import PLUGIN_DIR, check, main, skill_dirs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLUGIN = {
    "name": "dax",
    "version": "0.1.0",
    "skills": ["./skills/alpha-skill", "./skills/beta-skill"],
}
MARKET = {
    "name": "dax-for-agents",
    "owner": {"name": "someone"},
    "plugins": [{"name": "dax", "source": f"./{PLUGIN_DIR}", "description": "x"}],
}


class Fixture:
    """A throwaway repo with the plugin in its subfolder, two skills and a manifest pair."""

    def __init__(self, plugin=None, market=None, skills=("alpha-skill", "beta-skill")):
        self.dir = tempfile.mkdtemp()
        self.plugin = os.path.join(self.dir, *PLUGIN_DIR.split("/"))
        os.makedirs(os.path.join(self.plugin, ".claude-plugin"))
        os.mkdir(os.path.join(self.dir, ".claude-plugin"))
        for name in skills:
            self.put(f"skills/{name}/SKILL.md",
                     f"---\nname: {name}\ndescription: Use when testing.\n---\n")
        self.write("plugin.json", PLUGIN if plugin is None else plugin)
        self.write("marketplace.json", MARKET if market is None else market)

    def put(self, rel, text="x"):
        path = os.path.join(self.plugin, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def write(self, name, obj):
        base = self.plugin if name == "plugin.json" else self.dir
        with open(os.path.join(base, ".claude-plugin", name), "w", encoding="utf-8") as f:
            json.dump(obj, f)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)


def deep(obj, **changes):
    out = json.loads(json.dumps(obj))
    out.update(changes)
    return out


class SkillsList(unittest.TestCase):
    def test_a_matching_manifest_passes(self):
        with Fixture() as f:
            self.assertEqual(check(f.dir), [])

    def test_a_skill_missing_from_the_manifest_fails(self):
        # El fallo que motiva todo esto: la skill existe, el plugin la ignora, y nadie
        # se entera porque instalar sigue diciendo exito.
        with Fixture(plugin=deep(PLUGIN, skills=["./skills/alpha-skill"])) as f:
            errors = check(f.dir)
        self.assertEqual(len(errors), 1)
        self.assertIn("beta-skill", errors[0])

    def test_a_listed_path_that_does_not_exist_fails(self):
        with Fixture(plugin=deep(PLUGIN, skills=["./skills/alpha-skill",
                                                 "./skills/beta-skill",
                                                 "./skills/ghost-skill"])) as f:
            errors = check(f.dir)
        self.assertEqual(len(errors), 1)
        self.assertIn("ghost-skill", errors[0])

    def test_a_path_without_the_dot_slash_prefix_fails(self):
        # Sin la comprobacion del prefijo, 'alpha-skill' se recorta a 'pha-skill' y el
        # error de ruta inexistente tambien lleva './'.
        with Fixture(plugin=deep(PLUGIN, skills=["skills/alpha-skill",
                                                 "./skills/beta-skill"])) as f:
            errors = check(f.dir)
        prefix = [e for e in errors if "must be a path starting" in e]
        self.assertEqual(len(prefix), 1, errors)
        self.assertIn("alpha-skill", prefix[0])

    def test_no_skills_array_fails(self):
        plugin = deep(PLUGIN)
        del plugin["skills"]
        with Fixture(plugin=plugin) as f:
            errors = check(f.dir)
        self.assertTrue(any("reviewable" in e for e in errors), errors)

    def test_an_empty_skills_array_fails(self):
        with Fixture(plugin=deep(PLUGIN, skills=[])) as f:
            errors = check(f.dir)
        self.assertTrue(any("reviewable" in e for e in errors), errors)

    def test_a_trailing_slash_is_the_same_path(self):
        with Fixture(plugin=deep(PLUGIN, skills=["./skills/alpha-skill/",
                                                 "./skills/beta-skill"])) as f:
            self.assertEqual(check(f.dir), [])


class TheTwoNames(unittest.TestCase):
    """`/plugin install dax-for-agents@dax-for-agents` se deletrea con estos dos nombres."""

    def test_a_plugin_name_absent_from_the_marketplace_fails(self):
        with Fixture(plugin=deep(PLUGIN, name="other")) as f:
            errors = check(f.dir)
        self.assertTrue(any("not among the marketplace entries" in e for e in errors))

    def test_a_source_that_is_not_the_plugin_folder_fails(self):
        # La raiz era el plugin hasta 0.9.0; un source './' volveria a enviar todo el repo.
        market = deep(MARKET)
        market["plugins"][0]["source"] = "./"
        with Fixture(market=market) as f:
            errors = check(f.dir)
        self.assertTrue(any(f"has to be './{PLUGIN_DIR}'" in e for e in errors), errors)

    def test_skills_declared_twice_fails(self):
        market = deep(MARKET)
        market["plugins"][0]["skills"] = ["./skills/alpha-skill"]
        with Fixture(market=market) as f:
            errors = check(f.dir)
        self.assertTrue(any("two sources of truth" in e for e in errors), errors)

    def test_a_version_in_the_marketplace_entry_fails(self):
        market = deep(MARKET)
        market["plugins"][0]["version"] = "0.1.0"
        with Fixture(market=market) as f:
            errors = check(f.dir)
        self.assertTrue(any("release-please" in e for e in errors), errors)


class ShippedTypes(unittest.TestCase):
    """v0.9.0 was refused for scripts inside skills/: only accepted types may ship."""

    def test_markdown_json_and_images_pass(self):
        with Fixture() as f:
            for rel in ("README.md", "LICENSE.md", "skills/alpha-skill/catalog.json",
                        "skills/alpha-skill/shot.webp", ".claude-plugin/icon.png"):
                f.put(rel)
            self.assertEqual(check(f.dir), [])

    def test_a_script_inside_a_skill_fails(self):
        for rel in ("skills/alpha-skill/scripts/run.py", "skills/alpha-skill/refresh.ps1",
                    "skills/alpha-skill/NOTICE", "skills/alpha-skill/diagram.svg"):
            with self.subTest(rel=rel), Fixture() as f:
                f.put(rel)
                errors = check(f.dir)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn(rel, errors[0])

    def test_a_claude_folder_inside_the_plugin_fails(self):
        with Fixture() as f:
            f.put(".claude/agents/x.md")
            errors = check(f.dir)
        self.assertTrue(any(".claude/ folder" in e for e in errors), errors)

    def test_a_second_claude_plugin_folder_fails(self):
        with Fixture() as f:
            f.put("skills/alpha-skill/.claude-plugin/plugin.json", "{}")
            errors = check(f.dir)
        self.assertTrue(any("only .claude-plugin/" in e for e in errors), errors)


class MissingOrBroken(unittest.TestCase):
    def test_a_missing_plugin_json_fails(self):
        with Fixture() as f:
            os.remove(os.path.join(f.plugin, ".claude-plugin", "plugin.json"))
            errors = check(f.dir)
        self.assertTrue(any("plugin.json is missing" in e for e in errors))

    def test_broken_json_fails(self):
        with Fixture() as f:
            with open(os.path.join(f.dir, ".claude-plugin", "marketplace.json"), "w",
                      encoding="utf-8") as fh:
                fh.write("{not json")
            errors = check(f.dir)
        self.assertTrue(any("not valid JSON" in e for e in errors))

    def test_no_manifest_directory_is_refused_rather_than_passing(self):
        with tempfile.TemporaryDirectory() as d:
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(d), 2)

    def test_main_reports_the_count_it_checked(self):
        with Fixture() as f:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = main(f.dir)
        self.assertEqual(code, 0)
        self.assertIn("2 skill(s)", out.getvalue())


class TheRealRepo(unittest.TestCase):
    def test_this_repo_passes(self):
        errors = check(ROOT)
        self.assertEqual(errors, [], "\n".join(errors or []))

    def test_the_six_skills_are_the_ones_shipped(self):
        self.assertEqual(skill_dirs(ROOT), ["skills/dax-feedback",
                                            "skills/dax-lib",
                                            "skills/dax-lib-install",
                                            "skills/dax-reference",
                                            "skills/dax-udf-authoring",
                                            "skills/dax-window-functions"])


if __name__ == "__main__":
    unittest.main()
