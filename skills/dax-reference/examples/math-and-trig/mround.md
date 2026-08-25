---
function: MROUND
model: ninguno
---

# MROUND — examples

## 1. It rounds to the nearest multiple

It is how amounts get bucketed, or times snapped to 15-minute blocks.

```dax
EVALUATE
ROW(
  "siete_a_tres",   MROUND(7, 3),
  "medio_sube",     MROUND(2.5, 1),
  "a_medios",       MROUND(2.3, 0.5),
  "a_veinticincos", MROUND(0.37, 0.25)
)
```

```result
siete_a_tres | medio_sube | a_medios | a_veinticincos
6 | 3 | 2.5 | 0.25
```

## 2. If the number and the multiple have DIFFERENT signs, it aborts

This is not in the signature and it is the real trap: it returns neither a strange value nor a
blank, it brings the query down. And it arrives when the first negative amount appears, not when
the formula is written.

```dax
EVALUATE ROW("signos_distintos", MROUND(-2.5, 1))
```

```result
ERROR: An argument of function 'MROUND' has the wrong data type or the result is too large or too small.
```

With both negative it works:

```dax
EVALUATE
ROW(
  "ambos_negativos", MROUND(-7, -3),
  "negativo_medio",  MROUND(-2.5, -1),
  "positivo_normal", MROUND(7, 3)
)
```

```result
ambos_negativos | negativo_medio | positivo_normal
-6 | -3 | 6
```

So a `MROUND(column, 100)` over a column that can carry negatives is a query that works until it
does not.

## 3. A zero multiple gives zero, not an error

It is the exception to the above, and worth knowing because a calculated multiple that comes out
zero gives no warning: it returns zero and the whole bucket disappears.

```dax
EVALUATE
ROW(
  "multiplo_cero", MROUND(5, 0),
  "ceiling_cero",  CEILING(5, 0),
  "blanco",        MROUND(BLANK(), 3),
  "es_blanco",     ISBLANK(MROUND(BLANK(), 3))
)
```

```result
multiplo_cero | ceiling_cero | blanco | es_blanco
0 | 0 | (blank) | True
```

See [`ceiling`](./ceiling.md) and [`floor`](./floor.md), which do the same but always in one
direction.
