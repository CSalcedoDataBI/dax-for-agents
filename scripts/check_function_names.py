#!/usr/bin/env python3
"""Fail when a catalogue name is not something you could put in front of a parenthesis.

`catalog.md` is the file an agent reads to learn what exists. Two of its 479 rows said
`DISTINCT column` and `DISTINCT table` — Microsoft's own labels for two pages of one
function, taken as if they were names. A DAX function name has no space in it, so the
library that exists to stop an agent inventing was handing it something that does not
compile.

It survived because the catalogue had only ever been compared against documentation. The
engine answers in one query, and it is the only authority on what functions exist:

    EVALUATE INFO.FUNCTIONS()      -- 470 rows, exactly one of them DISTINCT

That comparison needs a tabular engine with data, so it belongs beside `lab/check_lab.py`
and cannot run in CI. This is the part that can: a name is a single token, and that is
checkable from the tree alone.

    python scripts/check_function_names.py           # gate
    python scripts/check_function_names.py --fix     # repair the frozen tree

`--fix` exists because `generated/` is frozen at its stamp and the sync cannot be re-run to
produce it (see the 2026-08-27 decision record). It repairs a field this repository parsed
wrongly — not Microsoft's prose — and it takes the normalisation from
`sync_query_docs.function_name`, so the repair and the next regeneration cannot disagree.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "skills", "dax-reference")
GENERATED = os.path.join(REF, "generated")
sys.path.insert(0, os.path.join(REF, "scripts"))

import sync_query_docs as sync                                    # noqa: E402

# Letters, digits and underscores, in dot-separated parts: ABS, ISO.CEILING,
# INFO.VIEW.TABLES. Deliberately not a guess at what DAX allows in general — it is what
# all 470 names the engine returns look like.
NAME_RE = re.compile(r"[A-Z][A-Z0-9_]*(?:\.[A-Z0-9_]+)*")
_FM_NAME = re.compile(r"^name:.*$", re.M)


def offenders(catalog):
    return [f["name"] for f in catalog["functions"] if not NAME_RE.fullmatch(f["name"])]


def _load():
    with open(os.path.join(GENERATED, "catalog.json"), encoding="utf-8") as f:
        return f.read()


def fix():
    """Repair catalog.json, the two indexes and the affected cards. Returns what changed."""
    raw = _load()
    catalog = json.loads(raw)
    changed = []
    for entry in catalog["functions"]:
        good = sync.function_name(entry["name"])
        if good == entry["name"]:
            continue
        changed.append((entry["file"], entry["name"], good))
        entry["name"] = good

        card = os.path.join(GENERATED, "library", entry["file"] + ".md")
        if os.path.exists(card):
            with open(card, encoding="utf-8") as f:
                text = f.read()
            # A lambda, not a replacement string: `re.sub` reads backslashes in one.
            text = _FM_NAME.sub(lambda _: f"name: {good}", text, count=1)
            with open(card, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)

    if changed:
        after = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
        with open(os.path.join(GENERATED, "catalog.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(after)
        with open(os.path.join(GENERATED, "catalog.md"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(sync._catalog_md(catalog["functions"], catalog["source"],
                                     catalog.get("sourceCommitDate", "")))
    return changed


def main(argv):
    if "--fix" in argv:
        changed = fix()
        if not changed:
            print("OK: nothing to repair.")
            return 0
        print(f"repaired {len(changed)} catalogue name(s):")
        for stem, before, after in changed:
            print(f"  {stem}: {before!r} -> {after!r}")
        return 0

    catalog = json.loads(_load())
    bad = offenders(catalog)
    if not bad:
        print(f"OK: all {len(catalog['functions'])} catalogue names are typeable "
              f"function names.")
        return 0
    print(f"ERROR: {len(bad)} catalogue name(s) are not function names. `catalog.md` is "
          f"what an agent reads to learn what exists, so a name it cannot type is a "
          f"function it will get wrong. Run: python scripts/check_function_names.py --fix")
    for name in bad:
        print(f"  {name!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
