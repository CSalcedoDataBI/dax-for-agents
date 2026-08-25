## Trampa: depende de quién puso el filtro, no de la fórmula

`ALLSELECTED` devuelve el total de lo que el usuario tiene seleccionado, no el de la tabla
entera. Es el único de la familia `ALL*` cuyo resultado cambia según **de dónde venga** el
filtro: respeta los externos (slicer, filtro de página, la consulta) y quita los que pone
el propio visual fila a fila.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[den ALLEXCEPT] = CALCULATE([Unidades], ALLEXCEPT(DimProduct, DimProduct[CategoryName]))
  MEASURE _Measures[den ALLSELECTED] = CALCULATE([Unidades], ALLSELECTED(DimProduct))
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(
    VALUES(DimProduct[Brand]),
    "unidades", [Unidades],
    "den_ALLEXCEPT", [den ALLEXCEPT],
    "den_ALLSELECTED", [den ALLSELECTED]
  ),
  DimProduct[CategoryName] = "Electrónica",
  DimProduct[Brand] IN {"Apple", "Sony"}
)
```

| marca | unidades | den_ALLEXCEPT | den_ALLSELECTED |
|---|---|---|---|
| Apple | 1.219 | 8.386 | **2.411** |
| Sony | 1.192 | 8.386 | **2.411** |

Que esa misma medida dé otro número al moverla a otro visual **no es un bug**: es la
definición. Por eso es la función más difícil de depurar de la familia — el código no
cambia y el resultado sí.

## No confundir con
`ALL` (quita los filtros de **su** tabla, no los de las demás — ver [`all`](./all.md), donde
está medido) y `ALLEXCEPT` (todo lo de esa tabla menos las columnas nombradas, ver
[`allexcept`](./allexcept.md)).

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
