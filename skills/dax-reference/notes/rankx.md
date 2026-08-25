## Trap: `RANKX(VALUES(...))` returns 1 for everything

`RANKX(<table>, <expr>)` ranks within the table you pass it, and that table is evaluated **in the
filter context of the row being drawn**. In a matrix or a `SUMMARIZECOLUMNS`, that context already
has a single brand, so `VALUES(DimProduct[Brand])` returns **one row**, and ranking within a list
of one always gives 1.

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
  MEASURE _Measures[RankVALUES] = RANKX(VALUES(DimProduct[Brand]), [Ventas])
  MEASURE _Measures[RankALL]    = RANKX(ALL(DimProduct[Brand]), [Ventas])
EVALUATE
TOPN(5,
  SUMMARIZECOLUMNS(DimProduct[Brand], "Ventas", [Ventas], "RankVALUES", [RankVALUES], "RankALL", [RankALL]),
  [Ventas], DESC)
ORDER BY [Ventas] DESC
```

| brand | sales | `RANKX(VALUES(...))` | `RANKX(ALL(...))` |
|---|---|---|---|
| Sony | 1,273,417.32 | **1** | 1 ✅ |
| Microsoft | 1,164,898.94 | **1** ❌ | 2 ✅ |
| Nintendo | 1,131,477.23 | **1** ❌ | 3 ✅ |
| Lutron | 1,066,213.09 | **1** ❌ | 4 ✅ |
| Apple | 744,415.28 | **1** ❌ | 5 ✅ |

It is the function's quietest failure: no error, no blank, just a plausible number. A whole column
of ones looks like a ranking until somebody looks twice.

The table being ranked has to **ignore** the filter on the column you are ranking by:
`ALL(DimProduct[Brand])` to rank against the whole catalogue, or
[`ALLSELECTED`](./allselected.md) to rank against what the user left selected — which is almost
always what people want when they put a slicer in.

## Ties and gaps

By default `RANKX` uses `Skip`: two tied at 3 leave 4 empty and the next is 5. With `Dense` there
are no gaps. The argument sits in fifth position, behind `<order>`, so it is easy to forget.

## Not to be confused with
- [`TOPN`](./topn.md) — it takes the leading rows, and **does not return N rows** when there are
  ties.
- `RANK` — the new window function, with explicit `ORDERBY`/`PARTITIONBY` instead of a table.
  Clearer once you are already in a query.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
