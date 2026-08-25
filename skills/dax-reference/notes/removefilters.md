## Trampa: hace lo mismo que `ALL`, pero no se puede usar donde `ALL`

Como modificador de `CALCULATE`, `REMOVEFILTERS(X)` y `ALL(X)` dan **exactamente** el mismo
resultado. La diferencia es que `ALL` además es una función de tabla y `REMOVEFILTERS` no:

```dax
EVALUATE ROW("filas", COUNTROWS(REMOVEFILTERS(DimProduct)))
```

```
REMOVEFILTERS function cannot be used as a table expression.
It can appear only as a filter in CALCULATE.
```

Cambiar un `ALL` por `REMOVEFILTERS` "porque se lee mejor" funciona dentro de `CALCULATE` y
rompe en cuanto ese `ALL` estaba iterándose o pasándose a otra función.

## Para qué existe entonces

Para decir en el código lo que la expresión hace. `ALL` significa dos cosas —"dame toda la
tabla" y "quita estos filtros"— y el lector tiene que deducir cuál por la posición.
`REMOVEFILTERS` solo significa la segunda, así que un `CALCULATE` largo se entiende sin
reconstruirlo.

## La decisión que sí cambia el número: columna o tabla

Con el contexto filtrado a la categoría *Electrónica*:

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

| marca | ventas | `ALL(Brand)` | `REMOVEFILTERS(Brand)` | `ALL(DimProduct)` |
|---|---|---|---|---|
| Apple | 744.415,28 | **11,14%** | **11,14%** ✅ idéntico | **3,74%** |
| Sony | 692.829,80 | 10,37% | 10,37% | 3,48% |
| Jabra | 489.943,26 | 7,33% | 7,33% | 2,46% |

Las dos primeras columnas coinciden hasta el último decimal. La tercera es otra pregunta: al
quitar los filtros de **toda** la tabla se lleva también el de categoría, así que el
denominador pasa de "Electrónica" a todo el catálogo y el porcentaje se divide por tres.

Es la misma trampa que [`ALL`](./all.md), y no desaparece por escribirla con otro nombre.

## No confundir con
- [`ALL`](./all.md) — mismo efecto como modificador, y además función de tabla.
- [`ALLSELECTED`](./allselected.md) — respeta lo que el usuario seleccionó fuera del visual.
- [`KEEPFILTERS`](./keepfilters.md) — el contrario: añade en vez de sustituir.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
