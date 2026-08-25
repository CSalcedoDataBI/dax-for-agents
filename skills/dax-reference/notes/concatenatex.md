## Trap: without `orderBy` the order is arbitrary, not the table's

`CONCATENATEX` walks the table you give it in whatever order the engine decides. Passing it a
[`TOPN`](./topn.md) ordered by sales does **not** preserve that order: the result comes out
plausible — a list of brands separated by commas — and is ordered by nothing.

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
EVALUATE
VAR Top5 = TOPN(5, VALUES(DimProduct[Brand]), [Ventas], DESC)
RETURN
{
  ("sin orderBy",           CONCATENATEX(Top5, DimProduct[Brand], ", ")),
  ("orderBy ventas DESC",   CONCATENATEX(Top5, DimProduct[Brand], ", ", [Ventas], DESC)),
  ("orderBy alfabético",    CONCATENATEX(Top5, DimProduct[Brand], ", ", DimProduct[Brand], ASC))
}
```

| expression | result |
|---|---|
| no `orderBy` | `Apple, Nintendo, Lutron, Microsoft, Sony` ❌ |
| `orderBy` sales DESC | `Sony, Microsoft, Nintendo, Lutron, Apple` ✅ |
| `orderBy` alphabetical | `Apple, Lutron, Microsoft, Nintendo, Sony` ✅ |

The first is ordered neither by sales nor by name. It is the worst kind of failure for text in a
report: **"Top 5: Apple, Nintendo, Lutron…" reads as a ranking and is not one.**

The order without `orderBy` is also not guaranteed between runs or between engine versions. That
a particular one comes out today is not a promise.

## The separator comes before the order

The signature is `CONCATENATEX(<table>, <expr>, [<delimiter>], [<orderBy>], [<order>])`. The
delimiter is optional, so it is easy to write the `orderBy` in its slot and end up with the brands
glued together with no separator — a mistake that raises no error.

For the last item joined with "and" instead of a comma there is no argument: you build that
separately.

## Not to be confused with
- `CONCATENATE` — joins **two** strings, not a table. For several, the `&` operator chains
  better.
- `COMBINEVALUES` — meant for composite keys, not for readable text.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
