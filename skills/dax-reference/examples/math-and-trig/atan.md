---
function: ATAN
model: ninguno
---

# ATAN — examples

## 1. It has no domain: it accepts any number without aborting

It is the exception of the inverse family. [`asin`](./asin.md) and [`acos`](./acos.md) die
outside [-1, 1]; `ATAN` never dies. That is why it is the one used when the argument comes out of
a division that can run away.

```dax
EVALUATE
ROW(
  "atan_1",     ROUND(ATAN(1), 6),
  "atan_1000",  ROUND(ATAN(1000), 6),
  "atan_m1000", ROUND(ATAN(-1000), 6),
  "pi_medios",  ROUND(PI() / 2, 6)
)
```

```result
atan_1 | atan_1000 | atan_m1000 | pi_medios
0.785398 | 1.569796 | -1.569796 | 1.570796
```

It approaches ±π/2 without reaching it: the open range is **(-π/2, π/2)**.

## 2. That range is half a turn, not a whole one

Practical consequence: `ATAN(y/x)` does **not** tell a third-quadrant angle from a first-quadrant
one, because `y/x` is the same number in both. It is why other languages have `atan2`, which DAX
does not.

```dax
EVALUATE
ROW(
  "primer_cuadrante",  ROUND(DEGREES(ATAN(DIVIDE(1, 1))), 6),
  "tercer_cuadrante",  ROUND(DEGREES(ATAN(DIVIDE(-1, -1))), 6),
  "son_iguales",       ATAN(DIVIDE(1, 1)) = ATAN(DIVIDE(-1, -1)),
  "division_igual",    DIVIDE(1, 1) = DIVIDE(-1, -1)
)
```

```result
primer_cuadrante | tercer_cuadrante | son_iguales | division_igual
45 | 45 | True | True
```

The quadrant has to be reconstructed by hand from the sign of each component.

## 3. It is odd, and it returns radians

```dax
EVALUATE
ROW(
  "atan_2",     ROUND(ATAN(2), 6),
  "atan_m2",    ROUND(ATAN(-2), 6),
  "impar",      ROUND(ATAN(2) + ATAN(-2), 10),
  "en_grados",  ROUND(DEGREES(ATAN(1)), 6)
)
```

```result
atan_2 | atan_m2 | impar | en_grados
1.107149 | -1.107149 | 0 | 45
```

`ATAN(1)` in degrees is 45. See [`acot`](./acot.md), its complement, which has a different range.
