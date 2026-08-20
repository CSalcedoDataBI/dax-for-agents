## Trampa: `TOPN(3, ...)` no devuelve 3 filas

Con empates en el valor de orden, `TOPN` se lleva **todas** las filas empatadas en el último
puesto. Pides 3 y te pueden llegar 4, o 7. Si lo que sigue asume 3 —una división, un
`CONCATENATEX`, un "top 3" en un título— el número que sale es otro.

```dax
EVALUATE
VAR PorColor = SUMMARIZE(DimProduct, DimProduct[Color], "N", COUNTROWS(DimProduct))
RETURN
{
  ("colores distintos",              COUNTROWS(PorColor)),
  ("TOPN 3 por N",                   COUNTROWS(TOPN(3, PorColor, [N], DESC))),
  ("TOPN 5 por N",                   COUNTROWS(TOPN(5, PorColor, [N], DESC))),
  ("TOPN 3 con desempate por Color", COUNTROWS(TOPN(3, PorColor, [N], DESC, DimProduct[Color], ASC)))
}
```

| expresión | filas devueltas |
|---|---|
| colores distintos | 15 |
| `TOPN(3, …)` | **4** ❌ |
| `TOPN(5, …)` | **6** ❌ |
| `TOPN(3, …, DimProduct[Color], ASC)` | **3** ✅ |

El arreglo es un criterio de desempate: `TOPN` acepta más pares `<orderBy>, <order>` después
del primero, y con uno que sea único (una clave, un nombre) el empate deja de existir.

Elegir el desempate es una decisión, no un detalle: alfabético por nombre es arbitrario pero
**estable**, y estable es lo que hace que el informe diga lo mismo mañana.

## `N` no acota, ordena

`TOPN` no garantiza el orden de lo que devuelve; garantiza *qué* filas. Para que salgan
ordenadas hay que ordenarlas después — con `ORDER BY` en la consulta, o con el `orderBy` de
[`CONCATENATEX`](./concatenatex.md) si vas a pegarlas en un texto.

Un `N` de 0 o negativo devuelve una tabla vacía, no un error.

## No confundir con
- [`RANKX`](./rankx.md) — numera, no recorta. Es lo que quieres si necesitas el puesto.
- `SAMPLE` — devuelve filas repartidas, no las de cabeza.

> Medido sobre [`lab/contoso`](../../lab/contoso/) —Contoso Retail, FactSales 126.524
> filas, 137 productos, DimDate 2023-01-01 a 2024-12-31— el 2026-08-13. La consulta es de
> solo lectura: define sus medidas con `DEFINE` y no toca el modelo. Se ejecuta y se
> compara sola con `python lab/check_lab.py contoso localhost:<puerto>`.
