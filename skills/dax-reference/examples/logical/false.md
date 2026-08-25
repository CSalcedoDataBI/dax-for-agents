---
function: FALSE
model: ninguno
---

# FALSE — ejemplos

## 1. Un blanco y un FALSE son iguales con `=`, distintos con `==`

```dax
EVALUATE
ROW(
  "false_mas_cero",  FALSE() + 0,
  "blanco_igual",    BLANK() = FALSE(),
  "blanco_estricto", BLANK() == FALSE(),
  "es_blanco_false", ISBLANK(FALSE())
)
```

```result
false_mas_cero | blanco_igual | blanco_estricto | es_blanco_false
0 | True | False | False
```

Es la misma distinción que arrastra media biblioteca: `=` iguala el blanco a su valor
neutro, `==` no.

Lo que **no** se puede es compararlo con el número que representa, aunque en aritmética
valga cero:

```dax
EVALUATE ROW("comparado_con_cero", FALSE() = 0)
```

```result
ERROR: DAX comparison operations do not support comparing values of type True/False with values of type Integer. Consider using the VALUE or FORMAT function to convert one of the values.
```

## 2. Devolver FALSE no es lo mismo que devolver blanco

Una medida que devuelve `FALSE()` ocupa sitio en el visual; una que devuelve blanco
desaparece. La diferencia decide si una fila se ve o no.

```dax
EVALUATE
ROW(
  "es_blanco_false",  ISBLANK(FALSE()),
  "es_blanco_blanco", ISBLANK(BLANK()),
  "if_sin_else",      ISBLANK(IF(FALSE(), "sí")),
  "cuenta_vacia",     COUNTROWS(FILTER({1, 2, 3}, FALSE()))
)
```

```result
es_blanco_false | es_blanco_blanco | if_sin_else | cuenta_vacia
False | True | True | (blank)
```

`COUNTROWS` de una tabla vacía devuelve blanco, no cero — otra vez lo mismo.

## 3. Como filtro constante, apaga la expresión entera

Útil para aislar un problema: sustituir una condición por `FALSE()` y ver qué queda.

```dax
EVALUATE
ROW(
  "filtro_falso",  COUNTROWS(FILTER({1, 2, 3}, FALSE())),
  "filtro_cierto", COUNTROWS(FILTER({1, 2, 3}, TRUE())),
  "es_vacia",      ISEMPTY(FILTER({1, 2, 3}, FALSE()))
)
```

```result
filtro_falso | filtro_cierto | es_vacia
(blank) | 3 | True
```
