---
function: ASINH
model: ninguno
---

# ASINH — examples

## 1. It accepts any number, which makes it the family's exception

No domain and no holes. It is the only one of the inverse hyperbolics that never aborts.

```dax
EVALUATE
ROW(
  "cero", ASINH(0),
  "negativo", ROUND(ASINH(-1), 6),
  "positivo", ROUND(ASINH(1), 6),
  "enorme", ROUND(ASINH(1000000), 6)
)
```

```result
cero | negativo | positivo | enorme
0 | -0.881374 | 0.881374 | 14.508658
```

Compare with [`acosh`](./acosh.md), which demands 1 or more, and with [`atanh`](./atanh.md),
which demands being inside (-1, 1). `ASINH` swallows everything.

## 2. The blank comes out blank, and that also separates it from its neighbours

```dax
EVALUATE
ROW(
  "blanco", ASINH(BLANK()),
  "es_blanco", ISBLANK(ASINH(BLANK())),
  "cero", ASINH(0),
  "acosh_blanco", IFERROR(ACOSH(BLANK()), "aborta")
)
```

```result
blanco | es_blanco | cero | acosh_blanco
(blank) | True | 0 | aborta
```

The blank goes in as zero, `ASINH(0)` is zero, and that zero comes back out blank. In the same
family, `ACOSH` with a blank **kills the query**. Choosing wrong between the two turns a gap from
"it is ignored" into "there is no report".

## 3. It is odd, it is the exact inverse of `SINH`, and it is a logarithm

```dax
EVALUATE
ROW(
  "impar", ROUND(ASINH(2) + ASINH(-2), 10),
  "ida_y_vuelta", ROUND(ASINH(SINH(3)), 10),
  "formula_cerrada", ROUND(ASINH(2) - LN(2 + SQRT(5)), 10),
  "asinh_2", ROUND(ASINH(2), 6)
)
```

```result
impar | ida_y_vuelta | formula_cerrada | asinh_2
0 | 3 | 0 | 1.443635
```

`ASINH(x) = LN(x + √(x² + 1))`. The `+1` instead of [`acosh`](./acosh.md)'s `-1` is exactly what
removes the domain: the root never runs out of argument.

See [`sinh`](./sinh.md), [`acosh`](./acosh.md) and [`atanh`](./atanh.md).
