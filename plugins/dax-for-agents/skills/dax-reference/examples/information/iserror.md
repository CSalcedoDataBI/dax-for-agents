---
function: ISERROR
model: ninguno
---

# ISERROR — examples

## 1. A blank is not an error, and `DIVIDE` by zero is not one either

It is the distinction that separates the two families of "something went wrong" in DAX.

```dax
EVALUATE
ROW(
  "division_con_operador", ISERROR(1 / 0),
  "division_con_funcion", ISERROR(DIVIDE(1, 0)),
  "blanco", ISERROR(BLANK()),
  "normal", ISERROR(1 / 2)
)
```

```result
division_con_operador | division_con_funcion | blanco | normal
True | False | False | False
```

`1 / 0` is an error; `DIVIDE(1, 0)` is a **blank**, which is not. That is the entire reason
[`divide`](../math-and-trig/divide.md) exists.

## 2. It does catch what aborts the query — unlike `IFERROR` around an iterator

```dax
EVALUATE
ROW(
  "log_de_cero", ISERROR(LN(0)),
  "raiz_negativa", ISERROR(SQRT(-1)),
  "cero_a_la_cero", ISERROR(POWER(0, 0)),
  "texto_mas_numero", ISERROR(1 + "hola")
)
```

```result
log_de_cero | raiz_negativa | cero_a_la_cero | texto_mas_numero
True | True | True | True
```

All four would kill the query written on their own. `ISERROR` evaluates them and returns true
without the query falling over — mind you, that holds for the **expression** it wraps, not for a
whole `SUMX`, as measured in [`ln`](../math-and-trig/ln.md).

## 3. It is for classifying, not for replacing

If all you want is an alternative value, `IFERROR` says so in one line. `ISERROR` wins when you
need to **count** or **label** the errors rather than cover them up.

```dax
EVALUATE
VAR Entradas = { 4, 0, -1 }
RETURN
ROW(
  "cuantas_fallan", COUNTROWS(FILTER(Entradas, ISERROR(SQRT([Value])))),
  "cuantas_valen", COUNTROWS(FILTER(Entradas, NOT ISERROR(SQRT([Value])))),
  "suma_de_las_buenas", SUMX(FILTER(Entradas, NOT ISERROR(SQRT([Value]))), SQRT([Value]))
)
```

```result
cuantas_fallan | cuantas_valen | suma_de_las_buenas
1 | 2 | 2
```

One of the three inputs is impossible. `IFERROR` would have turned it into zero and the report
would say there are three correct measurements; this way it says there are two and one broken.

See [`isblank`](./isblank.md) and [`divide`](../math-and-trig/divide.md).
