---
function: QUOTIENT
model: ninguno
---

# QUOTIENT — examples

## 1. It truncates towards zero, not downwards

With positive numbers the two coincide and nobody notices. With negatives they part company, and
`QUOTIENT` is **not** `INT` of the division.

```dax
EVALUATE
ROW(
  "quotient_pos", QUOTIENT(10, 3),
  "int_pos", INT(10 / 3),
  "quotient_neg", QUOTIENT(-10, 3),
  "int_neg", INT(-10 / 3),
  "trunc_neg", TRUNC(-10 / 3)
)
```

```result
quotient_pos | int_pos | quotient_neg | int_neg | trunc_neg
3 | 3 | -3 | -4 | -3
```

`QUOTIENT` goes with `TRUNC` (towards zero) and not with `INT` (downwards). If you are paginating
or batching and some value can be negative, the difference is a whole batch.

## 2. It discards the remainder silently, decimals included

It does not round: it keeps the integer part of the quotient and throws the rest away without
warning.

```dax
EVALUATE
ROW(
  "casi_cuatro", QUOTIENT(11.9, 3),
  "division_real", ROUND(11.9 / 3, 6),
  "decimales_arriba", QUOTIENT(7, 2),
  "division_real_2", 7 / 2
)
```

```result
casi_cuatro | division_real | decimales_arriba | division_real_2
3 | 3.966667 | 3 | 3.5
```

3.97 becomes 3. It is what integer division is for, but it is worth seeing written down before
using it to allocate amounts.

## 3. A zero divisor aborts the query

Like [`mod`](./mod.md) and unlike [`divide`](./divide.md), there is no courtesy blank here.

```dax
EVALUATE
ROW(
  "divisor_cero", IFERROR(QUOTIENT(10, 0), "aborta"),
  "dividendo_blanco", QUOTIENT(BLANK(), 3),
  "divisor_blanco", IFERROR(QUOTIENT(10, BLANK()), "aborta")
)
```

```result
divisor_cero | dividendo_blanco | divisor_blanco
aborta | (blank) | aborta
```

A **blank** divisor also aborts, because it goes in as zero. That is the case that arrives from
the data rather than from a constant written by hand.

See [`mod`](./mod.md), [`divide`](./divide.md) and [`int`](./int.md).
