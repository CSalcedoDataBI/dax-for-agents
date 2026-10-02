---
name: dax-reference
description: Use when you need what a built-in DAX function does — signature, return type, where it is legal (measure, calculated column or table, visual calculation), whether it is discouraged or deprecated, or which of several similar functions to pick — or a DAX language concept — evaluation, filter and row context, context transition, EVALUATE/DEFINE query syntax, operators, data types, BLANK, VAR, Microsoft best practices. Triggers on "what does X do in DAX", "DAX function signature", "which DAX function", "difference between two DAX functions", "is X deprecated", "can I use X in a calculated column", "context transition", "EVALUATE syntax", "BLANK in DAX".
---

# DAX Reference

The complete DAX function library, agent-native. Derived from `MicrosoftDocs/query-docs`
(CC BY 4.0 — see [`NOTICE`](./NOTICE)), which has returned 404 since 2026-08; the same
material is published on [Microsoft Learn](https://learn.microsoft.com/en-us/dax/).
Annotated with the gotchas the docs leave out.

> **Status.** `generated/` is built — 479 functions and 34 conceptual pages from
> `MicrosoftDocs/query-docs@323524c`, plus **31 field notes**, each one measured
> against a real model rather than asserted.
> See [the design spec](../../docs/superpowers/specs/2026-08-06-dax-for-agents-design.md).

## How to use this

**One hop. Do not read the whole library — it is ~376,000 tokens.**

1. Read **[`generated/catalog.md`](./generated/catalog.md)** (~14k tokens). Every function, one
   row each: name, category, return type, where it applies, one-line summary, and flags.
2. Find the function. Open its card: **`generated/library/<function>.md`**, where the
   filename is the catalogue name lowercased with `.` turned into `-` (`ISO.CEILING` →
   `iso-ceiling.md`, `T.DIST.2T` → `t-dist-2t.md`). `notes/` and `examples/` use the same rule.
3. If the catalog row is flagged **★**, also read **`notes/<function>.md`** — that is the field
   knowledge that is not in Microsoft's docs. It sits outside `generated/` because it is
   written by hand.
4. If the catalog row is flagged **▶** — or, the same fact seen from the card, its
   frontmatter says `examples: N` with N greater than zero — the card links to
   **`examples/<category>/<function>.md`**: N queries **executed against a model that is in
   this repository**, each one published with the number the engine returned. The flag is
   there so this can be decided from the index instead of by opening 479 cards.

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
| ▶ | There are runnable examples in `examples/` — queries executed against a model that is in this repository, each published with the number the engine returned. The card carries the count in `examples:` |

### Where a function applies

The `appliesTo` field says where the function is legal: `measure`, `column` (calculated column),
`table` (calculated table), `visual-calculation`, or `query` (query-only). Check it before
suggesting a function in the wrong place — that is a common invented-answer failure.
In `catalog.md` the `Aplica` column abbreviates it: `M` measure, `C` calculated column,
`T` calculated table, `V` visual calculation, `Q` query-only.

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

## Maintaining `generated/`

Regenerating, the gates that stop a bad generation and the weekly CI sync are maintainer
material, kept out of this file so it does not load on every lookup: see
[`scripts/README.md`](./scripts/README.md).

## Related skills

- **`dax-lib`** — ready-made UDFs from daxlib.org. Check there before authoring one.
- **`dax-udf-authoring`** — how to write your own `FUNCTION` correctly.
- **`dax-window-functions`** — the window family in depth.
- **Performance tuning is not here.** Use the `dax` skill from the
  [data-goblin plugin](https://github.com/data-goblin/power-bi-agentic-development).
