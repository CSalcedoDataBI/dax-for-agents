---
function: ACOTH
model: ninguno
---

# ACOTH — examples

## 1. Its domain is what lies OUTSIDE [-1, 1], the opposite of `ATANH`

It is the opposite of what habit suggests: here the small values are the forbidden ones.

```dax
EVALUATE
ROW(
  "acoth_2", ROUND(ACOTH(2), 6),
  "acoth_menos_2", ROUND(ACOTH(-2), 6),
  "acoth_1_01", ROUND(ACOTH(1.01), 6),
  "dentro_del_intervalo", IFERROR(ACOTH(0.5), "aborta")
)
```

```result
acoth_2 | acoth_menos_2 | acoth_1_01 | dentro_del_intervalo
0.549306 | -0.549306 | 2.651652 | aborta
```

`ACOTH(0.5)` aborts. And at 1.01 — just outside the interval — the value is already 2.65 and
still climbing: the function blows up as it approaches ±1 from outside.

## 2. 1, -1, zero and the blank all abort

```dax
EVALUATE ROW("acoth_de_uno", ACOTH(1))
```

```result
ERROR: An argument of function 'ACOTH' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE
ROW(
  "uno", IFERROR(ACOTH(1), "aborta"),
  "menos_uno", IFERROR(ACOTH(-1), "aborta"),
  "cero", IFERROR(ACOTH(0), "aborta"),
  "blanco", IFERROR(ACOTH(BLANK()), "aborta")
)
```

```result
uno | menos_uno | cero | blanco
aborta | aborta | aborta | aborta
```

The blank goes in as zero and zero is inside the forbidden interval. Any gap in the column brings
the whole query down, so the protection has to be written — and inside the iterator, not around
it, as measured in [`ln`](./ln.md).

## 3. It is `ATANH` of the reciprocal, and that is the practical way to remember it

```dax
EVALUATE
ROW(
  "acoth_2", ROUND(ACOTH(2), 6),
  "atanh_de_un_medio", ROUND(ATANH(1/2), 6),
  "identicos", ROUND(ACOTH(2) - ATANH(0.5), 10),
  "coth_ida_vuelta", ROUND(COTH(ACOTH(3)), 10)
)
```

```result
acoth_2 | atanh_de_un_medio | identicos | coth_ida_vuelta
0.549306 | 0.549306 | 0 | 3
```

`ACOTH(x) = ATANH(1/x)`, and the domain follows from that alone: for `1/x` to fall inside
(-1, 1), `x` has to be outside.

See [`coth`](./coth.md), [`atanh`](./atanh.md) and [`acot`](./acot.md).
