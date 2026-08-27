"""Render the README's two SVG assets from the tree.

    python scripts/render_readme_assets.py            # write docs/assets/*.svg
    python scripts/render_readme_assets.py --check    # fail if they are stale

Two pieces, each in a light and a dark variant so the README can pick with
`<picture media="(prefers-color-scheme: dark)">`:

    banner-{light,dark}.svg     the header, with the four headline counts
    coverage-{light,dark}.svg   one cell per function, grouped by category

Both are generated, never hand-edited, and `check_readme_assets.py` fails the
build when the tree moves and they do not.

Two rules this file exists to keep, both learned the hard way:

1.  Coverage is counted from the FILES, not from `catalog.json`. That field is
    not a reliable mirror of what is on disk, so drawing the map from it would
    reproduce the very gap the map is supposed to expose. Only the function
    name and its category come from the catalogue.

2.  Text is XML and is placed by anchor, never by arithmetic. An unescaped `&`
    ("Math & trig") makes the whole document unparseable, and GitHub renders
    Linux fonts, so any layout that centres text by estimating character widths
    drifts there. Every string goes through `esc()`; every label is centred
    with `text-anchor`.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REF = ROOT / "skills" / "dax-reference"
OUT = ROOT / "docs" / "assets"

ACCENT = "#116B62"      # a function with a hand-written field note
ACCENT_D = "#72EBC4"    # ...on a dark ground
ACCENT2 = "#3FB8A6"     # a function with runnable examples
FONT = "ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

THEMES = {
    "light": dict(page="#F4F9F8", card="#FFFFFF", border="#CFE3DD", ink="#0B1A17",
                  muted="#44544F", empty="#D5E4DF", note=ACCENT, ex=ACCENT2, rule=ACCENT),
    # `ex` is NOT ACCENT2 here. On a dark ground #3FB8A6 sits too close to the
    # bright #72EBC4 and the two states stop being separable -- the single note in
    # "Math & trig" vanished among its 48 examples. Dark needs the wider spread.
    "dark": dict(page="#08110F", card="#0F1B18", border="#263B35", ink="#E4F0EC",
                 muted="#93A8A2", empty="#2B3D38", note=ACCENT_D, ex="#2C7D71",
                 rule=ACCENT_D),
}

LABEL = {
    "info": "INFO.*", "financial": "Financial", "math-and-trig": "Math & trig",
    "statistical": "Statistical", "information": "Information",
    "time-intelligence": "Time intel.", "filter": "Filter", "table-manipulation": "Table",
    "date-and-time": "Date & time", "aggregation": "Aggregation", "text": "Text",
    "uncategorised": "Uncategorised", "logical": "Logical", "other": "Other",
    "parent-and-child": "Parent-child", "relationship": "Relationship",
}


def esc(value: object) -> str:
    """SVG is XML: one raw `&` makes the whole document unparseable."""
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def read_tree() -> dict:
    """Names and categories from the catalogue; coverage from the files."""
    catalogue = json.loads((REF / "generated" / "catalog.json").read_text(encoding="utf-8"))
    functions = catalogue["functions"]

    notes = {p.stem.upper() for p in (REF / "notes").glob("*.md")}

    examples: set[str] = set()
    for path in (REF / "examples").rglob("*.md"):
        match = re.search(r"^function:\s*(.+)$", path.read_text(encoding="utf-8"), re.M)
        if match:
            examples.add(match.group(1).strip().strip("\"'").upper())

    grouped = collections.defaultdict(list)
    for function in functions:
        name = function["name"].upper()
        grouped[function.get("primaryCategory") or "uncategorised"].append(
            2 if name in notes else (1 if name in examples else 0))

    groups = [{"label": LABEL.get(key, key), "cells": sorted(states, reverse=True),
               "n": len(states)}
              for key, states in sorted(grouped.items(), key=lambda kv: -len(kv[1]))]

    return {
        "groups": groups,
        "total": len(functions),
        "notes": sum(1 for f in functions if f["name"].upper() in notes),
        "examples": len(examples),
        "blank": [g for g in groups if not any(g["cells"])],
    }


def banner(data: dict, theme: str) -> str:
    t = THEMES[theme]
    w, h = 1200, 290
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
           f'height="{h}" font-family="{FONT}">',
           f'<rect width="{w}" height="{h}" rx="16" fill="{t["page"]}" stroke="{t["border"]}"/>',
           f'<rect x="16" y="0" width="{w-32}" height="6" rx="3" fill="{t["rule"]}"/>',
           f'<text x="60" y="106" font-size="54" font-weight="800" fill="{t["ink"]}" '
           f'font-family="{MONO}">dax-for-agents</text>',
           f'<text x="60" y="152" font-size="25" fill="{t["muted"]}">'
           f'The DAX language reference your agent can actually consult.</text>']

    pills = [(data["total"], "function cards"), (data["notes"], "measured field notes"),
             (data["examples"], "with runnable examples"), (4, "labs you can open")]
    x = 60.0
    for number, caption in pills:
        # The pill is sized from the text it holds, but the text inside is centred on
        # the pill rather than laid out left-to-right by estimated glyph widths.
        width = 46 + len(str(number)) * 20 + len(caption) * 8.8
        out.append(f'<rect x="{x:.0f}" y="192" width="{width:.0f}" height="54" rx="27" '
                   f'fill="{t["card"]}" stroke="{t["border"]}"/>')
        out.append(f'<text x="{x + width/2:.0f}" y="227" text-anchor="middle" font-size="20" '
                   f'fill="{t["muted"]}"><tspan font-size="26" font-weight="800" '
                   f'fill="{t["note"]}">{number}</tspan> {esc(caption)}</text>')
        x += width + 14
    out.append("</svg>")
    return "".join(out)


def coverage(data: dict, theme: str) -> str:
    t = THEMES[theme]
    cell, gap, cols, pad, title_h = 13, 4, 9, 10, 22
    box_w = cols * cell + (cols - 1) * gap + pad * 2
    per_row, gx, gy, w, top = 6, 12, 12, 1200, 78

    def box_h(n: int) -> int:
        rows = math.ceil(n / cols)
        return pad + title_h + rows * cell + (rows - 1) * gap + pad

    rows = [data["groups"][i:i + per_row] for i in range(0, len(data["groups"]), per_row)]
    row_h = [max(box_h(g["n"]) for g in row) for row in rows]
    h = top + sum(row_h) + gy * (len(rows) - 1) + 84
    blank_n = sum(g["n"] for g in data["blank"])

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
           f'height="{h}" font-family="{FONT}">',
           f'<rect width="{w}" height="{h}" rx="14" fill="{t["page"]}" stroke="{t["border"]}"/>',
           f'<text x="{w/2}" y="42" text-anchor="middle" font-size="23" font-weight="700" '
           f'fill="{t["ink"]}">Coverage map — {data["total"]} DAX functions</text>',
           f'<text x="{w/2}" y="65" text-anchor="middle" font-size="16" fill="{t["muted"]}">'
           f'{data["notes"]} field notes · {data["examples"]} with runnable examples · '
           f'{blank_n} functions across {len(data["blank"])} categories with neither</text>']

    y = float(top)
    for row, height in zip(rows, row_h):
        x = (w - (len(row) * box_w + gx * (len(row) - 1))) / 2
        for group in row:
            out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{box_w}" '
                       f'height="{box_h(group["n"])}" rx="9" fill="{t["card"]}" '
                       f'stroke="{t["border"]}"/>')
            out.append(f'<text x="{x + box_w/2:.0f}" y="{y+pad+12:.0f}" text-anchor="middle" '
                       f'font-size="13" font-weight="700" fill="{t["ink"]}">'
                       f'{esc(group["label"])} ({group["n"]})</text>')
            for i, state in enumerate(group["cells"]):
                cx = x + pad + (i % cols) * (cell + gap)
                cy = y + pad + title_h + (i // cols) * (cell + gap)
                if state:
                    fill = t["note"] if state == 2 else t["ex"]
                    out.append(f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{cell}" height="{cell}" '
                               f'rx="3" fill="{fill}"/>')
                else:
                    out.append(f'<rect x="{cx+0.75:.0f}" y="{cy+0.75:.0f}" width="{cell-1.5}" '
                               f'height="{cell-1.5}" rx="2.5" fill="none" stroke="{t["empty"]}" '
                               f'stroke-width="1.5"/>')
            x += box_w + gx
        y += height + gy

    legend = ((t["note"], f'{data["notes"]} field note', True),
              (t["ex"], f'{data["examples"]} runnable examples', True),
              (t["empty"], "Microsoft's card only", False))
    for i, (colour, caption, filled) in enumerate(legend):
        cx = w * (i + 1) / 4
        swatch = (f'fill="{colour}"/>' if filled
                  else f'fill="none" stroke="{colour}" stroke-width="1.6"/>')
        out.append(f'<rect x="{cx-100:.0f}" y="{y+16:.0f}" width="13" height="13" rx="3" ' + swatch)
        out.append(f'<text x="{cx-80:.0f}" y="{y+27:.0f}" font-size="15" '
                   f'fill="{t["muted"]}">{esc(caption)}</text>')

    out.append(f'<text x="{w/2}" y="{y+56:.0f}" text-anchor="middle" font-size="13" '
               f'fill="{t["muted"]}">Counted from the files, not from catalog.json — '
               f'regenerated and checked by CI.</text></svg>')
    return "".join(out)


def render_all() -> dict[pathlib.Path, str]:
    data = read_tree()
    return {OUT / f"{name}-{theme}.svg": fn(data, theme)
            for name, fn in (("banner", banner), ("coverage", coverage))
            for theme in THEMES}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if any asset is stale")
    args = parser.parse_args()

    rendered = render_all()

    if args.check:
        stale = [p for p, content in rendered.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != content]
        if stale:
            print("The README assets no longer match the tree:")
            for path in stale:
                print(f"  {path.relative_to(ROOT).as_posix()}")
            print("\nRegenerate them with:  python scripts/render_readme_assets.py")
            return 1
        print(f"OK: {len(rendered)} README asset(s) match the tree.")
        return 0

    OUT.mkdir(parents=True, exist_ok=True)
    for path, content in rendered.items():
        path.write_text(content, encoding="utf-8")
        print(f"{path.relative_to(ROOT).as_posix():<34} {len(content.encode('utf-8')):>7} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
