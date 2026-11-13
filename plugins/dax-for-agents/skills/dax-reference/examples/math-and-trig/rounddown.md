---
function: ROUNDDOWN
model: ninguno
---

# ROUNDDOWN — examples

## 1. "Down" means TOWARDS ZERO, not towards minus infinity

It is the confusion that produces broken sums with negative amounts. `ROUNDDOWN(-2.7)` is not
`-3`: it is `-2`, because it moves towards zero. Anyone who wants a real floor needs
[`int`](./int.md).

```dax
EVALUATE
ROW(
  "positivo",     ROUNDDOWN(2.7, 0),
  "negativo",     ROUNDDOWN(-2.7, 0),
  "int_negativo", INT(-2.7),
  "trunc_negativo", TRUNC(-2.7)
)
```

```result
positivo | negativo | int_negativo | trunc_negativo
2 | -2 | -3 | -2
```

With positives all three coincide. With negatives, `INT` parts from the other two — and it only
shows when the first negative amount arrives.

## 2. It does not look at the half: it always cuts

Unlike [`round`](./round.md), `.5` decides nothing here. It is truncation at whatever position
you name.

```dax
EVALUATE
ROW(
  "medio_arriba", ROUND(2.5, 0),
  "medio_abajo",  ROUNDDOWN(2.5, 0),
  "casi_tres",    ROUNDDOWN(2.999, 0),
  "dos_decimales", ROUNDDOWN(2.999, 2)
)
```

```result
medio_arriba | medio_abajo | casi_tres | dos_decimales
3 | 2 | 2 | 2.99
```

## 3. Negative decimals, and the blank

```dax
EVALUATE
ROW(
  "a_decenas",  ROUNDDOWN(1999, -1),
  "a_millares", ROUNDDOWN(1999, -3),
  "blanco",     ROUNDDOWN(BLANK(), 2),
  "es_blanco",  ISBLANK(ROUNDDOWN(BLANK(), 2))
)
```

```result
a_decenas | a_millares | blanco | es_blanco
1990 | 1000 | (blank) | True
```

`ROUNDDOWN(1999, -3)` gives 1000: for grouping by magnitude that is what you want, and for
computing a total it is not.

See [`roundup`](./roundup.md), which is its mirror and carries the same confusion in reverse.
