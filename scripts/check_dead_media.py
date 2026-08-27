#!/usr/bin/env python3
"""Fail when a generated card points an image at the upstream host that is gone.

`MicrosoftDocs/query-docs` returned 404 in August 2026 and the tree is frozen at its stamp
(`docs/decisions/2026-08-27-generated-is-frozen-at-323524c.md`). The prose survived that;
the pictures did not. 87 image URLs across 33 files pointed at
`raw.githubusercontent.com/MicrosoftDocs/query-docs/...`, and 47 of them were in the eight
conceptual pages — the ones read to understand the language rather than one function.

The images are not lost. Microsoft Learn serves every one of them, at a path derived from
the upstream one by swapping the prefix, and **all 87 were verified to answer 200** before
this was written. So they are pointed there: alive, canonical, the same CC BY 4.0 material,
and no dependency on a third-party archive.

  https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/query-languages/dax/X
  https://learn.microsoft.com/en-us/dax/X

    python scripts/check_dead_media.py          # gate: fail if any dead-host URL is left
    python scripts/check_dead_media.py --fix     # rewrite them
    python scripts/check_dead_media.py --online  # also HTTP-check every image (slow)

The gate is **offline**. It compares text against a host known to be gone, which is
deterministic and costs nothing. Fetching 87 URLs on every pull request would be slow, and
worse, it would make a green build depend on someone else's uptime — a gate that fails when
learn.microsoft.com has a bad minute teaches people to re-run it, which is how a gate stops
being read. `--online` is there for the day someone wants to re-verify by hand.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED = os.path.join(ROOT, "skills", "dax-reference", "generated")

# The exact prefix the sync used to write. Narrow on purpose: this gate knows about one
# host that is known to be gone, and says so. A general "is every URL alive" check is a
# different tool and it needs the network.
DEAD_PREFIX = ("https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/"
               "query-languages/dax/")
LIVE_PREFIX = "https://learn.microsoft.com/en-us/dax/"

_URL_RE = re.compile(re.escape(DEAD_PREFIX) + r"[^)\s\"']+")


def _files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(dirnames)
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def scan(root=GENERATED):
    """(urls, files) — every dead-host URL and the files carrying them."""
    urls, files = [], {}
    for path in _files(root):
        with open(path, encoding="utf-8") as f:
            found = _URL_RE.findall(f.read())
        if found:
            rel = os.path.relpath(path, root).replace("\\", "/")
            files[rel] = len(found)
            urls += found
    return urls, files


def fix(root=GENERATED):
    """Rewrite the dead prefix to the live one. Returns the files changed."""
    changed = []
    for path in _files(root):
        with open(path, encoding="utf-8") as f:
            before = f.read()
        after = before.replace(DEAD_PREFIX, LIVE_PREFIX)
        if after != before:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(after)
            changed.append(os.path.relpath(path, root).replace("\\", "/"))
    return changed


def check_online(root=GENERATED):
    """Every image URL in the tree, fetched. Returns the ones that do not answer 200."""
    import urllib.request
    import urllib.error
    seen, bad = set(), []
    pattern = re.compile(r"https://[^)\s\"']+\.(?:png|jpg|jpeg|gif|svg)")
    for path in _files(root):
        with open(path, encoding="utf-8") as f:
            for url in pattern.findall(f.read()):
                if url in seen:
                    continue
                seen.add(url)
                try:
                    req = urllib.request.Request(url, method="HEAD")
                    with urllib.request.urlopen(req, timeout=30) as r:
                        if r.status != 200:
                            bad.append((url, r.status))
                except Exception as exc:                      # noqa: BLE001
                    bad.append((url, getattr(exc, "code", type(exc).__name__)))
    return len(seen), bad


def main(argv):
    if "--fix" in argv:
        changed = fix()
        print(f"rewrote image URLs in {len(changed)} file(s) "
              f"from the dead upstream host to learn.microsoft.com.")
        return 0

    if "--online" in argv:
        total, bad = check_online()
        print(f"checked {total} image URL(s) over the network.")
        for url, status in bad:
            print(f"  {status}  {url}")
        return 1 if bad else 0

    urls, files = scan()
    if not urls:
        print("OK: no generated card points an image at the upstream host that is gone.")
        return 0
    print(f"ERROR: {len(urls)} image URL(s) in {len(files)} file(s) still point at "
          f"{DEAD_PREFIX} — a host that has returned 404 since 2026-08. "
          f"Run: python scripts/check_dead_media.py --fix")
    for rel, n in sorted(files.items(), key=lambda kv: -kv[1])[:15]:
        print(f"  {n:>3}  {rel}")
    if len(files) > 15:
        print(f"  ... and {len(files) - 15} more file(s)")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
