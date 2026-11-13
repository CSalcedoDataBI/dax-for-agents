---
function: SQRT
model: ninguno
---

# SQRT — examples

## 1. A negative aborts the whole query

It returns neither blank nor a cell error: it kills the query. With a constant you see it
coming; with a column that occasionally carries a negative, you do not.

```dax
EVALUATE ROW("raiz_de_menos_uno", SQRT(-1))
```

```result
ERROR: An argument of function 'SQRT' has the wrong data type or the result is too large or too small.
```

The protection, and where to put it:

```dax
EVALUATE
VAR Valores = { 9, 4, -1 }
RETURN
ROW(
  "protegido", SUMX(Valores, IF([Value] >= 0, SQRT([Value]))),
  "iferror_dentro", SUMX(Valores, IFERROR(SQRT([Value]), 0)),
  "filtrando", SUMX(FILTER(Valores, [Value] >= 0), SQRT([Value]))
)
```

```result
protegido | iferror_dentro | filtrando
5 | 5 | 5
```

All three work because the protection goes **inside** the iterator. Wrapping the whole `SUMX` in
`IFERROR` is not enough — measured in [`ln`](./ln.md).

## 2. The blank does get through, and comes out blank

```dax
EVALUATE
ROW(
  "blanco", SQRT(BLANK()),
  "es_blanco", ISBLANK(SQRT(BLANK())),
  "compara_cero", SQRT(BLANK()) = 0,
  "cero", SQRT(0)
)
```

```result
blanco | es_blanco | compara_cero | cero
(blank) | True | True | 0
```

Zero is not negative, so it does not abort: it goes in, comes out zero, and that zero which came
from a blank comes back out blank. It is the same mechanic as [`abs`](./abs.md) and
[`sign`](./sign.md).

## 3. It is `POWER(n, 0.5)`, with the precision that implies

```dax
EVALUATE
ROW(
  "sqrt_2", ROUND(SQRT(2), 6),
  "power_2", ROUND(POWER(2, 0.5), 6),
  "identicos", SQRT(2) = POWER(2, 0.5),
  "cuadrado", ROUND(SQRT(2) * SQRT(2), 10),
  "exacto", SQRT(2) * SQRT(2) = 2
)
```

```result
sqrt_2 | power_2 | identicos | cuadrado | exacto
1.414214 | 1.414214 | True | 2 | False
```

The last two columns are the point. `SQRT(2) * SQRT(2)` **prints as 2** and **is not 2**: there is
4.4 × 10⁻¹⁶ left over. The output format rounds, the comparison does not, and an
`IF(x = 2, ...)` over that takes the wrong branch without any signal.

The third column, on the other hand, is true: `SQRT(2)` and `POWER(2, 0.5)` return exactly the
same `double`. Two calculations agreeing bit for bit does not mean the round trip reconciles — it
is the same trap [`currency`](./currency.md) solves for money.

See [`power`](./power.md), [`sqrtpi`](./sqrtpi.md) and [`abs`](./abs.md).
