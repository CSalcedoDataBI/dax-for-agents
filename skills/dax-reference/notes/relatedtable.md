## Trap: it returns a table, and it goes one to many

`RELATEDTABLE` is the mirror of `RELATED`: from the dimension towards the facts. It returns **a
table**, so it almost always goes wrapped in `COUNTROWS` or in an iterator.

```dax
EVALUATE
ADDCOLUMNS(
  VALUES(DimProduct[ProductKey]),
  "filas_de_venta", COUNTROWS(RELATEDTABLE(FactSales))
)
```

| ProductKey | filas_de_venta |
|---|---|
| 114 | 7,861 |
| 121 | 7,594 |
| 118 | 6,218 |

## What it is underneath
`RELATEDTABLE(T)` is `CALCULATETABLE(T)`: it carries a context transition, and that is why the
dimension's row ends up filtering the facts. Knowing that explains the result — it is not
relationship magic, it is the same old `CALCULATE`.

This note **claims nothing about performance**. On this model (137 products, 126,524 fact rows)
the queries take single-digit milliseconds, so any cost figure or cardinality threshold would be
a guess dressed up as a measurement. If you need to decide on performance, measure it on your
model with the query analyser.

## Not to be confused with
[`RELATED`](./related.md), which goes many to one and returns a scalar value.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
