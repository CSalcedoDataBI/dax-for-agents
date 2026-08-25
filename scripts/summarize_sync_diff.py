#!/usr/bin/env python3
"""Split a regenerated `generated/` diff into what actually changed and what is the stamp.

Every card carries the upstream commit it came from:

    source: query-languages/dax/abs-function-dax.md@c6a9a72

so any upstream move rewrites one line in all 479 of them plus the three indexes,
whether or not a word of DAX documentation changed. Measured on the first real run: 516
files, 517 insertions, 517 deletions, and **zero** files with anything but the stamp in
them. A weekly pull request of that shape is unreadable, and the week it does carry a
real change looks exactly like the weeks it does not.

So the diff gets classified before a person is asked to read it: the pull request body
says which functions changed and which files only moved their stamp.

Reads a `git diff -U0` on stdin.

Run: git diff -U0 -- skills/dax-reference/generated |
       python scripts/summarize_sync_diff.py --old-sha c6a9a72 --new-sha 323524c
"""
import re
import sys
import argparse

# Only the two index files carry it, and it moves with the stamp for the same reason.
_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?")
_FILE_HEADER = re.compile(r"^diff --git a/(\S+) b/(\S+)$")
# 7 is git's shortest abbreviation, 40 a full SHA-1. Only tokens that turn out to be one
# of the two commits are flattened, so a hex string in the prose survives untouched.
_HEX_TOKEN = re.compile(r"\b[0-9a-f]{7,40}\b")


def _same_commit(token, sha):
    """Whether an abbreviated and a full SHA name the same commit.

    They are never written the same length: `git ls-remote` hands the workflow 40 hex
    characters and the cards carry the 7 that `rev-parse --short` produced. Comparing
    them literally matched nothing, so every one of 516 stamp-only files was reported
    as a real change — the wall this script exists to prevent, rebuilt by the caller.
    """
    return bool(sha) and (sha.startswith(token) or token.startswith(sha))


def _normalise(line, old_sha, new_sha):
    """The line with everything that moves on every sync flattened out."""
    def flatten(match):
        token = match.group(0)
        if _same_commit(token, old_sha) or _same_commit(token, new_sha):
            return "<SHA>"
        return token

    line = _HEX_TOKEN.sub(flatten, line)
    # Only on the two lines that carry the upstream commit date. Flattening timestamps
    # everywhere would take a date out of a card's prose -- the date functions are full
    # of worked examples -- and a real change to one would read as no change at all.
    if "sourceCommitDate" in line or "<SHA>" in line:
        line = _TIMESTAMP.sub("<DATE>", line)
    return line


def classify(diff_text, old_sha="", new_sha=""):
    """Return (substantive, stamp_only): two sorted lists of paths.

    A file is stamp-only when its removed and added lines are the same text once the two
    commit SHAs and any timestamp are flattened. An added or deleted file has lines on
    one side only, so it falls out of that comparison as substantive on its own -- a
    function appearing or disappearing upstream is the most interesting thing this
    pipeline can report and must never be filed under noise.

    A file with no changed lines at all is substantive too. That is a rename or a mode
    change: nothing was compared, and "we compared nothing" is not the same claim as
    "nothing changed".

    Hunk by hunk, not file by file. Text moved from one place in a card to another shows
    up as a removal in one hunk and the identical addition in another; pooling the whole
    file makes those cancel out and the move disappears from the report.
    """
    files, renamed = {}, set()
    path = hunk = None
    for line in diff_text.splitlines():
        header = _FILE_HEADER.match(line)
        if header:
            path = header.group(2)
            files[path] = []
            hunk = None
            continue
        if path is None:
            continue
        if line.startswith("@@"):
            hunk = {"removed": [], "added": []}
            files[path].append(hunk)
        elif hunk is None and line.startswith(("rename from", "rename to")):
            # A rename arrives with the stamp hunk beside it, and that hunk balances,
            # so judging on hunks alone filed the whole thing as noise -- a function
            # renamed upstream would have vanished from the report entirely.
            renamed.add(path)
        elif hunk is None:
            # Everything before the first @@ is header: ---, +++, index, mode. Matching
            # those by their text instead would eat content, because a DAX comment reads
            # `-- like this` and a removed one arrives as `--- like this`. A card whose
            # only real change was a deleted comment would have passed as stamp-only.
            continue
        elif line.startswith("-"):
            hunk["removed"].append(_normalise(line[1:], old_sha, new_sha))
        elif line.startswith("+"):
            hunk["added"].append(_normalise(line[1:], old_sha, new_sha))

    substantive, stamp_only = [], []
    for path, hunks in files.items():
        # In order within a hunk, not as sets: upstream reordering a card's lines without
        # changing a word is still a change, and sorted lists would file it as noise.
        if path not in renamed and hunks and all(h["removed"] == h["added"]
                                                 for h in hunks):
            stamp_only.append(path)
        else:
            substantive.append(path)
    return sorted(substantive), sorted(stamp_only)


def _name_of(path):
    """'…/library/abs.md' -> 'abs'. Anything else keeps its path."""
    for marker in ("/generated/library/", "/generated/concepts/"):
        if marker in path:
            return path.split(marker, 1)[1].rsplit(".md", 1)[0]
    return path


def render(substantive, stamp_only, old_sha="", new_sha="", limit=40):
    """The pull request body: what a person has to look at, first."""
    total = len(substantive) + len(stamp_only)
    # Abbreviated for reading: the workflow hands this the 40-character SHA `ls-remote`
    # printed, and a title carrying all of it is unreadable in a PR list.
    short = (lambda s: s[:7])
    move = f"`{short(old_sha)}` → `{short(new_sha)}`" if old_sha and new_sha else "upstream"
    lines = [f"Regenerated from {move}.", ""]
    if not total:
        lines.append("**Nothing changed.** No file differs, not even the stamp — which "
                     "should be impossible when the commit moved, so read this as the "
                     "sync not having run rather than as good news.")
        return "\n".join(lines)

    if substantive:
        lines.append(f"## {len(substantive)} file(s) changed for real")
        lines.append("")
        for path in substantive[:limit]:
            lines.append(f"- `{_name_of(path)}`")
        if len(substantive) > limit:
            lines.append(f"- …and {len(substantive) - limit} more")
        lines.append("")
        lines.append("**Read these.** The rest of the diff is the stamp.")
    else:
        lines.append("## Nothing changed except the stamp")
        lines.append("")
        lines.append(f"All {total} files differ only in the upstream commit they name. "
                     f"Upstream moved without touching anything this pipeline reads, so "
                     f"there is nothing to review — merging just records the new commit.")
    lines.append("")
    lines.append(f"<sub>{len(substantive)} substantive · {len(stamp_only)} stamp-only · "
                 f"{total} total</sub>")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--old-sha", default="")
    parser.add_argument("--new-sha", default="")
    parser.add_argument("--limit", type=int, default=40,
                        help="how many substantive files to name before summarising")
    args = parser.parse_args(argv)
    # The body is markdown bound for GitHub, so it keeps its arrows and middots. A
    # Windows console defaults to cp1252 and would crash on them instead of printing.
    for stream in (sys.stdin, sys.stdout):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    substantive, stamp_only = classify(sys.stdin.read(), args.old_sha, args.new_sha)
    print(render(substantive, stamp_only, args.old_sha, args.new_sha, args.limit))
    return 0


if __name__ == "__main__":
    sys.exit(main())
