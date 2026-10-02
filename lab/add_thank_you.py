#!/usr/bin/env python3
"""Add the author's "Thank You!!" page, first, to every report under lab/.

The page lives once, in lab/thank-you/ (the same page powerquery-m-for-agents ships), and
this script copies it into each report. A link that changes is edited there and rolled out by
running this again; nobody edits four copies.

Its Deneb cover draws fixed links and reads no data, but Deneb renders nothing without fields,
so each copy is bound to a column and a measure that exist in that report's own model. The
source page's filters point at fields of another model, so they are dropped.

    python lab/add_thank_you.py           # write
    python lab/add_thank_you.py --check   # gate mode: exit 1 if any report would change

Idempotent: a second run changes nothing.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "thank-you")
DENEB = "deneb7E15AEF80B9E4D4F8E12924291ECE89A"
PAGE = "thankyou"

# report folder -> (measures table, its placeholder column, a measure in it). All four exist
# in the model's TMDL; none of them is read by the cover, they only let Deneb render.
REPORTS = {
    os.path.join("blancos", "Blancos.Report"): ("_Medidas", "Marcador", "Media"),
    os.path.join("claves-huerfanas", "ClavesHuerfanas.Report"): ("_Medidas", "Marcador", "Unidades"),
    os.path.join("contoso", "Contoso.Report"): ("_Measures", "Placeholder", "Total Sales"),
    os.path.join("rendimiento", "Rendimiento.Report"): ("_Medidas", "Marcador", "Total"),
}


def _ref(kind, table, name):
    return {"field": {kind: {"Expression": {"SourceRef": {"Entity": table}}, "Property": name}},
            "queryRef": f"{table}.{name}", "nativeQueryRef": name}


def _text(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def planned(report, binding):
    """{path relative to the report folder: file text} for the page and what it touches."""
    table, column, measure = binding
    files = {}
    with open(os.path.join(TEMPLATE, "page.json"), encoding="utf-8") as f:
        page = json.load(f)
    page["name"] = PAGE
    files[os.path.join("definition", "pages", PAGE, "page.json")] = _text(page)

    visuals = os.path.join(TEMPLATE, "visuals")
    for vid in sorted(os.listdir(visuals)):
        with open(os.path.join(visuals, vid, "visual.json"), encoding="utf-8") as f:
            v = json.load(f)
        if v["visual"]["visualType"] == DENEB:
            v["visual"]["query"] = {"queryState": {"dataset": {"projections": [
                _ref("Column", table, column), _ref("Measure", table, measure)]}}}
            v.pop("filterConfig", None)
        files[os.path.join("definition", "pages", PAGE, "visuals", vid, "visual.json")] = _text(v)

    pages_path = os.path.join(report, "definition", "pages", "pages.json")
    with open(pages_path, encoding="utf-8") as f:
        pages = json.load(f)
    # First, and the page the report opens on: the author asked for it ahead of the scenarios.
    pages["pageOrder"] = [PAGE] + [p for p in pages["pageOrder"] if p != PAGE]
    pages["activePageName"] = PAGE
    files[os.path.join("definition", "pages", "pages.json")] = _text(pages)

    report_path = os.path.join(report, "definition", "report.json")
    with open(report_path, encoding="utf-8") as f:
        rep = json.load(f)
    custom = rep.get("publicCustomVisuals", [])
    if DENEB not in custom:
        rep["publicCustomVisuals"] = custom + [DENEB]
    files[os.path.join("definition", "report.json")] = _text(rep)
    return files


def run(check=False):
    changed = []
    for rel, binding in REPORTS.items():
        report = os.path.join(HERE, rel)
        for path, text in planned(report, binding).items():
            full = os.path.join(report, path)
            try:
                with open(full, encoding="utf-8") as f:
                    current = f.read()
            except FileNotFoundError:
                current = None
            if current == text:
                continue
            changed.append(os.path.join(rel, path))
            if not check:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
    return changed


def main(argv):
    check = "--check" in argv
    changed = run(check)
    if not changed:
        print("OK: every lab report opens on the Thank You!! page from lab/thank-you/.")
        return 0
    verb = "would change" if check else "wrote"
    print(f"{verb} {len(changed)} file(s):")
    for c in changed:
        print(f"  - {c}")
    return 1 if check else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
