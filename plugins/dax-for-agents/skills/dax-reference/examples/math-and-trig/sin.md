---
function: SIN
model: ninguno
---

# SIN — examples

## 1. The argument is in RADIANS, and with degrees it does not fail: it lies

It is the number-one trap of the whole family. `SIN(90)` does not give 1 — it gives the sine of
90 radians, which is a perfectly believable and completely wrong number. No error gives it away.

```dax
EVALUATE
ROW(
  "sin_90_grados",   ROUND(SIN(90), 6),
  "sin_90_radianes", ROUND(SIN(RADIANS(90)), 6),
  "sin_0",           SIN(0),
  "sin_30_bien",     ROUND(SIN(RADIANS(30)), 6)
)
```

```result
sin_90_grados | sin_90_radianes | sin_0 | sin_30_bien
0.893997 | 1 | 0 | 0.5
```

If the data arrives in degrees — and it almost always arrives in degrees — it has to go through
[`radians`](./radians.md) **every time**.

## 2. It has no domain: it accepts any number

Unlike its inverse [`asin`](./asin.md), which only takes [-1, 1]. Here the result always falls
inside that interval.

```dax
EVALUATE
ROW(
  "muy_grande",  ROUND(SIN(1000), 6),
  "negativo",    ROUND(SIN(-1), 6),
  "impar",       ROUND(SIN(-1) + SIN(1), 6),
  "en_rango",    ABS(SIN(1000)) <= 1
)
```

```result
muy_grande | negativo | impar | en_rango
0.82688 | -0.841471 | 0 | True
```

`SIN(-x) = -SIN(x)`: the sum gives exact zero, which is the check that it is odd.

## 3. SIN(PI()) DISPLAYS as zero and is not equal to zero

Both at once, and that contradiction is the example. `PI()` is an approximation, so the sine comes
out around 10⁻¹⁶: any format shows it as `0`, and the `= 0` comparison returns **false**. An
`IF(SIN(x) = 0, …)` that looks correct in the visual never takes that branch.

```dax
EVALUATE
ROW(
  "sin_pi",        SIN(PI()),
  "es_cero",       SIN(PI()) = 0,
  "sin_pi_medios", SIN(PI() / 2),
  "identidad",     ROUND(SIN(1) * SIN(1) + COS(1) * COS(1), 10)
)
```

```result
sin_pi | es_cero | sin_pi_medios | identidad
0 | False | 1 | 1
```

With floating-point values you have to compare against a tolerance — `ABS(x) < 1e-9` — or round
first. See [`cos`](./cos.md), [`tan`](./tan.md) and [`asin`](./asin.md).
