#!/usr/bin/env python3
"""Fail if a hand-written document states a count the repository contradicts.

The size of this library is quoted in prose in four files, in two languages, and every
one of those numbers rots the moment the artifact grows. It has already happened: the
notes count sat at 18 in SKILL.md while notes/ held 19, and the design spec promised 61
conceptual pages against a tree of 34.

Nothing here parses meaning. It looks for a number written next to one of the nouns this
library counts -- "479 functions", "30 notas de campo" -- and checks it against what is
on disk. That way a sentence written tomorrow is checked by the fact that it names the
thing, with no list to keep up to date.

What is in scope, and what is not
--------------------------------
Only quantities the repository can count about ITSELF, exactly: skills, cards, concepts,
notes, workflows, lab scenarios, tests, plugins. Each has an entry in
`_counts` and a noun in `NOUNS`, and a claim about one of them must be right.

Deliberately out of scope, and this is the boundary that stops the list growing forever:

  * estimates — "~14k tokens", "376.000 tokens". They are approximations by design.
  * facts about other things — Contoso's 126.524 rows, daxlib's catalogue, the 15 category
    index files upstream publishes, "191 Azure skills" in somebody else's repository.
  * versions and identifiers — Claude Code 2.1.142, issue numbers, release 0.2.0.
  * measurements of one past run — "516 files and zero substantive changes" describes a
    sync that happened, not the tree as it stands.

A number of those kinds is not a promise this repository can keep, so a gate that argued
with it would only teach people to ignore the gate.

The cost of the approach, said out loud
---------------------------------------
Adjacency is all this reads, so it cannot tell a total from a handful: "estas dos
funciones" would be read as a claim that the library holds two, and fail. Nothing in the
repository trips it today, but it is a real constraint on how prose gets written — say
"este par de funciones", or name them. The alternative is a checker that understands
Spanish, and the trade was made knowingly: a gate that occasionally asks for a rewrite is
worth more than one that misses the stale totals it exists for.

Run: python scripts/check_doc_claims.py
"""
import os
import re
import sys
import glob
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Prose only. generated/ states its own counts and is rewritten by the sync every time,
# so a number there cannot drift from the tree it was produced with.
DOCS = ["README.md",
        "INDEX.md",
        "CONTRIBUTING.md",
        os.path.join("skills", "dax-reference", "SKILL.md"),
        os.path.join("lab", "README.md"),
        os.path.join("lab", "contoso", "README.md")]

# Documents that quote counts on purpose and must NOT be checked, because the number they
# carry is a record of what was true then. A decision record explaining that the spec said
# 61 has to keep saying 61. The list is short and each entry is a deliberate exception;
# a test fails if any other hand-written document starts stating counts without a decision.
HISTORICAL = [
    "CHANGELOG.md",                                   # release-please, past releases
    os.path.join("docs", "decisions"),                # what was true when decided
    os.path.join("docs", "superpowers"),              # specs and plans, dated
    "HANDOFF.md",                                     # a session snapshot, true when written
    ".handoffs",                                      # the archived ones, same reason
]

# Where documents about THIS library live: the repo root, docs/, and the two directories
# that describe the reference and its lab. The sibling skills are out of scope on purpose
# — dax-udf-authoring says "1,649 functions" about daxlib's catalogue, which is a true
# sentence about something else, and a checker that argues with it would be wrong.
SCOPE_FILES = [""]                                    # top-level .md, not recursive
SCOPE_TREES = ["docs", os.path.join("skills", "dax-reference"), "lab"]

# Prose about what DAX does is not prose about what this repository holds, and the example
# files are all of the first kind. `floor.md` says "Tres funciones, dos comportamientos"
# about FLOOR, INT and ROUNDDOWN; the `funciones` noun makes this gate read it as a claim
# that the library ships three function cards. That is exactly the cry-wolf failure the
# NOUNS comment above warns about, except here it scales with 479 files still to write.
#
# Excluding them is not leaving them unchecked. The numbers in an example are MEASURED
# RESULTS and they have a stricter gate than this one: check_examples.py rejects any query
# without a result block, and lab/check_lab.py re-runs every single one against the engine
# and fails if a digit moved. This gate checks inventory claims; that one checks the DAX.
OUT_OF_SCOPE = [os.path.join("skills", "dax-reference", "examples")]

# The noun must follow the number directly. Only markdown emphasis and spaces may sit
# between them.
#
# Letting words intervene was tried and read three sentences wrong: "191 Azure skills" is
# a count of somebody else's repository, and the ordered-list markers in "1. **Una skill**"
# and "2. Find the function" are not counts at all. A checker that cries wolf on prose
# gets switched off, so it only speaks when the number and the thing are adjacent.
_GAP = r"[\s\*_`]*"


def _counts(root=ROOT):
    """What the repository at `root` actually holds.

    Takes the root instead of reading the module constant. Counting the real tree while
    checking a fixture's prose compares two different repositories, and every test in the
    suite failed on exactly that.
    """
    ref = os.path.join(root, "skills", "dax-reference")
    gen = os.path.join(ref, "generated")

    def md(path):
        return len([f for f in os.listdir(path) if f.endswith(".md")]) \
            if os.path.isdir(path) else 0

    skills_dir = os.path.join(root, "skills")
    skills = len([d for d in (os.listdir(skills_dir) if os.path.isdir(skills_dir) else [])
                  if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))])

    workflows = len(glob.glob(os.path.join(root, ".github", "workflows", "*.yml")))
    scenarios = len([d for d in glob.glob(os.path.join(root, "lab", "*"))
                     if os.path.isdir(d) and not os.path.basename(d).startswith("__")])

    # Counted as test METHODS, not by running anything: a gate that runs the suites from
    # inside one of them is a loop. Verified equal to what `unittest discover` reports
    # across the three directories, which is what makes the proxy honest.
    tests = 0
    for pattern in ("skills/dax-reference/scripts", "scripts", "evals"):
        for path in glob.glob(os.path.join(root, pattern, "test_*.py")):
            with open(path, encoding="utf-8") as f:
                tests += len(re.findall(r"^\s+def test_", f.read(), re.M))

    plugins = 0
    market = os.path.join(root, ".claude-plugin", "marketplace.json")
    if os.path.isfile(market):
        try:
            with open(market, encoding="utf-8") as f:
                plugins = len(json.load(f).get("plugins") or [])
        except (ValueError, AttributeError):
            plugins = 0

    return {
        "cards": md(os.path.join(gen, "library")),
        "concepts": md(os.path.join(gen, "concepts")),
        "notes": md(os.path.join(ref, "notes")),
        "skills": skills,
        "workflows": workflows,
        "scenarios": scenarios,
        "tests": tests,
        "plugins": plugins,
    }


# One entry per counted thing, both languages. The noun is what makes a sentence
# checkable, so a new claim is covered as soon as it names what it is counting.
NOUNS = {
    "cards": [r"functions?\b", r"function cards?\b", r"function files?\b", r"fichas?\b",
              r"funciones?\b"],
    "concepts": [r"conceptual pages?\b", r"p[áa]ginas? conceptuales?\b", r"concepts?\b",
                 r"conceptos?\b"],
    # The bare forms matter: the first live failure this gate found was "The 18 notes
    # already here" in CONTRIBUTING.md, invisible while only the qualified phrases were
    # listed. They do not double-match "30 field notes", because there the number is not
    # adjacent to the short noun.
    "notes": [r"field notes?\b", r"notas de campo\b", r"notes?\b", r"notas?\b"],
    "skills": [r"skills?\b"],
    "workflows": [r"workflows?\b"],
    "scenarios": [r"lab scenarios?\b", r"escenarios? de laboratorio\b"],
    "tests": [r"tests?\b"],
    "plugins": [r"plugins?\b"],
}


# Numbers written as words, because "The four skills sit flat…" and "Cuatro skills, una
# sola idea" are claims too and rot the same way.
#
# It starts at TWO on purpose. "one"/"uno"/"una" is the indefinite article in Spanish and
# sits next to these nouns constantly without counting anything: "una nota sin demostrar no
# se escribe", "**Una skill = una carpeta**". Those are rules, not counts, and reading them
# as 1 would make the gate cry wolf on correct prose — the failure that gets it switched off.
WORDS = {
    "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8,
    "nueve": 9, "diez": 10, "once": 11, "doce": 12,
}


def _as_int(text):
    """'1.234' and '1,234' are one number, and so is 'four'."""
    word = WORDS.get(text.lower())
    if word is not None:
        return word
    return int(text.replace(".", "").replace(",", ""))


_NUMBER = r"(\d[\d.,]*|\b(?:" + "|".join(sorted(WORDS)) + r")\b)"


def claims_in(text):
    """Every (quantity, stated number, matched phrase) a document asserts."""
    found = []
    for quantity, nouns in NOUNS.items():
        for noun in nouns:
            # A space inside a multi-word noun becomes \s+, because prose wraps. A doc
            # writing "4 escenarios de\n   laboratorio" across a line break was invisible
            # with a literal space, while the same phrase on one line matched.
            pattern = _NUMBER + _GAP + noun.replace(" ", r"\s+")
            for m in re.finditer(pattern, text, re.IGNORECASE):
                found.append((quantity, _as_int(m.group(1)),
                              " ".join(m.group(0).split())))
    return found


_STAMP_IN_PROSE = re.compile(r"MicrosoftDocs/query-docs@([0-9a-fA-F]{7,40})")


def stale_stamps(root=ROOT, docs=None):
    """Prose naming an upstream commit that is not the one generated/ was built from.

    Not a count, but the same failure and the same fix. The sync rewrites every card's
    stamp and touches no prose, so merging a sync pull request leaves any sentence that
    quotes the commit behind — which is what happened the first time one was merged, in
    two files at once.

    Unlike a version number or an issue id, this one IS a fact the repository can read
    about itself: catalog.json says which commit the tree came from.

    Two limits, both accepted rather than hidden:

      * only the full `MicrosoftDocs/query-docs@<sha>` form is read, so a sentence about
        an OLDER commit trips it. The escape hatch is to write the bare sha — "el árbol
        venía de c6a9a72" is prose about history and is left alone.
      * a short sha matching a long one by prefix could in principle name two different
        commits. Seven hex characters is one in 268 million, the same trade already made
        elsewhere in this repository.
    """
    claimed = {}
    for rel in (docs if docs is not None else DOCS):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for said in set(_STAMP_IN_PROSE.findall(f.read())):
                claimed.setdefault(rel.replace(os.sep, "/"), set()).add(said.lower())
    if not claimed:
        return []                          # no prose names a commit: nothing to verify

    # Read only once something claims a commit. Then an unreadable catalog is not "no
    # stale stamps", it is "a sentence names a commit and I cannot check it" — which
    # `validate_skills` would not catch, because it only notices a missing catalog when
    # cards exist beside it.
    catalog = os.path.join(root, "skills", "dax-reference", "generated", "catalog.json")
    try:
        with open(catalog, encoding="utf-8") as f:
            stamped = json.load(f)["source"].split("@")[-1].lower()
    except (OSError, ValueError, KeyError, AttributeError, TypeError) as e:
        return [f"{sorted(claimed)[0]} names an upstream commit, but "
                f"generated/catalog.json does not say which one the tree came from "
                f"({type(e).__name__}), so it cannot be checked"]

    stale = []
    for rel, saids in claimed.items():
        for said in saids:
            if not (said.startswith(stamped) or stamped.startswith(said)):
                stale.append(f"{rel}: names query-docs@{said}, "
                             f"but generated/ was built from @{stamped}")
    return sorted(stale)


def unlisted_documents(root=ROOT, docs=None):
    """Hand-written markdown that makes a claim and is neither checked nor exempt.

    DOCS is a list, and a list nobody rechecks is how the old function ceiling rotted. This
    is what rechecks it: add a document with counts in it and something has to be decided —
    check it, or say in HISTORICAL why its numbers are allowed to age.
    """
    skip = {".git", "__pycache__", ".venv", "node_modules", "generated"}
    listed = {os.path.normpath(d) for d in (DOCS if docs is None else docs)}
    exempt = [os.path.normpath(h) for h in HISTORICAL + OUT_OF_SCOPE]

    candidates = []
    for rel_dir in SCOPE_FILES:
        base = os.path.join(root, rel_dir) if rel_dir else root
        if os.path.isdir(base):
            candidates += [os.path.join(base, n) for n in os.listdir(base)
                           if n.endswith(".md")]
    for rel_dir in SCOPE_TREES:
        base = os.path.join(root, rel_dir)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in skip]
            candidates += [os.path.join(dirpath, n) for n in filenames if n.endswith(".md")]

    stray = []
    for path in candidates:
        rel = os.path.normpath(os.path.relpath(path, root))
        if rel in listed or any(rel == e or rel.startswith(e + os.sep) for e in exempt):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        # A stamp counts as a claim too. A document naming the upstream commit and no
        # numbers was invisible to both halves of this gate: no count for the list
        # check, and not in DOCS for the stamp check.
        if claims_in(text) or _STAMP_IN_PROSE.search(text):
            stray.append(rel.replace(os.sep, "/"))
    return sorted(set(stray))


def check(root=ROOT, docs=None):
    """Every stated count that disagrees with the tree, as a list of strings."""
    real = _counts(root)
    if not any(real.values()):
        return ["nothing was counted, so no claim could be wrong. Is generated/ built?"]

    errors = []
    stated_anything = False
    for rel in (docs if docs is not None else DOCS):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            errors.append(f"{rel} is missing, and it is one of the documents checked")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        found = claims_in(text)
        stated_anything = stated_anything or bool(found)
        for quantity, stated, phrase in found:
            if stated != real[quantity]:
                errors.append(f"{rel.replace(os.sep, '/')}: says {phrase!r} but there "
                              f"are {real[quantity]} {quantity}")

    if docs is None and not stated_anything and not errors:
        # The tree was counted and the repository's own documents were read, and between
        # them not one sentence stated a size. That is either prose that lost its numbers
        # or patterns that stopped matching, and both look identical from here: a green
        # run that compared nothing.
        #
        # Only when the caller did not name the documents. A caller that passes its own
        # list may legitimately hand over prose with no counts in it, and refusing that
        # would make the function unusable for anything but the repository itself.
        errors.append("none of the checked documents states a count, so nothing was "
                      "compared. Either the prose lost its numbers or NOUNS stopped "
                      "matching them.")

    errors += stale_stamps(root, docs)

    for stray in unlisted_documents(root, docs):
        errors.append(f"{stray} states a count or an upstream commit, and is neither in "
                      f"DOCS nor in HISTORICAL. Decide which: checked, or allowed to age "
                      f"on the record.")
    return errors


def main(root=ROOT):
    errors = check(root)
    if errors:
        print("DOC CLAIM CHECK FAILED:")
        for e in errors:
            print(f"  - {e}")
        print("\nEither the sentence is stale or the tree is. Fix whichever is wrong; "
              "a number in prose is a promise like any other.")
        return 1
    real = _counts(root)
    print("OK: prose agrees with the tree ("
          + ", ".join(f"{v} {k}" for k, v in sorted(real.items())) + ").")
    return 0


if __name__ == "__main__":
    sys.exit(main())
