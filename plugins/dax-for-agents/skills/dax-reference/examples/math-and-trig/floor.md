---
function: FLOOR
model: ninguno
---

# FLOOR — examples

## 1. It goes towards minus infinity, so with negatives it moves AWAY from zero

The mirror of [`ceiling`](./ceiling.md). With a negative, `FLOOR` goes down — unlike
[`rounddown`](./rounddown.md), which cuts towards zero.

```dax
EVALUATE
ROW(
  "positivo",   FLOOR(2.9, 1),
  "negativo",   FLOOR(-2.1, 1),
  "rounddown",  ROUNDDOWN(-2.1, 0),
  "int",        INT(-2.1)
)
```

```result
positivo | negativo | rounddown | int
2 | -3 | -2 | -3
```

`FLOOR(x, 1)` and `INT(x)` agree; `ROUNDDOWN` does not. Three functions, two behaviours.

## 2. With a significance, it buckets downwards

The real use: putting a value on its step.

```dax
EVALUATE
ROW(
  "a_medios",     FLOOR(2.3, 0.5),
  "a_centenas",   FLOOR(1234, 100),
  "a_cuartos",    FLOOR(0.37, 0.25),
  "ya_en_tramo",  FLOOR(6, 3)
)
```

```result
a_medios | a_centenas | a_cuartos | ya_en_tramo
2 | 1200 | 0.25 | 6
```

## 3. A zero significance: here it DOES abort, and its siblings do not

It is the asymmetry documented nowhere. With a zero multiple, [`ceiling`](./ceiling.md) and
[`mround`](./mround.md) return 0; `FLOOR` throws division by zero. Three functions in the same
family, two different behaviours faced with the same bad data.

```dax
EVALUATE ROW("sig_cero", FLOOR(5, 0))
```

```result
ERROR: Division by zero has occurred when evaluating function 'FLOOR'.
```

Everything else behaves like the rest of the family:

```dax
EVALUATE
ROW(
  "blanco",    FLOOR(BLANK(), 1),
  "es_blanco", ISBLANK(FLOOR(BLANK(), 1)),
  "cero",      FLOOR(0, 1)
)
```

```result
blanco | es_blanco | cero
(blank) | True | 0
```

See [`mround`](./mround.md), which rounds to the **nearest** multiple instead of always to one
side — and which aborts when the signs do not match.
