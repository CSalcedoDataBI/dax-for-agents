# examples — the contract

One file per function, with **at least three examples**, and every example carries **the query and
the number the engine returned**.

An *example* is exactly that: **a query with its measured result**. It is the unit the gate counts
and the one the card advertises, so a prose section showing two queries counts as two. The `## 1.`,
`## 2.` numbering organises the reading, not the count.

This exists because the cards already carry examples — Microsoft's, measured against *Adventure
Works DW 2020* — and that model is not in this repository. Nobody here has run its figures. What
is written in this tree is the opposite: **examples that run**.

## Where everything goes

```
dax-reference/examples/<primaryCategory>/<stem>.md
```

The `<stem>` is the same as the card's in `generated/library/` — `if.md`, `if-eager.md`,
`bitlshift.md`. It is not the function's name: `IF.EAGER` lives in `if-eager.md`.

**This tree is hand-written and the sync never touches it**, just like `notes/`. The examples
cannot live inside the card because the card is regenerated whole every time `query-docs` moves,
and it would take them with it.

## The file

```markdown
---
function: IF
model: ninguno
---

# IF — examples

## 1. Without the third argument the result is BLANK, not zero

A sentence saying what is being shown. Do not repeat the syntax: that is what the card is for.

​```dax
EVALUATE ROW("sin_else", IF(1 = 2, "sí"))
​```

​```result
sin_else
(blank)
​```

And below it, if needed, why that matters.
```

### The frontmatter

| key | what it is |
|---|---|
| `function` | the name exactly as DAX writes it — `IF`, `IF.EAGER`, `BITLSHIFT` |
| `model` | which `lab/` scenario it runs against |

`model: ninguno` means **it reads no model data**: pure arithmetic, text, logic. It runs against
`contoso` because an engine is needed, not because that model is. The distinction matters for
knowing what breaks when a model changes.

The value stays in Spanish because it is not prose: it is the sentinel `examples_io.py` compares
against, alongside the real directory names under `lab/`. Any other value has to be a genuine
`lab/` directory: `contoso`, `blancos`, `claves-huerfanas`, `rendimiento`.

### The `result` block

It is what makes the example executable. The first line holds the column names; the following
ones, the rows, with cells separated by ` | `.

```
sin_else | con_else
(blank) | 0
```

| value | is written |
|---|---|
| blank | `(blank)` |
| true / false | `True` / `False` |
| number | as it comes, rounded to **6 decimals** |
| text | as it comes, without quotes |

If the query **aborts on purpose** — some functions can only be understood by seeing the error —
the block carries the message:

```
ERROR: The value for column X cannot be determined
```

Every ` ```dax ` block has to be followed by its ` ```result `. An example with no measured result
is not an example: it is an assertion, and the catalogue is already full of those.

## How it is checked

```bash
python scripts/check_examples.py                    # structure: 3 per function, real model, all with a result
python lab/check_lab.py examples localhost:<port>   # runs each query and compares against its result
```

The first runs in CI. The second does **not**, and that is deliberate: it needs a tabular engine
with data and CI has no Power BI Desktop.

To record a new example's result without copying it by hand:

```bash
python lab/dump_examples.py localhost:<port> dax-reference/examples/logical/if.md
```

It writes the `result` block of every query that lacks one. Whatever it writes has to be **looked
at**: it moves across what the engine returned, it does not decide whether the example was a good
idea.

## What makes a good example

Three is the **floor**, not the target. `BITLSHIFT` is well served by three; `CALCULATE` with three
falls short.

- **Show something the syntax does not say.** If the example can be deduced from reading the
  signature, it is surplus.
- **The number surprises, or the example is not needed.** The value is in the case where intuition
  fails.
- **It reads in one glance.** A forty-line query is not an example.
- **It does not repeat its neighbour.** Three variants of the same case are one example, not three.
