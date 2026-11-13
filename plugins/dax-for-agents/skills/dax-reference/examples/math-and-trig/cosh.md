---
function: COSH
model: ninguno
---

# COSH — examples

## 1. It never drops below 1

Unlike [`cos`](./cos.md), which runs from -1 to 1. `COSH` has its minimum at `COSH(0) = 1` and
grows from there in both directions. A negative `COSH` is impossible, so if your calculation
produces one, the function is not the one you think.

```dax
EVALUATE
ROW(
  "cosh_0",  COSH(0),
  "cosh_1",  ROUND(COSH(1), 6),
  "cosh_m1", ROUND(COSH(-1), 6),
  "minimo",  COSH(0.5) >= 1
)
```

```result
cosh_0 | cosh_1 | cosh_m1 | minimo
1 | 1.543081 | 1.543081 | True
```

## 2. It is even: the sign is lost

`COSH(x) = COSH(-x)`. It is the structural difference from [`sinh`](./sinh.md), which is odd, and
the reason `COSH` cannot be inverted over the whole axis — see [`acosh`](./acosh.md), whose
domain starts at 1 for exactly this reason.

```dax
EVALUATE
ROW(
  "cosh_2",     ROUND(COSH(2), 6),
  "cosh_m2",    ROUND(COSH(-2), 6),
  "coinciden",  COSH(2) = COSH(-2),
  "sinh_no",    SINH(2) = SINH(-2)
)
```

```result
cosh_2 | cosh_m2 | coinciden | sinh_no
3.762196 | 3.762196 | True | False
```

## 3. The same ceiling as SINH, for the same reason

```dax
EVALUATE ROW("desbordado", COSH(710))
```

```result
ERROR: An argument of function 'COSH' has the wrong data type or the result is too large or too small.
```

And the definition, verified:

```dax
EVALUATE
ROW(
  "definicion",  ROUND(COSH(3) - (EXP(3) + EXP(-3)) / 2, 10),
  "blanco",      COSH(BLANK()),
  "suma_con_sinh", ROUND(COSH(2) + SINH(2) - EXP(2), 10)
)
```

```result
definicion | blanco | suma_con_sinh
0 | 1 | 0
```

`COSH(x) + SINH(x) = eˣ` — the one-line check that the two are the even and odd halves of the
exponential.

And `COSH(BLANK())` is **1**, not blank: the blank goes in as zero and `COSH(0)` is 1. Be careful
about generalising that, because [`sinh`](./sinh.md) and [`tanh`](./tanh.md) **do** return blank
on the same input — not because the blank goes in differently, but because their result at zero
is zero, and a zero that comes out of a blank comes back out as blank.
