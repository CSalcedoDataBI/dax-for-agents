---
function: SQRTPI
model: ninguno
---

# SQRTPI — examples

## 1. It is `SQRT(n × π)`, not `SQRT(n) × π` nor `SQRT(π)`

The name allows three readings and only one is right. The multiplication goes **inside** the
root.

```dax
EVALUATE
ROW(
  "sqrtpi_4", ROUND(SQRTPI(4), 6),
  "raiz_de_4_por_pi", ROUND(SQRT(4 * PI()), 6),
  "raiz_de_4_por_pi_fuera", ROUND(SQRT(4) * PI(), 6),
  "sqrtpi_1", ROUND(SQRTPI(1), 6)
)
```

```result
sqrtpi_4 | raiz_de_4_por_pi | raiz_de_4_por_pi_fuera | sqrtpi_1
3.544908 | 3.544908 | 6.283185 | 1.772454
```

Columns 1 and 2 agree; column 3 is almost double. And `SQRTPI(1)` is `SQRT(π)` = 1.772454, which
is where the confusion over the name comes from.

## 2. It inherits `SQRT`'s domain: a negative aborts

```dax
EVALUATE ROW("negativo", SQRTPI(-1))
```

```result
ERROR: An argument of function 'SQRTPI' has the wrong data type or the result is too large or too small.
```

And zero and the blank behave as in [`sqrt`](./sqrt.md):

```dax
EVALUATE
ROW(
  "cero", SQRTPI(0),
  "blanco", SQRTPI(BLANK()),
  "es_blanco", ISBLANK(SQRTPI(BLANK()))
)
```

```result
cero | blanco | es_blanco
0 | (blank) | True
```

The blank goes in as zero, `SQRTPI(0)` is zero, and that zero comes back out blank.

## 3. What it exists for: the normal distribution's constant

Practically its only use is the normal density formula, where `√(2π)` appears as a denominator.
Writing it as `SQRTPI(2)` saves one bracket and little else.

```dax
EVALUATE
ROW(
  "raiz_2pi", ROUND(SQRTPI(2), 6),
  "escrita_larga", ROUND(SQRT(2 * PI()), 6),
  "densidad_en_cero", ROUND(1 / SQRTPI(2), 6)
)
```

```result
raiz_2pi | escrita_larga | densidad_en_cero
2.506628 | 2.506628 | 0.398942
```

0.398942 is the height of the bell at its centre. If you are not writing statistics by hand,
`SQRT(n * PI())` reads better and does the same.

See [`sqrt`](./sqrt.md) and [`pi`](./pi.md).
