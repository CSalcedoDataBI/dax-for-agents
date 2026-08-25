## Trap: the alternative comes out with ZERO values and with SEVERAL, not only with several

`SELECTEDVALUE(col, alternative)` returns the value **only if exactly one is left**. With none and
with two or more it returns the alternative, which defaults to blank — so an empty card does not
distinguish "the user selected several" from "nothing is selected".

```dax
DEFINE
  MEASURE _Measures[sel] = SELECTEDVALUE(DimProduct[Color], "-- alternativa --")
  MEASURE _Measures[n] = COALESCE(COUNTROWS(VALUES(DimProduct[Color])), 0)
EVALUATE
UNION(
  CALCULATETABLE(ROW("caso","un valor",   "sel",[sel],"n",[n]), DimProduct[Color] = "Black"),
  CALCULATETABLE(ROW("caso","dos valores","sel",[sel],"n",[n]), DimProduct[Color] IN {"Black","White"}),
  CALCULATETABLE(ROW("caso","CERO valores","sel",[sel],"n",[n]), DimProduct[Color] = "NoExisteEsteColor")
)
```

| case | no. of values | SELECTEDVALUE |
|---|---|---|
| one value | 1 | **Black** |
| two values | 2 | **-- alternativa --** |
| zero values | 0 | **-- alternativa --** |

If you need to tell the two cases apart, `HASONEVALUE` does **not** help: it is false in both,
which is exactly what makes both return the alternative. And be careful counting, because
`COUNTROWS` over an empty table returns **blank, not zero**:

```dax
EVALUATE
CALCULATETABLE(
  ROW(
    "COUNTROWS",     COUNTROWS(VALUES(DimProduct[Color])),
    "es_blank",      ISBLANK(COUNTROWS(VALUES(DimProduct[Color]))),
    "con_COALESCE",  COALESCE(COUNTROWS(VALUES(DimProduct[Color])), 0),
    "ISEMPTY",       ISEMPTY(VALUES(DimProduct[Color]))
  ),
  DimProduct[Color] = "NoExisteEsteColor"
)
```

| expression, with zero values in context | result |
|---|---|
| `COUNTROWS(VALUES(col))` | **(blank)** |
| `ISBLANK(COUNTROWS(...))` | TRUE |
| `COALESCE(COUNTROWS(...), 0)` | 0 |
| `ISEMPTY(VALUES(col))` | TRUE |

That is why the query above wraps the count in `COALESCE`. To ask "is it zero?", `ISEMPTY` is more
direct than counting.

## Not to be confused with
`VALUES`, which returns the whole table and errors when forced to a scalar with more than one row.
Microsoft
[recommends SELECTEDVALUE](https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue)
to avoid that; that page is not in the function card.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
