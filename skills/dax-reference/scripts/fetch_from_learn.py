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
_ARTICLE = re.compile(r'<div class="content">(.*?)(?=<h2[^>]*>\s*Feedback\s*</h2>|$)', re.S)
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


def article(page):
    """The article body: from the content div to just before Learn's own Feedback heading.

    Everything after that heading is site furniture — feedback widgets, related links,
    the footer — and it is not part of the document Microsoft authored.
    """
    m = _ARTICLE.search(page)
    if not m:
        return ""
    body = m.group(1)
    # The applies-to paragraph becomes the [!INCLUDE] line, so it must not survive as prose.
    return _APPLIES_BLOCK.sub("", body, count=1)


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
