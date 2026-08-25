## Trampa: sin `orderBy` el orden es arbitrario, no el de la tabla

`CONCATENATEX` recorre la tabla que le das en el orden que el motor decida. Pasarle un
[`TOPN`](./topn.md) ordenado por ventas **no** conserva ese orden: el resultado sale
plausible —una lista de marcas separadas por comas— y no está ordenado por nada.

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
EVALUATE
VAR Top5 = TOPN(5, VALUES(DimProduct[Brand]), [Ventas], DESC)
RETURN
{
  ("sin orderBy",           CONCATENATEX(Top5, DimProduct[Brand], ", ")),
  ("orderBy ventas DESC",   CONCATENATEX(Top5, DimProduct[Brand], ", ", [Ventas], DESC)),
  ("orderBy alfabético",    CONCATENATEX(Top5, DimProduct[Brand], ", ", DimProduct[Brand], ASC))
}
```

| expresión | resultado |
|---|---|
| sin `orderBy` | `Apple, Nintendo, Lutron, Microsoft, Sony` ❌ |
| `orderBy` ventas DESC | `Sony, Microsoft, Nintendo, Lutron, Apple` ✅ |
| `orderBy` alfabético | `Apple, Lutron, Microsoft, Nintendo, Sony` ✅ |

El primero no está ordenado por ventas ni por nombre. Es el peor tipo de fallo para un texto
en un informe: **"Top 5: Apple, Nintendo, Lutron…" se lee como un ranking y no lo es.**

El orden sin `orderBy` tampoco está garantizado entre ejecuciones ni entre versiones del
motor. Que hoy salga uno concreto no es una promesa.

## El separador va antes que el orden

La firma es `CONCATENATEX(<tabla>, <expr>, [<delimitador>], [<orderBy>], [<order>])`. El
delimitador es opcional, así que es fácil escribir el `orderBy` en su hueco y acabar con las
marcas pegadas sin separador — un error que no da error.

Para el último elemento con "y" en vez de coma no hay argumento: se construye aparte.

## No confundir con
- `CONCATENATE` — junta **dos** cadenas, no una tabla. Para varias, el operador `&` encadena
  mejor.
- `COMBINEVALUES` — pensado para claves compuestas, no para texto legible.

> Medido sobre [`lab/contoso`](../../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
