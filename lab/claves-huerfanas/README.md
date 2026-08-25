# Orphan keys and the blank row

## What it demonstrates

When the fact table references a key that **does not exist** in the dimension, the engine does
not discard those rows and does not raise an error: it adds a **blank row** to the dimension and
hangs everything orphaned off it. That row is not in the data, it appears on its own.

Contoso cannot show this because its referential integrity is intact. That is why the
[`countrows`](../../skills/dax-reference/notes/countrows.md) note had to **withdraw** that claim
after a review: it could not be demonstrated, and a note you cannot demonstrate does not get
written. This model exists so it can be.

## The model

Three tables, seven rows of data, and the problem on a single line:

| `DimProducto` | | | `Ventas` | |
|---|---|---|---|---|
| **ProductoKey** | **Nombre** | | **ProductoKey** | **Unidades** |
| 1 | Alfa | | 1 | 10 |
| 2 | Beta | | 2 | 20 |
| 3 | Gamma | | 3 | 30 |
| | | | **99** | **50** |

`Ventas[ProductoKey] = 99` does not exist in `DimProducto`. Those seven rows are the table
above, in full: there is nothing else in the model.

## 1. Which side the blank row shows up on

```dax
EVALUATE
ROW(
  "filas_en_DimProducto",        COUNTROWS(DimProducto),
  "VALUES_del_lado_UNO",         COUNTROWS(VALUES(DimProducto[ProductoKey])),
  "VALUES_del_lado_MUCHOS",      COUNTROWS(VALUES(Ventas[ProductoKey])),
  "ALLNOBLANKROW_del_lado_UNO",  COUNTROWS(ALLNOBLANKROW(DimProducto[ProductoKey]))
)
```

| expression | result | |
|---|---|---|
| `COUNTROWS(DimProducto)` | **3** | the base table does not have the blank row |
| `COUNTROWS(VALUES(DimProducto[ProductoKey]))` | **4** | ← here it does appear |
| `COUNTROWS(VALUES(Ventas[ProductoKey]))` | **4** | but for another reason: they are 1, 2, 3 and **99** |
| `COUNTROWS(ALLNOBLANKROW(DimProducto[ProductoKey]))` | **3** | it excludes it on purpose |

The two `VALUES` give 4 and **do not mean the same thing**. On the *one* side the fourth element
is the blank row the engine invented; on the *many* side it is the real key 99, which is still
there. Confusing the two was exactly the mistake the note's review caught.

> This trap is also **drawn**: page «1. Which side the blank row shows up on» of the report
> ([screenshot](../screenshots/claves-huerfanas-de-que-lado.webp)). Open it with the `.pbip` and
> look, because that is where you see what the query result does not show.

## 2. Where the orphaned units end up

```dax
EVALUATE
ADDCOLUMNS(
  VALUES(DimProducto[Nombre]),
  "unidades", CALCULATE(SUM(Ventas[Unidades]))
)
ORDER BY DimProducto[Nombre]
```

| Nombre | unidades |
|---|---|
| *(blank)* | **50** |
| Alfa | 10 |
| Beta | 20 |
| Gamma | 30 |

A row with no name holding 50 units. In a real report this is the empty category that shows up
in the chart and that nobody can account for: they are the sales whose product is not in the
dimension.

> This trap is also **drawn**: page «2. Where the orphaned units end up» of the report
> ([screenshot](../screenshots/claves-huerfanas-donde-caen.webp)). Open it with the `.pbip` and
> look, because that is where you see what the query result does not show.

## 3. The total does count them, and "cleaning up" the blank row loses them

```dax
EVALUATE
ROW(
  "total_Ventas",              SUM(Ventas[Unidades]),
  "suma_por_producto_visible", SUMX(VALUES(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades]))),
  "suma_sin_fila_en_blanco",   SUMX(ALLNOBLANKROW(DimProducto[Nombre]), CALCULATE(SUM(Ventas[Unidades])))
)
```

| expression | result |
|---|---|
| `SUM(Ventas[Unidades])` | **110** |
| Sum per product, with `VALUES` | **110** ✅ reconciles |
| Sum per product, with `ALLNOBLANKROW` | **60** ❌ 50 missing |

This is the part that hurts. `ALLNOBLANKROW` sounds like "remove the noise", and what it does is
**lose 50 units without warning**: the detail stops adding up to the total, and the difference is
exactly the orphans.

> This trap is also **drawn**: page «3. Cleaning up the blank row loses 50» of the report
> ([screenshot](../screenshots/claves-huerfanas-limpiar-pierde.webp)). Open it with the `.pbip`
> and look, because that is where you see what the query result does not show.

## Where the data comes from

Two Parquet files, **2 KB between them**, published in
[`CSalcedoDataBI/SampleDataSets`](https://github.com/CSalcedoDataBI/SampleDataSets) (public, MIT,
synthetic), which the model reads the same way as the other three scenarios:

```
Parquet.Document(Web.Contents(DataBaseUrl, [RelativePath="Ventas.parquet"]))
```

The orphan is **written by hand**, not injected by a data-quality percentage. The difference
matters: the scenario needs *one* specific orphan with *one* specific number of units, because
the three result tables above reconcile with it row by row. An `orphan_fk_pct = 0.25` would give
a different orphan on every regeneration and the 110, 60 and 50 in this README would stop being
checkable.

They are regenerated with [`build_datasets.py`](../build_datasets.py).

## How to reproduce it

1. Open `ClavesHuerfanas.pbip` in Power BI Desktop.
2. **Refresh** — opening a PBIP loads the model without data, you have to ask for it. It needs
   internet; there are no credentials to give.
3. Paste the queries into the DAX query view, or let the runner execute them:

```bash
python lab/check_lab.py claves-huerfanas localhost:<port>
```

Measured on 2026-08-12 with the three queries above, exactly as written.
