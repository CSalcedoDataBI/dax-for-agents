---
function: ATANH
model: ninguno
---

# ATANH — examples

## 1. Only between -1 and 1, and the endpoints do NOT count

`TANH` lives inside (-1, 1) without ever reaching the edges, so its inverse blows up there.

```dax
EVALUATE ROW("en_el_borde", ATANH(1))
```

```result
ERROR: An argument of function 'ATANH' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE
ROW(
  "medio", ROUND(ATANH(0.5), 6),
  "casi_uno", ROUND(ATANH(0.999), 6),
  "uno", IFERROR(ATANH(1), "aborta"),
  "mas_de_uno", IFERROR(ATANH(2), "aborta")
)
```

```result
medio | casi_uno | uno | mas_de_uno
0.549306 | 3.800201 | aborta | aborta
```

At 0.999 the value is still 3.8: it blows up only in the very last stretch. It is the open
interval, not the closed one — and a normalised figure that lands exactly on 1 brings the query
down.

## 2. The blank gets through and comes out blank

```dax
EVALUATE
ROW(
  "blanco", ATANH(BLANK()),
  "es_blanco", ISBLANK(ATANH(BLANK())),
  "cero", ATANH(0),
  "acoth_blanco", IFERROR(ACOTH(BLANK()), "aborta")
)
```

```result
blanco | es_blanco | cero | acoth_blanco
(blank) | True | 0 | aborta
```

Zero is **inside** its domain, so the blank goes in, comes out zero and comes back out blank.
[`acoth`](./acoth.md), whose domain is exactly the complement, aborts on the same blank.

## 3. It is odd, it is a logarithm, and that is why it is used for correlations

```dax
EVALUATE
ROW(
  "impar", ROUND(ATANH(0.5) + ATANH(-0.5), 10),
  "ida_y_vuelta", ROUND(ATANH(TANH(2)), 10),
  "formula_cerrada", ROUND(ATANH(0.5) - 0.5 * LN(1.5 / 0.5), 10),
  "fisher_de_0_9", ROUND(ATANH(0.9), 6)
)
```

```result
impar | ida_y_vuelta | formula_cerrada | fisher_de_0_9
0 | 2 | 0 | 1.472219
```

`ATANH(x) = ½ · LN((1+x)/(1-x))`. It is Fisher's *z* transform: it turns a correlation
coefficient — which lives bounded in (-1, 1) and cannot be averaged without bias — into an
unbounded scale where it can.

See [`tanh`](./tanh.md), [`acoth`](./acoth.md) and [`ln`](./ln.md).
