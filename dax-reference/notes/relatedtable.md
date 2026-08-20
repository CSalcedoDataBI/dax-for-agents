## Trampa: devuelve una tabla, y va de uno a muchos

`RELATEDTABLE` es el espejo de `RELATED`: desde la dimensión hacia los hechos. Devuelve
**una tabla**, así que casi siempre va envuelta en `COUNTROWS` o en un iterador.

```dax
EVALUATE
ADDCOLUMNS(
  VALUES(DimProduct[ProductKey]),
  "filas_de_venta", COUNTROWS(RELATEDTABLE(FactSales))
)
```

| ProductKey | filas_de_venta |
|---|---|
| 114 | 7.861 |
| 121 | 7.594 |
| 118 | 6.218 |

## Qué es por dentro
`RELATEDTABLE(T)` es `CALCULATETABLE(T)`: lleva transición de contexto, y por eso la fila de
la dimensión acaba filtrando los hechos. Saberlo explica el resultado — no es magia de
relaciones, es el mismo `CALCULATE` de siempre.

Esta nota **no afirma nada sobre rendimiento**. Sobre este modelo (137 productos, 126.524
filas de hechos) las consultas tardan milisegundos de un dígito, así que cualquier cifra de
coste o umbral de cardinalidad sería una suposición disfrazada de medición. Si necesitas
decidir por rendimiento, mídelo en tu modelo con el analizador de consultas.

## No confundir con
[`RELATED`](./related.md), que va de muchos a uno y devuelve un valor escalar.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
