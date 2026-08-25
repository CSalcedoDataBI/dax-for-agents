---
function: TAN
model: ninguno
---

# TAN — examples

## 1. Radians again, and here the error is larger

`TAN(45)` gives 1.62 instead of 1. It is not a small drift: the tangent grows fast, so confusing
degrees with radians can give a number of a different order of magnitude.

```dax
EVALUATE
ROW(
  "tan_45_grados",   ROUND(TAN(45), 6),
  "tan_45_radianes", ROUND(TAN(RADIANS(45)), 6),
  "tan_0",           TAN(0),
  "tan_30_bien",     ROUND(TAN(RADIANS(30)), 6)
)
```

```result
tan_45_grados | tan_45_radianes | tan_0 | tan_30_bien
1.619775 | 1 | 0 | 0.57735
```

## 2. At π/2 it gives neither infinity nor an error: it gives a huge number

Mathematically the tangent does not exist there. Numerically, `PI()/2` is an approximation, so
the engine returns a gigantic number and carries on as if nothing happened. A division by that
value gives almost zero and nobody notices.

```dax
EVALUATE
ROW(
  "cerca_del_polo", ROUND(TAN(PI() / 2), 0),
  "es_muy_grande",  TAN(PI() / 2) > 1000000000,
  "hay_error",      ISERROR(TAN(PI() / 2)),
  "justo_despues",  ROUND(TAN(PI() / 2 + 0.1), 6)
)
```

```result
cerca_del_polo | es_muy_grande | hay_error | justo_despues
16324552277619100 | True | False | -9.966644
```

If the angle comes out of a calculation and can approach 90°, it has to be clamped by hand: there
is no error to warn you.

## 3. It is odd, and periodic with period π

```dax
EVALUATE
ROW(
  "tan_1",       ROUND(TAN(1), 6),
  "tan_menos_1", ROUND(TAN(-1), 6),
  "impar",       ROUND(TAN(1) + TAN(-1), 10),
  "periodo",     ROUND(TAN(1) - TAN(1 + PI()), 6)
)
```

```result
tan_1 | tan_menos_1 | impar | periodo
1.557408 | -1.557408 | 0 | 0
```

The period is **π**, not 2π as in [`sin`](./sin.md) and [`cos`](./cos.md).

See [`atan`](./atan.md), its inverse, which has no domain.
