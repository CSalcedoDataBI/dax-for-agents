#!/usr/bin/env python3
"""Tests for the examples gate. Run: python -m unittest discover -s scripts"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_examples import check  # noqa: E402

EJEMPLO = """---
function: IF
model: ninguno
---

# IF

```dax
EVALUATE ROW("a", 1)
```

```result
a
1
```

```dax
EVALUATE ROW("b", 2)
```

```result
b
2
```

```dax
EVALUATE ROW("c", 3)
```

```result
c
3
```
"""


class Fixture:
    """Un repo de mentira: un catalogo con IF y ABS, un lab con contoso, un ejemplo."""

    def __init__(self, body=EJEMPLO, name="if.md", category="logical"):
        self.dir = tempfile.mkdtemp()
        self.examples = os.path.join(self.dir, "examples")
        os.makedirs(os.path.join(self.examples, category))
        with open(os.path.join(self.examples, category, name), "w", encoding="utf-8") as f:
            f.write(body)

        self.catalog = os.path.join(self.dir, "catalog.json")
        with open(self.catalog, "w", encoding="utf-8") as f:
            json.dump({"functions": [
                {"name": "IF", "file": "if-function-dax.md"},
                {"name": "ABS", "file": "abs-function-dax.md"},
            ]}, f)

        self.lab = os.path.join(self.dir, "lab")
        os.makedirs(os.path.join(self.lab, "contoso"))

    def run(self, min_covered=1):
        return check(root=self.examples, catalog=self.catalog, lab=self.lab,
                     min_covered=min_covered)[0]

    def close(self):
        shutil.rmtree(self.dir, ignore_errors=True)


class Gate(unittest.TestCase):
    def tearDown(self):
        if getattr(self, "fx", None):
            self.fx.close()

    def assertAccepts(self, fixture):
        """Que NO haya problemas solo prueba algo si el gate llego a mirar el fichero.

        Un check que no encuentra el arbol devuelve la lista vacia igual que uno que lo
        aprueba. Esta comprobacion ya se colo cuatro veces en este repo, asi que aqui se
        exige primero que el fichero se haya CONTADO.
        """
        problems, covered, _ = check(root=fixture.examples, catalog=fixture.catalog,
                                     lab=fixture.lab, min_covered=1)
        self.assertEqual(covered, 1, "el gate no llego a leer el ejemplo")
        self.assertEqual(problems, [])

    def test_a_well_formed_file_passes(self):
        self.fx = Fixture()
        self.assertAccepts(self.fx)

    def test_two_examples_are_not_enough(self):
        self.fx = Fixture(EJEMPLO[:EJEMPLO.index('```dax\nEVALUATE ROW("c"')])
        self.assertIn("2 example(s)", " ".join(self.fx.run()))

    def test_a_query_with_no_result_block_fails(self):
        body = EJEMPLO + '\n```dax\nEVALUATE ROW("d", 4)\n```\n'
        self.fx = Fixture(body)
        self.assertIn("no result block", " ".join(self.fx.run()))

    def test_a_model_that_is_not_a_lab_scenario_fails(self):
        self.fx = Fixture(EJEMPLO.replace("model: ninguno", "model: inventado"))
        self.assertIn("is not a lab/ scenario", " ".join(self.fx.run()))

    def test_a_real_lab_scenario_is_accepted(self):
        self.fx = Fixture(EJEMPLO.replace("model: ninguno", "model: contoso"))
        self.assertAccepts(self.fx)

    def test_a_missing_model_key_fails(self):
        self.fx = Fixture(EJEMPLO.replace("model: ninguno\n", ""))
        self.assertIn("has no 'model:'", " ".join(self.fx.run()))

    def test_a_stem_with_no_function_in_the_catalog_fails(self):
        self.fx = Fixture(name="noexiste.md")
        self.assertIn("no function with the stem", " ".join(self.fx.run()))

    def test_frontmatter_naming_another_function_fails(self):
        """if.md que dice `function: ABS` mandaria al lector a la ficha equivocada."""
        self.fx = Fixture(EJEMPLO.replace("function: IF", "function: ABS"))
        self.assertIn("but the stem", " ".join(self.fx.run()))

    def test_coverage_below_the_ratchet_fails(self):
        self.fx = Fixture()
        problems = check(root=self.fx.examples, catalog=self.fx.catalog, lab=self.fx.lab,
                         min_covered=2)[0]
        self.assertIn("coverage", " ".join(problems))


if __name__ == "__main__":
    unittest.main()
