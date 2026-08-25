---
function: EXP
model: ninguno
---

# EXP — examples

## 1. A blank comes out as 1, not blank

It is the trap that separates `EXP` from almost all its neighbours. The blank goes in as zero,
and `e⁰` is **one**, so there is no zero to collapse back to blank.

```dax
EVALUATE
ROW(
  "exp_blanco", EXP(BLANK()),
  "exp_cero", EXP(0),
  "sqrt_blanco", SQRT(BLANK()),
  "abs_blanco", ABS(BLANK())
)
```

```result
exp_blanco | exp_cero | sqrt_blanco | abs_blanco
1 | 1 | (blank) | (blank)
```

In a calculated column over data with gaps, `EXP` **fills** every gap with a 1 and the other two
let them through. It is the same mechanic that separates [`cosh`](./cosh.md) from
[`sinh`](./sinh.md).

## 2. The wall is at 710, and it is a real wall

```dax
EVALUATE ROW("desbordado", EXP(710))
```

```result
ERROR: An argument of function 'EXP' has the wrong data type or the result is too large or too small.
```

Just below it still fits, and only just:

```dax
EVALUATE
ROW(
  "exp_709_enorme", EXP(709) > POWER(10, 307),
  "exp_1", ROUND(EXP(1), 6),
  "exp_menos_1", ROUND(EXP(-1), 6),
  "producto_es_1", ROUND(EXP(1) * EXP(-1), 10)
)
```

```result
exp_709_enorme | exp_1 | exp_menos_1 | producto_es_1
True | 2.718282 | 0.367879 | 1
```

709 and 710 are the `double`'s frontier. An exponent that comes from data and grows without a
ceiling — a compounded rate, say — reaches it sooner than you would think.

## 3. It is the inverse of `LN`, and that is why it undoes a sum of logarithms

```dax
EVALUATE
VAR Factores = { 1.10, 1.05, 1.20 }
RETURN
ROW(
  "ln_ida_vuelta", ROUND(EXP(LN(7)), 10),
  "producto", ROUND(PRODUCTX(Factores, [Value]), 6),
  "por_logaritmos", ROUND(EXP(SUMX(Factores, LN([Value]))), 6)
)
```

```result
ln_ida_vuelta | producto | por_logaritmos
7 | 1.386 | 1.386
```

The last two columns are the same sum by two routes. That detour is what makes it possible to
compute a geometric mean with the tools available — see [`ln`](./ln.md).

See [`ln`](./ln.md), [`power`](./power.md) and [`sinh`](./sinh.md).
