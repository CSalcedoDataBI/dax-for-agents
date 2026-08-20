## Trampa: un `+ 0` cambia el denominador

`AVERAGEX` **salta los blancos**, igual que `AVERAGE`: divide entre las filas que tienen
valor, no entre todas. La intuición de que "el iterador recorre todas las filas y por tanto
cuenta las vacías" es falsa, y está medida.

Lo que sí cambia el resultado es cualquier expresión que convierta el blanco en cero. Un
`COALESCE` puesto por seguridad, o un simple `+ 0`, mueve el denominador.

Sobre cinco tiendas de las que **dos tienen los metros en blanco** (100 + 200 + 300 = 600;
entre 3 son 200, entre 5 son 120):

```dax
EVALUATE
ROW(
  "AVERAGE",               AVERAGE(Tiendas[Metros]),
  "AVERAGEX_columna",      AVERAGEX(Tiendas, Tiendas[Metros]),
  "AVERAGEX_con_COALESCE", AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0)),
  "AVERAGEX_con_mas_cero", AVERAGEX(Tiendas, Tiendas[Metros] + 0)
)
```

| expresión | resultado | divide entre |
|---|---|---|
| `AVERAGE(Tiendas[Metros])` | **200** | 3 |
| `AVERAGEX(Tiendas, Tiendas[Metros])` | **200** | 3 |
| `AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0))` | **120** | 5 |
| `AVERAGEX(Tiendas, Tiendas[Metros] + 0)` | **120** | 5 |

**`Tiendas[Metros] + 0` baja la media de 200 a 120.** El `+ 0` no altera ningún valor
existente; lo único que hace es que el blanco deje de ser blanco, y con eso entra en el
denominador.

El `COALESCE` es peor porque parece deliberado: quien lo escribe cree estar evitando un
error, y lo que hace es cambiar la definición de la métrica.

Ninguno de los dos números está mal — depende de si "sin dato" significa "no aplica" o
"cero". Lo que está mal es que esa decisión quede escondida en un `+ 0`.

## No confundir con
`AVERAGE`, que aquí da exactamente lo mismo. La diferencia entre ambas no es el tratamiento
del blanco: es que `AVERAGEX` puede promediar una **expresión** y `AVERAGE` solo una columna.

> Modelo, datos y consultas en [`lab/blancos`](../../lab/blancos/) — se abre en Power BI
> Desktop y se ejecuta. Medido el 2026-08-12.
