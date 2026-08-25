## Trampa: sin `EARLIER` la comparación es siempre verdadera

Dentro de un `FILTER` anidado sobre la misma tabla, `DimProduct[Col] = DimProduct[Col]`
compara la fila interna consigo misma. Es cierta siempre, así que el filtro no filtra nada
y devuelve la tabla entera — sin error, sin aviso.

```dax
EVALUATE
ADDCOLUMNS(
  SUMMARIZE(DimProduct, DimProduct[CategoryName], DimProduct[Brand]),
  "con_EARLIER",     COUNTROWS(FILTER(DimProduct, DimProduct[CategoryName] = EARLIER(DimProduct[CategoryName]))),
  "sin_EARLIER_mal", COUNTROWS(FILTER(DimProduct, DimProduct[CategoryName] = DimProduct[CategoryName]))
)
```

| categoría | con_EARLIER | sin_EARLIER |
|---|---|---|
| Electrónica | **46** ✅ | **137** ❌ |

137 es el total de productos del modelo. El síntoma es que todas las filas del resultado
muestran el mismo número.

## No confundir con
Una **variable**. `VAR cat = DimProduct[CategoryName]` capturada antes del `FILTER` hace lo
mismo y se lee sin pensar en cuántos contextos de fila hay abiertos. `EARLIER` sigue siendo
necesario en columnas calculadas antiguas, pero en código nuevo la variable gana casi siempre.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
