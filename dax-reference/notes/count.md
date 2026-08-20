## Trampa: sobre una columna entera en blanco devuelve blanco, no cero

`COUNT` cuenta valores, no filas: descarta los blancos. Si la columna está entera en blanco
el resultado es **(en blanco)**, no `0` — y un blanco desaparece del visual mientras que un
cero se dibuja.

`DimStore[CloseDate]` está vacía en las 25 tiendas (ninguna ha cerrado):

```dax
EVALUATE
ROW(
  "COUNT_CloseDate",      COUNT(DimStore[CloseDate]),
  "COUNTROWS_DimStore",   COUNTROWS(DimStore),
  "COUNTBLANK_CloseDate", COUNTBLANK(DimStore[CloseDate])
)
```

| expresión | resultado |
|---|---|
| `COUNT(DimStore[CloseDate])` | **(en blanco)** |
| `COUNTROWS(DimStore)` | **25** |
| `COUNTBLANK(DimStore[CloseDate])` | 25 |

Si querías "cuántas tiendas hay", `COUNT` sobre una columna con blancos te da otra cosa.

## No confundir con
[`COUNTROWS`](./countrows.md), que cuenta filas y no mira el contenido. Microsoft
[recomienda COUNTROWS sobre COUNT](https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows)
por este motivo, y esa página no está en la ficha de la función.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
