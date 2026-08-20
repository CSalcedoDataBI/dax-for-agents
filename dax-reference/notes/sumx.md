## Trampa: el iterador solo filtra si dentro hay una medida

`SUMX(T, expr)` abre contexto de **fila** sobre T. El contexto de fila no filtra por sí
mismo: hace falta una transición de contexto para que la fila actual se convierta en filtro.
Referenciar una medida la provoca; escribir la agregación a mano, no.

```dax
DEFINE MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
EVALUATE
{
  ("SUMX con la MEDIDA",    SUMX(DimProduct, [Unidades])),
  ("SUMX con la EXPRESIÓN", SUMX(DimProduct, SUM(FactSales[Quantity])))
}
```

| expresión | resultado |
|---|---|
| `SUMX(DimProduct, [Unidades])` | **180.224** ✅ |
| `SUMX(DimProduct, SUM(FactSales[Quantity]))` | **24.690.688** ❌ |

24.690.688 = 180.224 × 137. Ver [`calculate`](./calculate.md) para el mecanismo.

Sobre la **propia** tabla del iterador no hace falta: `SUMX(FactSales, FactSales[Quantity] *
FactSales[NetPrice])` es correcto, porque lee columnas de la fila actual en vez de agregar
otra tabla.

## Y además cuesta: ~290× sobre dos millones de filas

La transición de contexto no solo cambia el número. Sobre una tabla de 2.000.000 de filas,
con las dos formas devolviendo **el mismo** resultado:

| | mediana en frío | pico de memoria |
|---|---|---|
| `SUMX(Ventas, [Total])` | **871 ms** | **~193 MB** |
| `SUMX(Ventas, Ventas[Importe])` | **3 ms** | 0 |

Dos millones de transiciones de contexto, una por fila. En el mismo modelo, envolver la tabla
entera en un `FILTER` —lo que todo el mundo llama caro— no costó nada medible: el motor empuja
el predicado al almacenamiento. **El bulto es la medida dentro del iterador, no el `FILTER`.**

Medido en el escenario [`lab/rendimiento`](../../lab/rendimiento/README.md), que se puede
abrir y volver a correr. Los milisegundos son de un portátil; la razón es lo que aguanta un
cambio de máquina.

## No confundir con
`SUM`, que no abre contexto de fila. Si tu expresión multiplica dos columnas fila a fila,
necesitas el iterador; si solo suma una columna, `SUM` es más barato y más claro.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-12. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
