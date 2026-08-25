---
function: COMBINEVALUES
model: ninguno
---

# COMBINEVALUES — ejemplos

## 1. Existe para claves compuestas, y no comprueba colisiones

Une valores con un delimitador para poder relacionar dos tablas por más de una columna. Lo
que **no** hace es asegurarse de que el delimitador no aparezca dentro de los valores — y ahí
dos filas distintas producen la misma clave.

```dax
EVALUATE
ROW(
  "normal",     COMBINEVALUES("-", "ES", "2024"),
  "colision_a", COMBINEVALUES("-", "ES-2", "024"),
  "colision_b", COMBINEVALUES("-", "ES", "2-024"),
  "iguales",    COMBINEVALUES("-", "ES-2", "024") = COMBINEVALUES("-", "ES", "2-024")
)
```

```result
normal | colision_a | colision_b | iguales
ES-2024 | ES-2-024 | ES-2-024 | True
```

Dos pares de valores **distintos** dan la misma clave. La relación los cruza como si fueran
el mismo, y no hay error: hay filas de más.

Por eso el delimitador debe ser un carácter que el dato no pueda contener. Y aquí llega la
restricción que no está en la firma: **tiene que ser una constante literal**. No se puede
calcular, así que la vía obvia —`UNICHAR(31)`, un carácter de control que ningún dato trae—
está cerrada:

```dax
EVALUATE ROW("delimitador_calculado", COMBINEVALUES(UNICHAR(31), "a", "b"))
```

```result
ERROR: The delimiter value in the 'COMBINEVALUES' function can only be a constant non empty string.
```

Queda escribirlo literal, con una secuencia lo bastante rara. `raro` sale **falso**: con
`||#||` los dos pares de valores dejan de producir la misma clave, que era el problema.

```dax
EVALUATE
ROW(
  "raro",     COMBINEVALUES("||#||", "ES-2", "024") = COMBINEVALUES("||#||", "ES", "2-024"),
  "resultado", COMBINEVALUES("||#||", "ES", "2024")
)
```

```result
raro | resultado
False | ES||#||2024
```

## 2. Acepta más de dos valores, y convierte lo que no sea texto

```dax
EVALUATE
ROW(
  "tres",     COMBINEVALUES("|", "a", "b", "c"),
  "con_numero", COMBINEVALUES("|", "ES", 2024),
  "decimal",  COMBINEVALUES("|", "x", 1.5),
  "booleano", COMBINEVALUES("|", "x", TRUE())
)
```

```result
tres | con_numero | decimal | booleano
a|b|c | ES|2024 | x|1,5 | x|TRUE
```

La conversión usa la cultura del modelo, así que una clave construida con un decimal **no es
portable** entre modelos con distinta configuración regional.

## 3. Con blancos

```dax
EVALUATE
ROW(
  "blanco_en_medio", COMBINEVALUES("-", "a", BLANK(), "c"),
  "blanco_al_final", COMBINEVALUES("-", "a", BLANK()),
  "todos_blancos",   COMBINEVALUES("-", BLANK(), BLANK()),
  "es_blanco",       ISBLANK(COMBINEVALUES("-", BLANK(), BLANK()))
)
```

```result
blanco_en_medio | blanco_al_final | todos_blancos | es_blanco
a--c | a- | - | False
```

El delimitador se escribe igualmente, así que un blanco deja un hueco visible en la clave —
lo cual, para variar, es bueno: la colisión con un valor vacío de verdad se ve.
