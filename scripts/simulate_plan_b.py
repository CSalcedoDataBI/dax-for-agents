"""Plan B simulator: how many files would the plugin directory see after bundling the cards?

Read-only and stdlib-only. Computes every number in
docs/proposals/2026-10-25-plan-b-under-512-files.md from `git ls-files`, the PR #26 branch tree
(when it is fetched) and skills/dax-reference/generated/catalog.json. Bundles are built in
memory only, so their sizes and line ranges are exact; nothing is written to disk.

    python -X utf8 scripts/simulate_plan_b.py
    python -X utf8 scripts/simulate_plan_b.py --sub-ref origin/refactor/plugin-subfolder
"""
import argparse
import collections
import fnmatch
import json
import os
import re
import subprocess
import sys

LIMIT_FILES = 512
LIMIT_BYTES = 256 * 1024
TARGET = int(LIMIT_BYTES * 0.9)          # bundles aim at 90% of the directory's 256 KiB
REF = "skills/dax-reference"
GEN = f"{REF}/generated"

# --- what an installed plugin reads or runs -----------------------------------------------
# First match wins. "runtime" = a SKILL.md tells the agent to read/run it, or the plugin
# loader reads it. "keep" = no agent reads it, but it must stay on the default branch for the
# listing, the license, CI or release tooling. "dev" = maintainer, CI input, tests, sync.
RULES = [
    (".claude-plugin/*", "runtime", "plugin loader; dax-feedback reads plugin.json version"),
    ("skills/*/SKILL.md", "runtime", "skill entry point"),
    ("skills/*/NOTICE", "runtime", "attribution, linked from SKILL.md (CC BY 4.0)"),
    ("skills/dax-lib/catalog.*", "runtime", "dax-lib SKILL.md reads catalog.md/json"),
    ("skills/dax-lib/scripts/refresh-daxlib.ps1", "runtime", "named by dax-lib + dax-lib-install"),
    (f"{GEN}/*", "runtime", "catalog.md, concepts.md, cards (catalog.json: scripts)"),
    (f"{REF}/notes/*", "runtime", "read when the catalog row is flagged ★"),
    (f"{REF}/examples/*/*", "runtime", "read when the catalog row is flagged ▶"),
    (f"{REF}/scripts/inject_example.py", "runtime", "the agent runs it (SKILL.md)"),
    (f"{REF}/examples/README.md", "dev", "index for humans; no SKILL.md points at it"),
    (f"{REF}/scripts/test_*", "dev", "unit tests"),
    (f"{REF}/scripts/*", "dev", "sync/fetch/refresh tooling + its README (maintainer)"),
    (f"{REF}/overrides.json", "dev", "generator input"),
    ("LICENSE", "keep", "license"),
    ("README.md", "keep", "listing / homepage"),
    ("PRIVACY.md", "keep", "privacyPolicyUrl = blob/main/PRIVACY.md"),
    ("CHANGELOG.md", "keep", "release-please writes it on main"),
    (".release-please-manifest.json", "keep", "release-please state"),
    ("release-please-config.json", "keep", "release-please config"),
    (".gitattributes", "keep", "eol rules"),
    (".gitignore", "keep", "ignore rules"),
    (".github/*", "keep", "CI must live on the default branch"),
    ("*", "dev", "docs, lab, evals, gates, contributor notes"),
]

# B-root: what leaves the default branch. (glob, destination, why it is safe)
B_ROOT_MOVES = [
    ("docs/examples-es/*", "tag archive/examples-es-2026-08-25",
     "frozen Spanish snapshot; nothing runs it; check_doc_claims only skips it"),
]
HEAVY_MOVES = B_ROOT_MOVES + [
    (g, "sibling repo / dev-assets", "rejected")
    for g in ("lab/*", "docs/*", "evals/*", "scripts/*", ".agentic-board/*", ".claude/*",
              "CLAUDE.md", "CONTRIBUTING.md", "FICHA.md", "INDEX.md")]


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True,
                          encoding="utf-8", check=True).stdout


def classify(path):
    for pat, cls, why in RULES:
        if fnmatch.fnmatchcase(path, pat):
            return cls, why
    raise AssertionError(path)


def top(path):
    return path.split("/")[0] if "/" in path else "(root files)"


def read(root, path):
    with open(os.path.join(root, path), encoding="utf-8", newline="") as f:
        return f.read()


# --- bundling, in memory ------------------------------------------------------------------
# Each card sits verbatim between two markers, so a bundle splits back into the exact bytes of
# the card it came from (roundtrip() proves it on the real tree). The only edit is a relative
# link to another card, './abs.md' -> './functions-math-and-trig.md#abs', reversed on split.
# Bundles go in a NEW directory (generated/bundles/), so a stale 'library/<fn>.md' path fails
# loudly instead of opening a category file that happens to share a function's name (FILTER).
BEGIN = '<a id="{0}"></a>\n<!-- card: {0} -->\n'
# Six cards have no final newline. The bundle adds one before END and says so in the marker,
# so the split drops exactly that newline and the round trip compares bytes, not rstrip().
BEGIN_NONL = '<a id="{0}"></a>\n<!-- card: {0} no-final-newline -->\n'
END = "<!-- /card -->\n\n"
# A section anchor ('./if.md#examples') cannot stay an anchor: every card in a bundle has its
# own "Examples". It rides along as the link title, and the split turns it back.
LINK = re.compile(r"\]\(((?:\.\./)*\.?\.?/?(?:library/|concepts/)?)([a-z0-9][a-z0-9.-]*)\.md(#[^)\s]*)?\)")
BACK = re.compile(r'\]\(\./([a-z0-9-]+)\.md#([a-z0-9][a-z0-9.-]*)(?: "section:([^"]+)")?\)')


def rewrite(text, bundle_of, here):
    def sub(m):
        pre, stem, anchor = m.groups()
        d = "library" if "library/" in pre else "concepts" if "concepts/" in pre else here
        b = bundle_of.get((d, stem))
        if b is None:
            return m.group(0)
        return f"](./{b}.md#{stem}" + (f' "section:{anchor[1:]}"' if anchor else "") + ")"
    return LINK.sub(sub, text)


def unrewrite(text, dir_of, here):
    def sub(m):
        b, stem, section = m.groups()
        d = dir_of.get(b, {}).get(stem)
        if d is None:
            return m.group(0)
        tail = f"#{section})" if section else ")"
        return f"](./{stem}.md{tail}" if d == here else f"](../{d}/{stem}.md{tail}"
    return BACK.sub(sub, text)


def build(root, groups, kind, links=None):
    """{bundle: [(slug, path, dir)]} -> {bundle: (bytes, {slug: (first, last line)}, text)}"""
    out = {}
    for name, members in groups.items():
        text = (f"# {kind}: {name}\n\n> Generated. Do not read it whole: Grep `card: <slug>` "
                f"or Read the line range the catalog gives.\n\n")
        ranges = {}
        for slug, path, d in members:
            card = read(root, path)
            card = rewrite(card, links, d) if links else card
            start = text.count("\n") + 1
            nl = card.endswith("\n")
            text += (BEGIN if nl else BEGIN_NONL).format(slug) + card + ("" if nl else "\n") + END
            ranges[slug] = (start, text.count("\n") - 1)
        out[name] = (len(text.encode("utf-8")), ranges, text)
    return out


def fit(root, groups):
    """Split any group whose cards exceed TARGET, in order and by bytes, into name-1, name-2, ...
    By bytes, not by count: each part aims at an even share of the group, never goes over
    TARGET, and none is empty."""
    final = {}
    for name, members in groups.items():
        sizes = [os.path.getsize(os.path.join(root, m[1])) + 80 for m in members]
        goal = sum(sizes) / -(-sum(sizes) // TARGET)
        parts, cur, size = [], [], 0
        for m, s in zip(members, sizes):
            if cur and (size + s > TARGET or size >= goal):
                parts.append(cur)
                cur, size = [], 0
            cur.append(m)
            size += s
        parts.append(cur)
        for i, part in enumerate(parts):
            final[name if len(parts) == 1 else f"{name}-{i + 1}"] = part
    return final


def roundtrip(root, built, groups, links):
    """Split every bundle back into cards; count cards that differ from the file on disk."""
    dir_of = collections.defaultdict(dict)
    for (d, stem), b in links.items():
        dir_of[b][stem] = d
    bad = 0
    for name, (_, _, text) in built.items():
        for slug, path, d in groups[name]:
            nl = BEGIN.format(slug) in text
            mark = (BEGIN if nl else BEGIN_NONL).format(slug)
            i = text.index(mark) + len(mark)
            card = unrewrite(text[i:text.index(END, i)], dir_of, d)
            bad += (card if nl else card[:-1]) != read(root, path)
    return bad


def alpha_name(taken, cur):
    """functions-<first>-<last> letter, with -2, -3 ... when one letter spans two bundles."""
    base = f"functions-{cur[0][0][0]}-{cur[-1][0][0]}"
    name, n = base, 1
    while name in taken:
        n += 1
        name = f"{base}-{n}"
    return name


def plan_bundles(root, files):
    with open(os.path.join(root, GEN, "catalog.json"), encoding="utf-8") as f:
        cat = json.load(f)
    lib = {f"{GEN}/library/{f['file']}.md": f for f in cat["functions"]}
    assert set(lib) == {p for p in files if p.startswith(f"{GEN}/library/")}, "catalog/library drift"
    by_cat = collections.defaultdict(list)
    for path, f in sorted(lib.items()):
        by_cat["functions-" + (f["primaryCategory"] or "uncategorized")].append((f["file"], path, "library"))
    concepts = {"concepts": sorted((c["file"], f"{GEN}/concepts/{c['file']}.md", "concepts")
                                   for c in cat["concepts"])}
    groups = {**fit(root, dict(by_cat)), **fit(root, concepts)}

    alpha, cur, size = {}, [], 0
    for m in sorted((f["file"], p, "library") for p, f in lib.items()):   # greedy, A to Z
        s = os.path.getsize(os.path.join(root, m[1])) + 80
        if cur and size + s > TARGET:
            alpha[alpha_name(alpha, cur)], cur, size = cur, [], 0
        cur.append(m)
        size += s
    alpha[alpha_name(alpha, cur)] = cur

    links = {(d, slug): b for b, ms in groups.items() for slug, _, d in ms}
    built = build(root, groups, "DAX reference", links)
    ex = collections.defaultdict(list)
    for p in files:
        m = re.fullmatch(rf"{REF}/examples/([^/]+)/([^/]+)\.md", p)
        if m:
            ex[m.group(1)].append((m.group(2), p, "examples"))
    notes = sorted((os.path.basename(p)[:-3], p, "notes") for p in files
                   if re.fullmatch(rf"{REF}/notes/[^/]+\.md", p))
    sets = {
        "library_by_category": (f"{GEN}/library/", {k: v for k, v in built.items() if k.startswith("functions-")}),
        "library_alphabetical": (f"{GEN}/library/", build(root, alpha, "DAX functions")),
        "concepts": (f"{GEN}/concepts/", {k: v for k, v in built.items() if k.startswith("concepts")}),
        "examples": (f"{REF}/examples/", build(root, fit(root, dict(ex)), "Executed examples")),
        "notes": (f"{REF}/notes/", build(root, fit(root, {"notes": notes}), "Field notes")),
    }
    return sets, roundtrip(root, built, groups, links)


def apply(files, sets, which, moves=()):
    """File list after dropping `moves` and replacing each bundled folder by its bundles."""
    out = [p for p in files if not any(fnmatch.fnmatchcase(p, g) for g, _, _ in moves)]
    for key in which:
        src, built = sets[key]
        cards = re.compile(re.escape(src) + r"([^/]+/)?[^/]+\.md$")
        out = [p for p in out if not cards.match(p) or p == f"{src}README.md"]
        dest = f"{GEN}/bundles/" if src.startswith(f"{GEN}/") else src
        out += [f"{dest}{name}.md" for name in built]
    return out


def handwritten_links(root, files):
    """Links in hand-written files that name a card path; each needs a one-time rewrite."""
    pat = re.compile(r"(?:generated/)?(?:library|concepts)/[a-z0-9][a-z0-9.-]*\.md")
    hits = collections.Counter()
    for p in files:
        if p.endswith(".md") and not p.startswith((f"{GEN}/", "docs/examples-es/")):
            n = len(pat.findall(read(root, p)))
            if n:
                hits[p.split("/")[2] if p.startswith(f"{REF}/") and p.count("/") > 2 else top(p)] += n
    return hits


def table(rows, head):
    w = [max(len(str(r[i])) for r in rows + [head]) for i in range(len(head))]
    for r in [head, None] + rows:
        print("|" + "|".join("-" * (x + 2) for x in w) + "|" if r is None else
              "| " + " | ".join(str(c).ljust(w[i]) for i, c in enumerate(r)) + " |")
    print()


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # catalog marks (▶ ★) break a cp1252 console
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--sub-ref", default="origin/refactor/plugin-subfolder",
                    help="branch holding PR #26 (plugins/dax-for-agents/)")
    a = ap.parse_args()
    root = git(os.path.dirname(os.path.abspath(__file__)), "rev-parse", "--show-toplevel").strip()
    files = [p for p in git(root, "ls-files", "-z").split("\0") if p]

    print(f"## 1. Tracked files at the repo root (all ship today): {len(files)}\n")
    per = collections.defaultdict(collections.Counter)
    for p in files:
        per[top(p)][classify(p)[0]] += 1
    rows = [(k, sum(v.values()), v["runtime"], v["keep"], v["dev"]) for k, v in sorted(per.items())]
    rows.append(("TOTAL", len(files), *(sum(r[i] for r in rows) for i in (2, 3, 4))))
    table(rows, ("folder", "files", "runtime", "keep (listing/CI/release)", "dev only"))

    print("## 2. Inside skills/, by rule\n")
    by_rule = collections.Counter(classify(p) for p in files if p.startswith("skills/"))
    table([(c, n, w) for (c, w), n in sorted(by_rule.items(), key=lambda x: (x[0][0], -x[1]))],
          ("class", "files", "rule"))

    sets, bad = plan_bundles(root, files)
    print(f"## 3. Bundles (in memory; target {TARGET // 1024} KiB = 90% of 256 KiB)\n")
    rows = []
    for key, (src, built) in sets.items():
        sizes = [v[0] for v in built.values()]
        rows.append((key, len(built), sum(len(v[1]) for v in built.values()),
                     f"{max(sizes) / 1024:.1f}", "OK" if max(sizes) <= LIMIT_BYTES else "OVER"))
    table(rows, ("bundle set", "files", "cards", "largest KiB", "<= 256 KiB"))
    core = {**sets["library_by_category"][1], **sets["concepts"][1]}
    table([(n, len(v[1]), f"{v[0] / 1024:.1f}", v[2].count("\n")) for n, v in sorted(core.items())],
          ("generated/bundles/<file>.md", "cards", "KiB", "lines"))
    print(f"round trip (split each bundle, compare with the card on disk): {bad} card(s) differ")
    for slug, b in (("calculate", "functions-filter"), ("abs", "functions-math-and-trig")):
        f, l = core[b][1][slug]
        print(f"catalog pointer: {slug.upper()} -> `{b}:{f}-{l}`  (Read offset={f} limit={l - f + 1})")
    spans = [(b, r) for b, v in sets["library_by_category"][1].items() for r in v[1].values()]
    chars = sum(len(f" {b}:{r[0]}-{r[1]} |") for b, r in spans)
    print(f"extra catalog.md size of a 'bundle:first-last' column: {chars} chars (~{chars // 4} tokens); "
          f"longest card {max(r[1] - r[0] + 1 for _, r in spans)} lines")
    cards = [p for p in files if re.match(rf"{GEN}/(library|concepts)/[^/]+\.md$", p)]
    stems = {p.rsplit("/", 1)[1][:-3] for p in cards}
    kinds = collections.Counter(m.group(1) or "./" for p in cards for m in LINK.finditer(read(root, p))
                                if m.group(2) in stems)
    print(f"card-to-card links rewritten on bundle, reversed on split: {sum(kinds.values())} ("
          + ", ".join(f"'{k}x.md' {v}" for k, v in sorted(kinds.items())) + ")")
    links = handwritten_links(root, files)
    print(f"hand-written links that name a card path: {sum(links.values())} ("
          + ", ".join(f"{k} {v}" for k, v in sorted(links.items())) + ")\n")

    c = ["library_by_category", "concepts"]
    print("## 4. Scenarios\n")
    rows = [("NOW: root (main)", len(files), LIMIT_FILES - len(files))]
    for label, which, moves in (
            ("B-root 1: bundle library+concepts", c, ()),
            ("B-root 2: 1 + move docs/examples-es", c, B_ROOT_MOVES),
            ("B-root 3: 2 + bundle examples  <- proposed", c + ["examples"], B_ROOT_MOVES),
            ("B-root 4: 3 + bundle notes", c + ["examples", "notes"], B_ROOT_MOVES),
            ("B-root 5: 1 + move every dev folder (rejected)", c, HEAVY_MOVES)):
        n = len(apply(files, sets, which, moves))
        rows.append((label, n, LIMIT_FILES - n))
    try:
        sub = git(root, "ls-tree", "-r", "--name-only", a.sub_ref, "plugins/dax-for-agents").split()
        rows.append((f"B-sub: {a.sub_ref} as it is", len(sub), LIMIT_FILES - len(sub)))
    except subprocess.CalledProcessError:
        sub = [f"plugins/dax-for-agents/{p}" for p in
               (".claude-plugin/plugin.json", ".claude-plugin/icon.png", "LICENSE", "PRIVACY.md", "README.md")]
        rows.append((f"B-sub: {a.sub_ref}", "not fetched", "-"))
    extra = [p.split("/", 2)[2] for p in sub if "/skills/" not in p]
    model = [p for p in files if p.startswith("skills/")] + extra
    rows.append((f"B-sub model: main's skills/ + {len(extra)} PR files", len(model), LIMIT_FILES - len(model)))
    for label, which in (("B-sub 1: bundle library+concepts  <- proposed", c),
                         ("B-sub 2: + examples", c + ["examples"]),
                         ("B-sub 3: + examples + notes", c + ["examples", "notes"])):
        n = len(apply(model, sets, which))
        rows.append((label, n, LIMIT_FILES - n))
    table(rows, ("scenario", "files shipped", "margin to 512"))

    print("## 5. B-root moves\n")
    table([(g, sum(fnmatch.fnmatchcase(p, g) for p in files), d, w) for g, d, w in B_ROOT_MOVES],
          ("glob", "files", "destination", "why"))
    big = [p for p in files if os.path.getsize(os.path.join(root, p)) > LIMIT_BYTES]
    print(f"tracked files > 256 KiB today: {len(big)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
