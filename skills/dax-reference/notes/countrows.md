## Trampa: cuenta filas, no valores — y eso importa cuando hay blancos

`COUNTROWS(T)` cuenta las filas de T tal como queda tras el contexto de filtro, sin mirar el
contenido. Es lo que casi siempre se quiere para "cuántos hay", y es justo donde `COUNT` se
comporta distinto.

`DimStore[CloseDate]` está vacía en las 25 tiendas:

```dax
EVALUATE
ROW(
  "COUNTROWS_DimStore", COUNTROWS(DimStore),
  "COUNT_CloseDate",    COUNT(DimStore[CloseDate])
)
```

| expresión | resultado |
|---|---|
| `COUNTROWS(DimStore)` | **25** |
| `COUNT(DimStore[CloseDate])` | **(en blanco)** |

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura y no toca el modelo. Se ejecuta y se compara sola con `python
> lab/check_lab.py contoso localhost:<puerto>`.

## No confundir con
[`COUNT`](./count.md), que descarta blancos y puede devolver blanco donde esperabas cero.
Microsoft
[recomienda COUNTROWS sobre COUNT](https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows),
y esa página no está en la ficha de la función.

## Trampa: la fila en blanco se ve desde el lado *uno*, no desde el hecho

Cuando la tabla de hechos referencia una clave que no existe en la dimensión, el motor añade
una fila en blanco **a la dimensión**. Medido en
[`lab/claves-huerfanas`](../../../lab/claves-huerfanas/), con una sola clave huérfana:

| expresión | resultado | |
|---|---|---|
| `COUNTROWS(DimProducto)` | **3** | la tabla base no la tiene |
| `COUNTROWS(VALUES(DimProducto[ProductoKey]))` | **4** | ← aquí aparece |
| `COUNTROWS(VALUES(Ventas[ProductoKey]))` | **4** | pero son 1, 2, 3 y **99**: la clave real |

Los dos `VALUES` dan 4 y **no significan lo mismo**. Del lado *uno* el cuarto elemento es la
fila inventada; del lado *muchos* es el valor huérfano de verdad. Confundirlos hace creer que
la fila en blanco está en los hechos, y no lo está.

Y limpiar esa fila cuesta caro: `SUMX(ALLNOBLANKROW(...))` da **60** donde el total es
**110**. Las 50 unidades huérfanas desaparecen sin aviso.

> Medido en [`lab/claves-huerfanas`](../../../lab/claves-huerfanas/) el 2026-08-12, **no** sobre
> Contoso: Contoso tiene la integridad referencial intacta y por eso no puede demostrar nada
> de esta sección. El modelo, los datos y las consultas están ahí para ejecutarlos.
