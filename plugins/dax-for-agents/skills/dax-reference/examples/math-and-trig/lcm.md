---
function: LCM
model: ninguno
---

# LCM — examples

## 1. Two arguments at most, just like `GCD`

```dax
EVALUATE
ROW(
  "dos", LCM(4, 6),
  "tres_anidada", LCM(LCM(4, 6), 10),
  "coprimos", LCM(7, 9),
  "uno_multiplo_del_otro", LCM(4, 12)
)
```

```result
dos | tres_anidada | coprimos | uno_multiplo_del_otro
12 | 60 | 63 | 12
```

With coprimes the least common multiple is the product; when one divides the other, it is the
larger. For more than two numbers you have to nest, as in [`gcd`](./gcd.md).

## 2. It rounds decimals, it does not truncate them

```dax
EVALUATE
ROW(
  "cuatro_coma_cuatro", LCM(4.4, 6),
  "cuatro_coma_seis", LCM(4.6, 6),
  "cuatro", LCM(4, 6),
  "cinco", LCM(5, 6)
)
```

```result
cuatro_coma_cuatro | cuatro_coma_seis | cuatro | cinco
12 | 30 | 12 | 30
```

4.6 behaves like 5 and returns 30 instead of 12. It is the same rule as [`gcd`](./gcd.md) and the
opposite of [`fact`](./fact.md).

## 3. Zero absorbs, negatives abort, and the result grows fast

```dax
EVALUATE
ROW(
  "con_cero", LCM(0, 5),
  "con_blanco", LCM(BLANK(), 5),
  "negativo", IFERROR(LCM(-4, 6), "aborta"),
  "grandes", LCM(123456, 789012)
)
```

```result
con_cero | con_blanco | negativo | grandes
0 | 0 | aborta | 8117355456
```

`LCM(0, n)` is **0**, not `n` — the opposite of [`gcd`](./gcd.md), where zero is the identity. A
blank in the data turns the whole calculation into zero without warning.

And with two six-figure numbers the result already passes 8 billion: `LCM(a, b)` is
`a × b / GCD(a, b)`, so with large coprimes it overflows sooner than you would think.

See [`gcd`](./gcd.md) and [`mod`](./mod.md).
