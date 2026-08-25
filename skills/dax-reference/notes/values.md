## Trap: over a COLUMN it returns a column; over a TABLE it returns the table

`VALUES` has two forms and only one gives something convertible to a scalar:

- `VALUES(table[column])` → a table of **one** column.
- `VALUES(table)` → the table's rows, with **all** their columns.

```dax
EVALUATE TOPN(2, VALUES(DimCurrency))
```

returns 5 columns (`CurrencyKey`, `CurrencyCode`, `CurrencyName`, `Symbol`, `Language`), not one.

The automatic conversion to a scalar only happens with a table of **one column and one row**.
`VALUES(DimCurrency)` never satisfies that because the table has five columns; a single-column
table could. With the column form it depends on the context:

The measure forces the conversion by concatenating, which is what any expression expecting a
scalar does. They are **two queries**, because the second never gets to return a table: it aborts.

```dax
-- 1. un solo color -> devuelve "Black"
DEFINE MEASURE _Measures[forzado] = VALUES(DimProduct[Color]) & ""
EVALUATE
CALCULATETABLE(ROW("caso", "un solo color", "forzado", [forzado]),
               DimProduct[Color] = "Black")
```

```dax
-- 2. dos colores -> la consulta falla
DEFINE MEASURE _Measures[forzado] = VALUES(DimProduct[Color]) & ""
EVALUATE
CALCULATETABLE(ROW("caso", "dos colores", "forzado", [forzado]),
               DimProduct[Color] IN {"Black", "White"})
```

| context | result |
|---|---|
| one colour only | **`Black`** — the conversion works |
| two colours | **error**: *A table of multiple values was supplied where a single value was expected* |

The second case does not return a strange value: it **aborts the query**. And it only shows up
when the user widens the selection, so it passes testing with one colour and fails in production
with two.

## Not to be confused with
[`SELECTEDVALUE`](./selectedvalue.md), which is this pattern already solved and without the error.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
