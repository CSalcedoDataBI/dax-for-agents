---
function: CONCATENATEX
model: contoso
---

# CONCATENATEX — examples

> The [`concatenatex`](../../notes/concatenatex.md) field note covers the ordering. Here are the
> size of the result and what it does with duplicates and blanks.

## 1. It walks the table you give it, duplicates included

If the table has one row per value — a clean dimension — they give the same thing. As soon as the
column repeats within the table, `CONCATENATEX` repeats it too, and what you wanted was `VALUES`
of the column.

```dax
EVALUATE
ROW(
  "marcas_distintas", COUNTROWS(VALUES(DimProduct[Brand])),
  "productos",        COUNTROWS(DimProduct),
  "por_valores",      LEN(CONCATENATEX(VALUES(DimProduct[Brand]), DimProduct[Brand], ", ")),
  "por_la_tabla",     LEN(CONCATENATEX(DimProduct, DimProduct[Brand], ", "))
)
```

```result
marcas_distintas | productos | por_valores | por_la_tabla
58 | 137 | 494 | 1193
```

The second length is several times the first: one entry per product instead of one per brand.

## 2. It has no short cap: over a large column it returns an enormous text

Nothing warns you. The measure does not fail, the visual sits thinking, and the tooltip is
unreadable.

```dax
EVALUATE
ROW(
  "cuantos_productos", COUNTROWS(VALUES(DimProduct[ProductName])),
  "longitud_total",    LEN(CONCATENATEX(VALUES(DimProduct[ProductName]), DimProduct[ProductName], ", ")),
  "primeros_60",       LEFT(CONCATENATEX(VALUES(DimProduct[ProductName]), DimProduct[ProductName], ", "), 60)
)
```

```result
cuantos_productos | longitud_total | primeros_60
128 | 3006 | Dell Desktop M3 Pro/36GB, Microsoft Workstation i7/32GB/1TB,
```

The healthy pattern is to cap with [`topn`](../../notes/topn.md) and say how many are missing, not
to dump the whole column.

## 3. Blanks are NOT skipped: they leave the separator doubled

I wrote it the other way round and the engine corrected it. A gap does not disappear from the list
— it takes its place as an empty element, so two separators come out in a row. It is ugly in the
visual, and at the same time it is the only thing warning that a value was missing.

```dax
EVALUATE
VAR ConHuecos = { "a", BLANK(), "c" }
RETURN
ROW(
  "filas",    COUNTROWS(ConHuecos),
  "unidos",   CONCATENATEX(ConHuecos, [Value], "-"),
  "longitud", LEN(CONCATENATEX(ConHuecos, [Value], "-")),
  "vacia",    ISBLANK(CONCATENATEX(FILTER(ConHuecos, FALSE()), [Value], "-"))
)
```

```result
filas | unidos | longitud | vacia
3 | a--c | 4 | True
```

Over an empty table it does return blank, not an empty string — the same distinction as always.
