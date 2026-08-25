---
function: TRUE
model: ninguno
---

# TRUE — ejemplos

## 1. Es una función, y lleva paréntesis

`TRUE` no es una palabra reservada: es una función sin argumentos. Sin `()` DAX intenta
resolverla como un nombre y falla.

```dax
EVALUATE
ROW(
  "con_parentesis", TRUE(),
  "comparada",      TRUE() = TRUE(),
  "dentro_de_if",   IF(TRUE(), "rama SI", "rama NO")
)
```

```result
con_parentesis | comparada | dentro_de_if
True | True | rama SI
```

## 2. Vale 1 en aritmética, pero NO se puede comparar con 1

Esto es lo que se descubre ejecutándolo. `TRUE() + 0` da 1 sin problema, así que la intuición
dice que `TRUE() = 1` también debería funcionar. No funciona: DAX se niega a comparar un
booleano con un entero.

```dax
EVALUATE
ROW(
  "true_mas_cero",  TRUE() + 0,
  "false_mas_cero", FALSE() + 0,
  "suma_de_tres",   (1 = 1) + (2 = 2) + (3 = 4)
)
```

```result
true_mas_cero | false_mas_cero | suma_de_tres
1 | 0 | 2
```

`(1=1) + (2=2) + (3=4)` cuenta cuántas condiciones se cumplen sin escribir tres `IF`. La
conversión ocurre porque el `+` la fuerza; la comparación no la fuerza y por eso aborta:

```dax
EVALUATE ROW("comparado_con_uno", TRUE() = 1)
```

```result
ERROR: DAX comparison operations do not support comparing values of type True/False with values of type Integer. Consider using the VALUE or FORMAT function to convert one of the values.
```

Si necesitas comparar, convierte tú primero:

```dax
EVALUATE ROW("convertido_antes", TRUE() + 0 = 1)
```

```result
convertido_antes
True
```

## 3. Comparar contra TRUE() con `=` o con `==` no es lo mismo

```dax
EVALUATE
ROW(
  "sin_comparar",     IF(1 = 1, "sí", "no"),
  "comparado_simple", IF((1 = 1) = TRUE(), "sí", "no"),
  "blanco_simple",    IF(BLANK() = TRUE(), "sí", "no"),
  "blanco_estricto",  IF(BLANK() == TRUE(), "sí", "no")
)
```

```result
sin_comparar | comparado_simple | blanco_simple | blanco_estricto
sí | sí | no | no
```

Ver [`false`](./false.md), y la nota de campo de [`blank`](../../notes/blank.md) para el
mecanismo detrás de `=` frente a `==`.
