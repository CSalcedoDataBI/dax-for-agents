---
function: RAND
model: ninguno
---

# RAND — ejemplos

> Los bloques `result` de esta ficha afirman **propiedades** y no valores: `RAND` no devuelve
> dos veces lo mismo, así que un número concreto no se podría volver a comprobar.

## 1. Cada llamada devuelve un valor distinto, incluso en la misma fila

Esto es lo que rompe las medidas que llaman a `RAND` más de una vez creyendo que hablan del
mismo número.

```dax
EVALUATE
ROW(
  "dentro_del_rango", RAND() >= 0 && RAND() < 1,
  "dos_llamadas_difieren", RAND() <> RAND(),
  "nunca_es_blanco", ISBLANK(RAND())
)
```

```result
dentro_del_rango | dos_llamadas_difieren | nunca_es_blanco
True | True | False
```

El intervalo es **[0, 1)**: el cero puede salir y el uno no. Y `RAND()` nunca devuelve blanco,
a diferencia de casi todo lo demás en esta categoría.

## 2. Una variable lo congela; repetir la llamada no

Si necesitas usar el mismo número aleatorio dos veces —comparar contra un umbral y además
mostrarlo—, tiene que pasar por un `VAR`.

```dax
EVALUATE
VAR Sorteo = RAND()
RETURN
ROW(
  "la_variable_es_estable", Sorteo = Sorteo,
  "la_funcion_no", RAND() <> RAND(),
  "umbral_coherente", (Sorteo < 0.5) = (Sorteo < 0.5)
)
```

```result
la_variable_es_estable | la_funcion_no | umbral_coherente
True | True | True
```

Sin el `VAR`, `IF(RAND() < 0.5, RAND(), 0)` sortea **dos veces**: una para decidir y otra para
el valor que devuelve.

## 3. Se recalcula, así que no sirve para una columna estable

`RAND` es no determinista. En una medida se reevalúa cada vez que se refresca el visual; en una
columna calculada se fija en el refresco, pero cambia en el siguiente. Para un identificador
estable no vale.

```dax
EVALUATE
VAR Muestra = GENERATESERIES(1, 200, 1)
VAR ConSorteo = ADDCOLUMNS(Muestra, "r", RAND())
RETURN
ROW(
  "todos_en_rango", COUNTROWS(FILTER(ConSorteo, [r] < 0 || [r] >= 1)),
  "hay_variedad", COUNTROWS(DISTINCT(SELECTCOLUMNS(ConSorteo, "v", [r]))) > 190,
  "cuantos", COUNTROWS(ConSorteo)
)
```

```result
todos_en_rango | hay_variedad | cuantos
(blank) | True | 200
```

Ninguna de las 200 filas se sale del intervalo —la primera columna cuenta las que sí y da
blanco— y casi todas son distintas. Si quieres reproducibilidad, la semilla tiene que venir de
los datos: algo como `MOD(HASH_de_la_clave, n)` escrito a mano.

Ver [`randbetween`](./randbetween.md).
