## Trap: the iterator only filters if there is a measure inside

`SUMX(T, expr)` opens **row** context over T. Row context does not filter by itself: a context
transition is needed for the current row to become a filter. Referencing a measure triggers it;
writing the aggregation out by hand does not.

```dax
DEFINE MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
EVALUATE
{
  ("SUMX con la MEDIDA",    SUMX(DimProduct, [Unidades])),
  ("SUMX con la EXPRESIÓN", SUMX(DimProduct, SUM(FactSales[Quantity])))
}
```

| expression | result |
|---|---|
| `SUMX(DimProduct, [Unidades])` | **180,224** ✅ |
| `SUMX(DimProduct, SUM(FactSales[Quantity]))` | **24,690,688** ❌ |

24,690,688 = 180,224 × 137. See [`calculate`](./calculate.md) for the mechanism.

Over the iterator's **own** table it is not needed: `SUMX(FactSales, FactSales[Quantity] *
FactSales[NetPrice])` is correct, because it reads columns from the current row instead of
aggregating another table.

## And it also costs: ~290× over two million rows

The context transition does not only change the number. Over a table of 2,000,000 rows, with both
forms returning **the same** result:

| | cold median | peak memory |
|---|---|---|
| `SUMX(Ventas, [Total])` | **871 ms** | **~193 MB** |
| `SUMX(Ventas, Ventas[Importe])` | **3 ms** | 0 |

Two million context transitions, one per row. On the same model, wrapping the whole table in a
`FILTER` — the thing everyone calls expensive — cost nothing measurable: the engine pushes the
predicate down to storage. **The bulk is the measure inside the iterator, not the `FILTER`.**

Measured in the [`lab/rendimiento`](../../../lab/rendimiento/README.md) scenario, which can be
opened and run again. The milliseconds are from a laptop; the ratio is what survives a change of
machine.

## Not to be confused with
`SUM`, which does not open row context. If your expression multiplies two columns row by row you
need the iterator; if it only adds up one column, `SUM` is cheaper and clearer.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
