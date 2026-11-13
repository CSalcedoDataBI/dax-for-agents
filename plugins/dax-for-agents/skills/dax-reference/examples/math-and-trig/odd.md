---
function: ODD
model: ninguno
---

# ODD — examples

## 1. It does not check whether a number is odd: it rounds up to the next odd one

Just like [`even`](./even.md), the name promises a question and the function returns **another
number**.

```dax
EVALUATE
ROW(
  "odd_2", ODD(2),
  "odd_3", ODD(3),
  "odd_1", ODD(1),
  "odd_1_5", ODD(1.5)
)
```

```result
odd_2 | odd_3 | odd_1 | odd_1_5
3 | 3 | 1 | 3
```

To ask whether something is odd, the form is `MOD(n, 2) <> 0`, with the care [`mod`](./mod.md)
calls for when there are negatives.

## 2. It moves away from zero, and zero does **not** stay put

This is the real difference from `EVEN`, and the one that makes the blank behave differently.

```dax
EVALUATE
ROW(
  "odd_0", ODD(0),
  "even_0", EVEN(0),
  "odd_m2", ODD(-2),
  "odd_m1", ODD(-1)
)
```

```result
odd_0 | even_0 | odd_m2 | odd_m1
1 | 0 | -3 | -1
```

`ODD(0)` is **1**: zero is not odd, so it has to move. `EVEN(0)` is 0 because it was already where
it had to be. That detail, which looks like trivia, decides the next point.

## 3. A blank comes out as 1, not blank

```dax
EVALUATE
ROW(
  "odd_blanco", ODD(BLANK()),
  "even_blanco", EVEN(BLANK()),
  "odd_texto", ODD("2"),
  "odd_m0_5", ODD(-0.5)
)
```

```result
odd_blanco | even_blanco | odd_texto | odd_m0_5
1 | (blank) | 3 | -1
```

The blank goes in as zero in both. `EVEN(0)` is zero, and a zero that came from a blank comes back
out blank; `ODD(0)` is **1**, which is not zero, so there is nothing to collapse and the 1 stays.
It is the same mechanic that separates [`sinh`](./sinh.md) from [`cosh`](./cosh.md).

In a calculated column over data with gaps, that means `ODD` **fills** the gaps with a 1 and
`EVEN` lets them through. It is rarely what was wanted.

See [`even`](./even.md), [`mround`](./mround.md) and [`ceiling`](./ceiling.md).
