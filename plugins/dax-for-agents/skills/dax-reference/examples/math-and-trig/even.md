---
function: EVEN
model: ninguno
---

# EVEN — examples

## 1. It does not check whether a number is even: it rounds up to the next even one

The name fools everybody once. `EVEN` returns neither true nor false — it returns **another
number**.

```dax
EVALUATE
ROW(
  "even_3", EVEN(3),
  "even_2", EVEN(2),
  "even_1", EVEN(1),
  "even_0", EVEN(0)
)
```

```result
even_3 | even_2 | even_1 | even_0
4 | 2 | 2 | 0
```

To ask whether something is even, the form is `MOD(n, 2) = 0`. Watch out for negatives, which in
[`mod`](./mod.md) do not behave the way they do in other languages.

## 2. It rounds AWAY from zero, not upwards

With positives, "to the next even" and "upwards" are the same thing. With negatives they are not.

```dax
EVALUATE
ROW(
  "even_m3", EVEN(-3),
  "even_m1", EVEN(-1),
  "even_m2", EVEN(-2),
  "ceiling_m3", CEILING(-3, 2)
)
```

```result
even_m3 | even_m1 | even_m2 | ceiling_m3
-4 | -2 | -2 | -2
```

`EVEN(-3)` is **-4** and `CEILING(-3, 2)` is -2. They go in opposite directions: `EVEN` moves away
from zero and [`ceiling`](./ceiling.md) climbs towards positive infinity.

## 3. With decimals it goes up to the even one, however small the step

```dax
EVALUATE
ROW(
  "even_1_5", EVEN(1.5),
  "even_2_0001", EVEN(2.0001),
  "even_blanco", EVEN(BLANK()),
  "even_texto", EVEN("3")
)
```

```result
even_1_5 | even_2_0001 | even_blanco | even_texto
2 | 4 | (blank) | 4
```

`EVEN(2.0001)` gives **4**: anything above 2 already needs the next even number.

The blank column is worth stopping on. `EVEN(BLANK())` comes out **blank**, and `EVEN(0)` comes
out **0**. It is not an inconsistency: the blank goes in as zero, `EVEN(0)` is zero, and a zero
that came from a blank comes back out as blank. Compare with [`odd`](./odd.md), where
`ODD(BLANK())` is **1** for this very reason — its result at zero is not zero, so there is nothing
to collapse.

See [`odd`](./odd.md), [`ceiling`](./ceiling.md) and [`mround`](./mround.md).
