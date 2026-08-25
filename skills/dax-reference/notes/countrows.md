## Trap: it counts rows, not values — and that matters when there are blanks

`COUNTROWS(T)` counts T's rows as they stand after the filter context, without looking at the
content. It is what you almost always want for "how many are there", and it is exactly where
`COUNT` behaves differently.

`DimStore[CloseDate]` is empty across all 25 stores:

```dax
EVALUATE
ROW(
  "COUNTROWS_DimStore", COUNTROWS(DimStore),
  "COUNT_CloseDate",    COUNT(DimStore[CloseDate])
)
```

| expression | result |
|---|---|
| `COUNTROWS(DimStore)` | **25** |
| `COUNT(DimStore[CloseDate])` | **(blank)** |

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only and
> does not touch the model. It runs and compares itself with `python lab/check_lab.py contoso
> localhost:<port>`.

## Not to be confused with
[`COUNT`](./count.md), which discards blanks and can return blank where you expected zero.
Microsoft
[recommends COUNTROWS over COUNT](https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows),
and that page is not in the function card.

## Trap: the blank row shows on the *one* side, not on the fact

When the fact table references a key that does not exist in the dimension, the engine adds a blank
row **to the dimension**. Measured in
[`lab/claves-huerfanas`](../../../lab/claves-huerfanas/), with a single orphan key:

| expression | result | |
|---|---|---|
| `COUNTROWS(DimProducto)` | **3** | the base table does not have it |
| `COUNTROWS(VALUES(DimProducto[ProductoKey]))` | **4** | ← here it appears |
| `COUNTROWS(VALUES(Ventas[ProductoKey]))` | **4** | but they are 1, 2, 3 and **99**: the real key |

The two `VALUES` give 4 and **do not mean the same thing**. On the *one* side the fourth element
is the invented row; on the *many* side it is the genuine orphan value. Confusing them makes you
believe the blank row is in the facts, and it is not.

And cleaning that row up is expensive: `SUMX(ALLNOBLANKROW(...))` gives **60** where the total is
**110**. The 50 orphaned units disappear without warning.

> Measured in [`lab/claves-huerfanas`](../../../lab/claves-huerfanas/) on 2026-08-12, **not**
> against Contoso: Contoso's referential integrity is intact and so it cannot demonstrate anything
> in this section. The model, the data and the queries are there to run.
