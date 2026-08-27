#!/usr/bin/env python3
"""CI validation for the dax-for-agents repo.

Checks, for every skill folder (a dir under `skills/` containing SKILL.md):
  1. Frontmatter: name == folder, name is kebab-case, description starts with "Use when".
  2. The skill is referenced in INDEX.md.
Then, repo-wide:
  3. Every Python script under skills/*/scripts/ and scripts/ compiles.
  4. dax-reference integrity: catalog rows <-> library cards <-> notes all line up.
     Tolerates the pre-sync state where the library is still empty.

Exit non-zero (with a report) on any failure. Run: python scripts/validate_skills.py
"""
import os
import re
import sys
import glob
import json
import subprocess

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed (pip install pyyaml)")
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors = []


def frontmatter(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return {"__error__": str(e)}


# ---- 1 & 2: per-skill frontmatter + INDEX coverage ----
SKILLS = os.path.join(ROOT, "skills")
skill_dirs = sorted(
    d for d in (os.listdir(SKILLS) if os.path.isdir(SKILLS) else [])
    if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md"))
)
if not skill_dirs:
    errors.append("no skill folders found under skills/ (none contain SKILL.md)")

index_path = os.path.join(ROOT, "INDEX.md")
index_txt = open(index_path, encoding="utf-8").read() if os.path.exists(index_path) else ""
if not index_txt:
    errors.append("INDEX.md missing or empty")

for d in skill_dirs:
    fm = frontmatter(os.path.join(SKILLS, d, "SKILL.md"))
    if fm is None:
        errors.append(f"{d}: missing YAML frontmatter")
        continue
    if "__error__" in fm:
        errors.append(f"{d}: invalid YAML frontmatter ({fm['__error__']})")
        continue
    name = fm.get("name")
    desc = (fm.get("description") or "").strip()
    if name != d:
        errors.append(f"{d}: frontmatter name '{name}' != folder name")
    if not name or not KEBAB.match(str(name)):
        errors.append(f"{d}: name '{name}' is not kebab-case")
    if not desc.lower().startswith("use when"):
        errors.append(f"{d}: description must start with 'Use when' (got: {desc[:40]!r})")
    if d not in index_txt:
        errors.append(f"{d}: not referenced in INDEX.md")

# ---- 3: every Python script compiles ----
py_scripts = glob.glob(os.path.join(ROOT, "skills", "*", "scripts", "*.py")) + \
    glob.glob(os.path.join(ROOT, "scripts", "*.py")) + \
    glob.glob(os.path.join(ROOT, "lab", "*.py"))
for py in sorted(py_scripts):
    r = subprocess.run([sys.executable, "-m", "py_compile", py],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        errors.append(f"py_compile failed: {os.path.relpath(py, ROOT)}: {r.stderr.strip()}")

# ---- 4: dax-reference integrity ----
REF = os.path.join(SKILLS, "dax-reference")
GEN = os.path.join(REF, "generated")
cat_json = os.path.join(GEN, "catalog.json")
lib_dir = os.path.join(GEN, "library")
notes_dir = os.path.join(REF, "notes")

# The sync installs generated/ and nothing else. A copy left at the old top-level paths is
# never refreshed again, so an agent following a stale SKILL.md would read a library frozen
# at whatever commit it was abandoned on.
for stale in ("library", "concepts", "catalog.json", "catalog.md"):
    if os.path.exists(os.path.join(REF, stale)):
        errors.append(f"dax-reference/{stale} is the pre-generated/ layout — the sync no "
                      f"longer writes it, so it can only go stale. Move it into "
                      f"dax-reference/generated/ or delete it.")


def stems(d):
    if not os.path.isdir(d):
        return set()
    return {os.path.splitext(f)[0] for f in os.listdir(d) if f.endswith(".md")}


cards = stems(lib_dir)
notes = stems(notes_dir)
concept_cards = stems(os.path.join(GEN, "concepts"))

# A note without its card is always an error — the sync would leave it orphaned.
for orphan in sorted(notes - cards):
    if cards:
        errors.append(f"dax-reference/notes/{orphan}.md has no generated/library/{orphan}.md")

# Notes are hand-written, so the sync's broken-link gate never sees them: it checks what it
# generated. A note that points at another note is exactly as broken as a card that does.
_NOTE_LINK = re.compile(r"\]\((?!https?://)(?!#)([^)\s]+)\)")
for note in sorted(glob.glob(os.path.join(notes_dir, "*.md"))):
    with open(note, encoding="utf-8") as f:
        body = f.read()
    for target in _NOTE_LINK.findall(body):
        resolved = os.path.normpath(os.path.join(notes_dir, target.split("#")[0]))
        if not os.path.exists(resolved):
            errors.append(f"dax-reference/notes/{os.path.basename(note)} links to "
                          f"'{target}', which does not exist")

if os.path.exists(cat_json):
    try:
        cat = json.load(open(cat_json, encoding="utf-8"))
        rows = {f.get("file") or str(f.get("name", "")).lower()
                for f in cat.get("functions", [])}
        for missing in sorted(rows - cards):
            errors.append(f"catalog lists '{missing}' but generated/library/{missing}.md is missing")
        for extra in sorted(cards - rows):
            errors.append(f"generated/library/{extra}.md exists but is not in the catalog")
        flagged = {f.get("file") or str(f.get("name", "")).lower()
                   for f in cat.get("functions", []) if f.get("notes")}
        for bad in sorted(flagged - notes):
            errors.append(f"catalog flags '{bad}' as having notes but notes/{bad}.md is missing")

        # The OTHER direction, which nothing checked until it had already cost something.
        #
        # The line above catches a flag with no file — a promise the tree cannot keep. The
        # reverse is a file with no flag, and it is worse, because it fails silently: the
        # work exists, nothing is broken, and no one can find it. SKILL.md routes on this
        # flag ("if the card's frontmatter says examples: N greater than zero, the card
        # links to examples/..."), so an unflagged file is work an agent has no reason to
        # open.
        #
        # Both had already rotted when this was written. examples/ held 99 functions and
        # the catalog marked 54 — 45 invisible, including ABS with three measured queries.
        # notes/ held 31 and the catalog marked 30: WINDOW, one of the functions the
        # window-functions skill exists for, carried a hand-written note behind a card
        # that said notes: false.
        for lost in sorted(notes - flagged):
            errors.append(f"notes/{lost}.md exists but the catalog does not flag '{lost}' "
                          f"as having notes, so nothing routes to it — re-run the sync")

        # Examples are the same contract, plus a count. The count matters on its own: a
        # card promising three when the file holds two sends an agent looking for one that
        # is not there.
        example_counts = {}
        examples_dir = os.path.join(REF, "examples")
        if os.path.isdir(examples_dir):
            for category in sorted(os.listdir(examples_dir)):
                cat_dir = os.path.join(examples_dir, category)
                if not os.path.isdir(cat_dir):
                    continue
                for name in sorted(os.listdir(cat_dir)):
                    if name.endswith(".md"):
                        with open(os.path.join(cat_dir, name), encoding="utf-8") as f:
                            example_counts[os.path.splitext(name)[0]] = f.read().count("```dax")

        stated = {f.get("file") or str(f.get("name", "")).lower(): (f.get("examples") or 0)
                  for f in cat.get("functions", [])}
        for lost in sorted(set(example_counts) - {s for s, n in stated.items() if n}):
            errors.append(f"examples/{lost}.md exists but the catalog says '{lost}' has no "
                          f"examples, so nothing routes to it — re-run the sync")
        for bad in sorted({s for s, n in stated.items() if n} - set(example_counts)):
            errors.append(f"catalog says '{bad}' has examples but no examples/**/{bad}.md "
                          f"is there")
        for stem, real in sorted(example_counts.items()):
            if stem in stated and stated[stem] and stated[stem] != real:
                errors.append(f"catalog says '{stem}' has {stated[stem]} example(s) but "
                              f"examples/**/{stem}.md holds {real}")
        # Same invariant for the conceptual pages: an index row with no page behind it
        # sends an agent to a file that is not there, which is worse than no row at all.
        concept_rows = {c.get("file") for c in cat.get("concepts", [])}
        for missing in sorted(concept_rows - concept_cards):
            errors.append(f"catalog lists concept '{missing}' but "
                          f"generated/concepts/{missing}.md is missing")
        for extra in sorted(concept_cards - concept_rows):
            errors.append(f"generated/concepts/{extra}.md exists but is not in the catalog")
    except (json.JSONDecodeError, AttributeError, TypeError) as e:
        errors.append(f"dax-reference/generated/catalog.json is not readable: {e}")
elif cards:
    errors.append("generated/library/ has cards but generated/catalog.json is missing — run the sync")
# else: pre-sync state, nothing generated yet. Not an error.

# ---- report ----
if errors:
    print("SKILL VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
state = (f"{len(cards)} cards, {len(concept_cards)} concepts, {len(notes)} notes"
         if cards else "library not built yet")
print(f"OK: {len(skill_dirs)} skill(s) validated, {len(py_scripts)} script(s) compiled, "
      f"dax-reference: {state}.")
