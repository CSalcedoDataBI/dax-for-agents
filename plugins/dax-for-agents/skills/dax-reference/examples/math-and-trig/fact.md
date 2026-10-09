---
function: FACT
model: ninguno
---

# FACT — examples

## 1. It truncates decimals, and that is where it parts from `GCD` and `LCM`

All three take numbers that ought to be integers. `FACT` **truncates** and the other two
**round**, so the same input gives different answers depending on the function.

```dax
EVALUATE
ROW(
  "fact_4_9", FACT(4.9),
  "fact_4_1", FACT(4.1),
  "fact_4", FACT(4),
  "gcd_4_9_con_6", GCD(4.9, 6)
)
```

```result
fact_4_9 | fact_4_1 | fact_4 | gcd_4_9_con_6
24 | 24 | 24 | 1
```

`FACT(4.9)` is 24, that is 4!. But `GCD(4.9, 6)` treats the 4.9 as **5** and returns 1 instead of
the 2 it would give with 4. Two different rules in the same family — it is measured in
[`gcd`](./gcd.md).

## 2. The ceiling is at 170, and the blank is worth 1

```dax
EVALUATE ROW("desbordado", FACT(171))
```

```result
ERROR: An argument of function 'FACT' has the wrong data type or the result is too large or too small.
```

Just below it still fits, and the blank has an answer that surprises:

```dax
EVALUATE
ROW(
  "fact_170_enorme", FACT(170) > POWER(10, 300),
  "fact_0", FACT(0),
  "fact_blanco", FACT(BLANK()),
  "negativo", IFERROR(FACT(-1), "aborta")
)
```

```result
fact_170_enorme | fact_0 | fact_blanco | negativo
True | 1 | 1 | aborta
```

`FACT(BLANK())` is **1**, not blank: the blank goes in as zero and `0!` is one, which is not
zero, so there is nothing to collapse. Same mechanic as [`exp`](./exp.md) and
[`cosh`](./cosh.md). In a calculated column that means the gaps get filled with a 1 in silence.

## 3. It grows so fast that 170 is not much headroom

```dax
EVALUATE
ROW(
  "fact_10", FACT(10),
  "fact_20", FACT(20),
  "fact_50_orden", ROUND(LOG10(FACT(50)), 4),
  "fact_100_orden", ROUND(LOG10(FACT(100)), 4)
)
```

```result
fact_10 | fact_20 | fact_50_orden | fact_100_orden
3628800 | 2432902008176640000 | 64.4831 | 157.97
```

50! already has 65 digits. For combinatorics over real data, the practical route is to work with
the [`log10`](./log10.md) of the factorial rather than the factorial itself, or the overflow
arrives immediately.

See [`gcd`](./gcd.md), [`lcm`](./lcm.md) and [`log10`](./log10.md).
