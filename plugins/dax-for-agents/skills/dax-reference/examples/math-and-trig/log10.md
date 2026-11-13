---
function: LOG10
model: ninguno
---

# LOG10 — examples

## 1. It counts digits, which is what it is for in a report

`LOG10` of a number is roughly how many digits it has, minus one. It is the short way to group by
orders of magnitude without writing a staircase of `IF`s.

```dax
EVALUATE
ROW(
  "cien", LOG10(100),
  "mil", LOG10(1000),
  "mil_y_pico", ROUND(LOG10(1234), 6),
  "orden", INT(LOG10(1234)),
  "digitos", INT(LOG10(1234)) + 1
)
```

```result
cien | mil | mil_y_pico | orden | digitos
2 | 3 | 3.091315 | 3 | 4
```

`INT(LOG10(n)) + 1` gives the digit count of a positive integer. To bucket into scales — tens,
hundreds, thousands — `INT(LOG10(n))` is the bucket directly.

## 2. It is `LOG` with no second argument, and it is not `LN`

```dax
EVALUATE
ROW(
  "log10", LOG10(1000),
  "log_sin_base", LOG(1000),
  "log_base_10", LOG(1000, 10),
  "ln", ROUND(LN(1000), 6),
  "cociente", ROUND(LN(1000) / LOG10(1000), 6)
)
```

```result
log10 | log_sin_base | log_base_10 | ln | cociente
3 | 3 | 3 | 6.907755 | 2.302585
```

The first three are identical. The fourth is another function, and that 2.302585 — `LN(10)` — is
the constant factor between them. A report with the wrong function does not fail: it publishes
figures 2.3 times too large.

## 3. Zero, negatives and blank abort the query

```dax
EVALUATE
ROW(
  "cero", IFERROR(LOG10(0), "aborta"),
  "negativo", IFERROR(LOG10(-1), "aborta"),
  "blanco", IFERROR(LOG10(BLANK()), "aborta"),
  "uno", LOG10(1)
)
```

```result
cero | negativo | blanco | uno
aborta | aborta | aborta | 0
```

The blank aborts because it goes in as zero. That is the case that arrives from a column with
gaps and not from a constant written by hand.

See [`log`](./log.md), [`ln`](./ln.md) and [`power`](./power.md).
