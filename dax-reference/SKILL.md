---
name: dax-reference
description: Use when you need to know what a built-in DAX function does, its exact signature, what it returns, whether it is legal in a measure, a calculated column, a calculated table or a visual calculation, whether Microsoft discourages it, or which of several similar functions to reach for — and equally for the DAX language itself when no single function is in question, such as evaluation context, context transition, filter and row context, the query statements EVALUATE, DEFINE, MEASURE, ORDER BY and START AT, operators, data types, BLANK semantics, variables with VAR, and Microsoft's own best-practice guidance. The canonical reference for DAX. Triggers on "what does X do in DAX", "DAX function signature", "which DAX function", "difference between", "is X deprecated", "can I use X in a calculated column", "does X work in a measure", "what is evaluation context", "context transition", "DAX query syntax", "EVALUATE statement", "what does BLANK mean in DAX", "DAX operators", "DAX best practice".
---

# DAX Reference

The complete DAX function library, agent-native. Derived from
[`MicrosoftDocs/query-docs`](https://github.com/MicrosoftDocs/query-docs) (CC BY 4.0 — see
[`NOTICE`](./NOTICE)) and annotated with the gotchas the docs leave out.

> **Status.** `generated/` is built — 479 functions and 34 conceptual pages from
> `MicrosoftDocs/query-docs@323524c`, plus **30 field notes**, each one measured
> against a real model rather than asserted.
> See [the design spec](../docs/superpowers/specs/2026-08-06-dax-for-agents-design.md).

## How to use this

**One hop. Do not read the whole library — it is ~376.000 tokens.**

1. Read **[`generated/catalog.md`](./generated/catalog.md)** (~14k tokens). Every function, one
   row each: name, category, return type, where it applies, one-line summary, and flags.
2. Find the function. Open its card: **`generated/library/<function>.md`**.
3. If the catalog row is flagged **★**, also read **`notes/<function>.md`** — that is the field
   knowledge that is not in Microsoft's docs. It sits outside `generated/` because it is
   written by hand.
4. If the card's frontmatter says `examples: N` with N greater than zero, the card links to
   **`examples/<category>/<function>.md`**: N queries **executed against a model that is in
   this repository**, each one published with the number the engine returned.

**Do not quote figures from the card's `## Examples (Microsoft — no verificados aquí)`
section as if they were verified.** Those come from `query-docs` and are measured against
Adventure Works DW 2020, a model this repo does not carry. They are useful for shape and
intent; they are not evidence. The executable examples above them are.

For a question that is not about one specific function — evaluation context, the query
statements (`EVALUATE`, `DEFINE`, `ORDER BY`), operators, the glossary, best-practice guidance
— take the other path instead: read **[`generated/concepts.md`](./generated/concepts.md)** (34
concepts, ~2k tokens) and open the one page it points to. Going through `catalog.md` would cost
14k tokens of function rows to reach a page that is not about a function.

### Reading the flags

| Flag | Meaning |
|---|---|
| ⛔ | Microsoft discourages it **in visual calculations only** — it says the function there "likely returns meaningless results". It says nothing about using it in a measure or a calculated column. The card field is `discouragedInVisualCalculations`, named that way because "discouraged" on its own gets read as deprecated, and warning someone off a function that is fine where they are using it is a wrong answer said with confidence |
| ★ | There is a hand-written note in `notes/` — read it |

### Where a function applies

The `appliesTo` field says where the function is legal: `measure`, `column` (calculated column),
`table` (calculated table), `visual-calculation`, or `query` (query-only). Check it before
suggesting a function in the wrong place — that is a common invented-answer failure.

## Layout

Everything under `generated/` is produced by the sync and replaced wholesale on every run.
Everything beside it is written by hand. That boundary is the layout: the sync installs one
directory, so it can never half-update the tree, and it can never eat your notes.

| Path | What it is |
|---|---|
| `generated/catalog.md` | The function index the agent reads. **Generated** |
| `generated/concepts.md` | The concept index — 34 concepts. **Generated** |
| `generated/catalog.json` | Both indexes for scripts. **Generated**, never loaded into context |
| `generated/library/<fn>.md` | One card per function. **Generated — never edit by hand** |
| `generated/concepts/<page>.md` | One card per conceptual page. **Generated** |
| `notes/<fn>.md` | Field notes. **Hand-written — the sync never touches these** |
| `overrides.json` | Values the parser cannot derive (mostly `returns`). Hand-written |
| `scripts/sync_query_docs.py` | Regenerates `generated/` |

## Regenerating

Clone the upstream docs, then point the sync at the DAX folder:

```bash
python scripts/sync_query_docs.py /path/to/query-docs/query-languages/dax --write
```

Without `--write` it only reports; nothing on disk is touched.

It parses the 15 category index files to build the function → category map, parses the 479
function files, then picks up every remaining page — anything that is neither a function nor a
category index — as a concept. Cross-links are rewritten to local paths and all three indexes
are stamped with the upstream commit SHA.

The concept rule is mechanical rather than a list of filenames, so a page Microsoft adds is
picked up on the next sync. If it lands in a docs directory the sync does not read, the run
says so instead of quietly leaving it out.

### What stops a bad generation

Four gates, all before anything is written:

| Gate | Fails when |
|---|---|
| No category | A function gets none from the category indexes, the filename rules, `toc.yml`, or `overrides.json`. The exceptions are named in `overrides.json`, so a swap that keeps the total unchanged still fails — and a name left there after upstream classifies it fails too |
| Orphan note | A `notes/<fn>.md` has no card. The catalog would flag ★ and send a reader to a file that is not there |
| Broken cross-link | Any relative link in a card resolves to nothing |
| Count deviation | The function or concept count moved more than 5% since the last sync. Override with `--accept-count-change` for a real upstream release |

Plus a coverage floor of 90% as a coarse net against a total parser collapse.

The new tree is built in a scratch directory and only then swapped into place, so a failure
part-way leaves the previous `generated/` exactly as it was. `notes/` is read to set the ★ flag
and never written.

A weekly CI job compares the upstream SHA against the stamped one. When it moves, the job
sparse-clones the DAX folder, regenerates through the four gates, runs the repo's own
checks, and opens a pull request — one branch, `sync/query-docs`, replaced on every run.

That pull request touches every file whether or not any DAX changed, because each card
names the commit it came from. So its body classifies the diff before anyone reads it:
the functions that actually changed, and the count that only moved their stamp. The first
real run was 516 files and **zero** substantive changes, which is one sentence to read
instead of a wall.

## Related skills

- **`dax-lib`** — ready-made UDFs from daxlib.org. Check there before authoring one.
- **`dax-udf-authoring`** — how to write your own `FUNCTION` correctly.
- **`dax-window-functions`** — the window family in depth.
- **Performance tuning is not here.** Use the `dax` skill from the
  [data-goblin plugin](https://github.com/data-goblin/power-bi-agentic-development).
