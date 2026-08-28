#!/usr/bin/env python3
"""Compare the catalogue against the only authority on what DAX functions exist.

Every other gate in this repository compares prose against the tree. This one compares the
tree against the **engine**, which is the same idea as the 31 field notes — a claim is worth
what you can run — applied for the first time to the catalogue itself.

    EVALUATE INFO.FUNCTIONS()

It found three names no engine would accept (`DISTINCT column`, `DISTINCT table`,
`T.INV.2t`), which had survived because the catalogue had only ever been compared against
documentation, and documentation is where all three came from. Those are repaired and
guarded by `scripts/check_function_names.py`, which runs in CI. This is the part that
cannot: it needs an engine.

**It does not need a refresh.** `INFO.FUNCTIONS()` is model metadata, not table data, so any
`.pbip` opened in Power BI Desktop answers it straight away — unlike `check_lab.py`, which
needs the data loaded. Open a scenario, read the port, run this.

    python lab/check_engine.py                    # list the local instances
    python lab/check_engine.py localhost:49183
    python lab/check_engine.py localhost:49183 --record   # rewrite the baseline

## Why a baseline and not a plain equality

The two lists will never match exactly, and neither difference is a defect:

  - Microsoft documents functions this engine version does not expose. Nine today, and all
    nine are among the sixteen the catalogue leaves uncategorised — a correlation clean
    enough to suggest "undocumented category" and "not in the engine" are one fact seen
    twice.
  - The engine exposes functions Microsoft does not document. One today.

A gate that failed on those would fail every run and be switched off. A gate that ignored
them would never notice a new one. So the known differences are written down with a reason,
and the check is that reality still matches what was written — in both directions. A
baseline entry that has resolved fails too: that is good news, and good news that nobody
records rots into folklore.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import check_lab                                                  # noqa: E402

CATALOG = os.path.join(ROOT, "skills", "dax-reference", "generated", "catalog.json")
BASELINE = os.path.join(HERE, "engine-baseline.json")

QUERY = 'EVALUATE SELECTCOLUMNS(INFO.FUNCTIONS(), "name", [FUNCTION_NAME])'


def engine_names(data_source):
    """Every function name the engine admits to having."""
    with check_lab.connect(data_source) as conn:
        with conn.cursor().execute(QUERY) as cur:
            return {str(row[0]).strip() for row in cur.fetchall() if row and row[0]}


def catalogue_names(path=CATALOG):
    with open(path, encoding="utf-8") as f:
        catalog = json.load(f)
    return {f["name"] for f in catalog["functions"]}


def load_baseline(path=BASELINE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compare(engine, documented, baseline):
    """(problems, only_docs, only_engine). Empty problems means reality matches the record."""
    only_docs = documented - engine
    only_engine = engine - documented
    known_docs = set(baseline.get("documented_not_in_engine", {}))
    known_engine = set(baseline.get("in_engine_not_documented", {}))

    problems = []
    for name in sorted(only_docs - known_docs):
        problems.append(f"documented but this engine does not have it, and it is not in the "
                        f"baseline: {name}")
    for name in sorted(only_engine - known_engine):
        problems.append(f"the engine has it and nothing here documents it, and it is not in "
                        f"the baseline: {name}")
    for name in sorted(known_docs - only_docs):
        problems.append(f"the baseline says the engine lacks {name} and this engine has it — "
                        f"good news, and the baseline has to say so")
    for name in sorted(known_engine - only_engine):
        problems.append(f"the baseline says {name} is undocumented and it now has a card — "
                        f"good news, and the baseline has to say so")
    return problems, only_docs, only_engine


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    record = "--record" in argv

    if not args:
        ports = check_lab.local_instances()
        if not ports:
            print("No local Power BI Desktop instance is listening. Open a lab scenario:")
            print("  lab/blancos/Blancos.pbip      (the smallest; no refresh needed)")
            return 2
        print("Local instances:")
        for port in ports:
            print(f"  localhost:{port}")
        print("\nRun again with one of them.")
        return 2

    data_source = args[0]
    try:
        engine = engine_names(data_source)
    except ImportError:
        return 2
    documented = catalogue_names()
    print(f"engine: {len(engine)} function(s)   catalogue: {len(documented)} name(s)")

    if record:
        baseline = load_baseline()
        baseline["documented_not_in_engine"] = {
            name: baseline.get("documented_not_in_engine", {}).get(name, "TODO: say why")
            for name in sorted(documented - engine)}
        baseline["in_engine_not_documented"] = {
            name: baseline.get("in_engine_not_documented", {}).get(name, "TODO: say why")
            for name in sorted(engine - documented)}
        with open(BASELINE, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n")
        print(f"baseline rewritten. Every entry left as 'TODO: say why' needs a reason "
              f"before it means anything.")
        return 0

    problems, only_docs, only_engine = compare(engine, documented, load_baseline())
    print(f"  documented, not in this engine: {len(only_docs)}")
    print(f"  in this engine, not documented: {len(only_engine)}")
    if not problems:
        print("\nOK: the catalogue and the engine differ exactly where the baseline says "
              "they do.")
        return 0
    print(f"\nERROR: {len(problems)} difference(s) the baseline does not account for:")
    for p in problems:
        print(f"  - {p}")
    print("\nIf the change is real, record it with --record and write the reason.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
