## Trampa: intersecta, no suma

`KEEPFILTERS` no "añade" el filtro nuevo al conjunto anterior: **intersecta** ambos. Si el
contexto ya filtra la misma columna por otro valor, el resultado es vacío, no la unión.

Con el contexto en `Color = "White"`:

| forma | resultado |
|---|---|
| `CALCULATE([Unidades], DimProduct[Color] = "Black")` | 11.102 |
| `CALCULATE([Unidades], KEEPFILTERS(DimProduct[Color] = "Black"))` | **(en blanco)** |

Ver la consulta completa en [`filter`](./filter.md). El blanco es correcto: ningún producto
es blanco y negro a la vez.

## No confundir con
El predicado suelto, que **reemplaza** el filtro de esa columna. `KEEPFILTERS` es lo que
quieres cuando el usuario tiene un slicer puesto y no debes ignorarlo.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
