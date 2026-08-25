---
function: SIGN
model: ninguno
---

# SIGN — ejemplos

## 1. Tres valores y nada más, por pequeño que sea el número

`SIGN` no gradúa: cualquier negativo es -1 y cualquier positivo es 1, sin importar la magnitud.

```dax
EVALUATE
ROW(
  "casi_cero_neg", SIGN(-0.0001),
  "muy_negativo", SIGN(-1000000),
  "cero", SIGN(0),
  "casi_cero_pos", SIGN(0.0001)
)
```

```result
casi_cero_neg | muy_negativo | cero | casi_cero_pos
-1 | -1 | 0 | 1
```

Que devuelva **0** y no solo ±1 es lo que la hace útil para agrupar en tres cubos —
empeoró, igual, mejoró— con una sola expresión.

## 2. El blanco sale en blanco, y eso rompe el agrupamiento en tres

```dax
EVALUATE
ROW(
  "sign_blanco", SIGN(BLANK()),
  "es_blanco", ISBLANK(SIGN(BLANK())),
  "sign_cero", SIGN(0),
  "cero_es_blanco", ISBLANK(SIGN(0)),
  "compara", SIGN(BLANK()) = 0
)
```

```result
sign_blanco | es_blanco | sign_cero | cero_es_blanco | compara
(blank) | True | 0 | False | True
```

Hay **cuatro** resultados posibles y no tres: -1, 0, 1 y blanco. Un `SWITCH(SIGN([m]), -1, ..., 0, ..., 1, ...)`
deja las filas sin dato fuera de las tres ramas y las manda al `else`, o a blanco si no hay
`else`. La comparación `= 0` sí las captura, porque el blanco se compara como cero — así que
`SWITCH` y `IF([x] = 0, ...)` **no** clasifican igual.

## 3. Junto con `ABS`, descompone un número en magnitud y dirección

```dax
EVALUATE
VAR X = -42.5
RETURN
ROW(
  "original", X,
  "direccion", SIGN(X),
  "magnitud", ABS(X),
  "reconstruido", SIGN(X) * ABS(X),
  "cuadra", SIGN(X) * ABS(X) = X
)
```

```result
original | direccion | magnitud | reconstruido | cuadra
-42.5 | -1 | 42.5 | -42.5 | True
```

`n = SIGN(n) × ABS(n)` para todo número distinto de cero, y también para el cero. Es la forma
de ordenar por magnitud sin perder el signo, o de pintar de rojo lo que baja usando el mismo
valor que da la altura de la barra.

Ver [`abs`](./abs.md).
