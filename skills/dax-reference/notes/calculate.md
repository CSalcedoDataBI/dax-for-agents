## Trap: the context transition is invisible in the code

Referencing a **measure** inside an iterator wraps the expression in an implicit `CALCULATE`, and
that `CALCULATE` turns the current row into a filter. Writing the same formula "expanded" does
not do the same thing, and the result looks nothing alike.

```dax
DEFINE MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
EVALUATE
{
  ("SUMX con la MEDIDA",    SUMX(DimProduct, [Unidades])),
  ("SUMX con la EXPRESIÓN", SUMX(DimProduct, SUM(FactSales[Quantity]))),
  ("total real",            SUM(FactSales[Quantity]))
}
```

| expression | result |
|---|---|
| `SUMX(DimProduct, [Unidades])` | **180,224** ✅ |
| `SUMX(DimProduct, SUM(FactSales[Quantity]))` | **24,690,688** ❌ |
| `SUM(FactSales[Quantity])` | 180,224 |

24,690,688 = 180,224 × 137. Without the context transition each product receives the grand total
and it is added 137 times. The symptom is an absurdly large number, an exact multiple of the
total — if you see that, look for an iterator with no measure inside.

## Not to be confused with
An explicit `CALCULATE`. `SUMX(DimProduct, CALCULATE(SUM(FactSales[Quantity])))` does give
180,224: it is exactly what the measure reference does.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
