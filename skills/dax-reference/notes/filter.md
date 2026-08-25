## Trap: `CALCULATE(m, FILTER(T, p))` and `CALCULATE(m, p)` are not the same thing

They read like synonyms and return different results. `FILTER(T, p)` **iterates T inside the
current filter context**; the bare predicate expands to `FILTER(ALL(column), p)` and therefore
**replaces** whatever filter was on that column.

With the context set to `Color = "White"`:

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[a] = CALCULATE([Unidades], FILTER(DimProduct, DimProduct[Color] = "Black"))
  MEASURE _Measures[b] = CALCULATE([Unidades], DimProduct[Color] = "Black")
  MEASURE _Measures[c] = CALCULATE([Unidades], KEEPFILTERS(DimProduct[Color] = "Black"))
EVALUATE
CALCULATETABLE(
  ROW("contexto", [Unidades], "a_FILTER", [a], "b_predicado", [b], "c_KEEPFILTERS", [c]),
  DimProduct[Color] = "White"
)
```

| form | result |
|---|---|
| context (`White`) | 3,450 |
| `FILTER(DimProduct, Color="Black")` | **(blank)** |
| `DimProduct[Color] = "Black"` | **11,102** |
| `KEEPFILTERS(Color="Black")` | (blank) |

`FILTER` walks the products left after the White filter: none is Black, so the table comes out
empty and the measure blank. The predicate removes the colour filter and gives the Black total.
Neither is "wrong" — they measure different things, and that is the trap.

## Not to be confused with
`KEEPFILTERS`, which does keep the existing filter and **intersects** it: White ∩ Black is empty,
hence the blank. Use it when you want to add a condition without overriding the user's.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
