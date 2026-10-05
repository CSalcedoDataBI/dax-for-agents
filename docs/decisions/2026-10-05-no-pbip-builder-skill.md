# No PBIP builder in this plugin — make the DAX skills fire inside one instead

**Date:** 2026-10-05
**Status:** decided by the owner
**Affects:** the [PBIP builder proposal](../proposals/2026-10-05-pbip-builder-system-prompt.md),
the `dax-reference` description, `evals/cases.yaml`

---

## What happened

With the plugin installed on claude.ai, the owner asked for a didactic Power BI project — a
`.pbip` showing `CALCULATE` at work. Claude built it **without touching the plugin**: no skill
fired. Asked how to improve, it proposed a system prompt for a "PBIP builder" agent: templates
for every `.pbip` / TMDL / PBIR file, a generate-with-one-Python-script workflow, validation with
`jsonschema` and `TmdlSerializer`, and a section of DAX best practices.

The question the owner asked was the right one: *if it builds the thing without the plugin, what
is the plugin for?*

## Why no skill fired — and why that was correct

The request was not a DAX question. It was a **project-authoring** request that happened to
contain DAX. Every description in this plugin is about the language — what a function does,
which one to pick, how a UDF is written — so the router had nothing to match against "build me a
PBIP", and it was right not to: none of the five skills knows how to lay out a `.SemanticModel`
folder.

What was missing is narrower. Somewhere inside that build Claude **wrote measures**, and at that
moment `dax-reference` should have been consulted. It was not, because its description only
answered *questions about* DAX, never *the act of writing* it as one step of something bigger.

## The decision

1. **The PBIP builder does not ship here.** This repository is the DAX language, and the
   [README](../../README.md#complements-not-competitors) says so twice: no modeling, no reports.
   PBIP / TMDL / PBIR authoring is already covered by
   [`data-goblin/power-bi-agentic-development`](https://github.com/data-goblin/power-bi-agentic-development)
   (`pbip`, `tmdl`, `pbir-format` skills) and by Microsoft's own Power BI authoring plugin. A
   third copy of the file templates, maintained by one person, would drift from the schemas
   faster than either of those.
2. **`dax-reference` fires when DAX is being written, not only asked about.** Its description now
   names the case: writing or reviewing measures, calculated columns or calculated tables,
   including inside a PBIP, a TMDL file or a report being built. A routing case guards it.
3. **The proposal stays in the repo, marked not adopted,** because it is the evidence for this
   decision and because the PBIP-format half of it is a fair checklist for whoever does build
   that skill — in a repo whose scope it fits.

## What the review of the proposal found

Most of the file-format content is consistent with what Power BI Desktop writes. The two
problems are in the part that *is* this repo's subject:

| Claim in the proposal | Verdict |
|---|---|
| "`FILTER(Tabla, ...)` as a `CALCULATE` filter is an antipattern when a column would do" — listed as something to *detect* before delivering | **Contradicted by this repo's own measurement.** [`lab/rendimiento`](../../lab/rendimiento/README.md) was built to prove `FILTER` over a whole table is expensive, and showed it is not: what costs is the context transition of a measure inside the iterator. The two forms can also return different results (expanded table vs one column), so this is a semantics choice, not a lint rule |
| Step 2: "check `examples/` of the plugin", and `schemas/`, `tools/` "the plugin already brings" | **None of the three exists.** An instruction to look in a folder that is not there is how an agent ends up inventing its contents. The runnable models this repo does have are in [`lab/`](../../lab/README.md) |

## What would change this

If a PBIP builder is ever wanted under this author's name, it is a **second plugin** — the
layout already allows it (see [INDEX conventions](../../INDEX.md#conventions), point 7) — with
its own scope line in its own README, and it should *call* `dax-reference` for every measure it
writes rather than carry its own DAX rules.
