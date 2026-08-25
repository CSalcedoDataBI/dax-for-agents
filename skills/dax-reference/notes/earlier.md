## Trap: without `EARLIER` the comparison is always true

Inside a `FILTER` nested over the same table, `DimProduct[Col] = DimProduct[Col]` compares the
inner row with itself. That is always true, so the filter filters nothing and returns the whole
table — no error, no warning.

```dax
EVALUATE
ADDCOLUMNS(
  SUMMARIZE(DimProduct, DimProduct[CategoryName], DimProduct[Brand]),
  "con_EARLIER",     COUNTROWS(FILTER(DimProduct, DimProduct[CategoryName] = EARLIER(DimProduct[CategoryName]))),
  "sin_EARLIER_mal", COUNTROWS(FILTER(DimProduct, DimProduct[CategoryName] = DimProduct[CategoryName]))
)
```

| category | con_EARLIER | sin_EARLIER |
|---|---|---|
| Electrónica | **46** ✅ | **137** ❌ |

137 is the model's total product count. The symptom is that every row of the result shows the
same number.

## Not to be confused with
A **variable**. `VAR cat = DimProduct[CategoryName]` captured before the `FILTER` does the same
thing and reads without having to think about how many row contexts are open. `EARLIER` is still
needed in older calculated columns, but in new code the variable wins almost every time.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
