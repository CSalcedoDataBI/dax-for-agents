---
function: DIVIDE
model: ninguno
---

# DIVIDE — ejemplos

## 1. La diferencia con `/` no es el estilo: es que una aborta la consulta

Esta es la razón entera de que `DIVIDE` exista. Con denominador cero, la función devuelve
**blanco** y el operador **mata la consulta**.

```dax
EVALUATE
ROW(
  "con_funcion", DIVIDE(10, 0),
  "con_alternativa", DIVIDE(10, 0, 0),
  "con_operador", IFERROR(10 / 0, "aborta")
)
```

```result
con_funcion | con_alternativa | con_operador
(blank) | 0 | aborta
```

El `IFERROR` está ahí solo para poder enseñar la tercera columna en la misma fila; sin él, la
consulta entera falla y no se ve ninguna de las tres. Eso es lo que le pasa a un informe cuando
una sola fila trae un cero en el denominador.

## 2. El tercer argumento cambia lo que promete la métrica

`DIVIDE(a, b)` sin alternativa devuelve blanco, y el blanco **borra la categoría** de un
gráfico. `DIVIDE(a, b, 0)` la dibuja a ras de suelo. Ninguno está mal; son afirmaciones
distintas.

```dax
EVALUATE
ROW(
  "sin_alternativa", DIVIDE(10, 0),
  "es_blanco", ISBLANK(DIVIDE(10, 0)),
  "con_cero", DIVIDE(10, 0, 0),
  "es_blanco_con_cero", ISBLANK(DIVIDE(10, 0, 0))
)
```

```result
sin_alternativa | es_blanco | con_cero | es_blanco_con_cero
(blank) | True | 0 | False
```

El blanco dice «no lo medí» y el cero dice «lo medí y dio cero». La página
«El blanco borra la categoría; el cero la dibuja» del escenario `contoso` enseña esa diferencia
dibujada, que es donde se ve.

## 3. Un denominador en blanco cuenta como cero, y `0 / 0` también es blanco

```dax
EVALUATE
ROW(
  "denominador_blanco", DIVIDE(10, BLANK()),
  "cero_entre_cero", DIVIDE(0, 0),
  "numerador_blanco", DIVIDE(BLANK(), 5),
  "normal", DIVIDE(10, 4)
)
```

```result
denominador_blanco | cero_entre_cero | numerador_blanco | normal
(blank) | (blank) | (blank) | 2.5
```

Las tres primeras columnas salen igual y **no significan lo mismo**: la primera es un divisor
que faltaba, la segunda una indeterminación, y la tercera un numerador que no existía. `DIVIDE`
las colapsa todas en blanco, así que si tu informe necesita distinguirlas, la distinción tienes
que escribirla tú.

Ver [`quotient`](./quotient.md) para la división entera y [`mod`](./mod.md) para el resto.
