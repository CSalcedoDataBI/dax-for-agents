---
function: MOD
model: ninguno
---

# MOD — examples

## 1. The sign comes from the DIVISOR, not the dividend

This is where `MOD` surprises anyone arriving from C, Java, JavaScript or Go, where the
remainder keeps the dividend's sign. DAX follows Excel's convention: **the result carries the
sign of the second argument.**

```dax
EVALUATE
ROW(
  "pos_pos", MOD(10, 3),
  "neg_pos", MOD(-10, 3),
  "pos_neg", MOD(10, -3),
  "neg_neg", MOD(-10, -3)
)
```

```result
pos_pos | neg_pos | pos_neg | neg_neg
1 | 2 | -2 | -1
```

`MOD(-10, 3)` is **2**, not -1. If you are using `MOD` to spread into groups or to detect even
numbers, with negative dividends the spread is not the one you think.

## 2. It does not reconcile with `QUOTIENT`, and that is the consequence

The identity `dividend = divisor × quotient + remainder` **breaks** when you mix the two, because
`QUOTIENT` truncates towards zero and `MOD` does not.

```dax
EVALUATE
ROW(
  "quotient", QUOTIENT(-10, 3),
  "mod", MOD(-10, 3),
  "reconstruido", 3 * QUOTIENT(-10, 3) + MOD(-10, 3),
  "original", -10
)
```

```result
quotient | mod | reconstruido | original
-3 | 2 | -7 | -10
```

It comes out **-7** where it should be -10. The quotient that does reconcile with this remainder
is `INT(-10/3)` = -4, not `QUOTIENT`'s. Writing the two together and expecting them to cancel is
a mistake that gives no warning at all.

## 3. It accepts decimals, and a zero divisor aborts

The name and the habit suggest integers. It is not.

```dax
EVALUATE
ROW(
  "decimal", MOD(10.5, 3),
  "divisor_decimal", MOD(10, 2.5),
  "divisor_cero", IFERROR(MOD(10, 0), "aborta"),
  "dividendo_blanco", MOD(BLANK(), 3)
)
```

```result
decimal | divisor_decimal | divisor_cero | dividendo_blanco
1.5 | 0 | aborta | (blank)
```

A zero divisor does **not** return blank the way [`divide`](./divide.md) would: it aborts. If the
divisor can come from data, wrap it.

See [`quotient`](./quotient.md), [`even`](./even.md) and [`odd`](./odd.md).
