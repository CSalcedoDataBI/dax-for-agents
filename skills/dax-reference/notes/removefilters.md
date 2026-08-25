## Trap: it does the same as `ALL`, but cannot be used where `ALL` can

As a `CALCULATE` modifier, `REMOVEFILTERS(X)` and `ALL(X)` give **exactly** the same result. The
difference is that `ALL` is also a table function and `REMOVEFILTERS` is not:

```dax
EVALUATE ROW("filas", COUNTROWS(REMOVEFILTERS(DimProduct)))
```

```
REMOVEFILTERS function cannot be used as a table expression.
It can appear only as a filter in CALCULATE.
```

Swapping an `ALL` for `REMOVEFILTERS` "because it reads better" works inside `CALCULATE` and breaks
the moment that `ALL` was being iterated or passed to another function.

## What it exists for, then

To say in the code what the expression does. `ALL` means two things — "give me the whole table" and
"remove these filters" — and the reader has to work out which from its position. `REMOVEFILTERS`
only means the second, so a long `CALCULATE` can be understood without reconstructing it.

## The decision that does change the number: column or table

With the context filtered to the *Electrónica* category:

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
  MEASURE _Measures[PctALLcol]    = DIVIDE([Ventas], CALCULATE([Ventas], ALL(DimProduct[Brand])))
  MEASURE _Measures[PctREMOVEcol] = DIVIDE([Ventas], CALCULATE([Ventas], REMOVEFILTERS(DimProduct[Brand])))
  MEASURE _Measures[PctALLtabla]  = DIVIDE([Ventas], CALCULATE([Ventas], ALL(DimProduct)))
EVALUATE
TOPN(3,
  CALCULATETABLE(
    SUMMARIZECOLUMNS(DimProduct[Brand], "Ventas", [Ventas],
                     "PctALLcol", [PctALLcol], "PctREMOVEcol", [PctREMOVEcol], "PctALLtabla", [PctALLtabla]),
    DimProduct[CategoryName] = "Electrónica"
  ),
  [Ventas], DESC)
ORDER BY [Ventas] DESC
```

| brand | sales | `ALL(Brand)` | `REMOVEFILTERS(Brand)` | `ALL(DimProduct)` |
|---|---|---|---|---|
| Apple | 744,415.28 | **11.14%** | **11.14%** ✅ identical | **3.74%** |
| Sony | 692,829.80 | 10.37% | 10.37% | 3.48% |
| Jabra | 489,943.26 | 7.33% | 7.33% | 2.46% |

The first two columns agree to the last decimal. The third is a different question: removing the
filters from the **whole** table takes the category filter with it, so the denominator goes from
"Electrónica" to the entire catalogue and the percentage is divided by three.

It is the same trap as [`ALL`](./all.md), and it does not go away by writing it under another name.

## Not to be confused with
- [`ALL`](./all.md) — same effect as a modifier, and also a table function.
- [`ALLSELECTED`](./allselected.md) — respects what the user selected outside the visual.
- [`KEEPFILTERS`](./keepfilters.md) — the opposite: it adds instead of replacing.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
