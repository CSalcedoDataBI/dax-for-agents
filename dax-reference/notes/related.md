## Trampa: necesita contexto de fila y una relación en el sentido correcto

`RELATED` va de **muchos a uno**: desde la tabla de hechos hacia la dimensión. Solo funciona
donde hay contexto de fila — una columna calculada o dentro de un iterador. En una medida
suelta no compila.

```dax
EVALUATE
ADDCOLUMNS(
  VALUES(DimProduct[ProductKey]),
  "SUMX_con_RELATED",
    SUMX(RELATEDTABLE(FactSales), FactSales[Quantity] * RELATED(DimProduct[Price]))
)
```

Funciona porque `SUMX` abre contexto de fila sobre `FactSales`, y desde ahí `RELATED` puede
subir a `DimProduct`. Resultado para ProductKey 114: **127.515,72**.

## No confundir con
[`RELATEDTABLE`](./relatedtable.md), que va en el sentido contrario (uno a muchos) y
devuelve una tabla, no un valor.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
