#!/usr/bin/env python3
"""Fail if the hand-written examples tree breaks its own contract.

The promise is "at least three executable examples per function". A promise that nothing
checks is a sentence that rots, and this repo has already watched that happen to a count in
prose more than once.

What is checked here is STRUCTURE, because that is what CI can see: three examples, a real
model, a result block behind every query, a function that exists. Whether the numbers are
right is the runner's job (`lab/check_lab.py examples`), and it needs a tabular engine that
CI does not have.

Run: python scripts/check_examples.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import examples_io as exio

ROOT = exio.ROOT
CATALOG = os.path.join(ROOT, "skills", "dax-reference", "generated", "catalog.json")
LAB = os.path.join(ROOT, "lab")

MIN_EXAMPLES = 3

# Coverage ratchet. The tree is being filled category by category, so the gate cannot demand
# 479 yet -- it would be red for every PR until the last one. What it CAN do is refuse to go
# backwards: raise this as each phase lands, and a deleted example file fails immediately
# instead of quietly shrinking the library.
MIN_COVERED = 99


def _catalog_stems(path=CATALOG):
    """stem -> function name, from the generated catalog."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for entry in data.get("functions", []):
        filename = entry.get("file", "")
        stem = filename[: -len("-function-dax.md")] if filename.endswith(
            "-function-dax.md") else os.path.splitext(filename)[0]
        out[stem] = entry.get("name", "")
    return out


def _models(lab=LAB):
    """Scenario directories under lab/, plus the sentinel for "reads no model data"."""
    if not os.path.isdir(lab):
        return {exio.NO_MODEL}
    found = {d for d in os.listdir(lab)
             if os.path.isdir(os.path.join(lab, d)) and not d.startswith("__")}
    return found | {exio.NO_MODEL}


def _relative(path, root):
    """Ruta legible para el mensaje de error.

    En Windows `relpath` LANZA si los dos caminos estan en unidades distintas, y eso pasa en
    cuanto un test construye su arbol en el temporal de C: con el repo en E:. Se cae a algo
    relativo al propio arbol de ejemplos, que siempre esta en la misma unidad.
    """
    for base in (ROOT, os.path.dirname(root)):
        try:
            return os.path.relpath(path, base).replace("\\", "/")
        except ValueError:
            continue
    return os.path.basename(path)


def check(root=exio.EXAMPLES_DIR, catalog=CATALOG, lab=LAB, min_covered=MIN_COVERED):
    stems = _catalog_stems(catalog)
    models = _models(lab)
    problems = []
    covered = 0

    for path in exio.example_files(root):
        rel = _relative(path, root)
        stem = os.path.splitext(os.path.basename(path))[0]
        fm, pairs = exio.parse(path)
        covered += 1

        if stem not in stems:
            problems.append(f"{rel}: no function with the stem '{stem}' is in the catalogue")
        elif fm.get("function") and fm["function"] != stems[stem]:
            problems.append(f"{rel}: the frontmatter says function: {fm['function']} but "
                            f"the stem '{stem}' is {stems[stem]}")
        if not fm.get("function"):
            problems.append(f"{rel}: the frontmatter has no 'function:'")

        model = fm.get("model")
        if not model:
            problems.append(f"{rel}: the frontmatter has no 'model:'")
        elif model not in models:
            problems.append(f"{rel}: model: {model} is not a lab/ scenario "
                            f"(there are: {', '.join(sorted(models))})")

        if len(pairs) < MIN_EXAMPLES:
            problems.append(f"{rel}: {len(pairs)} example(s), the minimum is {MIN_EXAMPLES}")
        for i, (_, result) in enumerate(pairs, 1):
            if result is None:
                problems.append(f"{rel} [{i}]: a query with no result block — an example "
                                f"without a measured number is an assertion, not an example")

    if covered < min_covered:
        problems.append(f"coverage: {covered} function(s) with examples, and the floor is "
                        f"{min_covered}. If a file was deleted on purpose, lower "
                        f"MIN_COVERED in the same commit and say why.")
    return problems, covered, len(stems)


def main():
    problems, covered, total = check()
    if problems:
        print("EXAMPLES CHECK FAILED:")
        for p in problems:
            print(f"  - {p}")
        print(f"\n{len(problems)} problem(s). {covered} of {total} functions with examples.")
        return 1
    print(f"OK: {covered} of {total} functions with examples, {MIN_EXAMPLES}+ each, "
          f"every one carrying a measured result.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
