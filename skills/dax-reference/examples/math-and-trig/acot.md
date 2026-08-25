---
function: ACOT
model: ninguno
---

# ACOT — examples

## 1. It returns between 0 and π, so it is NOT symmetric like `ATAN`

This is the trap, and it is easy to step in because `ATAN` is odd. `ACOT(-1)` is **not**
`-ACOT(1)`.

```dax
EVALUATE
ROW(
  "acot_1", ROUND(ACOT(1), 6),
  "acot_menos_1", ROUND(ACOT(-1), 6),
  "suma", ROUND(ACOT(1) + ACOT(-1), 6),
  "atan_menos_1", ROUND(ATAN(-1), 6)
)
```

```result
acot_1 | acot_menos_1 | suma | atan_menos_1
0.785398 | 2.356194 | 3.141593 | -0.785398
```

`ACOT(-1)` is 3π/4 and not -π/4. The sum gives π, which is the real property:
`ACOT(-x) = π - ACOT(x)`. If you convert to degrees expecting -45 you get 135, and the angle's
sign changes the quadrant.

## 2. At zero it is π/2 — it does not abort and it is not blank

It is the only one in the family that handles zero well, and that is why it handles the blank
well too.

```dax
EVALUATE
ROW(
  "acot_0", ROUND(ACOT(0), 6),
  "medio_pi", ROUND(PI() / 2, 6),
  "acot_blanco", ROUND(ACOT(BLANK()), 6),
  "cot_0_aborta", IFERROR(COT(0), "aborta")
)
```

```result
acot_0 | medio_pi | acot_blanco | cot_0_aborta
1.570796 | 1.570796 | 1.570796 | aborta
```

`ACOT(BLANK())` returns **π/2**, not blank: the blank goes in as zero and `ACOT(0)` is not zero,
so there is nothing to collapse. In a calculated column, the gaps get filled with 1.5708 in
silence. Meanwhile [`cot`](./cot.md) aborts on the same blank.

## 3. It complements `ATAN`: the two add up to π/2

```dax
EVALUATE
ROW(
  "acot_2", ROUND(ACOT(2), 6),
  "atan_2", ROUND(ATAN(2), 6),
  "suma", ROUND(ACOT(2) + ATAN(2), 6),
  "medio_pi", ROUND(PI() / 2, 6)
)
```

```result
acot_2 | atan_2 | suma | medio_pi
0.463648 | 1.107149 | 1.570796 | 1.570796
```

`ACOT(x) = π/2 - ATAN(x)` for any x. It is how to write it if you prefer to keep a single inverse
function, and it also makes the range you are using explicit.

See [`cot`](./cot.md), [`acoth`](./acoth.md) and [`degrees`](./degrees.md).
