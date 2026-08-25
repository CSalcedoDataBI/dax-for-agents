## Trampa: quita los filtros de SU tabla, no todos

`ALL(DimProduct)` borra los filtros que haya sobre `DimProduct` y **solo esos**. Los de las
demás tablas siguen ahí. Es fácil leerlo como "el total de todo" y no lo es.

Con el contexto en `CategoryName = "Electrónica"` **y** `Year = 2024`:

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
EVALUATE
CALCULATETABLE(
  ROW(
    "contexto",             [Unidades],
    "ALL_solo_DimProduct",  CALCULATE([Unidades], ALL(DimProduct)),
    "ALL_producto_y_fecha", CALCULATE([Unidades], ALL(DimProduct), ALL(DimDate))
  ),
  DimProduct[CategoryName] = "Electrónica",
  DimDate[Year] = 2024
)
```

| denominador | resultado |
|---|---|
| contexto (Electrónica, 2024) | 4.301 |
| `ALL(DimProduct)` | **91.795** ← sigue siendo solo 2024 |
| `ALL(DimProduct), ALL(DimDate)` | **180.224** ← ahora sí, las dos tablas |

91.795 es el total de 2024, no el del modelo. Si tu "% del total" usa `ALL` de una sola
dimensión mientras hay un filtro de fecha vivo, el denominador es "todo dentro del año",
que puede ser justo lo que querías — o no. Hay que decidirlo, no heredarlo.

## No confundir con
- `ALLEXCEPT` — conserva las columnas que le nombres de esa tabla, borra el resto.
- [`ALLSELECTED`](./allselected.md) — respeta lo que el usuario seleccionó.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
