#!/usr/bin/env python3
"""Fail when the README's invention table and the saved runs disagree.

The README's headline claim used to be a sentence nobody could check. It is now a table of
numbers, which is better only if something checks it — otherwise it is the same sentence
with more places to rot. Every other count in this repository is compared against the tree;
this one is compared against the runs it came from.

The comparison is free. The answers are committed under `evals/hallucination/runs/`, and
counting inventions in them is a lookup against `catalog.json` — no model, no API call. So
this runs in CI beside the rest.

It also catches something a person would not: the counter itself changing. If the way an
invention is counted is ever edited — and it has been, twice, both times because a result
looked too good — every number in the README moves, and this is what says so.

Run: python scripts/check_eval_claims.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS = os.path.join(ROOT, "evals", "hallucination", "runs")
README = os.path.join(ROOT, "README.md")
sys.path.insert(0, os.path.join(ROOT, "evals", "hallucination"))

import run_ab                                                     # noqa: E402

# `| Claude Sonnet 5 | 8 | **0** |` — the bold on a zero is emphasis, not data.
_ROW = re.compile(r"^\|\s*([A-Za-z][A-Za-z0-9.\- ]+?)\s*\|\s*\**(\d+)\**\s*\|"
                  r"\s*\**(\d+)\**\s*\|\s*$", re.M)

# The README names models the way a person says them; the run files name them the way an API
# does. One table, written here, rather than a guess at the transformation between the two.
MODEL_FILES = {
    "Claude Haiku 4.5": "2026-08-29-claude-haiku-4-5.json",
    "Claude Sonnet 5": "2026-08-29-claude-sonnet-5.json",
    "DeepSeek V4-Pro": "2026-08-29-deepseek-v4-pro.json",
    "DeepSeek V4-Flash": "2026-08-29-deepseek-v4-flash.json",
}


def table_rows(path=README):
    """(model, arm A, arm B) for every row of the invention table."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return [(m.group(1), int(m.group(2)), int(m.group(3)))
            for m in _ROW.finditer(text) if m.group(1) in MODEL_FILES]


def counted(filename, names):
    """(arm A, arm B) recounted from the saved answers."""
    import json
    with open(os.path.join(RUNS, filename), encoding="utf-8") as f:
        saved = json.load(f)
    records = saved["records"]
    return (sum(len(run_ab.invented(r["A"]["text"], names)) for r in records),
            sum(len(run_ab.invented(r["B"]["text"], names)) for r in records))


def main():
    names, _ = run_ab.catalog_names()
    rows = table_rows()
    if not rows:
        print("ERROR: the README has no invention table this gate recognises. If it was "
              "removed on purpose, remove this gate in the same commit.")
        return 1

    problems = []
    for model, said_a, said_b in rows:
        try:
            got_a, got_b = counted(MODEL_FILES[model], names)
        except (OSError, ValueError, KeyError) as exc:
            problems.append(f"{model}: its run file cannot be read ({exc})")
            continue
        if (said_a, said_b) != (got_a, got_b):
            problems.append(f"{model}: the README says {said_a} -> {said_b}, the saved "
                            f"answers count {got_a} -> {got_b}")

    missing = sorted(set(MODEL_FILES) - {m for m, _, _ in rows})
    for model in missing:
        problems.append(f"{model} has a run file and no row in the README table — either "
                        f"publish it or delete the run, but do not keep a measurement the "
                        f"prose does not mention")

    if problems:
        print(f"ERROR: the README's invention table does not match the runs it came from:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"OK: the README's invention table matches all {len(rows)} saved run(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
