---
function: TANH
model: ninguno
---

# TANH — examples

## 1. It saturates between -1 and 1, and that is why it does not overflow

It is the only one of the three basic hyperbolics that has **no** overflow ceiling:
[`sinh`](./sinh.md) and [`cosh`](./cosh.md) die near 710, and `TANH` simply flattens out.

```dax
EVALUATE
ROW(
  "tanh_0",   TANH(0),
  "tanh_1",   ROUND(TANH(1), 6),
  "tanh_100", TANH(100),
  "tanh_1000", TANH(1000)
)
```

```result
tanh_0 | tanh_1 | tanh_100 | tanh_1000
0 | 0.761594 | 1 | 1
```

Past a moderate value it returns **exactly 1**. The saturation is not approximate: the result
stops telling different inputs apart, and that matters if you are using it to normalise.

## 2. That saturation erases information

Two widely separated values give the same result. As a normaliser it is convenient until the
large inputs stop ordering among themselves.

```dax
EVALUATE
ROW(
  "tanh_20",    TANH(20),
  "tanh_50",    TANH(50),
  "son_iguales", TANH(20) = TANH(50),
  "tanh_3",     ROUND(TANH(3), 6)
)
```

```result
tanh_20 | tanh_50 | son_iguales | tanh_3
1 | 1 | True | 0.995055
```

If you need the extremes to stay distinguishable, the scaling has to come first: `TANH(x/k)` with
a large `k`.

## 3. It is odd, and it is the ratio of the other two

```dax
EVALUATE
ROW(
  "impar",      ROUND(TANH(2) + TANH(-2), 10),
  "cociente",   ROUND(TANH(2) - DIVIDE(SINH(2), COSH(2)), 10),
  "blanco",     TANH(BLANK()),
  "en_rango",   ABS(TANH(-1000)) <= 1
)
```

```result
impar | cociente | blanco | en_rango
0 | 0 | (blank) | True
```

`TANH(BLANK())` comes out **blank**, just like [`sinh`](./sinh.md) and for the same reason: the
blank goes in as zero, `TANH(0)` is zero, and that zero comes back out as blank. `TANH(0)` written
by hand returns an ordinary **0**.

See [`sinh`](./sinh.md) and [`cosh`](./cosh.md), whose ratio it is.
