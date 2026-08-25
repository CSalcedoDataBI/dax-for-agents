## Trap: it needs row context and a relationship in the right direction

`RELATED` goes **many to one**: from the fact table towards the dimension. It only works where
there is row context — a calculated column, or inside an iterator. In a bare measure it does not
compile.

```dax
EVALUATE
ADDCOLUMNS(
  VALUES(DimProduct[ProductKey]),
  "SUMX_con_RELATED",
    SUMX(RELATEDTABLE(FactSales), FactSales[Quantity] * RELATED(DimProduct[Price]))
)
```

It works because `SUMX` opens row context over `FactSales`, and from there `RELATED` can climb to
`DimProduct`. Result for ProductKey 114: **127,515.72**.

## Not to be confused with
[`RELATEDTABLE`](./relatedtable.md), which goes the other way (one to many) and returns a table,
not a value.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
