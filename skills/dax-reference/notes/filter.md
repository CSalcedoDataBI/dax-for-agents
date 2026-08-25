## Trampa: `CALCULATE(m, FILTER(T, p))` y `CALCULATE(m, p)` no son la misma cosa

Se leen como sinónimos y devuelven resultados distintos. `FILTER(T, p)` **itera T dentro
del contexto de filtro actual**; el predicado suelto se expande a `FILTER(ALL(columna), p)`
y por tanto **reemplaza** el filtro que hubiera sobre esa columna.

Con el contexto puesto en `Color = "White"`:

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[a] = CALCULATE([Unidades], FILTER(DimProduct, DimProduct[Color] = "Black"))
  MEASURE _Measures[b] = CALCULATE([Unidades], DimProduct[Color] = "Black")
  MEASURE _Measures[c] = CALCULATE([Unidades], KEEPFILTERS(DimProduct[Color] = "Black"))
EVALUATE
CALCULATETABLE(
  ROW("contexto", [Unidades], "a_FILTER", [a], "b_predicado", [b], "c_KEEPFILTERS", [c]),
  DimProduct[Color] = "White"
)
```

| forma | resultado |
|---|---|
| contexto (`White`) | 3.450 |
| `FILTER(DimProduct, Color="Black")` | **(en blanco)** |
| `DimProduct[Color] = "Black"` | **11.102** |
| `KEEPFILTERS(Color="Black")` | (en blanco) |

`FILTER` recorre los productos que quedan tras el filtro White: ninguno es Black, así que
la tabla sale vacía y la medida en blanco. El predicado quita el filtro de color y da el
total de Black. Ninguno de los dos está "mal" — miden cosas distintas, y esa es la trampa.

## No confundir con
`KEEPFILTERS`, que sí conserva el filtro existente y lo **intersecta**: White ∩ Black es
vacío, de ahí el blanco. Úsalo cuando quieras añadir una condición sin pisar la del usuario.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
