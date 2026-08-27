#!/usr/bin/env python3
"""Sync the dax-reference library from MicrosoftDocs/query-docs.

Pass 1 (build_category_map and friends): parse the 15 category index files and
build the function -> category + summary map. The per-function files do not
declare their category anywhere, so these index pages are the only authoritative
source.

Pass 2 (parse_function_doc and friends): read each per-function file, extract
syntax, parameters, applies-to, and the discouraged flag from the [!INCLUDE]
shortcode, rewrite cross-links to local library paths, and produce the markdown
card written to generated/library/<fn>.md. Also stamps generated/catalog.json
and generated/catalog.md.

Everything the sync writes lives under generated/, so a new generation is
installed by moving one directory. The hand-written files — SKILL.md, NOTICE,
overrides.json and notes/ — sit outside it and are never touched.
"""
import os
import posixpath
import re
import sys

# The members table lives under this heading and ends at the next one. All 15 real
# indexes carry exactly one; scoping to it stops a future "Related content" or
# "Deprecated" table from being absorbed as category members.
SECTION = re.compile(r"^##\s+In this category\s*$", re.I)
HEADING = re.compile(r"^##\s")
# First cell of a member row: [CALCULATE](calculate-function-dax.md)
LINK = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)$")

INDEX_SUFFIX = "-functions-dax.md"
FUNCTION_SUFFIX = "-function-dax.md"

# Filename prefixes that carry a category the index tables never declare.
FILENAME_RULES = [("info-", "info")]

# The coarse net against silent parser drift: it catches a total collapse. Loose on
# purpose — pinning it just under the live 96.7% would break CI every time Microsoft ships
# a handful of functions the indexes have not caught up with yet.
#
# The sharp signal is no longer a number. A ceiling of 30 against a real set of 21 left
# nine slots a regression could hide in, and said nothing at all when one function gained
# a category while another lost one. The exceptions are now named in overrides.json and
# checked both ways — see uncategorized_gate and stale_uncategorized.
MIN_COVERAGE = 0.90

# Everything the sync writes goes under this one directory inside the skill, so installing
# a new generation moves a single path instead of three. The hand-written files — SKILL.md,
# NOTICE, overrides.json and notes/ — stay outside it and are never touched by the swap.
GENERATED = "generated"


def category_of(filename):
    """'filter-functions-dax.md' -> 'filter'."""
    return filename[: -len(INDEX_SUFFIX)] if filename.endswith(INDEX_SUFFIX) else filename


def discover_indexes(dax_dir):
    """Read every category index in `dax_dir` as (text, filename), alphabetically.

    Alphabetical order is not cosmetic: `build_category_map` gives primaryCategory to
    the first index that lists a function, so the order has to be deterministic.
    Override a specific function's primary category in overrides.json.
    """
    names = sorted(f for f in os.listdir(dax_dir) if f.endswith(INDEX_SUFFIX))
    out = []
    for fn in names:
        with open(os.path.join(dax_dir, fn), encoding="utf-8") as f:
            out.append((f.read(), fn))
    return out


def discover_function_docs(dax_dir):
    """Every per-function document in `dax_dir`, alphabetically.

    Note the single letter between the two suffixes: '-functions-dax.md' is a category
    index, '-function-dax.md' is one function. They must not be confused.
    """
    return sorted(f for f in os.listdir(dax_dir) if f.endswith(FUNCTION_SUFFIX))


# Directories under query-languages/dax/ that carry pages. "" is the dax/ root.
#
# Descending everywhere would sweep in includes/ (transclusion fragments, which are pieces
# of other pages rather than pages) and media/ (images). Listing what to read instead of
# what to skip means a NEW fragment directory cannot leak in — and unlisted_content_dirs
# below makes the opposite risk, a new content directory going unread, loud instead of
# silent.
CONCEPT_DIRS = ("", "best-practices")
NON_CONTENT_DIRS = frozenset({"includes", "media", "breadcrumb"})


def _fn_name(doc):
    """'topnskip-function-dax.md' -> 'TOPNSKIP', the key overrides.json uses."""
    stem = doc[: -len(FUNCTION_SUFFIX)] if doc.endswith(FUNCTION_SUFFIX) else doc
    return ".".join(p.upper() for p in stem.split("-")) if stem.startswith("info-") \
        else stem.upper()


def uncategorized_gate(leftover, declared):
    """Functions with no category that overrides.json does not declare, sorted.

    Gate 1. This replaced a ceiling of 30 against a real set of 21 — nine spare slots a
    regression could hide in, and no signal at all when one function gained a category
    while another lost one. Naming the exceptions makes the swap fail too.
    """
    return sorted(_fn_name(d) for d in leftover if _fn_name(d) not in declared)


def stale_uncategorized(leftover, declared):
    """Declared exceptions that now DO have a category, sorted.

    Upstream classifying one of them is good news, but a name left behind turns the list
    into claims nobody has rechecked — which is how the ceiling rotted in the first place.
    """
    live = {_fn_name(d) for d in leftover}
    return sorted(name for name in declared if name not in live)


TOC_FILE = "toc.yml"


def read_toc(dax_dir):
    """The raw toc.yml next to the docs. Raises OSError if it is not there.

    Deliberately not tolerant: a missing table of contents would quietly cost 5 functions
    their category, and "the toc classified nothing" must not look like "there is no toc".
    """
    with open(os.path.join(dax_dir, TOC_FILE), encoding="utf-8") as f:
        return f.read()


def _toc_slug(section):
    """'Date and time functions' -> 'date-and-time', matching the index filenames.

    Mechanical rather than a hand-written table: all 15 sections that contain functions
    derive to exactly the 15 index slugs, checked against the real toc.yml. A table would
    be one more thing to keep in step with upstream.
    """
    s = re.sub(r"\s+functions?$", "", section.strip(), flags=re.I)
    return re.sub(r"\s+", "-", s.strip()).lower()


def parse_toc(text, known_categories):
    """{function-doc filename: category} from Learn's own table of contents.

    The fourth route to a category, and the only authoritative one for functions no
    category index lists: the navigation is where Microsoft actually says where a function
    belongs. Only per-function pages are read — the index pages and the conceptual pages
    that share those sections are not functions and take no category from them.

    `known_categories` is the set of real category slugs, taken from the index filenames
    themselves so a genuinely new category is accepted the moment its index appears. A
    section that derives to anything else is REFUSED rather than used: a TOC section name
    is a display string, and stamping a slug derived from a renamed or newly invented one
    would put a category in the library that no index backs. A reader cannot tell an
    invented classification from a real one, which makes that worse than no category —
    upstream drift stops the run rather than being guessed at.
    """
    try:
        import yaml
    except ImportError:                                   # pragma: no cover - CI installs it
        raise SystemExit("ERROR: pyyaml is required to read toc.yml (pip install pyyaml)")

    found, unknown = {}, {}

    def walk(nodes, section):
        for node in nodes or []:
            name = node.get("name", "")
            href = node.get("href", "")
            if href.endswith(FUNCTION_SUFFIX) and section:
                slug = _toc_slug(section)
                if slug not in known_categories:
                    unknown.setdefault(section, []).append(href)
                elif found.get(href, slug) != slug:
                    # Last-write-wins would pick one silently, and which one depends on
                    # the order of the file.
                    raise ValueError(
                        f"{href} appears under two different categories in {TOC_FILE}: "
                        f"{found[href]!r} and {slug!r}. Pick one in overrides.json rather "
                        f"than letting the file order decide.")
                else:
                    found[href] = slug
            walk(node.get("items"), name)

    walk((yaml.safe_load(text) or {}).get("items"), "")
    if unknown:
        detail = "; ".join(f"{name!r} ({len(hrefs)} function(s))"
                           for name, hrefs in sorted(unknown.items()))
        raise ValueError(
            f"{TOC_FILE} groups functions under section(s) that are not a category: "
            f"{detail}. A category must be one an index declares — if Microsoft added a "
            f"real one it arrives as a new '*{INDEX_SUFFIX}' and needs no change here; if "
            f"they renamed a section, map it explicitly. Do not let a display name become "
            f"a category the library cannot back.")
    return found


def apply_toc(mapping, toc, function_docs):
    """Fill category gaps from the TOC. Mutates `mapping`; returns what it added, sorted.

    Gaps only. The category indexes stay the primary source — they carry the summary text
    as well as the category, and the TOC carries neither.
    """
    added = []
    for doc in function_docs:
        if doc in mapping or doc not in toc:
            continue
        category = toc[doc]
        mapping[doc] = {
            "name": "",                 # pass 2 reads the real name from the doc's heading
            "summary": "",              # the TOC has no descriptions
            "category": [category],
            "primaryCategory": category,
        }
        added.append(doc)
    return sorted(added)


def discover_concept_docs(dax_dir):
    """Every conceptual page in `dax_dir`, as posix-relative paths, alphabetically.

    A page is conceptual when it is neither one function ('-function-dax.md') nor a
    category index ('-functions-dax.md'). Those two are consumed by the library passes;
    everything else — the glossary, the query statements, the operator and syntax
    references, best practices — is prose an agent needs for a question that is not about
    one specific function.
    """
    found = []
    for sub in CONCEPT_DIRS:
        d = os.path.join(dax_dir, sub) if sub else dax_dir
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if not f.endswith(".md"):
                continue
            if f.endswith(FUNCTION_SUFFIX) or f.endswith(INDEX_SUFFIX):
                continue
            found.append(posixpath.join(sub, f) if sub else f)
    return sorted(found)


def unlisted_content_dirs(dax_dir):
    """Subdirectories holding .md files that CONCEPT_DIRS does not read, alphabetically.

    Upstream drift this pipeline must not absorb quietly: if Microsoft adds a docs area,
    its pages are missing from concepts/ and nothing about the output looks wrong. The
    report names it so the omission is a decision rather than an accident.
    """
    def holds_pages(d):
        # Walked, not listed: pages one more level down (guidance/advanced/page.md) left
        # the top of the tree holding only a folder, so the check saw no .md and said
        # nothing — a silent miss wearing the costume of a check.
        return any(f.endswith(".md") for _, _, files in os.walk(d) for f in files)

    unlisted = []
    for name in os.listdir(dax_dir):
        d = os.path.join(dax_dir, name)
        if not os.path.isdir(d) or name in NON_CONTENT_DIRS:
            continue
        if name not in CONCEPT_DIRS:
            if holds_pages(d):
                unlisted.append(name)
            continue
        # A directory we DO read still only gets read one level deep, so a subdirectory
        # inside it is missed twice over: not generated, and skipped by this check because
        # its parent is listed. That was the worst blind spot of the two together.
        for sub in os.listdir(d):
            child = os.path.join(d, sub)
            if os.path.isdir(child) and sub not in NON_CONTENT_DIRS and holds_pages(child):
                unlisted.append(posixpath.join(name, sub))
    return sorted(unlisted)


def parse_category_index(text, filename):
    """Return one entry per row of the index's "In this category" table.

    Only that section is read, and only its first two columns: the linked function and
    its description. Header and separator rows fall out because their first cell is not
    a link. An index without the heading (info-functions-dax.md is prose) yields nothing.
    """
    category = category_of(filename)
    entries = []
    inside = False
    for line in text.splitlines():
        if SECTION.match(line):
            inside = True
            continue
        if not inside:
            continue
        if HEADING.match(line):
            break
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        m = LINK.match(cells[0])
        if not m:
            continue
        entries.append({
            "name": m.group(1).strip(),
            "file": m.group(2).strip(),
            "summary": cells[1],
            "category": category,
        })
    return entries


def build_category_map(indexes):
    """Merge parsed indexes into {function_doc: {name, summary, category[], primaryCategory}}.

    `indexes` is an iterable of (text, filename) pairs, in the order the categories
    should be considered: the first index that lists a function owns it as primary.
    A function listed in several indexes collects every category, without repeats.
    """
    merged = {}
    for text, filename in indexes:
        for e in parse_category_index(text, filename):
            entry = merged.get(e["file"])
            if entry is None:
                merged[e["file"]] = {
                    "name": e["name"],
                    "summary": e["summary"],
                    "category": [e["category"]],
                    "primaryCategory": e["category"],
                }
            elif e["category"] not in entry["category"]:
                entry["category"].append(e["category"])
    return merged


def apply_filename_rules(mapping, function_docs):
    """Categorize function docs that no category index lists, by filename prefix.

    `info-functions-dax.md` is a prose page with no "In this category" table, so the
    72 INFO.* docs reach pass 1 with no category at all. Their filename carries the
    dotted name exactly (info-view-tables -> INFO.VIEW.TABLES), which is enough.

    Mutates `mapping`; returns the docs still without a category, sorted. Those need
    pass 2 (their applies-to include) or an entry in overrides.json.
    """
    leftover = []
    for doc in function_docs:
        if doc in mapping:
            continue
        stem = doc[: -len(FUNCTION_SUFFIX)] if doc.endswith(FUNCTION_SUFFIX) else doc
        for prefix, category in FILENAME_RULES:
            if stem.startswith(prefix):
                mapping[doc] = {
                    "name": ".".join(p.upper() for p in stem.split("-")),
                    "summary": "",          # pass 2 reads it from the function doc itself
                    "category": [category],
                    "primaryCategory": category,
                }
                break
        else:
            leftover.append(doc)
    return sorted(leftover)


# ---------------------------------------------------------------------------
# Pass 2 — per-function parsing
# ---------------------------------------------------------------------------

# Maps the include filename stem (without .md) to (appliesTo list, discouraged bool).
# The include file name is the canonical signal: it is part of the upstream schema and
# changes only when Microsoft adds a new applies-to combination.
APPLIES_TO_MAP = {
    "applies-to-measures-columns-tables-visual-calculations-discouraged":
        (["measure", "column", "table", "visual-calculation"], True),
    "applies-to-measures-columns-tables-visual-calculations":
        (["measure", "column", "table", "visual-calculation"], False),
    "applies-to-measures-columns-tables":
        (["measure", "column", "table"], False),
    "applies-to-query-only":
        (["query"], False),
    "applies-to-visual-calculations":
        (["visual-calculation"], False),
}

# No fallback. An earlier revision defaulted to (measure, column, table, not discouraged)
# and called it "the safest default" — it is the most PERMISSIVE one. On an unknown or
# missing include the card would have asserted that the function is legal in measures,
# columns and tables and is not discouraged. A reference whose job is to stop the agent
# inventing must not invent when it does not understand the page.
_NO_CLAIM = ([], None)

# Matches the [!INCLUDE[label](path)] shortcode that declares applies-to.
_INCLUDE_RE = re.compile(
    r'\[!INCLUDE\[([^\]]*)\]\(includes/([^)]*)\)\]'
)

# Matches a ```dax ... ``` fenced code block.
_DAX_BLOCK_RE = re.compile(r'```dax\n(.*?)```', re.S)

# Matches ms.date in YAML frontmatter (key: value, any whitespace).
_MS_DATE_RE = re.compile(r'^ms\.date:\s*(.+)$', re.MULTILINE)

# Strips the Microsoft YAML frontmatter block at the top of the file.
_MS_FRONTMATTER_RE = re.compile(r'^---\s*\n.*?\n---\s*\n', re.S)

# Matches the entire [!INCLUDE] line (including the trailing newline).
_INCLUDE_LINE_RE = re.compile(r'\[!INCLUDE\[applies-to[^\]]*\]\([^)]*\)\]\s*\n?')

# Rewrites function-doc cross-links: "other-function-dax.md" → "./other.md".
# Matches only -function-dax.md (singular), not -functions-dax.md (category index).
# The negative lookahead stops category index links from being rewritten.
# The '../' form is how a page in best-practices/ reaches the function docs. Without it
# those links fell through to the upstream-URL pass and left the local library unused.
_LINK_REWRITE_RE = re.compile(
    r'\[([^\]]+)\]\(((?:\.\./)?[a-z0-9][a-z0-9\-]+-function-dax\.md)(#[^)]*)?\)'
)

# Applies-to context abbreviations for catalog.md rendering.
_APPLIES_TO_ABBREV = {
    "measure": "M",
    "column": "C",
    "table": "T",
    "visual-calculation": "V",
    "query": "Q",
}


def parse_applies_to(text):
    """Extract (appliesTo, discouraged) from the [!INCLUDE] in a function doc.

    Returns (list_of_contexts, discouraged). Missing or unrecognised include -> ([], None):
    no claim, which the caller reports rather than papering over.
    """
    m = _INCLUDE_RE.search(text)
    if not m:
        return _NO_CLAIM
    stem = os.path.splitext(m.group(2))[0]
    return APPLIES_TO_MAP.get(stem, _NO_CLAIM)


def parse_title(text):
    """The function name from the document's own '# NAME' heading, or ''.

    Used for the 21 docs no category index lists. An earlier revision derived the name
    from the filename instead (upper-case, hyphens to dots). That happens to agree with
    the real heading on all 21 today, but agreeing by luck is not the same as being right:
    the page states its own name, so read it.
    """
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def parse_summary(text):
    """Extract the short description paragraph after the [!INCLUDE] line.

    Skips blank lines and blockquotes (> [!NOTE] etc.) immediately after the
    include, and returns the first plain paragraph. If no include is present,
    returns an empty string (the caller can use the category-map summary instead).
    """
    lines = text.splitlines()
    past_include = False
    for line in lines:
        if "[!INCLUDE[applies-to" in line:
            past_include = True
            continue
        if not past_include:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith(">"):
            continue
        return stripped
    return ""


def parse_syntax(text):
    """Extract the body of the first ```dax fenced code block."""
    m = _DAX_BLOCK_RE.search(text)
    return m.group(1).strip() if m else ""


def parse_ms_date(text):
    """Extract the ms.date value from the Microsoft YAML frontmatter."""
    m = _MS_DATE_RE.search(text)
    return m.group(1).strip() if m else ""


def rewrite_links(text, prefix="./"):
    """Rewrite function-doc cross-links to local library paths.

    Converts 'other-function-dax.md' -> './other.md' inside Markdown links.
    Category-index links ('-functions-dax.md') and external URLs are left intact.
    In-link anchors (e.g. '#remarks') are preserved on the rewritten target.

    `prefix` is where the cards sit relative to the page being written: './' for a card
    in library/, '../library/' for a concept one directory away. Any leading '../' on the
    upstream target is dropped — where the link came FROM says nothing about where the
    local card is.
    """
    def _replace(m):
        label = m.group(1)
        fn_file = posixpath.basename(m.group(2))
        anchor = m.group(3) or ""
        local = fn_file[: -len(FUNCTION_SUFFIX)]
        return f"[{label}]({prefix}{local}.md{anchor})"

    return _LINK_REWRITE_RE.sub(_replace, text)


_RETURN_SECTION_RE = re.compile(r'^##\s+Return value\s*$', re.I)
# The thing returned, as a noun phrase: "a table", "the filtered table", "a column of ...".
_RETURN_NP_RE = re.compile(
    r'\b(?:a|an|the)\s+(?:(?:single|new|one-column|whole|entire|filtered|complete)\s+){0,2}'
    r'(?:table|column)\b', re.I)
# ... but not when it sits behind a preposition: COUNTROWS returns "the number of rows IN
# THE TABLE" and is scalar.
_RETURN_PREP_RE = re.compile(r'\b(?:in|of|from|within|to|on|for|by)\s*$', re.I)


def parse_return_value(text):
    """'table' | 'scalar' from the doc's own '## Return value' section, or None.

    None means the page has no such section (3 of 479 upstream: DATEVALUE, DEGREES,
    RADIANS). Those belong in overrides.json, not in a guess.
    """
    inside = False
    first = None
    for line in text.splitlines():
        if _RETURN_SECTION_RE.match(line):
            inside = True
            continue
        if inside:
            if line.startswith("## "):
                break
            if line.strip():
                first = line.strip()
                break
    if first is None:
        return None
    if _looks_boolean(first):
        return "scalar"
    for m in _RETURN_NP_RE.finditer(first):
        if not _RETURN_PREP_RE.search(first[: m.start()]):
            return "table"
    return "scalar"


def determine_returns(filename, text, category_map, overrides):
    """Determine the return type ('scalar' or 'table') for a function.

    Resolution order (first match wins):
    1. overrides['returns'][function_name]
    2. the doc's own '## Return value' section
    3. '' — unresolved, for the caller to report

    There is deliberately no 'scalar' default. The previous version inferred the type from
    the category, marking as table only 'table-manipulation'; measured against the 479 real
    documents that stamped 'scalar' on 123 of 458 functions whose own docs say table —
    ALL, ALLEXCEPT, CALCULATETABLE, CALENDAR, DATEADD, the whole INFO family. Wrong metadata
    in a reference is worse than absent metadata.
    """
    entry = category_map.get(filename, {})
    name = entry.get("name", "")
    ovr = (overrides or {}).get("returns", {})
    if name in ovr:
        return ovr[name]
    return parse_return_value(text) or ""


# A scalar that YAML would read as something other than a plain string. The colon is the
# one that matters in practice: 17 of the 34 concept pages describe themselves as "Learn
# more about: X", and unquoted that turns the value into a mapping.
#
# An EMPTY value is deliberately not in here. Bare, it parses as null, which is what an
# absent ms.date or primaryCategory means — and quoting it would have rewritten the
# frontmatter of 458 of the 479 cards for no gain.
#
# The '#' rule reads `\s#`, not `#\s`: YAML opens a comment at a '#' PRECEDED by
# whitespace, whatever follows it. Looking for a space AFTER it let "See #123" through
# bare, and the value silently truncated to "See".
_YAML_NEEDS_QUOTING = re.compile(r'^[\[\]{}&*!|>%@`#\'"-]|:\s|:$|\s#|^\s|\s$')


def _yaml_scalar(value):
    """Render a string as a YAML scalar, quoting only when it would otherwise change.

    Plain tokens are left bare so the 479 function cards — whose values are all bare
    tokens — do not churn the first time this runs.
    """
    text = str(value)
    if not _YAML_NEEDS_QUOTING.search(text):
        return text
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _format_frontmatter(fm):
    """Render a frontmatter dict as a YAML block (no external deps).

    Lists use flow style ([a, b, c]).  Booleans use lowercase literals.
    Strings are quoted only where leaving them bare would change their meaning.
    """
    lines = []
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(_yaml_scalar(i) for i in v)}]")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        else:
            lines.append(f"{k}: {_yaml_scalar(v)}")
    return "\n".join(lines) + "\n"


UPSTREAM_DOC_URL = "https://learn.microsoft.com/en-us/dax/"

# [!INCLUDE [label](includes/file.md)] — a transclusion, not a link.
_INCLUDE_SHORTCODE_RE = re.compile(r'\[!INCLUDE\s*\[[^\]]*\]\(includes/([^)]+)\)\]')
# A bare markdown link to another query-docs page: not local, not already absolute.
#
# "Local" means anywhere inside this skill's generated tree: './card.md' from a library
# card, '../library/card.md' from a concept. Those are the OUTPUT of rewrite_links, not
# upstream paths — absolutising them turned a working local link into a Learn URL, and for
# the concept form into a hard failure, since '../library/...' is not a DAX docs area.
_LOCAL_MD_LINK_RE = re.compile(
    r'\]\((?!\./)(?!\.\./(?:library|concepts)/)(?!https?://)(?!#)([^)\s]+\.md)(#[^)]*)?\)')
# A Microsoft Learn site-absolute path, e.g. /power-bi/transform-model/dax-query-view
_SITE_ABS_LINK_RE = re.compile(r'\]\(/([^)\s]+)\)')
# An image kept in the upstream repo next to the docs.
_MEDIA_LINK_RE = re.compile(r'\]\((media/[^)\s]+)(\s+"[^"]*")?\)')
LEARN_ROOT = "https://learn.microsoft.com/en-us/"
UPSTREAM_RAW = ("https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/"
                "query-languages/dax/")



# --- 1. boolean guard -------------------------------------------------------------
# "TRUE when a column of TableName is being filtered" is a boolean, not a table. The
# noun-phrase match alone shipped ISFILTERED, ISCROSSFILTERED and ISEMPTY as tables.
# Checked before the table test because the boolean wording usually leads the sentence.
BOOL_RE = re.compile(r'(?:^|[^a-z])(true|false)(?:[^a-z]|$)', re.I)


def _looks_boolean(first):
    """A return sentence that states TRUE/FALSE as the result."""
    hits = BOOL_RE.findall(first)
    if len(hits) >= 2:                       # "TRUE when ... otherwise FALSE"
        return True
    # A single TRUE/FALSE counts only when it opens the sentence, so that "a table of the
    # true daily rates" is not mistaken for a boolean return.
    m = BOOL_RE.search(first)
    return bool(m and m.start() <= 1)


# --- 2. DocFX image directives ----------------------------------------------------
# query-docs mixes markdown images with DocFX :::image ... source="media/..." ...:::
# Rewriting only the markdown form left local media paths in the cards.
DOCFX_MEDIA_RE = re.compile(r'((?:source|lightbox)=")(media/[^"]+)(")')

# Subtrees of query-languages/dax/ that upstream links reach with a `..` even though they
# are inside it. Anything else behind a `..` is a sibling docs area and must not be routed
# to /dax/ silently.
DAX_INTERNAL_AREAS = {"dax", "best-practices"}

# --- 3. parent-relative targets ---------------------------------------------------
# ../best-practices/x.md must not become learn.microsoft.com/en-us/dax/../best-practices/x
def _learn_url(target, base=""):
    """Map a query-docs .md target to its Learn URL.

    `base` is the directory of the page the link appears on, relative to dax/ — "" for a
    page at the root, "best-practices" for one below it.

    The repo layout is NOT the URL route, so this cannot be resolved as a filesystem
    path. Everything under query-languages/dax/ serves from /dax/, including
    best-practices/ — yet upstream reaches it with `../best-practices/...`, a relative
    path that is wrong in the repo and only works because Learn routes differently.
    Treating it as a path dropped the /dax/ segment and produced a URL to no page.

    So a `..` is discarded — but only when what follows is known to be DAX content.
    query-languages/ holds nothing but dax/ today, and the whole corpus has 3 parent-
    relative targets, all dax-internal. If Microsoft ever adds a sibling area, discarding
    `..` would quietly route it to /dax/<that area>, inventing a URL. Raises instead:
    upstream drift should stop the run, not be guessed at.
    """
    stem = target[: -len(".md")] if target.endswith(".md") else target
    # Resolve against the directory the LINK IS IN, not against dax/. A page in
    # best-practices/ names its neighbours by bare filename; treating those as root-level
    # dropped the directory and produced a URL to a page that does not exist.
    # Always normalised, base or not: 'best-practices/../../power-query-m/page.md' hides
    # its climb out of the tree behind a directory that looks legitimate.
    stem = posixpath.normpath(posixpath.join(base, stem))
    parts = [p for p in stem.split("/") if p not in (".", "")]
    climbs_out = ".." in parts
    parts = [p for p in parts if p != ".."]
    if parts and parts[0] == "dax":
        parts = parts[1:]
    # An area name is REQUIRED when the link either climbed above dax/ or names a
    # subdirectory. Two ways this was got wrong: checking for a literal '..' missed the
    # case where resolving against a base consumed it, and dropping every '..' and then
    # asking only about subdirectories let '../foo.md' — which is query-languages/foo.md,
    # outside dax/ — map to /dax/foo. Both invent a URL to a page that does not exist,
    # from the guard whose whole job is to refuse to do that.
    #
    # A '..' that survives IS legitimate in one case: best-practices/ is inside dax/, yet
    # root pages reach it with '../best-practices/...'. That is why the area list exists.
    if (climbs_out or len(parts) > 1) and (not parts or parts[0] not in DAX_INTERNAL_AREAS):
        raise ValueError(
            f"link resolves outside the DAX area: {target!r} (base {base!r}) -> "
            f"{'/'.join(parts) or '(nothing)'}. Add its area to DAX_INTERNAL_AREAS if it "
            f"really is DAX content, or map it explicitly — do not let it be routed to "
            f"/dax/ by default.")
    return LEARN_ROOT + "dax/" + "/".join(parts)


def resolve_includes(text, includes_dir):
    """Inline every [!INCLUDE[...](includes/...)] with the include's own body.

    These are transclusions: the rendered Microsoft page shows the text, not a link. Left
    as-is they become dangling links in the card, and the most common one (266 of the 479
    docs) carries a real constraint — the function is unsupported in DirectQuery for
    calculated columns and RLS. An include that cannot be read is dropped rather than left
    pointing at a file this repo does not ship.
    """
    def _replace(m):
        path = os.path.join(includes_dir, m.group(1))
        try:
            with open(path, encoding="utf-8") as f:
                body = f.read()
        except OSError:
            return ""
        body = _MS_FRONTMATTER_RE.sub("", body, count=1)
        return body.strip()
    return _INCLUDE_SHORTCODE_RE.sub(_replace, text)


def absolutise_links(text, base=""):
    """Point links to query-docs pages this repo does not carry at learn.microsoft.com.

    Cards for other functions were already rewritten to ./stem.md by rewrite_links. What
    is left are category indexes and concept pages. Pointing them at the live docs is
    honest; leaving a relative path to a file that is not here is not.

    `base` is the directory the page itself lives in, relative to dax/. Every relative
    target — pages and images alike — is resolved against it. best-practices/ has its own
    media/ folder, so getting this wrong broke the images as well as the links.
    """
    def _rel(target):
        return posixpath.normpath(posixpath.join(base, target)) if base else target

    def _md(m):
        anchor = m.group(2) or ""
        return f"]({_learn_url(m.group(1), base=base)}{anchor})"
    text = _LOCAL_MD_LINK_RE.sub(_md, text)
    # /power-bi/... and /dax/... are Learn site-absolute paths, meaningless outside it.
    text = _SITE_ABS_LINK_RE.sub(lambda m: f"]({LEARN_ROOT}{m.group(1)})", text)
    # Images live beside the docs upstream; this repo carries no binaries.
    text = _MEDIA_LINK_RE.sub(
        lambda m: f"]({UPSTREAM_RAW}{_rel(m.group(1))}{m.group(2) or ''})", text)
    # DocFX directives carry their paths in attributes, not markdown link syntax.
    text = DOCFX_MEDIA_RE.sub(
        lambda m: f"{m.group(1)}{UPSTREAM_RAW}{_rel(m.group(2))}{m.group(3)}", text)
    return text


# Microsoft's own examples are measured against Adventure Works DW 2020, a model this repo
# does not carry. They are CC BY 4.0 and worth keeping for context, but a reader must not
# mistake "$109,809,274.20" for something anyone here executed. The heading is renamed and a
# note added; the examples themselves are left exactly as upstream wrote them.
#
# `[ \t]*` y no `\s*`: `\s` incluye el salto de linea, asi que la version con `\s*$` se comia
# la linea en blanco que sigue al encabezado y dejaba la cita pegada al parrafo. En markdown
# eso no es cosmetico — la continuacion perezosa absorbe el parrafo DENTRO de la cita.
_MS_EXAMPLES_HEADING = re.compile(r"^## Examples?[ \t]*$", re.M)

_MS_EXAMPLES_NOTICE = (
    "## Examples (Microsoft — no verificados aquí)\n"
    "\n"
    "> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW\n"
    "> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado\n"
    "> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que\n"
    "> aportan, y porque son CC BY 4.0 de Microsoft.\n"
)


def _examples_section(stem, entry):
    """The block that points at this function's executable examples."""
    category, count = entry
    return (
        f"## Ejemplos ejecutables\n"
        f"\n"
        f"**{count}** consulta(s) medidas contra un modelo que sí está en este repositorio, "
        f"cada una con el número que devolvió el motor:\n"
        f"[`examples/{category}/{stem}.md`](../../examples/{category}/{stem}.md).\n"
        f"\n"
        f"Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.\n"
    )


def build_library_card(text, filename, category_map, overrides, notes_set,
                       source_sha="", includes_dir="", examples_index=None):
    """Build the markdown content for library/<fn>.md.

    The card has a machine-readable YAML frontmatter block followed by the
    function body (syntax, parameters, remarks, examples) with:
      - The Microsoft YAML frontmatter stripped
      - The [!INCLUDE] applies-to line stripped (the info moves to frontmatter)
      - Cross-links to other function docs rewritten to ./local.md paths

    `notes_set` is a set of stems (without .md) of functions that have a
    hand-written notes/<fn>.md file. `source_sha` is the upstream commit SHA
    to stamp into the frontmatter (empty when not syncing from a live clone).
    """
    entry = category_map.get(filename, {})
    name = entry.get("name", "") or parse_title(text)

    applies_to, discouraged = parse_applies_to(text)
    summary = entry.get("summary") or parse_summary(text)
    ms_date = parse_ms_date(text)
    returns = determine_returns(filename, text, category_map, overrides)
    fn_stem = filename[: -len(FUNCTION_SUFFIX)]
    has_notes = fn_stem in (notes_set or set())
    example_entry = (examples_index or {}).get(fn_stem)

    source = f"query-languages/dax/{filename}"
    if source_sha:
        source = f"{source}@{source_sha}"

    fm = {
        "name": name,
        "category": entry.get("category", []),
        "primaryCategory": entry.get("primaryCategory", ""),
        "returns": returns,
        "appliesTo": applies_to,
        "discouragedInVisualCalculations": discouraged,
        "source": source,
        "sourceDate": ms_date,
        "notes": has_notes,
        "examples": example_entry[1] if example_entry else 0,
    }

    # Strip the upstream frontmatter and the applies-to include line.
    body = _MS_FRONTMATTER_RE.sub("", text, count=1)
    body = _INCLUDE_LINE_RE.sub("", body)

    # Order matters: local card links first, then transclusions inlined, then whatever
    # still points at a query-docs page this repo does not carry becomes an upstream URL.
    body = rewrite_links(body)
    if includes_dir:
        body = resolve_includes(body, includes_dir)
    body = absolutise_links(body)

    # Upstream's examples get their heading renamed and a notice, so nobody reads Adventure
    # Works figures as something this repo verified. Our own examples go ABOVE them: an
    # agent that stops reading early must hit the executable ones first.
    marked = _MS_EXAMPLES_HEADING.sub(
        lambda _: _MS_EXAMPLES_NOTICE.rstrip("\n"), body, count=1)
    if example_entry:
        ours = _examples_section(fn_stem, example_entry)
        if marked != body:
            # There is an upstream Examples section: insert ours immediately before it.
            at = marked.index(_MS_EXAMPLES_NOTICE.splitlines()[0])
            marked = marked[:at] + ours + "\n" + marked[at:]
        else:
            marked = marked.rstrip() + "\n\n" + ours
    body = marked

    return f"---\n{_format_frontmatter(fm)}---\n{body.lstrip()}"


# ---------------------------------------------------------------------------
# main — pass 1 only (pass 2 write mode is gated behind a second argument)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Writing the library
# ---------------------------------------------------------------------------

UPSTREAM_REPO = "MicrosoftDocs/query-docs"

# Compact codes for the catalog's "applies to" column, so a 479-row table stays scannable.
_APPLIES_CODE = {
    "measure": "M", "column": "C", "table": "T",
    "visual-calculation": "V", "query": "Q",
}


def _notes_stems(out_dir):
    """Stems of the hand-written notes/. Read only — the sync never writes there."""
    notes_dir = os.path.join(out_dir, "notes")
    if not os.path.isdir(notes_dir):
        return set()
    return {os.path.splitext(f)[0] for f in os.listdir(notes_dir) if f.endswith(".md")}


def _examples_index(out_dir):
    """stem -> (category, how many ```dax blocks), from the hand-written examples/.

    Same contract as notes/: read only, never written by the sync. The count is what the
    card advertises, so a card can never promise more examples than the file holds.
    """
    root = os.path.join(out_dir, "examples")
    if not os.path.isdir(root):
        return {}
    index = {}
    for category in sorted(os.listdir(root)):
        cat_dir = os.path.join(root, category)
        if not os.path.isdir(cat_dir):
            continue
        for name in sorted(os.listdir(cat_dir)):
            if not name.endswith(".md"):
                continue
            path = os.path.join(cat_dir, name)
            with open(path, encoding="utf-8") as f:
                body = f.read()
            index[os.path.splitext(name)[0]] = (category, body.count("```dax"))
    return index


def _wipe(path):
    """Remove every .md in a generated directory, creating it if absent.

    Only the generated trees are ever passed here. A card that upstream deleted must not
    survive as a ghost, so the directory is emptied rather than merged into.
    """
    os.makedirs(path, exist_ok=True)
    for name in os.listdir(path):
        if name.endswith(".md"):
            os.remove(os.path.join(path, name))


def _cell(value):
    """A markdown table cell. A raw pipe in the value silently adds a column."""
    return str(value).replace("|", "\\|")


def _catalog_md(entries, source, source_date):
    head = [
        "# DAX Reference — catálogo de funciones (índice generado)",
        "",
        f"> Fuente: `{source}` · commit {source_date}",
        f"> {len(entries)} funciones · generado por `scripts/sync_query_docs.py`",
        "> **No editar a mano.** ⛔ = Microsoft la desaconseja **en cálculos visuales** "
        "(dice que probablemente devuelve resultados sin sentido); en una medida o columna "
        "calculada no dice nada · ★ = tiene nota propia · ▶ = tiene ejemplos ejecutables "
        "en este repositorio.",
        "",
        "| Función | Cat | Ret | Aplica | Resumen | ⚑ |",
        "|---|---|---|---|---|---|",
    ]
    rows = []
    for e in entries:
        # ▶ existe porque sin el la unica forma de saber que una funcion tiene ejemplos
        # ejecutables era abrir su ficha: el catalogo marcaba la nota y callaba los
        # ejemplos. Con 99 funciones cubiertas eso son 99 fichas que abrir para encontrar
        # las que se pueden ejecutar.
        flags = (("⛔" if e["discouragedInVisualCalculations"] else "")
                 + ("★" if e["notes"] else "")
                 + ("▶" if e.get("examples") else ""))
        applies = " ".join(_APPLIES_CODE.get(a, a) for a in e["appliesTo"])
        summary = e["summary"].replace("|", "\\|")
        rows.append(f"| {_cell(e['name'])} | {_cell(e['primaryCategory'])} | "
                    f"{_cell(e['returns'])} | {applies} | {summary} | {flags} |")
    return "\n".join(head + rows) + "\n"


def _concepts_md(concepts, source, source_date):
    head = [
        "# DAX Reference — catálogo de conceptos (índice generado)",
        "",
        f"> Fuente: `{source}` · commit {source_date}",
        f"> {len(concepts)} páginas conceptuales · generado por `scripts/sync_query_docs.py`",
        "> **No editar a mano.** Para preguntas sobre una función concreta usa "
        "`catalog.md`.",
        "",
        "| Página | Tema | Título | Resumen |",
        "|---|---|---|---|",
    ]
    # Every cell, not just the summary: two upstream titles end in "| Microsoft Docs", and
    # emitted raw they added columns and the index stopped being a table.
    rows = [
        "| " + " | ".join(_cell(c[k]) for k in ("file", "topic", "title", "summary")) + " |"
        for c in concepts
    ]
    return "\n".join(head + rows) + "\n"


_MS_FIELD_RE = {}


def _ms_field(text, key):
    """Read one field out of Microsoft's own YAML frontmatter, unquoted. '' if absent."""
    rx = _MS_FIELD_RE.get(key)
    if rx is None:
        rx = _MS_FIELD_RE[key] = re.compile(rf'^{re.escape(key)}:\s*(.+)$', re.M)
    m = rx.search(_MS_FRONTMATTER_RE.match(text).group(0) if
                  _MS_FRONTMATTER_RE.match(text) else "")
    if not m:
        return ""
    value = m.group(1).strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def concept_slug(rel_path):
    """The card filename for a conceptual page: its upstream stem.

    Kept identical to upstream so a reader can always get from the card back to the page
    it came from. Verified collision-free across the two content directories.
    """
    return posixpath.splitext(posixpath.basename(rel_path))[0]


def build_concept_card(text, rel_path, source_sha="", includes_dir=""):
    """Build the markdown content for concepts/<slug>.md.

    Same shape as a library card — our frontmatter replacing Microsoft's, then the body —
    but the fields are the ones a conceptual page actually has. `title`, `description` and
    `ms.topic` are all present on all 34 upstream pages, so nothing here is invented:
    topic is Microsoft's own classification, not a bucket this pipeline made up.
    """
    fm = {
        "title": _ms_field(text, "title"),
        "topic": _ms_field(text, "ms.topic"),
        "summary": _ms_field(text, "description"),
        "source": f"query-languages/dax/{rel_path}"
                  + (f"@{source_sha}" if source_sha else ""),
        "sourceDate": parse_ms_date(text),
    }

    body = _MS_FRONTMATTER_RE.sub("", text, count=1)
    # Cards live in library/, one directory over from concepts/. Same order as the library
    # build: local links first, transclusions inlined, then whatever still points at a
    # query-docs page this repo does not carry becomes an upstream URL.
    body = rewrite_links(body, prefix="../library/")
    if includes_dir:
        body = resolve_includes(body, includes_dir)
    body = absolutise_links(body, base=posixpath.dirname(rel_path))

    return f"---\n{_format_frontmatter(fm)}---\n{body.lstrip()}"


# A relative markdown target inside the generated tree: './all.md', '../library/all.md'.
# Absolute URLs and in-page anchors are somebody else's problem.
_LOCAL_TARGET_RE = re.compile(r'\]\((?!https?://)(?!#)([^)\s#]+\.md)(#[^)]*)?\)')

# How far the counts may move between two syncs before the run stops to ask. Microsoft
# ships a handful of functions at a time; anything near a tenth of the library is the
# parser, not the docs.
MAX_COUNT_DRIFT = 0.05


def broken_local_links(trees, outside=()):
    """(source, target) for every relative link that resolves to nothing, sorted.

    Gate 3, checked in memory so a generation with dangling links never reaches disk. The
    first run of this pipeline shipped 637 broken relative links out of 1755 and exited 0;
    a card promising a page that is not there is worse than one that says nothing.

    `outside` are targets that live OUTSIDE the generated trees and are known to exist —
    today the hand-written `examples/`, which a card links to and the sync never writes.
    Paths are relative to the generated root, so an examples file reads `../examples/...`.
    Without this the gate would call every one of those links broken, which is exactly what
    it did the first time examples were wired in.
    """
    have = {f"{sub}/{stem}.md" for sub, cards in trees.items() for stem in cards}
    have |= set(outside)
    broken = []
    for sub, cards in trees.items():
        for stem, card in cards.items():
            for m in _LOCAL_TARGET_RE.finditer(card):
                target = m.group(1)
                resolved = posixpath.normpath(posixpath.join(sub, target))
                if resolved not in have:
                    broken.append((f"{sub}/{stem}.md", target))
    return sorted(broken)


def orphan_notes(notes, cards):
    """Note stems with no card of the same name, sorted. Gate 2."""
    return sorted(set(notes) - set(cards))


def _previous_counts(out_dir):
    """{functionCount, conceptCount} from the catalog already on disk, or {}.

    Unreadable is treated as absent rather than as an error: a corrupt or hand-edited
    catalog should not be able to block the sync that would replace it.
    """
    import json
    try:
        with open(os.path.join(out_dir, GENERATED, "catalog.json"), encoding="utf-8") as f:
            catalog = json.load(f)
    except (OSError, ValueError):
        return {}
    # Parsing is not the same as being readable. `[]`, `null` and a bare string are all
    # valid JSON, and .get on them raises — the promise above was not being kept. Same for
    # a count that is not a number: it would reach the arithmetic in count_deviation.
    if not isinstance(catalog, dict):
        return {}
    counts = {k: catalog.get(k) for k in ("functionCount", "conceptCount")}
    return {k: v for k, v in counts.items()
            if isinstance(v, int) and not isinstance(v, bool)}


def count_deviation(previous, current, label):
    """A message if the count moved too far since the last sync, else None. Gate 4.

    `previous` is None on a first sync and 0 before anything was built — neither is drift,
    they are the absence of a baseline.
    """
    if not previous:
        return None
    drift = abs(current - previous) / previous
    if drift <= MAX_COUNT_DRIFT:
        return None
    return (f"{label} moved from {previous} to {current} ({drift:.1%}), past the "
            f"{MAX_COUNT_DRIFT:.0%} the sync will accept without being asked. If Microsoft "
            f"really published that many, re-run with --accept-count-change.")


def _publish(out_dir, trees, files):
    """Install the generated tree under generated/.

    `trees` maps a subdirectory name to {stem: markdown} — 'library' and 'concepts'.
    `files` maps a filename at the root of generated/ to its content — the catalogs.
    Both are written whole into staging before anything is swapped, so adding an output
    never adds a step to the install.

    Everything the sync produces lives in one directory, so installing it moves ONE path.
    os.replace cannot land a directory on an existing one — on Windows it raises
    PermissionError even when the target is empty — so the swap is two renames: the
    previous generation moves aside, then the new one takes its place. Each rename is
    atomic, so the only state that can need undoing is the gap between them, and undoing
    it is putting one directory back.

    That single line is the point of the layout. With the library and the two catalogs
    installed as three separate targets, recovery needed per-file backups, an order to
    undo them in, a partial-copy window and bookkeeping for which targets this run had
    created — and every review finding on this pipeline landed in that machinery rather
    than in the generation it was protecting.
    """
    import shutil
    import tempfile
    target = os.path.join(out_dir, GENERATED)

    # Per-run scratch directory: a fixed name would let two syncs against the same tree
    # delete each other's work. Kept inside out_dir so both renames are same-volume.
    #
    # Deliberately NOT locked. Review argued for a lock or a versioned handoff; there is
    # no concurrent-writer scenario here — one repository, one working tree, one weekly
    # cron with cancel-in-progress — and lock machinery for a case that cannot arise is
    # complexity nobody will maintain. Unique names remove the file race; that is the part
    # worth having.
    run = tempfile.mkdtemp(prefix=".publish-", dir=out_dir)
    staging = os.path.join(run, GENERATED)
    retired = os.path.join(run, "prev")

    def stranded():
        """The previous generation is parked in `retired` with nothing at `target`.

        While that holds it is the only copy in existence: the swap did not finish and the
        restore has not put it back. Every decision below reads this off the filesystem
        rather than off a flag, because a flag is set on a bytecode after the call it
        describes, and a signal lands between bytecodes.

        lexists, not isdir: if `target` was a RELATIVE symlink, retiring it moved the link
        itself a directory deeper and its target no longer resolves. isdir answers False on
        a broken link, so the backup would look absent and the cleanup would delete the
        only record of where the tree actually lived. The question here is whether the path
        is occupied, not whether it is usable.
        """
        return os.path.lexists(retired) and not os.path.lexists(target)

    try:
        os.makedirs(staging)
        for sub, cards in trees.items():
            d = os.path.join(staging, sub)
            os.makedirs(d)
            for stem, card in cards.items():
                with open(os.path.join(d, f"{stem}.md"), "w", encoding="utf-8") as f:
                    f.write(card)
        for name, body in files.items():
            with open(os.path.join(staging, name), "w", encoding="utf-8") as f:
                f.write(body)

        if os.path.isdir(target):
            os.replace(target, retired)
        os.replace(staging, target)
    except BaseException:
        # The one recoverable state. A failure before the first rename left the tree
        # untouched, and once the second returns there is nothing partial to undo.
        if stranded():
            try:
                os.replace(retired, target)
            except OSError as restore_error:
                print(f"ROLLBACK FAILED: {restore_error}. The previous generation is kept "
                      f"in {retired} — move it back to {target} by hand before trusting "
                      f"this library.", file=sys.stderr)
        raise
    finally:
        # Re-checked here, not remembered from above. An earlier version recorded "the
        # restore failed" inside an `except OSError`, which a KeyboardInterrupt on the
        # restore skipped entirely — so the cleanup ran and deleted the only copy of the
        # previous generation. Asking the filesystem again cannot be skipped by anything.
        #
        # After a clean run `retired` still exists but `target` holds the new generation,
        # so this is false and the scratch directory goes, old tree and all.
        if not stranded():
            shutil.rmtree(run, ignore_errors=True)


def write_library(dax_dir, out_dir, category_map, docs, overrides,
                  source_sha="", source_date=""):
    """Generate library/<fn>.md plus catalog.json and catalog.md. Returns the entries.

    `out_dir` is the dax-reference skill root. notes/ is read to set the flag and never
    written. Re-running on unchanged input produces an identical tree, so the weekly sync
    PR shows only real upstream movement.

    **Failure-atomic.** Everything is built in memory first; nothing on disk is touched
    until every card and both catalogs exist. An earlier version wiped library/ up front,
    so a parser error on one upstream page left a partial library beside catalogs that
    disagreed with it — precisely the state this pipeline exists to make impossible.
    """
    import json
    notes = _notes_stems(out_dir)
    examples = _examples_index(out_dir)

    cards = {}
    entries = []
    for doc in docs:
        with open(os.path.join(dax_dir, doc), encoding="utf-8") as f:
            text = f.read()
        stem = doc[: -len(FUNCTION_SUFFIX)] if doc.endswith(FUNCTION_SUFFIX) else doc
        cards[stem] = build_library_card(text, doc, category_map, overrides, notes,
                                         source_sha=source_sha,
                                         includes_dir=os.path.join(dax_dir, "includes"),
                                         examples_index=examples)

        entry = category_map.get(doc, {})
        applies_to, discouraged = parse_applies_to(text)
        entries.append({
            "name": entry.get("name") or parse_title(text),
            "file": stem,
            "category": entry.get("category", []),
            "primaryCategory": entry.get("primaryCategory", ""),
            "returns": determine_returns(doc, text, category_map, overrides),
            "appliesTo": applies_to,
            "discouragedInVisualCalculations": bool(discouraged),
            # The summary comes from the index table's description cell, which can carry
            # markdown links. Normalising only the card body left raw paths in both
            # catalogs.
            "summary": absolutise_links(entry.get("summary") or parse_summary(text)),
            "notes": stem in notes,
            "examples": examples.get(stem, ("", 0))[1],
        })

    entries.sort(key=lambda e: e["name"])

    # Pass 3 — the conceptual pages. Not functions, so they carry no signature, return type
    # or applies-to; what they have is Microsoft's own ms.topic and description, used as-is.
    concept_cards, concepts = {}, []
    includes_dir = os.path.join(dax_dir, "includes")
    for rel in discover_concept_docs(dax_dir):
        with open(os.path.join(dax_dir, rel), encoding="utf-8") as f:
            text = f.read()
        slug = concept_slug(rel)
        if slug in concept_cards:
            # Two pages sharing a stem would overwrite each other's card while both still
            # emitted a catalog row — one page gone, and nothing about the output looking
            # wrong. Collision-free across the two directories today; this makes tomorrow
            # a hard failure rather than a silent loss.
            raise ValueError(
                f"two conceptual pages share the slug {slug!r}: {rel} collides with an "
                f"earlier one. Cards are keyed by stem, so one would overwrite the other.")
        concept_cards[slug] = build_concept_card(text, rel, source_sha=source_sha,
                                                 includes_dir=includes_dir)
        concepts.append({
            "file": slug,
            "title": _ms_field(text, "title"),
            "topic": _ms_field(text, "ms.topic"),
            "summary": _ms_field(text, "description"),
            "source": rel,
        })
    concepts.sort(key=lambda c: c["file"])

    source = f"{UPSTREAM_REPO}@{source_sha}" if source_sha else UPSTREAM_REPO
    catalog = {
        "source": source,
        "sourceCommitDate": source_date,
        "functionCount": len(entries),
        "conceptCount": len(concepts),
        "functions": entries,
        "concepts": concepts,
    }
    # --- gates 2 and 3, before anything reaches disk ----------------------------------
    trees = {"library": cards, "concepts": concept_cards}
    orphans = orphan_notes(notes, cards)
    if orphans:
        raise ValueError(
            f"{len(orphans)} note(s) have no card: {', '.join(orphans)}. The catalog would "
            f"flag a function with ★ and send a reader to a file that is not there. Rename "
            f"the note to match the card, or delete it if upstream dropped the function.")
    broken = broken_local_links(
        trees, outside={f"../examples/{cat}/{stem}.md"
                        for stem, (cat, _) in examples.items()})
    if broken:
        shown = ", ".join(f"{src} -> {tgt}" for src, tgt in broken[:5])
        raise ValueError(
            f"{len(broken)} cross-link(s) resolve to nothing: {shown}"
            f"{' ...' if len(broken) > 5 else ''}. A card that promises a page which is "
            f"not there is worse than one that says nothing.")

    _publish(
        out_dir,
        trees,
        {
            "catalog.json": json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
            "catalog.md": _catalog_md(entries, source, source_date),
            # Its own index, not rows in catalog.md: a conceptual question should not have
            # to read 14k tokens of function rows to find the page on evaluation context.
            "concepts.md": _concepts_md(concepts, source, source_date),
        },
    )
    return entries


def load_overrides(path=None):
    """Read overrides.json from the skill root. Missing or unreadable -> {}."""
    import json
    if path is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "overrides.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


USAGE = """Usage: sync_query_docs.py DAX_DIR [--write] [--out DIR] [--accept-count-change]
  DAX_DIR   a query-docs checkout's query-languages/dax
  --write   generate generated/{library/, catalog.json, catalog.md} (default: report only)
  --out     where to write (default: the dax-reference skill root)
  --accept-count-change
            publish even though the function or concept count moved more than
            5% since the last sync. For a real upstream release, not for a hunch"""


def _parse_args(argv):
    """Return (dax_dir, write, out) or None when the arguments are not understood.

    Unknown flags are refused rather than ignored: a typo like --wrote must not look like
    a successful dry run.
    """
    if len(argv) < 2:
        return None
    dax_dir, write, out, accept, i = argv[1], False, None, False, 2
    if dax_dir.startswith("-"):
        return None
    while i < len(argv):
        if argv[i] == "--write":
            write = True
        elif argv[i] == "--accept-count-change":
            accept = True
        elif argv[i] == "--out" and i + 1 < len(argv):
            i += 1
            out = argv[i]
        else:
            return None
        i += 1
    return dax_dir, write, out, accept


def _upstream_stamp(dax_dir):
    """(short sha, commit date) of the checkout dax_dir lives in; ('','') if not a repo."""
    import subprocess
    def _git(*args):
        try:
            r = subprocess.run(["git", "-C", dax_dir, *args], capture_output=True,
                               text=True, timeout=30)
            return r.stdout.strip() if r.returncode == 0 else ""
        except (OSError, subprocess.SubprocessError):
            return ""
    return _git("rev-parse", "--short", "HEAD"), _git("log", "-1", "--format=%cI")


def main(argv):
    """Report on, and optionally generate, the dax-reference library."""
    import json
    parsed = _parse_args(argv)
    if parsed is None:
        print(USAGE, file=sys.stderr)
        return 2
    _, do_write, out_dir, accept_count_change = parsed
    # Windows consoles default to cp1252; the docs are full of non-ASCII punctuation and
    # would come out mojibake (or crash the consumer) without this. Guarded because a
    # redirected or captured stream (tests, embedding) has no reconfigure().
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    dax_dir = parsed[0]
    indexes = discover_indexes(dax_dir)
    if not indexes:
        print(f"ERROR: no '*{INDEX_SUFFIX}' found in {dax_dir}", file=sys.stderr)
        return 1
    mapping = build_category_map(indexes)
    from_indexes = len(mapping)
    docs = discover_function_docs(dax_dir)
    apply_filename_rules(mapping, docs)
    try:
        # The valid categories are the index filenames themselves, so a genuinely new one
        # is accepted the moment Microsoft ships its index.
        toc = parse_toc(read_toc(dax_dir), {category_of(fn) for _, fn in indexes})
    except OSError:
        print(f"ERROR: no {TOC_FILE} in {dax_dir}. It is upstream's own table of contents "
              f"and the only route to a category for the functions no index lists — "
              f"running without it would silently drop them.", file=sys.stderr)
        return 1
    except ValueError as drift:
        print(f"ERROR: {drift}", file=sys.stderr)
        return 1
    # Measured BEFORE the TOC fills anything. The floor exists to catch the category-index
    # parser breaking, and the TOC alone classifies 459 of the 479 real docs — applying it
    # first let an index parser that matched NOTHING still clear a 90% floor and publish.
    # A fallback that can stand in for the thing it is a fallback for hides its failure.
    before_toc = sorted(d for d in docs if d not in mapping)
    from_toc = apply_toc(mapping, toc, docs)
    leftover = sorted(d for d in docs if d not in mapping)
    multi = [k for k, v in mapping.items() if len(v["category"]) > 1]

    # An index can point at a doc that is not a per-function page (e.g. table-Constructor.md).
    # Counting those as coverage would overstate it, so report them separately.
    non_function = sorted(set(mapping) - set(docs))

    print(f"{len(indexes)} indexes -> {from_indexes} entries "
          f"({len(multi)} in more than one category)", file=sys.stderr)
    print(f"filename rules -> {len(mapping) - from_indexes - len(from_toc)} more",
          file=sys.stderr)
    print(f"toc.yml -> {len(from_toc)} more", file=sys.stderr)
    print(f"coverage: {len(docs) - len(leftover)} / {len(docs)} function docs categorized",
          file=sys.stderr)
    if non_function:
        print(f"listed but not a function doc ({len(non_function)}): "
              f"{', '.join(non_function)}", file=sys.stderr)
    if leftover:
        print(f"NO CATEGORY YET ({len(leftover)}) — pass 2 (applies-to) or overrides.json:",
              file=sys.stderr)
        for doc in leftover:
            print(f"  {doc[: -len(FUNCTION_SUFFIX)].upper()}", file=sys.stderr)

    # Reporting a collapse on stderr and still exiting 0 would let silent parser drift
    # look like a clean run — the exact failure this pipeline exists to catch.
    if not docs:
        print(f"ERROR: no '*{FUNCTION_SUFFIX}' found in {dax_dir}", file=sys.stderr)
        return 1
    coverage = (len(docs) - len(before_toc)) / len(docs)
    if coverage < MIN_COVERAGE:
        print(f"ERROR: the category indexes and filename rules cover {coverage:.1%} of the "
              f"function docs, below the {MIN_COVERAGE:.0%} floor — the upstream format "
              f"probably shifted and the parser needs attention. toc.yml is not counted "
              f"here on purpose: it would cover for the very parser this floor watches.",
              file=sys.stderr)
        return 1
    # --- gate 1: no category by any of the four routes --------------------------------
    overrides = load_overrides()
    declared = set((overrides.get("uncategorized") or {}).get("functions") or [])
    undeclared = uncategorized_gate(leftover, declared)
    if undeclared:
        print(f"ERROR: {len(undeclared)} function(s) end up with no category by any route "
              f"— category index, filename rule, toc.yml or overrides.json: "
              f"{', '.join(undeclared)}. Either upstream stopped listing them, or the "
              f"parser regressed. If they really are unclassified upstream, add them to "
              f"'uncategorized' in overrides.json so the omission is on record.",
              file=sys.stderr)
        return 1
    stale = stale_uncategorized(leftover, declared)
    if stale:
        print(f"ERROR: overrides.json declares {', '.join(stale)} as unclassified "
              f"upstream, but {'they now have' if len(stale) > 1 else 'it now has'} a "
              f"category. Remove the name(s) — a list nobody rechecks is how the old "
              f"ceiling rotted.", file=sys.stderr)
        return 1

    # --- pass 2 -------------------------------------------------------------------
    # Shipping the per-function parsers without running them here is how a sync exits 0
    # having done only pass 1. Every doc is parsed and both ceilings are ZERO, measured:
    # all 479 real docs carry a recognisable applies-to include, and the only 3 without a
    # Return value section (DATEVALUE, DEGREES, RADIANS) are pinned in overrides.json.
    no_applies, no_returns = [], []
    for doc in docs:
        try:
            with open(os.path.join(dax_dir, doc), encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"ERROR: cannot read {doc}: {e}", file=sys.stderr)
            return 1
        contexts, _ = parse_applies_to(text)
        if not contexts:
            no_applies.append(doc)
        if not determine_returns(doc, text, mapping, overrides):
            no_returns.append(doc)

    print(f"pass 2: parsed {len(docs)} function docs "
          f"({len(no_applies)} without applies-to, {len(no_returns)} without a return type)",
          file=sys.stderr)

    def _report(label, docs_, hint):
        print(f"ERROR: {len(docs_)} doc(s) {label} — {hint}", file=sys.stderr)
        for doc in docs_[:20]:
            print(f"  {doc[: -len(FUNCTION_SUFFIX)].upper()}", file=sys.stderr)
        if len(docs_) > 20:
            print(f"  ... and {len(docs_) - 20} more", file=sys.stderr)

    if no_applies:
        _report("with no recognisable applies-to include", no_applies,
                "Microsoft probably added an include variant. Add it to APPLIES_TO_MAP "
                "rather than letting the card claim a permission the page never granted.")
        return 1
    if no_returns:
        _report("with no resolvable return type", no_returns,
                "no '## Return value' section and no overrides.json entry. Pin the real "
                "type in overrides rather than defaulting it.")
        return 1

    # Before publishing, not after. A warning printed once the swap has already happened
    # ships an incomplete concept set and passes CI unless somebody reads stderr — which
    # is the same as not checking. This is upstream drift, so it stops the run like the
    # other drift guards above.
    unlisted = unlisted_content_dirs(dax_dir)
    if unlisted:
        print(f"ERROR: {len(unlisted)} directory(ies) under query-languages/dax/ hold pages "
              f"this sync does not read: {', '.join(unlisted)}. Add each to CONCEPT_DIRS if "
              f"it is documentation, or to NON_CONTENT_DIRS if it is not — do not let pages "
              f"go missing from concepts/ without a decision.", file=sys.stderr)
        return 1

    if do_write:
        if out_dir is None:
            out_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # --- gate 4: how far the counts moved since the last sync ---------------------
        # The previous catalog.json is already on disk, so "compared with the last sync"
        # needs no state file of its own — and cannot drift out of step with the tree it
        # describes.
        previous = _previous_counts(out_dir)
        drifted = [m for m in (count_deviation(previous.get(k), n, k)
                               for k, n in (("functionCount", len(docs)),
                                            ("conceptCount",
                                             len(discover_concept_docs(dax_dir)))))
                   if m]
        if drifted and not accept_count_change:
            for message in drifted:
                print(f"ERROR: {message}", file=sys.stderr)
            return 1
        if drifted:
            for message in drifted:
                print(f"accepted by --accept-count-change: {message}", file=sys.stderr)

        sha, date = _upstream_stamp(dax_dir)
        try:
            entries = write_library(dax_dir, out_dir, mapping, docs, overrides,
                                    source_sha=sha, source_date=date)
        except ValueError as gate:
            # Gates 2 and 3 live inside write_library because they judge the cards, which
            # only exist there. Nothing was published — they run before the swap.
            print(f"ERROR: {gate}", file=sys.stderr)
            return 1
        stamp = f"{UPSTREAM_REPO}@{sha}" if sha else UPSTREAM_REPO
        print(f"wrote {len(entries)} cards + {len(discover_concept_docs(dax_dir))} "
              f"concepts + catalog.json + catalog.md + concepts.md to "
              f"{os.path.join(out_dir, GENERATED)} ({stamp})", file=sys.stderr)
        return 0

    json.dump(mapping, sys.stdout, indent=2, ensure_ascii=False, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
