## Trampa: `RANKX(VALUES(...))` devuelve 1 para todo

`RANKX(<tabla>, <expr>)` clasifica dentro de la tabla que le pasas, y esa tabla se evalúa
**en el contexto de filtro de la fila que se está pintando**. En una matriz o un
`SUMMARIZECOLUMNS`, ese contexto ya tiene una sola marca, así que `VALUES(DimProduct[Brand])`
devuelve **una fila** y clasificar dentro de una lista de uno da siempre 1.

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

| marca | ventas | `RANKX(VALUES(...))` | `RANKX(ALL(...))` |
|---|---|---|---|
| Sony | 1.273.417,32 | **1** | 1 ✅ |
| Microsoft | 1.164.898,94 | **1** ❌ | 2 ✅ |
| Nintendo | 1.131.477,23 | **1** ❌ | 3 ✅ |
| Lutron | 1.066.213,09 | **1** ❌ | 4 ✅ |
| Apple | 744.415,28 | **1** ❌ | 5 ✅ |

Es el fallo más silencioso de la función: no da error ni blanco, da un número plausible.
Una columna entera de unos parece un ranking hasta que alguien la mira dos veces.

La tabla que clasifica tiene que **ignorar** el filtro de la columna por la que clasificas:
`ALL(DimProduct[Brand])` para rankear contra todo el catálogo, o
[`ALLSELECTED`](./allselected.md) para rankear contra lo que el usuario dejó seleccionado —
que casi siempre es lo que la gente quiere cuando pone un slicer.

## Empates y huecos

Por defecto `RANKX` usa `Skip`: dos empatados en 3 dejan el 4 vacío y el siguiente es 5. Con
`Dense` no hay huecos. El argumento va en la quinta posición, detrás de `<order>`, así que se
olvida con facilidad.

## No confundir con
- [`TOPN`](./topn.md) — se lleva las filas de cabeza, y **no devuelve N filas** si hay empates.
- `RANK` — la función nueva de ventana, con `ORDERBY`/`PARTITIONBY` explícitos en vez de una
  tabla. Más clara cuando ya estás en una consulta.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
