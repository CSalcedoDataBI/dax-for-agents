---
function: COS
model: ninguno
---

# COS — examples

## 1. Radians, like the whole family

`COS(60)` is not 0.5. The cosine of 60 **degrees** is, and to say so you need
[`radians`](./radians.md).

```dax
EVALUATE
ROW(
  "cos_60_grados",   ROUND(COS(60), 6),
  "cos_60_radianes", ROUND(COS(RADIANS(60)), 6),
  "cos_0",           COS(0),
  "cos_pi",          COS(PI())
)
```

```result
cos_60_grados | cos_60_radianes | cos_0 | cos_pi
-0.952413 | 0.5 | 1 | -1
```

## 2. It is even: the argument's sign does not matter

The opposite of [`sin`](./sin.md), which is odd. Useful for checking at a glance that you are
using the function you think you are.

```dax
EVALUATE
ROW(
  "cos_1",       ROUND(COS(1), 6),
  "cos_menos_1", ROUND(COS(-1), 6),
  "coinciden",   COS(1) = COS(-1),
  "sin_no",      SIN(1) = SIN(-1)
)
```

```result
cos_1 | cos_menos_1 | coinciden | sin_no
0.540302 | 0.540302 | True | False
```

## 3. No domain, and always between -1 and 1

```dax
EVALUATE
ROW(
  "muy_grande", ROUND(COS(1000), 6),
  "en_rango",   ABS(COS(1000)) <= 1,
  "identidad",  ROUND(COS(2) * COS(2) + SIN(2) * SIN(2), 10),
  "blanco",     ISBLANK(COS(BLANK()))
)
```

```result
muy_grande | en_rango | identidad | blanco
0.562379 | True | 1 | False
```

`COS(BLANK())` is **not** blank: the blank converts to 0 and the cosine of 0 is 1. It is the
exception to the rule that blanks propagate, and it is worth seeing before trusting it.

See [`acos`](./acos.md), which does have a domain.
