---
function: SINH
model: ninguno
---

# SINH — examples

## 1. It is not circular trigonometry: no radians and no period

It is the trap of reading it by its name. `SINH` does not oscillate between -1 and 1: it **grows
without a ceiling**, exponentially. Passing it degrees converted with `RADIANS` makes no sense
here.

```dax
EVALUATE
ROW(
  "sinh_0",   SINH(0),
  "sinh_1",   ROUND(SINH(1), 6),
  "sinh_5",   ROUND(SINH(5), 6),
  "sinh_10",  ROUND(SINH(10), 6)
)
```

```result
sinh_0 | sinh_1 | sinh_5 | sinh_10
0 | 1.175201 | 74.203211 | 11013.232875
```

From 1 to 10 the value multiplies by nearly ten thousand. Comparing that with [`sin`](./sin.md),
which never leaves [-1, 1], makes the difference plain.

## 2. That growth has a ceiling, and past it the function aborts

Around 710 the result stops fitting in a floating-point number and the query dies. It is the same
wall as [`exp`](./exp.md), because `SINH` is made of exponentials.

```dax
EVALUATE ROW("desbordado", SINH(710))
```

```result
ERROR: An argument of function 'SINH' has the wrong data type or the result is too large or too small.
```

Just below it still works:

```dax
EVALUATE
ROW(
  "sinh_700", SINH(700) > 0,
  "es_enorme", SINH(700) > POWER(10, 300),
  "exp_equivale", ROUND(SINH(3) - (EXP(3) - EXP(-3)) / 2, 10)
)
```

```result
sinh_700 | es_enorme | exp_equivale
True | True | 0
```

The last column is the definition: `SINH(x) = (eˣ - e⁻ˣ) / 2`.

## 3. It is odd, and it has no lower domain

```dax
EVALUATE
ROW(
  "sinh_m1",  ROUND(SINH(-1), 6),
  "impar",    ROUND(SINH(2) + SINH(-2), 10),
  "blanco",   SINH(BLANK()),
  "identidad", ROUND(COSH(1) * COSH(1) - SINH(1) * SINH(1), 10)
)
```

```result
sinh_m1 | impar | blanco | identidad
-1.175201 | 0 | (blank) | 1
```

`COSH² - SINH² = 1` is the fundamental hyperbolic identity, the equivalent of `sin² + cos² = 1`.

The `blanco` column deserves a second look: `SINH(BLANK())` comes out **blank**, and yet
`SINH(BLANK()) = 0` returns **true**. They are not two facts in conflict — the blank goes in as
zero, `SINH(0)` is zero, and a zero that came from a blank comes back out as blank. `SINH(0)`
written by hand, on the other hand, returns a **0** that is not blank. Compare with
[`cosh`](./cosh.md), where `COSH(BLANK())` is **1** for this very reason: its result at zero is
not zero, so there is nothing to collapse.

See [`cosh`](./cosh.md), [`tanh`](./tanh.md) and [`asinh`](./asinh.md), its inverse.
