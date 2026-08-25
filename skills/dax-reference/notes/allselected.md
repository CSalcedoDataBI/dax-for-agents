## Trap: it depends on who set the filter, not on the formula

`ALLSELECTED` returns the total of what the user has selected, not that of the whole table. It is
the only one in the `ALL*` family whose result changes according to **where the filter came
from**: it respects the external ones (slicer, page filter, the query) and removes the ones the
visual itself sets row by row.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[den ALLEXCEPT] = CALCULATE([Unidades], ALLEXCEPT(DimProduct, DimProduct[CategoryName]))
  MEASURE _Measures[den ALLSELECTED] = CALCULATE([Unidades], ALLSELECTED(DimProduct))
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(
    VALUES(DimProduct[Brand]),
    "unidades", [Unidades],
    "den_ALLEXCEPT", [den ALLEXCEPT],
    "den_ALLSELECTED", [den ALLSELECTED]
  ),
  DimProduct[CategoryName] = "Electrónica",
  DimProduct[Brand] IN {"Apple", "Sony"}
)
```

| brand | unidades | den_ALLEXCEPT | den_ALLSELECTED |
|---|---|---|---|
| Apple | 1,219 | 8,386 | **2,411** |
| Sony | 1,192 | 8,386 | **2,411** |

That the same measure gives a different number when moved to another visual **is not a bug**: it
is the definition. That is why it is the hardest function in the family to debug — the code does
not change and the result does.

## Not to be confused with
`ALL` (clears the filters on **its** table, not those of the others — see [`all`](./all.md), where
it is measured) and `ALLEXCEPT` (everything on that table except the named columns, see
[`allexcept`](./allexcept.md)).

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
