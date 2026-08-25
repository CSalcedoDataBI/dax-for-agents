## Trap: it intersects, it does not add

`KEEPFILTERS` does not "add" the new filter to the previous set: it **intersects** them. If the
context already filters the same column by another value, the result is empty, not the union.

With the context on `Color = "White"`:

| form | result |
|---|---|
| `CALCULATE([Unidades], DimProduct[Color] = "Black")` | 11,102 |
| `CALCULATE([Unidades], KEEPFILTERS(DimProduct[Color] = "Black"))` | **(blank)** |

See the full query in [`filter`](./filter.md). The blank is correct: no product is white and
black at the same time.

## Not to be confused with
The bare predicate, which **replaces** that column's filter. `KEEPFILTERS` is what you want when
the user has a slicer set and you must not ignore it.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
