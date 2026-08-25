## Trap: over an all-blank column it returns blank, not zero

`COUNT` counts values, not rows: it discards blanks. If the column is entirely blank the result
is **(blank)**, not `0` — and a blank disappears from the visual while a zero gets drawn.

`DimStore[CloseDate]` is empty across all 25 stores (none has closed):

```dax
EVALUATE
ROW(
  "COUNT_CloseDate",      COUNT(DimStore[CloseDate]),
  "COUNTROWS_DimStore",   COUNTROWS(DimStore),
  "COUNTBLANK_CloseDate", COUNTBLANK(DimStore[CloseDate])
)
```

| expression | result |
|---|---|
| `COUNT(DimStore[CloseDate])` | **(blank)** |
| `COUNTROWS(DimStore)` | **25** |
| `COUNTBLANK(DimStore[CloseDate])` | 25 |

If what you wanted was "how many stores are there", `COUNT` over a column with blanks gives you
something else.

## Not to be confused with
[`COUNTROWS`](./countrows.md), which counts rows and does not look at the content. Microsoft
[recommends COUNTROWS over COUNT](https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows)
for this reason, and that page is not in the function card.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
