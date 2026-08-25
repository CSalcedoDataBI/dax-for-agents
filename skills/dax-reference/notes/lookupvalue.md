## Trap: the "not found" argument also swallows conflicting values

`LOOKUPVALUE` fails when the rows it finds do not agree **on the value you asked for**. The fourth
argument, `<alternateResult>`, exists for the "no match" case — but it is **also** returned on that
conflict. Both cases come out of the same door and cannot be told apart.

What decides is not how many rows match, but how many **distinct values** they return:

```dax
EVALUATE
{
  ("filas con Brand = Sony",              FORMAT(COUNTROWS(FILTER(DimProduct, DimProduct[Brand] = "Sony")), "0")),
  ("ProductName distintos entre ellas",   FORMAT(COUNTROWS(CALCULATETABLE(VALUES(DimProduct[ProductName]), DimProduct[Brand] = "Sony")), "0")),
  ("LOOKUPVALUE de ProductName",          LOOKUPVALUE(DimProduct[ProductName], DimProduct[Brand], "Sony", "SIN RESULTADO")),
  ("LOOKUPVALUE de Brand",                LOOKUPVALUE(DimProduct[Brand], DimProduct[Brand], "Sony", "SIN RESULTADO")),
  ("LOOKUPVALUE de CategoryName",         LOOKUPVALUE(DimProduct[CategoryName], DimProduct[Brand], "Sony", "SIN RESULTADO"))
}
```

| expression | result |
|---|---|
| rows with `Brand = "Sony"` | **9** |
| distinct `ProductName` among them | **8** |
| `LOOKUPVALUE(ProductName, Brand, "Sony", …)` | **`SIN RESULTADO`** ❌ 8 conflicting values |
| `LOOKUPVALUE(Brand, Brand, "Sony", …)` | **`Sony`** ✅ 9 rows, a single value |
| `LOOKUPVALUE(CategoryName, Brand, "Sony", …)` | **`SIN RESULTADO`** ❌ Sony is in several categories |

The fourth row is the one that breaks the intuition: **nine rows match and it still returns a
value**, because all nine say the same thing. And the third is the dangerous one: there are 9 Sony
products, the correct answer is not "no result" but "the question is badly posed", and the report
shows the second as if it were the first.

(9 rows and 8 names: two Sony products share a `ProductName`. In a real model those things are
there.)

Without the fourth argument the same expression fails, and the message is clear:

```
A table of multiple values was supplied where a single value was expected.
```

Which is more useful than a silent `SIN RESULTADO`. **Adding `alternateResult` without being sure
the value is unique turns an error into false data.**

## How to use it with a safety net

- Lookup by unique key → `LOOKUPVALUE` with no fourth argument, and let it blow up if the model
  changes.
- Lookup that may find nothing → fourth argument, but **only** if you know there can be no
  conflict.
- Lookup that may return different values → that is not a lookup. It is an aggregation:
  [`MAXX`](./maxx.md) or `MINX`, [`CONCATENATEX`](./concatenatex.md) or
  [`SELECTEDVALUE`](./selectedvalue.md), which says what to do with the tie.

## Not to be confused with
- [`RELATED`](./related.md) — follows an existing relationship and is cheaper. `LOOKUPVALUE` needs
  no relationship, which is why it gets used where there should be one.
- [`SELECTEDVALUE`](./selectedvalue.md) — a value from the current context, with an explicit exit
  for the several case.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only and
> does not touch the model. It runs and compares itself with `python lab/check_lab.py contoso
> localhost:<port>`.
