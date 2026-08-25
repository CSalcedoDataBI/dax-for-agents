---
function: POWER
model: ninguno
---

# POWER — examples

## 1. `POWER(0, 0)` aborts the query

Many languages return 1 by convention. DAX does not: it treats it as undefined and kills the
query.

```dax
EVALUATE ROW("cero_a_la_cero", POWER(0, 0))
```

```result
ERROR: An argument of function 'POWER' has the wrong data type or the result is too large or too small.
```

The neighbours do work, which makes the hole easier to step in:

```dax
EVALUATE
ROW(
  "cero_a_la_dos", POWER(0, 2),
  "dos_a_la_cero", POWER(2, 0),
  "cero_a_la_menos_uno", IFERROR(POWER(0, -1), "aborta"),
  "base_blanca", POWER(BLANK(), 2)
)
```

```result
cero_a_la_dos | dos_a_la_cero | cero_a_la_menos_uno | base_blanca
0 | 1 | aborta | (blank)
```

If the exponent comes from data and can be zero at the same time as the base, it has to be
guarded.

## 2. A negative base works, even with a fractional exponent

Excel refuses `(-8)^(1/3)`. DAX computes it — and the result shows in passing that this is
floating point.

```dax
EVALUATE
ROW(
  "menos_dos_al_cubo", POWER(-2, 3),
  "menos_dos_al_cuadrado", POWER(-2, 2),
  "raiz_cubica_negativa", POWER(-8, 1/3),
  "es_exactamente_menos_dos", POWER(-8, 1/3) = -2,
  "lo_que_sobra_x1e16", ROUND((POWER(-8, 1/3) + 2) * POWER(10, 16), 6)
)
```

```result
menos_dos_al_cubo | menos_dos_al_cuadrado | raiz_cubica_negativa | es_exactamente_menos_dos | lo_que_sobra_x1e16
-8 | 4 | -2 | False | 2.220446
```

The third column **prints** as -2 and the fourth says it is not. The fifth is multiplied by 10¹⁶
precisely because, unscaled, the remainder also prints as 0: there is 2.220446 × 10⁻¹⁶ left over.
The output format rounds and the comparison does not. `POWER` returns a `double`, so comparing it
against an expected integer fails silently — round first, or compare with a tolerance.

## 3. Negative and fractional exponents, which is where it stops being "multiply several times"

```dax
EVALUATE
ROW(
  "inverso", POWER(2, -2),
  "raiz_cuadrada", ROUND(POWER(9, 0.5), 6),
  "raiz_cubica", ROUND(POWER(27, 1/3), 6),
  "interes_compuesto", ROUND(POWER(1.05, 10), 6)
)
```

```result
inverso | raiz_cuadrada | raiz_cubica | interes_compuesto
0.25 | 3 | 3 | 1.628895
```

The last one is the real use in a report: 5% over ten periods is 62.9% compounded, not 50%.

See [`sqrt`](./sqrt.md), [`exp`](./exp.md) and [`log`](./log.md), its inverse.
