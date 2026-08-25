## Trampa: la transición de contexto no se ve en el código

Referenciar una **medida** dentro de un iterador envuelve la expresión en un `CALCULATE`
implícito, y ese `CALCULATE` convierte la fila actual en filtro. Escribir la misma fórmula
"desplegada" no hace lo mismo, y el resultado no se parece en nada.

```dax
DEFINE MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
EVALUATE
{
  ("SUMX con la MEDIDA",    SUMX(DimProduct, [Unidades])),
  ("SUMX con la EXPRESIÓN", SUMX(DimProduct, SUM(FactSales[Quantity]))),
  ("total real",            SUM(FactSales[Quantity]))
}
```

| expresión | resultado |
|---|---|
| `SUMX(DimProduct, [Unidades])` | **180.224** ✅ |
| `SUMX(DimProduct, SUM(FactSales[Quantity]))` | **24.690.688** ❌ |
| `SUM(FactSales[Quantity])` | 180.224 |

24.690.688 = 180.224 × 137. Sin transición de contexto cada producto recibe el total
general y se suma 137 veces. El síntoma es un número absurdamente grande, múltiplo exacto
del total — si ves eso, busca un iterador sin medida dentro.

## No confundir con
`CALCULATE` explícito. `SUMX(DimProduct, CALCULATE(SUM(FactSales[Quantity])))` sí da
180.224: es exactamente lo que hace la referencia a la medida.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
