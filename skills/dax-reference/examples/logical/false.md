---
function: FALSE
model: ninguno
---

# FALSE — examples

## 1. A blank and a FALSE are equal with `=`, different with `==`

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

It is the same distinction half this library carries: `=` equates the blank to its neutral value,
`==` does not.

What you **cannot** do is compare it with the number it represents, even though in arithmetic it
is worth zero:

```dax
EVALUATE ROW("comparado_con_cero", FALSE() = 0)
```

```result
ERROR: DAX comparison operations do not support comparing values of type True/False with values of type Integer. Consider using the VALUE or FORMAT function to convert one of the values.
```

## 2. Returning FALSE is not the same as returning blank

A measure returning `FALSE()` takes up space in the visual; one returning blank disappears. The
difference decides whether a row is seen at all.

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

`COUNTROWS` of an empty table returns blank, not zero — the same thing again.

## 3. As a constant filter, it switches the whole expression off

Useful for isolating a problem: replace a condition with `FALSE()` and see what is left.

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
