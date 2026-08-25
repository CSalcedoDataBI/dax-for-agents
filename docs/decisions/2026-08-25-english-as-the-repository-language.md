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

| | What | Cost |
|---|---|---|
| 1 | `INDEX.md` | done with this record |
| 2 | Every new example from the epic, English from the first one | zero — it only had to be decided |
| 3 | The 31 field notes | incremental, as each is touched |
| 4 | The `lab/` READMEs | whoever downloads a `.pbip` reads them |

## What "in English" does not reach: identifiers

Prose translates. The things around it often cannot, and the line is not a matter of taste — it
is what the reader sees on screen and what the runner compares literally.

**Report page names.** The lab READMEs quote pages by name: «2. El + 0 que mueve el
denominador». That string is a `displayName` inside the report definition, and it is what a
reader sees in the Power BI page tab. Translating the quote and not the report would send them
looking for a page that does not exist; translating both means editing seventeen page
definitions in four `.pbip` projects. The quotes stay verbatim, in Spanish, because they are UI
strings and not prose.

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
- Nothing already published moves. This record changes what gets written next; it does not
  invalidate the 31 notes or the 99 covered functions, which stay correct and stay useful
  until each is touched for another reason.
- No gate enforces this. Language is not something `check_doc_claims.py` can measure without
  guessing, and a guard that guesses gets switched off. This is a convention held by review.
