#!/usr/bin/env python3
"""Rebuild a `query-languages/dax/` source tree from Microsoft Learn.

`MicrosoftDocs/query-docs` returns 404 and every surviving copy of its markdown is older
than the tree here, so `generated/` is frozen — see
`docs/decisions/2026-08-27-generated-is-frozen-at-323524c.md`. Learn is the one source that
is both alive and current. It serves HTML, not markdown, which is why this exists.

**It does not build cards.** It writes markdown shaped like the upstream repository, so
`sync_query_docs.py` runs against it unchanged. That is the whole design: the categorising,
the four publish gates, the link rewriting and the 253 tests behind them stay exactly as
they are, and only the fetch is new. A second card builder would be a second definition of
what a card is, and the first thing to rot.

    python skills/dax-reference/scripts/fetch_from_learn.py DEST [--limit N] [--only SLUG]
    python skills/dax-reference/scripts/sync_query_docs.py DEST --write --out ...

Fetched HTML is cached under DEST/.cache so a re-run costs nothing. 513 pages is a lot to
ask of someone else's servers; ask once.
"""
import argparse
import html as html_mod
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

LEARN = "https://learn.microsoft.com/en-us/dax/"
TOC = LEARN + "toc.json"

# The five applies-to includes the sync knows, keyed by the icons Learn prints. Read off
# all 479 function pages rather than inferred from a few: the counts below add up to 479
# exactly, with no page falling outside the table and no key matching two includes.
#
# The order is the order the page prints: calculated column, calculated table, measure,
# visual calculation — and, on the INFO.* pages only, a FIFTH entry, "DAX query". That
# fifth one is why the query-only key is five long. A four-icon guess for it looked right
# against the top of the page and left all 68 INFO.* functions declaring nothing, which
# is how it was caught: by checking every page instead of a sample.
#
# `discouraged.png` is its own icon, and it is the only thing separating the discouraged
# variant from the plain one — both show three yeses and a fourth entry. Reading that
# fourth as a boolean puts 49 functions in the wrong include and drops the warning
# Microsoft prints directly underneath it.
APPLIES_TO_BY_ICONS = {
    # 312 functions
    ("yes", "yes", "yes", "yes"): "applies-to-measures-columns-tables-visual-calculations",
    # 49
    ("yes", "yes", "yes", "discouraged"):
        "applies-to-measures-columns-tables-visual-calculations-discouraged",
    # 36
    ("yes", "yes", "yes", "no"): "applies-to-measures-columns-tables",
    # 14
    ("no", "no", "no", "yes"): "applies-to-visual-calculations",
    # 68 — the fifth icon is "DAX query"
    ("no", "no", "no", "no", "yes"): "applies-to-query-only",
}

# `Applies to:` is bold and linked on most pages and plain text on the query-only ones.
# Matching the strong/anchor form only found four of the five variants and silently left
# the INFO.* pages with no claim at all.
_APPLIES_BLOCK = re.compile(r"<p>(?:<strong>)?Applies to:.*?</p>", re.S)
_ICON = re.compile(r'<img src="media/icons/(yes|no|discouraged)\.png"')
# A Learn page has TWO `<div class="content">`: the first wraps the h1 and the page
# furniture around it, the second is the article. Taking the first one — the obvious
# reading — returns the title block, the feedback button and the "Summarize this article"
# widget, and none of the prose.
_CONTENT_DIV = re.compile(r'<div class="content"[^>]*>')
_FEEDBACK = re.compile(r'<h2[^>]*>\s*Feedback\s*</h2>')
_H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
_META = re.compile(r'<meta name="([^"]+)" content="([^"]*)"')


def toc_slugs(text=None):
    """Every DAX page Learn lists, in its own order.

    Read from the table of contents rather than guessed from filenames: the repository
    layout was never the URL route, and inventing slugs is how a fetch silently misses a
    page Microsoft added.
    """
    doc = json.loads(text) if text is not None else json.loads(_get(TOC))
    slugs, seen = [], set()

    def walk(items):
        for item in items or []:
            if not isinstance(item, dict):
                continue
            href = item.get("href") or ""
            # Only same-area relative pages. `https://aka.ms/...` and `../power-bi/...`
            # are real entries in this toc and neither is a DAX page.
            if href and "://" not in href and not href.startswith(("/", "#", "..")):
                slug = href.split("#")[0].rstrip("/")
                if slug and slug not in ("./", ".") and slug not in seen:
                    seen.add(slug)
                    slugs.append(slug)
            walk(item.get("children"))

    walk(doc.get("items") if isinstance(doc, dict) else doc)
    return slugs


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"user-agent": "dax-for-agents/sync"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def fetch(slug, cache_dir):
    """The page's HTML, from the cache when it is there."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, slug.replace("/", "__") + ".html")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    text = _get(LEARN + slug)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return text


def page_meta(page):
    """The `<meta name=... content=...>` pairs, unescaped."""
    return {k: html_mod.unescape(v) for k, v in _META.findall(page)}


def applies_to_include(page):
    """The include stem the upstream page carried, or None when the block is unreadable.

    None is not "no claim it applies anywhere" — it is "this fetch did not understand the
    page", and the caller has to stop rather than write a card asserting the permissive
    default. That is the same rule `parse_applies_to` follows for the same reason.
    """
    m = _APPLIES_BLOCK.search(page)
    if not m:
        return None
    icons = tuple(_ICON.findall(m.group(0)))
    return APPLIES_TO_BY_ICONS.get(icons)


def heading(page):
    """The page's own `<h1>`, which is the function name as the document states it."""
    m = _H1.search(page)
    return html_mod.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""


def article(page):
    """The article body: the LAST content div, up to Learn's own Feedback heading.

    Everything after that heading is site furniture — feedback widgets, related links,
    the footer — and it is not part of the document Microsoft authored. Everything before
    the last content div is the title block, which is the same thing at the other end.
    """
    end = _FEEDBACK.search(page)
    limit = end.start() if end else len(page)
    starts = [m.end() for m in _CONTENT_DIV.finditer(page) if m.end() < limit]
    if not starts:
        return ""
    body = page[starts[-1]:limit]
    # The applies-to paragraph becomes the [!INCLUDE] line, so it must not survive as prose.
    return _APPLIES_BLOCK.sub("", body, count=1)


# Learn's own note boxes, and the shortcode each one came from upstream.
ALERTS = {"NOTE": "NOTE", "TIP": "TIP", "IMPORTANT": "IMPORTANT",
          "WARNING": "WARNING", "CAUTION": "CAUTION"}

_LEARN_PAGE = re.compile(r"^/[a-z]{2}-[a-z]{2}/dax/(?:.*/)?([a-z0-9][a-z0-9.\-]*)/?$")
_LOCALE = re.compile(r"^/[a-z]{2}-[a-z]{2}/")


def upstream_href(href):
    """Turn a Learn URL back into the link the upstream markdown carried.

    This is not cosmetic. `sync_query_docs.rewrite_links` recognises exactly one shape --
    `other-function-dax.md` -- and turns it into a local `./other.md`, which is what makes
    the library navigable without leaving it. A card full of absolute learn.microsoft.com
    links would pass every gate and send an agent to the internet for a page it already
    has on disk.

    Site-absolute links keep their path and lose the locale, because that is how upstream
    writes them: `/power-bi/transform-model/...`, never `/en-us/power-bi/...`.
    """
    if not href or href.startswith(("#", "mailto:")):
        return href
    if href.startswith("http"):
        return href
    path, _, anchor = href.partition("#")
    suffix = ("#" + anchor) if anchor else ""
    m = _LEARN_PAGE.match(path)
    if m:
        return m.group(1) + ".md" + suffix
    # Learn writes most in-area links relative, exactly as upstream did minus the
    # extension: `sign-function-dax`, not `sign-function-dax.md`. Without putting it back,
    # `rewrite_links` does not recognise them and the library stops linking to itself.
    if path and not path.startswith("/") and "." not in path.rsplit("/", 1)[-1]:
        return path + ".md" + suffix
    return _LOCALE.sub("/", path) + suffix


class _Markdown(HTMLParser):
    """Learn's rendered article back into markdown of the shape the sync expects.

    Deliberately narrow. It handles the constructs this corpus actually uses -- headings,
    paragraphs, fenced code, tables, lists, note boxes, links, images and inline emphasis
    -- and nothing else. A general-purpose converter would be more code and less checkable:
    the fidelity test is a diff against a real copy of the upstream markdown, and that only
    means something for constructs the corpus contains.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []          # finished block strings
        self.text = []            # the inline run being accumulated
        self.pre = None           # language of the fenced block being read
        self.lists = []           # 'ul' or an int counter for 'ol'
        self.rows = None          # table rows, each a list of cell strings
        self.cell = None
        self.alert = None
        self.alert_blocks = None
        self.href = []
        self.depth_skip = 0
        self._last_item = False

    # -- helpers ---------------------------------------------------------------
    def _flush(self, prefix="", list_item=False):
        run = "".join(self.text).strip()
        self.text = []
        if run:
            self._emit(prefix + run, list_item)

    def _emit(self, block, list_item=False):
        target = self.alert_blocks if self.alert is not None else self.blocks
        # A list is one block. Emitting an item per block put a blank line between every
        # bullet, which markdown reads as a loose list and renders with extra spacing.
        if list_item and target and self._last_item:
            target[-1] += "\n" + block
        else:
            target.append(block)
        self._last_item = list_item

    def result(self):
        self._flush()
        return "\n\n".join(b for b in self.blocks if b.strip()) + "\n"

    # -- tags ------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.depth_skip:
            self.depth_skip += 1
            return
        if tag in ("nav", "button", "script", "style", "form"):
            self.depth_skip = 1
            return
        if tag == "div":
            kind = (a.get("class") or "").strip().upper()
            if kind in ALERTS:
                self._flush()
                self.alert, self.alert_blocks = ALERTS[kind], []
            return
        if tag in ("h1", "h2", "h3", "h4", "p", "li"):
            self._flush()
        elif tag == "pre":
            self._flush()
            # The mode has to open HERE, not on the <code> inside. Opening it there let
            # `<code>` take the inline branch, so every fenced block came out as a
            # one-line `code span` with its language dropped and its whitespace collapsed.
            self.pre = ""
        elif tag == "code" and self.pre is None:
            self.text.append("`")
        elif tag == "code" and self.pre is not None:
            self.pre = (a.get("class") or "").replace("lang-", "").strip()
        elif tag in ("strong", "b"):
            self.text.append("**")
        elif tag in ("em", "i"):
            self.text.append("*")
        elif tag == "a":
            self.href.append(upstream_href(a.get("href", "")))
            self.text.append("[")
        elif tag == "img":
            src = a.get("src", "")
            alt = a.get("alt", "") or a.get("alt-text", "")
            self.text.append(f"![{alt}]({src})")
        elif tag == "br":
            # Inside a table cell a newline ENDS THE ROW, so a `<br>` turned into one
            # splits the cell into lines markdown reads as body text and the table loses
            # its shape. Upstream writes the literal tag there; so does this. The INFO.*
            # pages are full of them — one cell listing a dozen column types.
            self.text.append("<br/>" if self.cell is not None else "\n")
        elif tag in ("ul", "ol"):
            self._flush()
            self.lists.append(0 if tag == "ol" else "ul")
        elif tag == "table":
            self._flush()
            self.rows = []
        elif tag in ("th", "td"):
            self.cell = []
            self.text = []
        elif tag == "tr" and self.rows is not None:
            self.rows.append([])

    def handle_endtag(self, tag):
        if self.depth_skip:
            self.depth_skip -= 1
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self._flush("#" * int(tag[1]) + " ")
        elif tag == "p":
            self._flush()
        elif tag == "pre":
            code = "".join(self.text).rstrip("\n")
            self.text = []
            self._emit(f"```{self.pre or ''}\n{code}\n```")
            self.pre = None
        elif tag == "code" and self.pre is None:
            self.text.append("`")
        elif tag in ("strong", "b"):
            self.text.append("**")
        elif tag in ("em", "i"):
            self.text.append("*")
        elif tag == "a":
            self.text.append(f"]({self.href.pop() if self.href else ''})")
        elif tag == "li":
            marker = "- "
            if self.lists and self.lists[-1] != "ul":
                self.lists[-1] += 1
                marker = f"{self.lists[-1]}. "
            self._flush(marker, list_item=True)
        elif tag in ("ul", "ol"):
            if self.lists:
                self.lists.pop()
        elif tag in ("th", "td"):
            if self.rows:
                self.rows[-1].append("".join(self.text).strip())
            self.text = []
            self.cell = None
        elif tag == "table":
            self._emit(self._table())
            self.rows = None
        elif tag == "div" and self.alert is not None:
            self._flush()
            body = "\n>\n".join("\n".join("> " + line for line in b.splitlines())
                                for b in self.alert_blocks)
            kind, self.alert, self.alert_blocks = self.alert, None, None
            # The first paragraph of a Learn note box is the word "Note" -- the rendering
            # of the shortcode itself. Keeping it would put "> Note" under "> [!NOTE]".
            body = "\n".join(line for line in body.splitlines()
                              if line.strip().lower() not in ("> " + kind.lower(), ">"))
            self.blocks.append(f"> [!{kind}]\n{body}" if body.strip() else f"> [!{kind}]")

    def handle_data(self, data):
        if self.depth_skip:
            return
        if self.pre is not None:
            self.text.append(data)
        else:
            self.text.append(re.sub(r"\s+", " ", data))

    def _table(self):
        rows = [r for r in (self.rows or []) if r]
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        head, body = rows[0], rows[1:]
        lines = ["|" + "|".join(head) + "|",
                 "|" + "|".join(["---"] * width) + "|"]
        lines += ["|" + "|".join(r) + "|" for r in body]
        return "\n".join(lines)


def to_markdown(body):
    """The article body as markdown. Empty in, empty out."""
    if not body.strip():
        return ""
    parser = _Markdown()
    parser.feed(body)
    parser.close()
    return parser.result()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("dest", help="directory to write the query-docs-shaped tree into")
    ap.add_argument("--limit", type=int, help="only the first N pages")
    ap.add_argument("--only", action="append", help="only this slug (repeatable)")
    ap.add_argument("--report", action="store_true",
                    help="do not write markdown; report what the pages say")
    args = ap.parse_args(argv)

    cache = os.path.join(args.dest, ".cache")
    slugs = args.only or toc_slugs()
    if args.limit:
        slugs = slugs[:args.limit]
    print(f"{len(slugs)} page(s) from the Learn table of contents")

    unreadable = []
    for i, slug in enumerate(slugs, 1):
        try:
            page = fetch(slug, cache)
        except Exception as exc:                              # noqa: BLE001
            print(f"  {slug}: FETCH FAILED ({type(exc).__name__})")
            unreadable.append((slug, "fetch"))
            continue
        include = applies_to_include(page)
        meta = page_meta(page)
        if args.report:
            print(f"  {slug:<46} {include or '(UNREADABLE)':<62} "
                  f"ms.date={meta.get('ms.date', '')[:10]}")
        if include is None and slug.endswith("-function-dax"):
            unreadable.append((slug, "applies-to"))
        if i % 50 == 0:
            print(f"  ... {i}/{len(slugs)}")

    if unreadable:
        print(f"\n{len(unreadable)} page(s) this fetch does not understand:")
        for slug, why in unreadable[:20]:
            print(f"  {why:<12} {slug}")
        return 1
    print("\nOK: every function page read a known applies-to variant.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
