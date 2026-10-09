---
function: LOG
model: ninguno
---

# LOG — examples

## 1. With no second argument the base is 10, not *e*

Coming from C, Python or R — where `log` is the natural one — this reads backwards. In DAX, as in
Excel, `LOG` with no base is base 10.

```dax
EVALUATE
ROW(
  "log_100", LOG(100),
  "log10_100", LOG10(100),
  "ln_100", ROUND(LN(100), 6),
  "log_100_base_e", ROUND(LOG(100, EXP(1)), 6)
)
```

```result
log_100 | log10_100 | ln_100 | log_100_base_e
2 | 2 | 4.60517 | 4.60517
```

Columns 1 and 2 are the same function; so are 3 and 4. Confusing the two pairs gives a believable
number multiplied by 2.302585.

## 2. Base 1 aborts, and base 2 is the one actually used

```dax
EVALUATE ROW("base_uno", LOG(8, 1))
```

```result
ERROR: Division by zero has occurred when evaluating function 'LOG'.
```

There is no logarithm in base 1: `1ˣ` is always 1, so no exponent gives 8. The message is
literally a **division by zero**, and not the generic argument error the rest of this family
throws: internally `LOG(n, b)` is `LN(n) / LN(b)`, and `LN(1)` is zero. The genuinely useful case
is base 2, for counting doublings:

```dax
EVALUATE
ROW(
  "log2_8", LOG(8, 2),
  "log2_1024", LOG(1024, 2),
  "duplicaciones", ROUND(LOG(1000, 2), 6),
  "log2_1", LOG(1, 2)
)
```

```result
log2_8 | log2_1024 | duplicaciones | log2_1
3 | 10 | 9.965784 | 0
```

A thousand is nearly ten doublings. `LOG(1, base)` is 0 in any base, which is what the definition
says.

## 3. Zero and negatives abort, and the blank goes in as zero

```dax
EVALUATE
ROW(
  "cero", IFERROR(LOG(0), "aborta"),
  "negativo", IFERROR(LOG(-5), "aborta"),
  "blanco", IFERROR(LOG(BLANK()), "aborta"),
  "base_negativa", IFERROR(LOG(8, -2), "aborta")
)
```

```result
cero | negativo | blanco | base_negativa
aborta | aborta | aborta | aborta
```

Four ways to bring the same query down. And mind where you put the protection: wrapping an
iterator in `IFERROR` does **not** catch the error raised inside — it is measured in
[`ln`](./ln.md).

See [`ln`](./ln.md), [`log10`](./log10.md) and [`power`](./power.md), its inverse.
