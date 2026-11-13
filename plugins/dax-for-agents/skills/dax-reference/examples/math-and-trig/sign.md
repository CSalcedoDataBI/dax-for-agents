---
function: SIGN
model: ninguno
---

# SIGN — examples

## 1. Three values and nothing else, however small the number

`SIGN` does not grade: any negative is -1 and any positive is 1, whatever the magnitude.

```dax
EVALUATE
ROW(
  "casi_cero_neg", SIGN(-0.0001),
  "muy_negativo", SIGN(-1000000),
  "cero", SIGN(0),
  "casi_cero_pos", SIGN(0.0001)
)
```

```result
casi_cero_neg | muy_negativo | cero | casi_cero_pos
-1 | -1 | 0 | 1
```

That it returns **0** and not only ±1 is what makes it useful for bucketing into three — got
worse, stayed the same, got better — with a single expression.

## 2. The blank comes out blank, and that breaks the three-way bucketing

```dax
EVALUATE
ROW(
  "sign_blanco", SIGN(BLANK()),
  "es_blanco", ISBLANK(SIGN(BLANK())),
  "sign_cero", SIGN(0),
  "cero_es_blanco", ISBLANK(SIGN(0)),
  "compara", SIGN(BLANK()) = 0
)
```

```result
sign_blanco | es_blanco | sign_cero | cero_es_blanco | compara
(blank) | True | 0 | False | True
```

There are **four** possible results, not three: -1, 0, 1 and blank. A
`SWITCH(SIGN([m]), -1, ..., 0, ..., 1, ...)` leaves the rows with no data outside all three
branches and sends them to the `else`, or to blank if there is no `else`. The `= 0` comparison
does catch them, because the blank compares as zero — so `SWITCH` and `IF([x] = 0, ...)` do
**not** classify the same way.

## 3. Together with `ABS`, it decomposes a number into magnitude and direction

```dax
EVALUATE
VAR X = -42.5
RETURN
ROW(
  "original", X,
  "direccion", SIGN(X),
  "magnitud", ABS(X),
  "reconstruido", SIGN(X) * ABS(X),
  "cuadra", SIGN(X) * ABS(X) = X
)
```

```result
original | direccion | magnitud | reconstruido | cuadra
-42.5 | -1 | 42.5 | -42.5 | True
```

`n = SIGN(n) × ABS(n)` for every non-zero number, and for zero as well. It is how you sort by
magnitude without losing the sign, or paint what fell in red using the same value that gives the
bar its height.

See [`abs`](./abs.md).
