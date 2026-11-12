# The cards are bundled by category, not one file each

**Date:** 2026-11-12 · **Issue:** #40 · **Status:** decided

## Why

The Anthropic plugin directory holds any plugin that ships more than 512 files for a human
reviewer ("Ship fewer files"), and its waiver covers one version only. The listing's plugin
path is the repository root, so every tracked file ships. There were 1,056 of them, and
`generated/` alone held 513: one per function card and one per conceptual page.

## What changed

- The 513 cards live in **19 bundles** under `generated/bundles/`: one per `primaryCategory`
  (`functions-<category>.md`, an empty category is `uncategorized`), plus `concepts-1/2.md`.
  A group over 230 KiB splits in stem order. The largest is 173 KiB.
- Each card sits **verbatim** between `<a id="<stem>"></a>` / `<!-- card: <sub>/<stem> -->`
  and `<!-- /card -->`. The one edit is a card-to-card link, rewritten to its bundle and
  anchor and reversed on split. `card_bundles.py` owns the format; `check()` proves that
  splitting the bundles and rebuilding them gives the same bytes, and `validate_skills.py`
  runs it in CI.
- `catalog.md` and `concepts.md` gained a `Ficha` column, `bundle:first-last`, so an agent
  reads one card with Read `offset`/`limit`: still one hop. It costs about 3k tokens more per
  catalog read (72 KB to 89 KB).
- `docs/examples-es/` (100 files, a frozen Spanish snapshot nothing reads) moved to the tag
  `archive/examples-es-2026-08-25`.

## What did not change

The content. `generated/` is still frozen at `@323524c`
([decision of 2026-08-27](2026-08-27-generated-is-frozen-at-323524c.md)); only where each card
lies on disk changed, and the round trip proves it rather than asserting it. The sync,
`refresh_local_metadata.py` and `check_function_names.py --fix` read and write the cards
through `card_bundles`, so none of them knows the old one-file-per-card paths any more.

## Result

`measure_plugin.py .`: 1,056 files → 467, and zero holds. The plugin path did not have to
change (PR #26 stays parked), and nothing under `lab/`, `scripts/` or `evals/` left `main`.
Only the frozen `docs/examples-es/` moved, to a tag.

## Risk to watch

An agent reading a whole bundle (up to ~45k tokens) instead of the line range. `SKILL.md`
says not to, each bundle's header says not to, and the next routing eval should confirm it.
