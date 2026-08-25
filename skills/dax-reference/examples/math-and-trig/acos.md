---
function: ACOS
model: ninguno
---

# ACOS — examples

## 1. Same domain as ASIN, [-1, 1], and it aborts outside it too

```dax
EVALUATE ROW("fuera_de_rango", ACOS(2))
```

```result
ERROR: An argument of function 'ACOS' has the wrong data type or the result is too large or too small.
```

It is the error that shows up when computing angles from a dot product: the division gives
`1.0000000002` from floating-point accumulation and the query dies. The defence is to clamp the
argument with `MIN(1, MAX(-1, x))` before calling it.

```dax
EVALUATE
ROW(
  "acos_1",   ACOS(1),
  "acos_0",   ROUND(ACOS(0), 6),
  "acos_m1",  ROUND(ACOS(-1), 6),
  "pi",       ROUND(PI(), 6)
)
```

```result
acos_1 | acos_0 | acos_m1 | pi
0 | 1.570796 | 3.141593 | 3.141593
```

## 2. Its output range is [0, π] — different from ASIN's

That is the practical difference between the two: `ASIN` returns signed angles, `ACOS` never
returns a negative. For an angle between vectors that is what you want.

```dax
EVALUATE
ROW(
  "acos_de_neg", ROUND(ACOS(-0.5), 6),
  "asin_de_neg", ROUND(ASIN(-0.5), 6),
  "acos_positivo_siempre", ACOS(-0.5) > 0,
  "suma_constante", ROUND(ACOS(0.3) + ASIN(0.3), 6)
)
```

```result
acos_de_neg | asin_de_neg | acos_positivo_siempre | suma_constante
2.094395 | -0.523599 | True | 1.570796
```

`ACOS(x) + ASIN(x)` is always π/2. It is the quick check that neither of the two is being
misused.

## 3. In radians, like everything here

```dax
EVALUATE
ROW(
  "radianes", ROUND(ACOS(0.5), 6),
  "grados",   ROUND(DEGREES(ACOS(0.5)), 6),
  "vuelta",   ROUND(COS(ACOS(0.5)), 6),
  "blanco",   ROUND(ACOS(BLANK()), 6)
)
```

```result
radianes | grados | vuelta | blanco
1.047198 | 60 | 0.5 | 1.570796
```

`ACOS(BLANK())` is not blank: the blank goes in as 0 and the result is π/2.
