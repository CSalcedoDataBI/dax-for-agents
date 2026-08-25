## Trap: not finding is an error, not a blank

`SEARCH` without its fourth argument **fails the query** when the text does not appear. It is the
same behaviour as [`FIND`](./find.md) and it surprises just as much, because intuition says a
search that finds nothing returns "nothing".

```dax
EVALUATE
{
  ("SEARCH sony en 'Sony Bravia'", FORMAT(SEARCH("sony", "Sony Bravia", 1, -1), "0")),
  ("FIND sony en 'Sony Bravia'",   FORMAT(FIND("sony", "Sony Bravia", 1, -1), "0"))
}
```

| expression | result |
|---|---|
| `SEARCH("sony", "Sony Bravia", 1, -1)` | **1** ← found, case-insensitive |
| [`FIND`](./find.md)`("sony", "Sony Bravia", 1, -1)` | **-1** ← not found, case-sensitive |

Same signature, same argument positions, opposite answer. That is what makes it easy to write one
while thinking of the other.

In a calculated column the failure is worse than in a measure: a single row with no match brings
down the refresh of the whole model, and the message points at the function, not at the row.

## The fourth argument, and the third

- `<start>` (third) begins at **1**, not 0. A 0 raises an error.
- `<NotFoundValue>` (fourth) is what makes the search usable: `SEARCH(text, where, 1, BLANK())`
  for a blank, or `, 0)` if you are going to compare with `> 0`.

For "does it appear?" regardless of where, `CONTAINSSTRING` reads better and has no error case.

## It accepts wildcards, and that surprises too

`SEARCH` interprets `?` and `*`. Searching for those characters literally requires escaping them
with `~`. [`FIND`](./find.md) does not interpret them, so for a literal search it is the safe one.

## Not to be confused with
- [`FIND`](./find.md) — case-sensitive, no wildcards.
- `CONTAINSSTRING` / `CONTAINSSTRINGEXACT` — return a boolean; the second is the case-sensitive
  one.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only and
> does not touch the model. It runs and compares itself with `python lab/check_lab.py contoso
> localhost:<port>`.
