# English is the language of this repository

**Date:** 2026-08-25 · **Status:** accepted · **Affects:** `INDEX.md`, `notes/`, `examples/`,
`lab/`, and everything written from here on

## The problem

Nobody ever decided. That is the whole finding, and it explains the rest.

Measured across the 183 hand-written files in the tree (`generated/` excluded — that is
Microsoft's prose, not ours), the split is **60% Spanish, 40% English**. It is not a random
mix. It falls along a line so clean it is obviously an accident of who wrote what, and when:

| | Language |
|---|---|
| `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md` | English |
| The five `SKILL.md` — what an agent always has loaded | English |
| Most gate scripts | English |
| **`INDEX.md` — the routing file** | **Spanish** |
| The 31 field notes | Spanish |
| The example files | Spanish |
| The `lab/` READMEs | Spanish |
| `docs/decisions/`, `docs/superpowers/` | Spanish (one in English) |

**The public face speaks English and the knowledge speaks Spanish.** The README sells the
repository on exactly the thing that is written in Spanish: *"what does this function do, when
does it bite, and what should I use instead"* — that answer lives in `notes/`.

The worst single instance was `INDEX.md`. The README ends its skills section with
*"Full routing: INDEX.md"*, all five `SKILL.md` are English, and the routing file they point
at was Spanish. A reader arriving through the English front door landed in Spanish at the one
file whose whole job is to send them somewhere else.

## Why it had to be decided now, not later

`check_examples.py` currently reports **99 of 479** functions covered. The
[examples epic](https://github.com/CSalcedoDataBI/dax-for-agents/issues/6) is about writing
the rest: roughly **380 more files**.

Deciding today costs nothing — the files do not exist yet. Deciding in six months means
translating them. The cost of this decision grows by about four times if it is deferred past
the epic, and it is the only reason this record was written before touching a single note.

## The decision

**English**, for everything that is read to learn what this repository knows.

Not because Spanish is worse — the notes are better written than most of the English here —
but because the repository already chose. It positions itself against
`microsoft/skills-for-fabric`, `MicrosoftDocs/Agent-Skills`, `data-goblin` and `daxlib`, all
English; it ships as a plugin from a public marketplace; and its README, CONTRIBUTING and
plugin description are English. What is left is making the content agree with the shop window.

In order, and deliberately not all at once:

| | What | Status |
|---|---|---|
| 1 | `INDEX.md` | done with this record |
| 2 | The 99 example files, plus every new one from the epic | **done** — see below |
| 3 | The 31 field notes | **done** — see below |
| 4 | The five `lab/` READMEs | **done** |

Steps 3 and 4 were meant to be incremental and were finished in the same sitting instead. That
changes the plan, not the reasoning: the argument for English did not depend on doing it slowly,
only the risk did. The risk was handled by hashing all 39 `dax` blocks in the notes before the
first edit and checking them after the last — `check_lab.py` reads those blocks out of the `.md`
by position, so a single changed character would have altered what runs while CI stayed green.

Step 2 was decided here as "new files only, the existing 99 migrate when touched". They were
translated in full instead, the same day. The argument that had held them back was cost — 99
files carrying queries and measured results — and the notes had just shown that cost was
affordable: hashing the blocks before the first edit makes the risk checkable rather than
hoped for. Here it was 348 `dax` blocks, 348 `result` blocks and 99 frontmatter headers, all
verified identical after the last edit.

The Spanish originals are kept, frozen, in [`docs/examples-es/`](../examples-es/). Not as a
second copy to maintain — nothing reads it and it is never updated — but because translating
prose is the one step in this migration where meaning could drift with no gate noticing. The
queries could not drift; the sentences around them are what a reader has to take on trust, and
that directory is what they can check it against.

One value stayed Spanish on purpose: `model: ninguno` in the frontmatter. It is the sentinel
`examples_io.py` compares against, sitting beside the real `lab/` directory names — a value in
a data contract, not prose. Moving it would touch 98 files, a constant and three test files for
no reader benefit. The examples README says so where someone would ask.

## What "in English" does not reach: identifiers

Prose translates. The things around it often cannot, and the line is not a matter of taste — it
is what the reader sees on screen and what the runner compares literally.

**The reports are prose too, and they were translated.** This section first drew the line at the
report boundary: page names are `displayName` strings a reader sees in the Power BI page tab, the
lab READMEs quote them verbatim — «2. El + 0 que mueve el denominador» — and translating the
quote without the report would send someone looking for a page that does not exist. That
reasoning was right about the tabs and then wrongly swallowed everything inside them. A report
page here is a note textbox on top of a data visual: **eighteen textboxes and thirty-five visual
titles of plain prose**, which by this ADR's own rule belong in English. Leaving them Spanish was
not a decision about identifiers; it was not looking.

So the whole report moved: seventeen `displayName`s, thirty-five titles, nineteen textbox
paragraphs, the quotes in the READMEs, and the screenshots retaken. Two strings inside that sweep
stayed Spanish because they are not prose — `(sin un valor unico)`, the literal a `SELECTEDVALUE`
measure returns and the card displays, and `Alto con medida`, a measure name.

Screenshot filenames moved to `<scenario>-<page-id>.webp` in the same pass. Five of them were
slugs of the Spanish `displayName`, which is what made a rename break links; the page **id** is
stable and never translated, so the next rename cannot.

**Model identifiers.** `Ventas[Importe]`, `Tiendas[Metros]`, `DimProducto[Nombre]` are bound to
Parquet files published in another repository. Renaming them means regenerating the data, editing
the TMDL, and re-measuring every published result. That is a migration with a verification cost,
not a translation. (Contoso's own schema — `FactSales`, `DimProduct`, `DimDate` — is already
English, because it is Microsoft's.)

**Result aliases inside queries.** `"con_metros"`, `"es_blanco"`, `"suma_sin_fila_en_blanco"`
appear both in the query and in the published result that `check_lab.py` compares against a live
run. A find-and-replace over those changes what the runner expects. They move only when a file is
rewritten and its result re-measured — never as a sweep.

So a lab README is English prose wrapping Spanish identifiers, and that is the intended end
state, not a half-finished migration. Each README says so at the top.

## What stays in Spanish, on purpose

**`docs/decisions/` and `docs/superpowers/`.** These are dated records of what was decided and
what was built, at the time it happened. Translating a record rewrites it: the reader can no
longer tell whether a phrase is what was argued then or what someone reworded later. They are
already exempt from the doc-claims gate for the same underlying reason — a number in a record
is a fact about the past, not a claim about the tree.

New records are written in English, which makes this folder mixed on purpose.
[The 2026-08-11 record](2026-08-11-generated-tree-single-swap.md) was already in English, so
the mixture predates this decision rather than being introduced by it.

**Code comments.** They are dense, several are load-bearing arguments about why a guard exists,
and nobody is blocked by reading one in Spanish. Rewriting them is churn across files whose
tests would not notice a meaning drift.

## Consequences

- `INDEX.md` is English, and carries the rule as convention 8 so it is visible where skills
  are added rather than only here.
- A new note or example written in Spanish is now a review comment, not a matter of taste.
- No measurement changed. The notes carry the same queries, the same results and the same dates
  they were published with; only the prose around them is different. The 99 covered example
  files stay in Spanish and stay correct.
- No gate enforces this. Language is not something `check_doc_claims.py` can measure without
  guessing, and a guard that guesses gets switched off. This is a convention held by review.
