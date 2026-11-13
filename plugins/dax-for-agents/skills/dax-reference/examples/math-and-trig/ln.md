---
function: LN
model: ninguno
---

# LN — examples

## 1. It is the natural logarithm: the base is *e*, not 10

Confusing it with [`log10`](./log10.md) is the mistake that raises no error — it returns a
perfectly believable number, only 2.3 times the one you wanted.

```dax
EVALUATE
ROW(
  "ln_1000", ROUND(LN(1000), 6),
  "log10_1000", LOG10(1000),
  "factor", ROUND(LN(1000) / LOG10(1000), 6),
  "ln_de_e", ROUND(LN(EXP(1)), 10)
)
```

```result
ln_1000 | log10_1000 | factor | ln_de_e
6.907755 | 3 | 2.302585 | 1
```

That 2.302585 is `LN(10)`, the fixed factor between the two bases. `LN(EXP(1)) = 1` is the
definition.

## 2. Zero and negatives abort the query, they do not return blank

The logarithm is not defined there, and DAX does not paper over it.

```dax
EVALUATE ROW("ln_cero", LN(0))
```

```result
ERROR: An argument of function 'LN' has the wrong data type or the result is too large or too small.
```

In a real model this arrives from a column, not from a constant. And here is the part that is not
obvious: **wrapping the iterator in `IFERROR` does not help.**

```dax
EVALUATE
VAR Valores = { 100, 0, -5 }
RETURN ROW("por_fuera", IFERROR(SUMX(Valores, LN([Value])), -1))
```

```result
ERROR: An argument of function 'LN' has the wrong data type or the result is too large or too small.
```

The `IFERROR` is there and the query dies anyway. It is not that `IFERROR` does not work with
`LN` — `IFERROR(LN(0), -1)` returns -1 without trouble. It is that **around an iterator it does
not reach the error raised inside**. The protection has to go in the iterated expression:

```dax
EVALUATE
VAR Valores = { 100, 0, -5 }
RETURN
ROW(
  "iferror_dentro", ROUND(SUMX(Valores, IFERROR(LN([Value]), 0)), 6),
  "con_if", ROUND(SUMX(Valores, IF([Value] > 0, LN([Value]))), 6),
  "filtrando_antes", ROUND(SUMX(FILTER(Valores, [Value] > 0), LN([Value])), 6),
  "iferror_suelto", IFERROR(LN(0), -1)
)
```

```result
iferror_dentro | con_if | filtrando_antes | iferror_suelto
4.60517 | 4.60517 | 4.60517 | -1
```

The first three work. A single row with a zero brings the whole aggregation down if the
protection is in the wrong place, and the wrong place is exactly the one that looks most natural.

## 3. It turns multiplicative growth into something you can add up

That is the reason to use it in a report: the sum of logarithms is the logarithm of the product,
so compound growth becomes additive.

```dax
EVALUATE
VAR Factores = { 1.10, 1.05, 1.20 }
RETURN
ROW(
  "producto", ROUND(PRODUCTX(Factores, [Value]), 6),
  "exp_de_suma_ln", ROUND(EXP(SUMX(Factores, LN([Value]))), 6),
  "media_geometrica", ROUND(EXP(AVERAGEX(Factores, LN([Value]))), 6)
)
```

```result
producto | exp_de_suma_ln | media_geometrica
1.386 | 1.386 | 1.114947
```

The first two columns agree because it is the same sum by two routes. The third is the
**geometric** mean — the real average growth, 11.49% — which is not the arithmetic mean of 1.10,
1.05 and 1.20.

See [`exp`](./exp.md), its inverse, and [`log`](./log.md) for other bases.
