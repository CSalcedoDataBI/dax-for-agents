---
function: TRUNC
model: ninguno
---

# TRUNC — examples

## 1. It cuts towards zero, and that is why it is NOT INT

It is the same distinction as across the whole family, seen from the other side: `TRUNC` drops
the decimals without looking at the sign. `INT` goes down to the lower integer.

```dax
EVALUATE
ROW(
  "positivo",     TRUNC(2.7),
  "negativo",     TRUNC(-2.7),
  "int_negativo", INT(-2.7),
  "coinciden_en_positivo", TRUNC(2.7) = INT(2.7)
)
```

```result
positivo | negativo | int_negativo | coinciden_en_positivo
2 | -2 | -3 | True
```

## 2. It takes a second argument, like ROUND

That is what separates it from `INT`, which only makes integers. `TRUNC` can cut at any position.

```dax
EVALUATE
ROW(
  "sin_segundo",   TRUNC(2.789),
  "dos_decimales", TRUNC(2.789, 2),
  "a_decenas",     TRUNC(1999, -1),
  "negativo_dos",  TRUNC(-2.789, 2)
)
```

```result
sin_segundo | dos_decimales | a_decenas | negativo_dos
2 | 2.78 | 1990 | -2.78
```

`TRUNC(-2.789, 2)` gives `-2.78`, not `-2.79`: it cuts, it does not round.

## 3. With blank and with zero

```dax
EVALUATE
ROW(
  "blanco",    TRUNC(BLANK()),
  "es_blanco", ISBLANK(TRUNC(BLANK())),
  "cero",      TRUNC(0.9999),
  "cero_neg",  TRUNC(-0.9999)
)
```

```result
blanco | es_blanco | cero | cero_neg
(blank) | True | 0 | 0
```

The last two are the sign that this is not rounding: `0.9999` gives 0 and `-0.9999` gives 0 as
well — the same zero from both sides.

See [`int`](./int.md) and [`rounddown`](./rounddown.md), which does the same as `TRUNC` but goes
by another name.
