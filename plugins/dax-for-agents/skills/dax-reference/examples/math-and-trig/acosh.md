---
function: ACOSH
model: ninguno
---

# ACOSH — examples

## 1. It only accepts 1 or more, and the blank falls outside

`COSH` never drops below 1, so its inverse has nothing to return below there.

```dax
EVALUATE ROW("por_debajo_de_uno", ACOSH(0.5))
```

```result
ERROR: An argument of function 'ACOSH' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE
ROW(
  "uno", ACOSH(1),
  "medio", IFERROR(ACOSH(0.5), "aborta"),
  "cero", IFERROR(ACOSH(0), "aborta"),
  "blanco", IFERROR(ACOSH(BLANK()), "aborta")
)
```

```result
uno | medio | cero | blanco
0 | aborta | aborta | aborta
```

`ACOSH(1)` is exactly **0** — it is the floor of the domain and the function's zero. The blank
goes in as zero and zero is forbidden, so a gap in the data brings the query down. Compare with
[`asinh`](./asinh.md), which accepts any number.

## 2. It is not symmetric: it loses the sign `COSH` had already lost

```dax
EVALUATE
ROW(
  "cosh_2", ROUND(COSH(2), 6),
  "cosh_menos_2", ROUND(COSH(-2), 6),
  "acosh_de_eso", ROUND(ACOSH(COSH(-2)), 10),
  "no_recupera_el_signo", ACOSH(COSH(-2)) = -2
)
```

```result
cosh_2 | cosh_menos_2 | acosh_de_eso | no_recupera_el_signo
3.762196 | 3.762196 | 2 | False
```

`COSH(-2)` and `COSH(2)` are the same number, so `ACOSH` returns **2** and not -2. The round trip
only closes for non-negative values, which is what it means for `COSH` not to be injective.

## 3. It is a logarithm in disguise

```dax
EVALUATE
ROW(
  "acosh_2", ROUND(ACOSH(2), 6),
  "formula_cerrada", ROUND(LN(2 + SQRT(3)), 6),
  "identicos", ROUND(ACOSH(2) - LN(2 + SQRT(3)), 10),
  "crece_despacio", ROUND(ACOSH(1000), 6)
)
```

```result
acosh_2 | formula_cerrada | identicos | crece_despacio
1.316958 | 1.316958 | 0 | 7.600902
```

`ACOSH(x) = LN(x + √(x² - 1))`. Like every logarithm, it grows very slowly: at x = 1000 it barely
reaches 7.6.

See [`cosh`](./cosh.md), [`asinh`](./asinh.md) and [`ln`](./ln.md).
