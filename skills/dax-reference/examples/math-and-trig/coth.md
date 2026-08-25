---
function: COTH
model: ninguno
---

# COTH — examples

## 1. It is 1/TANH, and it flattens at ±1 straight away

Nothing like the circular cotangent of [`cot`](./cot.md): this one does not oscillate. It tends
to 1 from above and to -1 from below, and it gets there fast.

```dax
EVALUATE
ROW(
  "coth_1", ROUND(COTH(1), 6),
  "uno_entre_tanh", ROUND(1 / TANH(1), 6),
  "coth_3", ROUND(COTH(3), 6),
  "coth_20", ROUND(COTH(20), 10)
)
```

```result
coth_1 | uno_entre_tanh | coth_3 | coth_20
1.313035 | 1.313035 | 1.00497 | 1
```

At 3 it is already within five thousandths of 1, and at 20 it is indistinguishable from 1 at the
precision this report prints. For large values, `COTH(x)` is 1 for practical purposes.

## 2. There is only one forbidden point, and it is zero

```dax
EVALUATE ROW("coth_de_cero", COTH(0))
```

```result
ERROR: Division by zero has occurred when evaluating function 'COTH'.
```

Unlike [`cot`](./cot.md), which aborts at every multiple of π, here the only hole is zero —
because `TANH` is zero only there. And the blank falls into the hole:

```dax
EVALUATE
ROW(
  "blanco", IFERROR(COTH(BLANK()), "aborta"),
  "cero", IFERROR(COTH(0), "aborta"),
  "casi_cero", ROUND(COTH(0.001), 4),
  "casi_cero_neg", ROUND(COTH(-0.001), 4)
)
```

```result
blanco | cero | casi_cero | casi_cero_neg
aborta | aborta | 1000.0003 | -1000.0003
```

The jump at zero runs from -1000 to +1000. Any gap in the data brings the query down, and that is
the case that actually arrives.

## 3. It is odd, and it never sits between -1 and 1

```dax
EVALUATE
ROW(
  "impar", ROUND(COTH(2) + COTH(-2), 10),
  "coth_2", ROUND(COTH(2), 6),
  "fuera_del_intervalo", ABS(COTH(0.5)) > 1,
  "tanh_dentro", ABS(TANH(0.5)) < 1
)
```

```result
impar | coth_2 | fuera_del_intervalo | tanh_dentro
0 | 1.037315 | True | True
```

`TANH` lives inside (-1, 1) and `COTH`, its reciprocal, lives outside. The last two columns are
the same claim seen from both sides.

See [`cot`](./cot.md), [`acoth`](./acoth.md) and [`tanh`](./tanh.md).
