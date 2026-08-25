---
function: FIXED
model: ninguno
---

# FIXED — examples

## 1. It returns TEXT, and there the arithmetic ends

It looks like `ROUND` and it is not: `ROUND` returns a number, `FIXED` returns a string. Whatever
comes out of here no longer adds up or sorts as a number.

```dax
EVALUATE
ROW(
  "fixed",       FIXED(1234.5678, 2),
  "round",       ROUND(1234.5678, 2),
  "fixed_len",   LEN(FIXED(1234.5678, 2)),
  "orden_texto", FIXED(9, 0) < FIXED(10, 0)
)
```

```result
fixed | round | fixed_len | orden_texto
1.234,57 | 1234.57 | 8 | False
```

`"9" < "10"` is false as text and true as a number. It is the same trap as
[`format`](./format.md), and the reason these functions belong in the visual, not inside the
logic.

## 2. It adds a thousands separator unless you tell it not to

The third argument. And the separator is the **model's culture**, here `es-ES`: the dot for
thousands and the comma for decimals.

```dax
EVALUATE
ROW(
  "con_miles", FIXED(1234567.891, 2),
  "sin_miles", FIXED(1234567.891, 2, TRUE),
  "cero_dec",  FIXED(1234.5, 0),
  "un_dec",    FIXED(1234.55, 1)
)
```

```result
con_miles | sin_miles | cero_dec | un_dec
1.234.567,89 | 1234567,89 | 1.235 | 1.234,6
```

## 3. A negative number of decimals rounds to the LEFT of the point

Little known and very useful: `-3` rounds to thousands. And it still returns text.

```dax
EVALUATE
ROW(
  "menos_1", FIXED(12345.6, -1),
  "menos_3", FIXED(12345.6, -3),
  "menos_9", FIXED(12345.6, -9),
  "blanco",  FIXED(BLANK(), 2)
)
```

```result
menos_1 | menos_3 | menos_9 | blanco
12.350 | 12.000 | 0 | 0,00
```

Rounding beyond the number's own magnitude gives zero, not an error.
