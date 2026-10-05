"""Inject example measures into the lab's Contoso model and hand back a .pbip zip.

When a user wants a DAX example to open and none of the lab pages covers it, the agent does
not build a project: it writes the measures (after reading their cards in this skill) and this
script injects them into the master model the field notes were measured on, adds one page
showing them, and zips the result. Same files every time, so the format cannot drift.

Spec (JSON file):

    {
      "title": "CALCULATE vs KEEPFILTERS",
      "note": "One paragraph: what to look at on this page and why it differs.",
      "rows": "DimProduct[Brand]",
      "measures": [
        {"name": "Red sales", "expression": "CALCULATE([Total Sales], DimProduct[ColorName] = \\"Red\\")",
         "formatString": "\\\\$#,0", "description": "Replaces the color filter."}
      ]
    }

`rows` is optional (default DimProduct[Brand]); `formatString` and `description` too.

Run:
    python inject_example.py spec.json --out <dir>            # master from lab/ or the release
    python inject_example.py spec.json --out <dir> --master <folder-or-zip>

What it checks before writing: names do not collide, every Table[Column] and [Measure] the
expressions reference exists in the model (or among the new measures), parentheses balance.
What it CANNOT check: that the DAX evaluates to what you expect. There is no engine here —
say so to the user.
"""
import argparse
import io
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
import zipfile
import urllib.request

RELEASE_ZIP = ("https://github.com/CSalcedoDataBI/dax-for-agents/releases/latest/download/"
               "lab-contoso.zip")
HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL_MASTER = os.path.normpath(os.path.join(HERE, "..", "..", "..", "lab", "contoso"))
MODEL = "Contoso.SemanticModel"
REPORT = "Contoso.Report"
FOLDER = "00 Your example"
VISUAL_SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
                 "visualContainer/2.11.0/schema.json")
PAGE_SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"
               "page/2.0.0/schema.json")


def fail(msg):
    sys.exit(f"FAIL: {msg}")


# --- master -------------------------------------------------------------------------------

MAX_ZIP = 20 * 1024 * 1024


def safe_extract(z, workdir):
    root = os.path.realpath(workdir)
    for member in z.namelist():
        target = os.path.realpath(os.path.join(root, member))
        if os.path.isabs(member) or not target.startswith(root + os.sep):
            fail(f"zip entry escapes the work folder: {member}")
    z.extractall(root)


def fetch_master(source, workdir):
    """Copy the master into workdir/contoso and return that path."""
    dest = os.path.join(workdir, "contoso")
    if source is None:
        source = LOCAL_MASTER if os.path.isdir(LOCAL_MASTER) else RELEASE_ZIP
    if "://" in source:
        # Only the official asset. A URL taken from anywhere else would let whoever wrote it
        # pick the model the user opens and refreshes -- and a refresh runs Power Query.
        if source != RELEASE_ZIP:
            fail(f"--master URL must be {RELEASE_ZIP}")
        with urllib.request.urlopen(source, timeout=60) as r:
            data = r.read(MAX_ZIP + 1)
        if len(data) > MAX_ZIP:
            fail("the master zip is larger than expected")
        safe_extract(zipfile.ZipFile(io.BytesIO(data)), workdir)
    elif source.endswith(".zip"):
        safe_extract(zipfile.ZipFile(source), workdir)
    else:
        shutil.copytree(source, dest, ignore=shutil.ignore_patterns(".pbi", "cache.abf"))
    if not os.path.isfile(os.path.join(dest, "Contoso.pbip")):
        fail(f"no contoso/Contoso.pbip in the master ({source})")
    print(f"master: {source}")
    return dest


# --- model ----------------------------------------------------------------------------------

NAME = r"(?:'(?:[^']|'')+'|[^\s=']+)"


def unquote(name):
    return name[1:-1].replace("''", "'") if name.startswith("'") else name


def quote(name):
    return name if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name) else "'" + name.replace("'", "''") + "'"


def read_model(model_dir):
    """{table: {"columns": set, "measures": set}} from the TMDL tables folder."""
    tables = {}
    tdir = os.path.join(model_dir, "definition", "tables")
    for fn in sorted(os.listdir(tdir)):
        text = open(os.path.join(tdir, fn), encoding="utf-8").read()
        m = re.search(rf"^table ({NAME})", text, re.M)
        if not m:
            continue
        t = unquote(m.group(1))
        cols = {unquote(x) for x in re.findall(rf"^\tcolumn ({NAME})", text, re.M)}
        meas = {unquote(x) for x in re.findall(rf"^\tmeasure ({NAME})", text, re.M)}
        tables[t] = {"columns": cols, "measures": meas}
    return tables


def parse_ref(ref):
    m = re.fullmatch(r"\s*('(?:[^']|'')+'|[A-Za-z_][\w ]*?)\[([^\]]+)\]\s*", ref)
    if not m:
        fail(f"'{ref}' is not a Table[Column] reference")
    return unquote(m.group(1)), m.group(2)


def strip_strings(expr):
    return re.sub(r'"(?:[^"]|"")*"', '""', expr)


# A line break inside a value that lands on one TMDL line ends the property and starts whatever
# follows -- say, a partition whose Power Query source runs on the user's refresh. The spec is
# written by an agent that may have read untrusted text, so these are refused, not escaped.
LINE_BREAKS = "\r\n\v\f\x1c\x1d\x1e\x85  "


def has_control(text, allowed=""):
    return any((ord(c) < 32 or ord(c) == 127 or c in LINE_BREAKS) and c not in allowed
               for c in text)


def normalize_expression(expr):
    """Every kind of line break becomes \\n, so every line gets the expression's indent."""
    expr = expr.replace("\r\n", "\n")
    for c in LINE_BREAKS:
        expr = expr.replace(c, "\n")
    return expr.strip()


def check_fields(spec):
    problems = []
    for m in spec["measures"]:
        label = repr(m.get("name"))
        if not str(m.get("name") or "").strip() or not str(m.get("expression") or "").strip():
            problems.append(f"{label}: every measure needs a name and an expression")
            continue
        for field in ("name", "formatString"):
            if has_control(str(m.get(field) or "")):
                problems.append(f"{label}: {field} contains a line break or control character")
        if has_control(normalize_expression(m["expression"]), allowed="\n\t"):
            problems.append(f"{label}: expression contains a control character")
    if has_control(str(spec.get("rows", ""))):
        problems.append("rows contains a line break or control character")
    if problems:
        fail("\n  " + "\n  ".join(problems))


def check(spec, tables):
    all_measures = {m for t in tables.values() for m in t["measures"]}
    all_columns = {c for t in tables.values() for c in t["columns"]}
    new = [m["name"] for m in spec["measures"]]
    problems = []
    if len(set(new)) != len(new):
        problems.append("two new measures share a name")
    for n in new:
        if n in all_measures:
            problems.append(f"measure '{n}' already exists in the model - pick another name")
    known_measures = all_measures | set(new)
    for m in spec["measures"]:
        expr = strip_strings(m["expression"])
        if expr.count("(") != expr.count(")"):
            problems.append(f"'{m['name']}': unbalanced parentheses")
        for tbl, col in re.findall(r"('(?:[^']|'')+'|\b[A-Za-z_]\w*)\[([^\]]+)\]", expr):
            t = unquote(tbl)
            if t not in tables:
                problems.append(f"'{m['name']}': table {t} does not exist")
            elif col not in tables[t]["columns"] and col not in tables[t]["measures"]:
                problems.append(f"'{m['name']}': {t}[{col}] does not exist")
        # bare [X]: not preceded by a table name or a closing quote
        for name in re.findall(r"(?<![\w'\]])\[([^\]]+)\]", expr):
            if name not in known_measures and name not in all_columns:
                problems.append(f"'{m['name']}': [{name}] is neither a measure nor a column")
    t, c = parse_ref(spec.get("rows", "DimProduct[Brand]"))
    if t not in tables or c not in tables[t]["columns"]:
        problems.append(f"rows: {t}[{c}] does not exist")
    if problems:
        fail("\n  " + "\n  ".join(problems))


def tmdl_measure(m):
    lines = []
    for d in (m.get("description") or "").splitlines():
        lines.append(f"\t/// {d}".rstrip())
    expr = normalize_expression(m["expression"])
    if "\n" in expr:
        lines.append(f"\tmeasure {quote(m['name'])} =")
        lines += ["\t\t\t" + ln if ln.strip() else "" for ln in expr.split("\n")]
    else:
        lines.append(f"\tmeasure {quote(m['name'])} = {expr}")
    if m.get("formatString"):
        lines.append(f"\t\tformatString: {m['formatString']}")
    lines.append(f"\t\tdisplayFolder: {FOLDER}")
    lines.append(f"\t\tlineageTag: {uuid.uuid4()}")
    return "\n".join(lines)


def inject_measures(model_dir, spec):
    path = os.path.join(model_dir, "definition", "tables", "_Measures.tmdl")
    text = open(path, encoding="utf-8").read().rstrip("\n")
    # measures go right after the last measure block, before any partition
    block = "\n\n".join(tmdl_measure(m) for m in spec["measures"])
    m = re.search(r"^\tpartition ", text, re.M)
    if m:
        text = text[:m.start()] + block + "\n\n" + text[m.start():]
    else:
        text += "\n\n" + block
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")


# --- report ---------------------------------------------------------------------------------

def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return (s or "example")[:40]


def literal(text):
    return {"expr": {"Literal": {"Value": "'" + text.replace("'", "''") + "'"}}}


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def add_page(report_dir, spec):
    pages = os.path.join(report_dir, "definition", "pages")
    name = "ejemplo-" + slug(spec["title"])
    if os.path.exists(os.path.join(pages, name)):
        fail(f"page {name} already exists in the master")
    write_json(os.path.join(pages, name, "page.json"), {
        "$schema": PAGE_SCHEMA, "name": name, "displayName": spec["title"][:100],
        "displayOption": "FitToPage", "height": 720, "width": 1280})

    write_json(os.path.join(pages, name, "visuals", "nota", "visual.json"), {
        "$schema": VISUAL_SCHEMA, "name": "nota",
        "position": {"x": 40, "y": 40, "z": 1, "height": 140, "width": 1200, "tabOrder": 1},
        "visual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": [
            {"textRuns": [{"value": spec["title"], "textStyle": {"fontWeight": "bold", "fontSize": "16pt"}}]},
            {"textRuns": [{"value": spec.get("note", "")}]},
        ]}}]}, "drillFilterOtherVisuals": True}})

    t, c = parse_ref(spec.get("rows", "DimProduct[Brand]"))
    values = [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}},
                                     "Property": m["name"]}},
               "queryRef": f"_Measures.{m['name']}", "nativeQueryRef": m["name"]}
              for m in spec["measures"]]
    write_json(os.path.join(pages, name, "visuals", "matriz", "visual.json"), {
        "$schema": VISUAL_SCHEMA, "name": "matriz",
        "position": {"x": 40, "y": 200, "z": 0, "height": 480, "width": 1200, "tabOrder": 0},
        "visual": {"visualType": "pivotTable", "query": {"queryState": {
            "Rows": {"projections": [{
                "field": {"Column": {"Expression": {"SourceRef": {"Entity": t}}, "Property": c}},
                "queryRef": f"{t}.{c}", "nativeQueryRef": c, "active": True}]},
            "Values": {"projections": values}}},
            "visualContainerObjects": {"title": [{"properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "text": literal(f"Your measures by {c}")}}]},
            "drillFilterOtherVisuals": True}})

    meta_path = os.path.join(pages, "pages.json")
    meta = json.load(open(meta_path, encoding="utf-8"))
    meta["pageOrder"].insert(0, name)
    meta["activePageName"] = name
    write_json(meta_path, meta)
    return name


# --- main -----------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("--out", required=True, help="directory for the zip")
    ap.add_argument("--master", help="lab/contoso folder or lab-contoso.zip (default: local, else release)")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    if not spec.get("title") or not spec.get("measures"):
        fail("spec needs a title and at least one measure")

    check_fields(spec)
    # fail() exits through SystemExit, so only a finally removes the work folder on a refusal.
    work = tempfile.mkdtemp(prefix="dax-example-")
    try:
        master = fetch_master(a.master, work)
        check(spec, read_model(os.path.join(master, MODEL)))
        inject_measures(os.path.join(master, MODEL), spec)
        page = add_page(os.path.join(master, REPORT), spec)

        os.makedirs(a.out, exist_ok=True)
        zip_path = os.path.join(a.out, f"dax-example-{slug(spec['title'])}.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, _, files in os.walk(master):
                for fn in files:
                    full = os.path.join(root, fn)
                    z.write(full, os.path.relpath(full, work).replace(os.sep, "/"))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print(f"OK: {len(spec['measures'])} measure(s) in _Measures > {FOLDER}, page '{page}' "
          f"opens first.\n    {zip_path}")
    print("NOT checked: the numbers. Nothing evaluated the DAX - the user sees them after Refresh.")


if __name__ == "__main__":
    main()
