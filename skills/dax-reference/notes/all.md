## Trap: it clears the filters on ITS table, not all of them

`ALL(DimProduct)` clears whatever filters are on `DimProduct` and **only those**. The ones on the
other tables are still there. It is easy to read it as "the total of everything", and it is not.

With the context on `CategoryName = "Electrónica"` **and** `Year = 2024`:

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
EVALUATE
CALCULATETABLE(
  ROW(
    "contexto",             [Unidades],
    "ALL_solo_DimProduct",  CALCULATE([Unidades], ALL(DimProduct)),
    "ALL_producto_y_fecha", CALCULATE([Unidades], ALL(DimProduct), ALL(DimDate))
  ),
  DimProduct[CategoryName] = "Electrónica",
  DimDate[Year] = 2024
)
```

| denominator | result |
|---|---|
| context (Electrónica, 2024) | 4,301 |
| `ALL(DimProduct)` | **91,795** ← still 2024 only |
| `ALL(DimProduct), ALL(DimDate)` | **180,224** ← now yes, both tables |

91,795 is the 2024 total, not the model's. If your "% of total" uses `ALL` on a single dimension
while a date filter is live, the denominator is "everything within the year" — which may be
exactly what you wanted, or not. That has to be decided, not inherited.

## Not to be confused with
- `ALLEXCEPT` — keeps the columns you name from that table, clears the rest.
- [`ALLSELECTED`](./allselected.md) — respects what the user selected.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
