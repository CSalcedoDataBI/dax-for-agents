---
function: ASIN
model: ninguno
---

# ASIN — examples

## 1. Its domain is [-1, 1], and outside it ABORTS

It does not return blank: it brings the query down. And the value passed to it usually comes out
of a division, so the `1.0000001` of a rounding is enough to break it.

```dax
EVALUATE ROW("fuera_de_rango", ASIN(2))
```

```result
ERROR: An argument of function 'ASIN' has the wrong data type or the result is too large or too small.
```

Inside the domain:

```dax
EVALUATE
ROW(
  "asin_1",  ROUND(ASIN(1), 6),
  "asin_0",  ASIN(0),
  "asin_m1", ROUND(ASIN(-1), 6),
  "pi_medios", ROUND(PI() / 2, 6)
)
```

```result
asin_1 | asin_0 | asin_m1 | pi_medios
1.570796 | 0 | -1.570796 | 1.570796
```

`ASIN(1)` is exactly π/2. The output range is **[-π/2, π/2]**.

## 2. It returns RADIANS, not degrees

Symmetric to [`sin`](./sin.md)'s problem: if the result goes into a report where degrees are
read, it has to be converted with [`degrees`](./degrees.md).

```dax
EVALUATE
ROW(
  "en_radianes", ROUND(ASIN(0.5), 6),
  "en_grados",   ROUND(DEGREES(ASIN(0.5)), 6),
  "vuelta",      ROUND(SIN(ASIN(0.5)), 6),
  "medio",       ROUND(ASIN(SIN(RADIANS(30))), 6)
)
```

```result
en_radianes | en_grados | vuelta | medio
0.523599 | 30 | 0.5 | 0.523599
```

## 3. The round trip only works inside the range

`ASIN(SIN(x))` returns `x` only if `x` is in [-π/2, π/2]. Outside, it returns the equivalent
angle inside the range, without warning that it is not the one that went in.

```dax
EVALUATE
ROW(
  "dentro",  ROUND(ASIN(SIN(1)), 6),
  "fuera",   ROUND(ASIN(SIN(3)), 6),
  "original", 3,
  "coinciden", ROUND(ASIN(SIN(3)), 6) = 3
)
```

```result
dentro | fuera | original | coinciden
1 | 0.141593 | 3 | False
```

See [`acos`](./acos.md), which has the same domain and a different output range.
