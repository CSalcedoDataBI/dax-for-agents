## Trampa: ignora el slicer del usuario

`ALLEXCEPT(T, col)` conserva **solo** los filtros de las columnas que le nombras y borra
todos los demás. Suena a "total de la categoría", y lo es — pero también borra la selección
que el usuario haya hecho en cualquier otra columna de esa tabla.

Contexto: `CategoryName = "Electrónica"` **y** `Brand IN {Apple, Sony}`.

| marca | unidades | `ALLEXCEPT(…, CategoryName)` | `ALLSELECTED(DimProduct)` |
|---|---|---|---|
| Apple | 1.219 | **8.386** | 2.411 |
| Sony | 1.192 | **8.386** | 2.411 |

2.411 = 1.219 + 1.192: con `ALLSELECTED` los porcentajes suman 100 %. Con `ALLEXCEPT` el
denominador es toda la categoría aunque el usuario solo mire dos marcas, así que suman 29 %
y el informe parece roto.

Ver la consulta completa en [`allselected`](./allselected.md).

## No confundir con
`ALLSELECTED`, que es lo que casi siempre se quiere para un "% del total visible".
`ALLEXCEPT` es correcto cuando el denominador debe ser la categoría **pase lo que pase**.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
