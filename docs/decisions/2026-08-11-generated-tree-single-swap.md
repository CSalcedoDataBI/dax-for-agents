# Everything the sync writes lives under `generated/`

**Date:** 2026-08-11
**Status:** accepted
**Supersedes:** the layout drawn in [the design spec](../superpowers/specs/2026-08-06-dax-for-agents-design.md)

## Context

The sync installed three separate things into `dax-reference/`: the `library/` directory and
the two catalogs. Installing three targets cannot be done in one step, so `_publish` backed up
each one, replaced them in order, and unwound the order in reverse when anything failed.

That recovery code was about 120 lines and carried eight tests of its own. Across the seven
external review rounds on PR #20 the findings per round ran 4, 3, 3, 2, 3, 1, 2 — and **from
the third round on, every single one landed inside the recovery code**, none in the generation
it existed to protect. Each was real: a backup recorded before the copy finished, a first
publish leaving one orphan catalog, a rollback that could destroy the only backup. The pattern
was not any one bug. It was that a hand-written undo of a multi-step install has more states
than review can hold in its head.

## Decision

Everything the sync produces goes under one directory:

```
dax-reference/
  SKILL.md  NOTICE  overrides.json  notes/  scripts/   <- hand-written, never touched
  generated/
    catalog.json
    catalog.md
    library/
    concepts/                                          <- lands here too (issue #6)
```

`_publish` builds the whole tree in a per-run scratch directory and then swaps it in.

## The part that is not true

The issue that proposed this said "one atomic rename". **It is not one rename**, and this was
measured rather than assumed: `os.replace` cannot land a directory on an existing path. On
Windows it raises `PermissionError` even when the target directory is empty; only a target that
does not exist works. So the swap is two renames — the previous generation moves aside, then
the new one takes its place.

The win survives the correction, because two renames leave exactly **one** recoverable state:
the gap between them, where the old tree is parked and the new one has not landed. Undoing it
is one `os.replace` back. Recovery went from ~120 lines and 8 tests to one line and 4 tests,
and the states a reviewer has to enumerate went from a dozen to one.

## Consequences

- Agent-facing paths gained a segment: `generated/library/<fn>.md`, `generated/catalog.md`.
  `notes/<fn>.md` deliberately did **not** move — it is hand-written, and inside `generated/`
  the swap would delete it.
- `validate_skills.py` now fails if `library/`, `concepts/`, `catalog.json` or `catalog.md`
  reappear at the skill root. The sync no longer writes those paths, so a copy left there can
  only go stale while looking authoritative.
- Done before the repo went public. After publication this move would break every external
  reference to the old paths.
- Issue #6 (`concepts/`) inherits the property instead of reintroducing the problem: it lands
  inside `generated/` and rides the same swap.
