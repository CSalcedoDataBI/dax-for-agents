---
function: RANDBETWEEN
model: ninguno
---

# RANDBETWEEN — examples

> As with [`rand`](./rand.md), the `result` blocks assert **properties** and not specific values.

## 1. Both endpoints are included, and the result is always an integer

```dax
EVALUATE
VAR Tirada = RANDBETWEEN(1, 6)
RETURN
ROW(
  "dentro_del_rango", Tirada >= 1 && Tirada <= 6,
  "es_entero", Tirada = INT(Tirada),
  "sin_variable_no", RANDBETWEEN(1, 6) = INT(RANDBETWEEN(1, 6)),
  "extremos_iguales", RANDBETWEEN(5, 5),
  "negativos_valen", RANDBETWEEN(-3, -3)
)
```

```result
dentro_del_rango | es_entero | sin_variable_no | extremos_iguales | negativos_valen
True | True | False | 5 | -3
```

Unlike [`rand`](./rand.md), which excludes 1, here the interval is **closed on both sides**. With
equal endpoints the result is constant, which is how to check it without depending on chance.

The third column is [`rand`](./rand.md)'s trap again, and it comes out **false**: it is not
comparing one draw with itself, it is comparing **two different draws**. With the `VAR` the second
column does say what it means to. Writing that line without a variable and reading the `False` as
"it does not return integers" is the wrong conclusion from the wrong experiment.

## 2. With the endpoints the wrong way round it aborts the query

```dax
EVALUATE ROW("del_seis_al_uno", RANDBETWEEN(6, 1))
```

```result
ERROR: An argument of function 'RANDBETWEEN' has the wrong data type or the result is too large or too small.
```

If the bounds come from measures, the order is not guaranteed.
`RANDBETWEEN(MIN(a, b), MAX(a, b))` is the form that does not fall over.

## 3. It raises the minimum and lowers the maximum — so a decimal interval can end up empty

This is the part the signature does not tell you. With decimals, the lower bound rounds **up** and
the upper one rounds **down**, so the interval shrinks to the integers falling strictly inside. If
none is left, the query dies.

```dax
EVALUATE
ROW(
  "de_1_2_a_2_9", RANDBETWEEN(1.2, 2.9) = 2,
  "de_1_5_a_2_5", RANDBETWEEN(1.5, 2.5) = 2,
  "de_2_2_a_2_8", IFERROR(RANDBETWEEN(2.2, 2.8), "aborta"),
  "de_1_2_a_1_2", IFERROR(RANDBETWEEN(1.2, 1.2), "aborta"),
  "blancos", RANDBETWEEN(BLANK(), BLANK())
)
```

```result
de_1_2_a_2_9 | de_1_5_a_2_5 | de_2_2_a_2_8 | de_1_2_a_1_2 | blancos
True | True | aborta | aborta | 0
```

`RANDBETWEEN(1.2, 2.9)` always returns **2**: it is the only integer inside. And `(2.2, 2.8)`
becomes `[3, 2]`, which is inverted, so it aborts — the same error as point 2, with bounds that
looked perfectly well ordered.

See [`rand`](./rand.md) and [`int`](./int.md).
