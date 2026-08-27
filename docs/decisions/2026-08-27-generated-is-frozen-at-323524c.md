# `generated/` is frozen at `@323524c`, and stays a derived artifact

**Date:** 2026-08-27 · **Status:** accepted · **Affects:** `skills/dax-reference/generated/`,
`sync-check.yml`, `NOTICE`, and [issue #7](https://github.com/CSalcedoDataBI/dax-for-agents/issues/7)

## The problem

`MicrosoftDocs/query-docs` — the repository every one of the 479 cards and 34 concept pages
derives from — returns 404. Unauthenticated, on `github.com`, on `api.github.com` and on
`raw.githubusercontent.com` alike. Re-verified on the day of this record.

The issue framed it as a fork in the road: re-point the sync at some other source, or accept
that `generated/` is frozen and drop the "never edit by hand" invariant that only makes sense
while something can rewrite the directory.

It turned out to be neither, and the reason is worth writing down, because the obvious
answer is wrong in a way that would have cost real content.

## What was looked for, and what was found

**No successor exists.** `MicrosoftDocs/dax-docs`, `MicrosoftDocs/DAX-docs`,
`MicrosoftDocs/dax`, `MicrosoftDocs/powerquery-docs`, `microsoft/query-docs` — all 404. So is
`MicrosoftDocs/query-docs-pr`, though that one always was private.

**The content itself is not gone.** Microsoft Learn serves all of it, and says where it comes
from. Every DAX page carries the metadata:

```
original_content_git_url = .../MicrosoftDocs/query-docs-pr/blob/live/query-languages/dax/abs-function-dax.md
gitcommit                = .../MicrosoftDocs/query-docs-pr/blob/5de07c5f.../abs-function-dax.md
```

So the authoring repository still exists and still publishes; only the public mirror was
removed. `learn.microsoft.com/en-us/dax/toc.json` answers 200 and enumerates **508 pages, 459
of them `*-function-dax`** — a complete, machine-readable index of exactly the surface this
library covers.

**But Learn serves HTML, not markdown.** There is no raw form: `…/abs-function-dax.md` and
`.txt` are 404, and `?raw=true` returns the rendered page. The sync parses markdown with
frontmatter. Re-pointing at Learn means writing a different parser, not changing a URL.

**A complete copy of the markdown survives in a third-party repository.** Found with
`gh search code --filename abs-function-dax.md`:

| repository | function cards | last push | licence |
|---|---|---|---|
| `bredeespelid/PBIP_SemLin` — `docs/bpa/dax/` | **479** | 2026-06-11 | none declared |
| `pbimuxiaoqi/bi` — `posts/dax/` | 335 | 2023-09-08 | MIT |

The first one is a faithful copy: same 479 file names as our catalogue with **zero difference
in either direction**, and it even carries the upstream `toc.yml` and `index.yml`.

## The experiment that decided it

`sync_query_docs.py` was run against that copy, unmodified, into a scratch tree holding this
repository's own `notes/` and `examples/` so the comparison would be fair. It ran clean:
**479 cards + 34 concepts + the three indexes**, the same 16 uncategorised functions, no
parser complaints.

Its output was then compared against what is in the repository, ignoring the four fields the
sync computes from our tree rather than from upstream — `source`, `sourceDate`, `notes`,
`examples` — and the examples block it injects.

**24 of 513 files differ.** And the direction is the whole decision: **our copy is the newer
one.** From `CALCULATE`:

```
repo   @323524c : |`expression`|The expression to evaluate.|
mirror @b426cd5 : |`expression`|The expression to be evaluated.|

repo   @323524c : A Boolean expression filter […] It must follow several rules:
mirror @b426cd5 : A Boolean expression filter […] There are several rules that they must abide by:
```

Microsoft rewrote those pages between the copy's snapshot and our stamp. The 24 include
`CALCULATE`, `WINDOW`, `DATEDIFF`, `IF`, `LOOKUPVALUE`, `SEARCH`, `var-dax` and
`dax-user-defined-functions` — not a stale tail, the most-read pages in the library.
`calculate.md` corroborates it independently: our card carries `sourceDate: 06/29/2026`, the
copy's carries nothing.

## The decision

**`generated/` stays exactly as it is, at `@323524c`, and it is still not edited by hand.**

Frozen is not the same as unreproducible, and the distinction is the point. Regeneration was
demonstrated to work — that is what the experiment above is. What no reachable source can do
is regenerate it *at the state it is already in*. Every copy that survives is older, so
re-pointing the sync at one would be a downgrade of 24 files dressed up as maintenance.

Which is also why the "never edit by hand" invariant survives. It is not an invariant about
whether a generator runs this week; it is what keeps the directory replaceable wholesale the
day a source arrives that is newer than `@323524c`. Hand edits are the one thing that would
make that day expensive. The rule stays, and the reason changes: it used to protect a weekly
sync, and now it protects the option of ever syncing again.

## What follows from it

- **Attribution stops pointing at a 404.** CC BY 4.0 does not lapse because the source
  disappeared, but the way this repository discharged it — a link — now leads nowhere.
  `NOTICE` names Microsoft Learn, which is live, canonical, and per-card addressable
  (`learn.microsoft.com/en-us/dax/<slug>`), and records `query-docs` / `query-docs-pr` as the
  git origin Learn itself declares. `SKILL.md` drops the dead link.
- **`sync-check.yml` stops asking a question nobody can answer.** It could not tell
  "unchanged" from "unreachable", which is the specific complaint in #7. It now probes for the
  upstream and reports it as gone — and fails only if it comes **back**, which is the one
  event that would unfreeze this decision.
- **The 45 invisible examples are a symptom of this, not a separate bug.** Re-running the sync
  restores `examples: N` and the runnable-examples block on 45 cards on its own. See
  [#8](https://github.com/CSalcedoDataBI/dax-for-agents/issues/8): its fix is a regeneration,
  not a gate.

## One thing the freeze did NOT have to cost: the pictures

87 image URLs across 33 cards pointed at the dead host, 47 of them in eight conceptual pages.
The obvious readings were all bad — re-point at Wayback (sampled six, only two archived, and it
ties the content to a third party), delete the images (loses CC BY material Microsoft
published), or say it out loud in `SKILL.md` and leave them broken.

None was needed. Learn serves every one of those files, at the same path behind a different
prefix, and **all 87 answered 200** when fetched. So the URLs were repaired rather than the
content changed, `sync_query_docs.py` now writes Learn URLs for images so a future
regeneration does the same, and `check_dead_media.py` keeps the dead host from coming back.

This is the same finding as the attribution one, applied twice: the upstream mirror is gone,
the published form is not.

## What this does not decide

Whether to build a Learn-HTML path back to regeneration. It is the only source that is both
live and current, it has a complete table of contents, and it is a parser-sized project rather
than a decision. Filed separately.

## What would reverse this

A markdown source at or past `@323524c`: the public mirror returning, Microsoft publishing the
DAX docs somewhere else in source form, or a Learn parser that reproduces the cards. Any of
them makes `generated/` regenerable forward instead of backward, and this record is why the
tree was left untouched and un-hand-edited until then.
