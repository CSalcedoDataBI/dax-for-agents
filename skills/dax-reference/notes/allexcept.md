## Trap: it ignores the user's slicer

`ALLEXCEPT(T, col)` keeps **only** the filters on the columns you name it and clears all the
rest. It sounds like "category total", and it is — but it also clears whatever selection the user
made on any other column of that table.

Context: `CategoryName = "Electrónica"` **and** `Brand IN {Apple, Sony}`.

| brand | units | `ALLEXCEPT(…, CategoryName)` | `ALLSELECTED(DimProduct)` |
|---|---|---|---|
| Apple | 1,219 | **8,386** | 2,411 |
| Sony | 1,192 | **8,386** | 2,411 |

2,411 = 1,219 + 1,192: with `ALLSELECTED` the percentages add up to 100%. With `ALLEXCEPT` the
denominator is the whole category even though the user is only looking at two brands, so they add
up to 29% and the report looks broken.

See the full query in [`allselected`](./allselected.md).

## Not to be confused with
`ALLSELECTED`, which is what you almost always want for a "% of visible total". `ALLEXCEPT` is
correct when the denominator must be the category **no matter what**.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
