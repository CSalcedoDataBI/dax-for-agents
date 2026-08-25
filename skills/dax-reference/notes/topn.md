## Trap: `TOPN(3, ...)` does not return 3 rows

When there are ties on the ordering value, `TOPN` takes **every** row tied for the last place. You
ask for 3 and you may get 4, or 7. If whatever follows assumes 3 — a division, a `CONCATENATEX`,
a "top 3" in a title — the number that comes out is a different one.

```dax
EVALUATE
VAR PorColor = SUMMARIZE(DimProduct, DimProduct[Color], "N", COUNTROWS(DimProduct))
RETURN
{
  ("colores distintos",              COUNTROWS(PorColor)),
  ("TOPN 3 por N",                   COUNTROWS(TOPN(3, PorColor, [N], DESC))),
  ("TOPN 5 por N",                   COUNTROWS(TOPN(5, PorColor, [N], DESC))),
  ("TOPN 3 con desempate por Color", COUNTROWS(TOPN(3, PorColor, [N], DESC, DimProduct[Color], ASC)))
}
```

| expression | rows returned |
|---|---|
| distinct colours | 15 |
| `TOPN(3, …)` | **4** ❌ |
| `TOPN(5, …)` | **6** ❌ |
| `TOPN(3, …, DimProduct[Color], ASC)` | **3** ✅ |

The fix is a tie-breaker: `TOPN` accepts further `<orderBy>, <order>` pairs after the first, and
with one that is unique (a key, a name) the tie stops existing.

Choosing the tie-breaker is a decision, not a detail: alphabetical by name is arbitrary but
**stable**, and stable is what makes the report say the same thing tomorrow.

## `N` does not cap, it orders

`TOPN` does not guarantee the order of what it returns; it guarantees *which* rows. To get them
ordered you have to order them afterwards — with `ORDER BY` in the query, or with
[`CONCATENATEX`](./concatenatex.md)'s `orderBy` if you are going to paste them into text.

An `N` of 0 or negative returns an empty table, not an error.

## Not to be confused with
- [`RANKX`](./rankx.md) — it numbers, it does not trim. That is what you want if you need the
  position.
- `SAMPLE` — returns rows spread across, not the leading ones.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
