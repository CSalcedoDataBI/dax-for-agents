## Trap: over an empty table it returns **blank**, and the blank equals zero when compared

`MAXX` of nothing is not zero: it is `BLANK()`. And since the blank is coerced to the type of the
other operand, `[Máximo] = 0` comes out true — so the check you were going to protect yourself
with does not distinguish "there are no rows" from "the maximum is zero".

```dax
EVALUATE
VAR Vacia = FILTER(DimProduct, DimProduct[Brand] = "NoExiste")
RETURN
{
  ("MAXX real sobre DimProduct", FORMAT(MAXX(DimProduct, DimProduct[Price]), "0.00")),
  ("filas de la tabla vacía",    IF(ISBLANK(COUNTROWS(Vacia)), "BLANK", FORMAT(COUNTROWS(Vacia), "0"))),
  ("MAXX sobre tabla vacía",     IF(ISBLANK(MAXX(Vacia, DimProduct[Price])), "BLANK", "algo")),
  ("MAXX + 0",                   FORMAT(MAXX(Vacia, DimProduct[Price]) + 0, "0.00")),
  ("MAXX = 0",                   IF(MAXX(Vacia, DimProduct[Price]) = 0, "IGUAL A CERO", "distinto")),
  ("MAXX == 0",                  IF(MAXX(Vacia, DimProduct[Price]) == 0, "IGUAL A CERO", "distinto"))
}
```

| expression | result |
|---|---|
| `MAXX(DimProduct, [Price])` | 3,804.72 |
| `COUNTROWS(<empty table>)` | **BLANK** ← not 0 |
| `MAXX(<empty table>, [Price])` | **BLANK** |
| `MAXX(…) + 0` | 0.00 ← the addition coerces the blank |
| `MAXX(…) = 0` | **IGUAL A CERO** ❌ |
| `MAXX(…) == 0` | distinto ✅ |

`COUNTROWS` also returns blank, not zero, so `IF(COUNTROWS(T) = 0, …)` suffers the same. To
genuinely ask whether there are rows: `ISEMPTY(T)`, which answers that question and not another
one.

See [`blank`](./blank.md) for the coercion mechanism and the difference between `=` and `==`.

## The maximum across different columns is not `MAX` of the row

`MAXX(T, expr)` walks rows and returns the largest value of the expression. For the largest
**between two columns of the same row** the function is `MAXX` over a `{}` of values, or directly
`MAX(a, b)` with two scalar arguments — which is a different overload from the `MAX(column)`
aggregation and gets confused with it.

## It ignores blanks, it does not count them as zero

If the column has blanks, `MAXX` skips them. That is usually what you want; it stops being so when
the blank meant "zero" at the source. It is the same decision behind
[`AVERAGEX`](./averagex.md), and there it changes the result far more.

## Not to be confused with
- `MAX(column)` — the plain aggregation, with no row context. Cheaper and clearer.
- [`TOPN`](./topn.md) — gives you the **row** of the maximum, not the value.
- `MAXA` — the variant that treats `TRUE`/`FALSE` and text as numbers.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only and
> does not touch the model. It runs and compares itself with `python lab/check_lab.py contoso
> localhost:<port>`.
