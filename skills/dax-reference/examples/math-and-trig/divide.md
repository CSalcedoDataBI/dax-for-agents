---
function: DIVIDE
model: ninguno
---

# DIVIDE — examples

## 1. The difference from `/` is not style: it is that one aborts the query

This is the entire reason `DIVIDE` exists. With a zero denominator, the function returns
**blank** and the operator **kills the query**.

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

The `IFERROR` is only there so the third column can be shown on the same row; without it the
whole query fails and none of the three is visible. That is what happens to a report when a
single row carries a zero in the denominator.

## 2. The third argument changes what the metric promises

`DIVIDE(a, b)` with no alternative returns blank, and the blank **erases the category** from a
chart. `DIVIDE(a, b, 0)` draws it flat on the floor. Neither is wrong; they are different claims.

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

The blank says "I did not measure it" and the zero says "I measured it and it was zero". The
«El blanco borra la categoria; el cero la dibuja» page of the `contoso` scenario shows that
difference drawn, which is where you see it.

## 3. A blank denominator counts as zero, and `0 / 0` is blank too

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

The first three columns come out the same and **do not mean the same thing**: the first is a
divisor that was missing, the second an indeterminate form, and the third a numerator that did
not exist. `DIVIDE` collapses them all into blank, so if your report needs to tell them apart,
you have to write that distinction yourself.

See [`quotient`](./quotient.md) for integer division and [`mod`](./mod.md) for the remainder.
