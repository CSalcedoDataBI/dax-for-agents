## Trap: it is case-sensitive, and what surrounds it is not

`FIND` is case-sensitive. The `=` operator, the model's filters and [`SEARCH`](./search.md) — what
you have around you when you write one — are **not**. So the same comparison changes its answer
depending on what you write it with.

It is not the only sensitive one: `CONTAINSSTRINGEXACT` and `EXACT` are too, and that is exactly
the problem. Sensitivity follows no rule you can deduce from the name; it goes function by
function.

| function | case-sensitive? | measured with `sony` against `Sony` |
|---|---|---|
| `=` (operator) | no | `TRUE` |
| [`SEARCH`](./search.md) | no | `1` (found) |
| `CONTAINSSTRING` | no | `TRUE` |
| **`FIND`** | **yes** | `-1` (not found) |
| **`CONTAINSSTRINGEXACT`** | **yes** | `FALSE` |
| **`EXACT`** | **yes** | `FALSE` |

```dax
EVALUATE
{
  ("comparar sony con Sony",       IF("sony" = "Sony", "TRUE", "FALSE")),
  ("filas filtrando en minuscula", FORMAT(COUNTROWS(FILTER(DimProduct, DimProduct[Brand] = "sony")), "0")),
  ("filas filtrando en mayuscula", FORMAT(COUNTROWS(FILTER(DimProduct, DimProduct[Brand] = "Sony")), "0")),
  ("FIND sony en Sony Bravia",     FORMAT(FIND("sony", "Sony Bravia", 1, -1), "0")),
  ("SEARCH sony en Sony Bravia",   FORMAT(SEARCH("sony", "Sony Bravia", 1, -1), "0"))
}
```

| expression | result |
|---|---|
| `"sony" = "Sony"` | **TRUE** |
| `FILTER(DimProduct, Brand = "sony")` | **9 rows** |
| `FILTER(DimProduct, Brand = "Sony")` | **9 rows** |
| `FIND("sony", "Sony Bravia")` | **-1** ← not found |
| [`SEARCH`](./search.md)`("sony", "Sony Bravia")` | **1** ← found |

The query's labels say `minuscula` and `mayuscula` instead of `= "sony"` and `= "Sony"` for the
very reason you are reading about. With the literal labels, this:

```dax
EVALUATE { ("filas con Brand = sony", 9), ("filas con Brand = Sony", 9) }
```

returns **both rows** — it does not merge them — but both come out printed as
`filas con Brand = sony`: being equal ignoring case, the engine returns them under a single
spelling, the first one it saw. Two identical labels on screen for two different rows, which is
this note's trap demonstrating itself.

The lowercase filter returns the same 9 rows as the uppercase one: **the model is not
case-sensitive.** Only `FIND` is, and that is why it is the one that surprises.

## Without the fourth argument, not finding is an error

`FIND("sony", "Sony Bravia")` without `<NotFoundValue>` does not return blank: **it fails the
query.**

```
The search Text provided to function 'FIND' could not be found in the given text.
```

A `-1` or a `BLANK()` as the fourth argument turns the error into a value you can keep working
with. In a calculated column over thousands of rows, a single non-matching one brings down the
whole refresh.

## When you do want FIND

Almost never for its case sensitivity, but when that sensitivity **is** the requirement: codes
where `AB` and `ab` mean different things. To search text a person typed, [`SEARCH`](./search.md)
is what you expect.

And if what you need is "does it appear?" without the position, `CONTAINSSTRINGEXACT` says the same
with less noise and without the error case.

## Not to be confused with
- [`SEARCH`](./search.md) — same signature, case-insensitive, and it accepts wildcards.
- `CONTAINSSTRING` / `CONTAINSSTRINGEXACT` — return a boolean instead of a position; the first is
  insensitive, the second is not.
- `EXACT` — compares two whole strings case-sensitively, it does not search inside one.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only and
> does not touch the model. It runs and compares itself with `python lab/check_lab.py contoso
> localhost:<port>`.
