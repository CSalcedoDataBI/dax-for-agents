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

from check_plugin_manifest import check, main, skill_dirs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLUGIN = {
    "name": "dax",
    "version": "0.1.0",
    "skills": ["./skills/alpha-skill", "./skills/beta-skill"],
}
MARKET = {
    "name": "dax-for-agents",
    "owner": {"name": "someone"},
    "plugins": [{"name": "dax", "source": "./", "description": "x"}],
}


class Fixture:
    """A throwaway repo with two skills and a manifest pair, mutated per test."""

    def __init__(self, plugin=None, market=None, skills=("alpha-skill", "beta-skill")):
        self.dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.dir, ".claude-plugin"))
        os.mkdir(os.path.join(self.dir, "skills"))
        for name in skills:
            os.mkdir(os.path.join(self.dir, "skills", name))
            with open(os.path.join(self.dir, "skills", name, "SKILL.md"),
                      "w", encoding="utf-8") as f:
                f.write(f"---\nname: {name}\ndescription: Use when testing.\n---\n")
        self.write("plugin.json", PLUGIN if plugin is None else plugin)
        self.write("marketplace.json", MARKET if market is None else market)

    def write(self, name, obj):
        path = os.path.join(self.dir, ".claude-plugin", name)
        with open(path, "w", encoding="utf-8") as f:
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
        # Claude Code no falla aqui: si NINGUNA ruta existe vuelve al escaneo por
        # defecto. Ahora ese escaneo SI encuentra skills/, asi que una entrada muerta
        # ya no vacia el plugin -- pero sigue siendo una mentira en el manifiesto.
        with Fixture(plugin=deep(PLUGIN, skills=["./skills/alpha-skill",
                                                 "./skills/beta-skill",
                                                 "./skills/ghost-skill"])) as f:
            errors = check(f.dir)
        self.assertEqual(len(errors), 1)
        self.assertIn("ghost-skill", errors[0])

    def test_a_path_without_the_dot_slash_prefix_fails(self):
        # Ojo con afirmar solo que el mensaje contiene './': sin la comprobacion del
        # prefijo, 'alpha-skill' se recorta a 'pha-skill' y el error de ruta inexistente
        # tambien lleva './'. El test pasaba con el arreglo quitado.
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
        # `assertTrue(check(...))` pasaria con la comprobacion quitada: el array vacio
        # deja las dos skills sin listar y eso ya devuelve errores. Hay que afirmar el
        # mensaje concreto, no que la lista no este vacia.
        with Fixture(plugin=deep(PLUGIN, skills=[])) as f:
            errors = check(f.dir)
        self.assertTrue(any("reviewable" in e for e in errors), errors)

    def test_a_trailing_slash_is_the_same_path(self):
        with Fixture(plugin=deep(PLUGIN, skills=["./skills/alpha-skill/",
                                                 "./skills/beta-skill"])) as f:
            self.assertEqual(check(f.dir), [])


class TheTwoNames(unittest.TestCase):
    """`/plugin install dax@dax-for-agents` se deletrea con estos dos nombres."""

    def test_a_plugin_name_absent_from_the_marketplace_fails(self):
        with Fixture(plugin=deep(PLUGIN, name="other")) as f:
            errors = check(f.dir)
        self.assertTrue(any("not among the marketplace entries" in e for e in errors))

    def test_a_source_that_is_not_the_repo_root_fails(self):
        market = deep(MARKET)
        market["plugins"][0]["source"] = "./plugins/dax"
        with Fixture(market=market) as f:
            errors = check(f.dir)
        self.assertTrue(any("has to be './'" in e for e in errors), errors)

    def test_skills_declared_twice_fails(self):
        market = deep(MARKET)
        market["plugins"][0]["skills"] = ["./skills/alpha-skill"]
        with Fixture(market=market) as f:
            errors = check(f.dir)
        self.assertTrue(any("two sources of truth" in e for e in errors), errors)

    def test_a_version_in_the_marketplace_entry_fails(self):
        # release-please solo bumpea plugin.json. Una copia aqui se congela.
        market = deep(MARKET)
        market["plugins"][0]["version"] = "0.1.0"
        with Fixture(market=market) as f:
            errors = check(f.dir)
        self.assertTrue(any("release-please" in e for e in errors), errors)


class MissingOrBroken(unittest.TestCase):
    def test_a_missing_plugin_json_fails(self):
        with Fixture() as f:
            os.remove(os.path.join(f.dir, ".claude-plugin", "plugin.json"))
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

    def test_the_five_skills_are_the_ones_shipped(self):
        self.assertEqual(skill_dirs(ROOT), ["skills/dax-lib",
                                            "skills/dax-lib-install",
                                            "skills/dax-reference",
                                            "skills/dax-udf-authoring",
                                            "skills/dax-window-functions"])


if __name__ == "__main__":
    unittest.main()
