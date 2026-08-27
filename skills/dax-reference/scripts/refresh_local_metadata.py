#!/usr/bin/env python3
"""Rewrite the parts of `generated/` that come from THIS repository, not from Microsoft.

A generated card carries two kinds of field. Most of them are upstream's: the name, the
signature, the remarks. Two are not — `notes:` and `examples:` are counted from `notes/`
and `examples/`, directories the sync only ever reads. So is the runnable-examples block
the card carries, and the `★` / `▶` flags in `catalog.md`.

The sync writes both kinds in one pass, which was fine while it could run. It cannot: the
upstream returned 404 and `generated/` is frozen at its stamp on purpose — see
`docs/decisions/2026-08-27-generated-is-frozen-at-323524c.md`. The local half then had no
way to be brought up to date, and it rotted exactly where nothing was watching: 99
functions had example files and 54 cards admitted it. The other 45 were unreachable by the
route `SKILL.md` documents, which reads `examples: N` off the card.

This script is the local half on its own. It touches no Microsoft prose — it rewrites two
frontmatter fields, the block those fields point at, and the two indexes. Everything it
needs, it imports from the sync rather than restating: one definition of where the block
goes and what the catalogue looks like, so the two writers cannot drift apart.

    python skills/dax-reference/scripts/refresh_local_metadata.py            # rewrite
    python skills/dax-reference/scripts/refresh_local_metadata.py --check    # gate mode

`--check` writes nothing and exits 1 if a rewrite would change anything. That is a stronger
statement than the three hand-written comparisons it replaces, because it covers whatever
the sync derives locally, including the parts nobody thought to assert.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sync_query_docs as sync                                    # noqa: E402

REF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED = os.path.join(REF, "generated")

# The heading of the block this script owns, and the upstream heading it sits above. Both
# come from the sync so a rename there cannot leave this script cutting at the old text.
OURS_HEADING = sync._examples_section("x", ("c", 1)).splitlines()[0]
MS_HEADING = sync._MS_EXAMPLES_NOTICE.splitlines()[0]

# From the heading to the next `## ` or the end. `re.S` so `.` crosses lines, `re.M` so the
# lookahead anchors a real heading rather than a `## ` inside a fenced block — there are
# none today, and a card that grows one should not lose its examples to this regex.
_OURS_RE = re.compile(r"^" + re.escape(OURS_HEADING) + r"\n.*?(?=^## |\Z)", re.S | re.M)
_FM_RE = re.compile(r"\A---\n(.*?\n)---\n", re.S)


def _set_field(frontmatter, key, value):
    """Replace one frontmatter line, leaving every other byte alone.

    Re-serialising the whole block would be the obvious move and the wrong one: it would
    make this script a second opinion on formatting, and the first difference between the
    two writers would show up as a diff on all 479 cards with no way to tell which half
    meant it.

    A lambda, not a replacement string: `re.sub` reads backslashes in the replacement, and
    a summary containing one would come out mangled.
    """
    line = f"{key}: {value}"
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.M)
    if pattern.search(frontmatter):
        return pattern.sub(lambda _: line, frontmatter, count=1)
    return frontmatter.rstrip("\n") + "\n" + line + "\n"


def refresh_card(text, stem, has_notes, entry):
    """The card as the sync would write it today, given this repo's notes/ and examples/.

    `entry` is `(category, count)` or None. Pure: takes text, returns text, so a test can
    state the contract on a card literal instead of on a tree.
    """
    m = _FM_RE.match(text)
    if not m:
        raise ValueError(f"{stem}: no frontmatter")
    frontmatter, body = m.group(1), text[m.end():]

    frontmatter = _set_field(frontmatter, "notes", "true" if has_notes else "false")
    frontmatter = _set_field(frontmatter, "examples", entry[1] if entry else 0)

    # Always strip, then re-place. Editing in place would need a third branch for "the
    # block exists but belongs somewhere else", and placement is the sync's decision.
    body = _OURS_RE.sub("", body)

    if entry:
        ours = sync._examples_section(stem, entry)
        at = body.find(MS_HEADING)
        if at != -1:
            # Above Microsoft's own examples, on purpose: an agent that stops reading
            # early has to meet the measured ones first.
            body = body[:at] + ours + "\n" + body[at:]
        else:
            body = body.rstrip() + "\n\n" + ours

    return f"---\n{frontmatter}---\n{body.lstrip()}"


def _reasons(stem, before, after, has_notes, entry):
    """Why this card changed, in the words of the thing that is wrong.

    A diff would be honest and useless at 479 files. These read like the finding: a file
    exists and nothing routes to it, a card promises a count the file cannot cover.
    """
    out = []
    old = _FM_RE.match(before).group(1)
    old_notes = re.search(r"^notes:\s*(\S+)$", old, re.M)
    old_ex = re.search(r"^examples:\s*(\S+)$", old, re.M)
    stated_notes = (old_notes.group(1) == "true") if old_notes else False
    stated_ex = int(old_ex.group(1)) if old_ex and old_ex.group(1).isdigit() else 0
    count = entry[1] if entry else 0

    if has_notes and not stated_notes:
        out.append(f"{stem}: notes/{stem}.md exists and the card says notes: false, "
                   f"so nothing routes to it")
    elif stated_notes and not has_notes:
        out.append(f"{stem}: the card claims a note and notes/{stem}.md is not there")
    if count != stated_ex:
        if stated_ex == 0:
            out.append(f"{stem}: examples/{entry[0]}/{stem}.md holds {count} queries and "
                       f"the card says examples: 0 — unreachable by SKILL.md step 4")
        elif count == 0:
            out.append(f"{stem}: the card promises {stated_ex} examples and there is no "
                       f"examples file")
        else:
            out.append(f"{stem}: the card promises {stated_ex} examples, the file holds "
                       f"{count}")
    if not out:
        out.append(f"{stem}: the runnable-examples block does not match the file")
    return out


def refresh(root=GENERATED, ref=REF, check=False):
    """Returns (changed_paths, reasons). Writes nothing when `check`."""
    notes = sync._notes_stems(ref)
    examples = sync._examples_index(ref)

    library = os.path.join(root, "library")
    changed, reasons = [], []

    for name in sorted(os.listdir(library)):
        if not name.endswith(".md"):
            continue
        stem = name[:-3]
        path = os.path.join(library, name)
        with open(path, encoding="utf-8") as f:
            before = f.read()
        after = refresh_card(before, stem, stem in notes, examples.get(stem))
        if after == before:
            continue
        changed.append(os.path.join("library", name))
        reasons += _reasons(stem, before, after, stem in notes, examples.get(stem))
        if not check:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(after)

    # The two indexes are derived from the same two directories, so they rot together and
    # are repaired together. catalog.json first: catalog.md is rendered from it.
    cat_path = os.path.join(root, "catalog.json")
    with open(cat_path, encoding="utf-8") as f:
        before_json = f.read()
    catalog = json.loads(before_json)
    for fn in catalog.get("functions", []):
        stem = fn.get("file") or str(fn.get("name", "")).lower()
        entry = examples.get(stem)
        fn["notes"] = stem in notes
        fn["examples"] = entry[1] if entry else 0
    # Byte for byte how the sync writes it. Comparing parsed objects instead would let this
    # script quietly reformat the file the first time the two dumps disagreed.
    after_json = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if after_json != before_json:
        changed.append("catalog.json")
        reasons.append("catalog.json: the notes/examples flags disagree with the tree")
        if not check:
            with open(cat_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(after_json)

    md_path = os.path.join(root, "catalog.md")
    with open(md_path, encoding="utf-8") as f:
        before_md = f.read()
    after_md = sync._catalog_md(catalog["functions"], catalog["source"],
                                catalog.get("sourceCommitDate", ""))
    if after_md != before_md:
        changed.append("catalog.md")
        reasons.append("catalog.md: the flag column disagrees with the tree")
        if not check:
            with open(md_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(after_md)

    return changed, reasons


def main(argv):
    check = "--check" in argv
    changed, reasons = refresh(check=check)
    if not changed:
        print("OK: generated/ agrees with notes/ and examples/ (nothing to rewrite).")
        return 0
    if check:
        print(f"ERROR: {len(changed)} file(s) in generated/ disagree with notes/ and "
              f"examples/. Run: python skills/dax-reference/scripts/"
              f"refresh_local_metadata.py")
        for r in reasons[:40]:
            print(f"  - {r}")
        if len(reasons) > 40:
            print(f"  ... and {len(reasons) - 40} more")
        return 1
    print(f"rewrote {len(changed)} file(s) in generated/ from notes/ and examples/.")
    for r in reasons[:20]:
        print(f"  - {r}")
    if len(reasons) > 20:
        print(f"  ... and {len(reasons) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
