---
function: INT
model: ninguno
---

# INT — examples

## 1. It is the ONLY one that goes towards minus infinity

Of the whole family, `INT` is the one that really floors. `TRUNC` and `ROUNDDOWN` cut towards
zero. With positives all three agree; with negatives, `INT` parts company.

```dax
EVALUATE
ROW(
  "int_positivo", INT(2.7),
  "int_negativo", INT(-2.7),
  "trunc",        TRUNC(-2.7),
  "rounddown",    ROUNDDOWN(-2.7, 0)
)
```

```result
int_positivo | int_negativo | trunc | rounddown
2 | -3 | -2 | -2
```

If you are allocating negative amounts — refunds, adjustments — choosing wrong here throws the
total out by one unit per row.

## 2. With no decimals, it touches nothing

```dax
EVALUATE
ROW(
  "entero",      INT(42),
  "negativo_ent", INT(-42),
  "casi_entero", INT(2.9999999),
  "justo_medio", INT(-0.5)
)
```

```result
entero | negativo_ent | casi_entero | justo_medio
42 | -42 | 2 | -1
```

`INT(-0.5)` is `-1`: any decimal part in a negative drops it a whole integer.

## 3. With blank and with zero

```dax
EVALUATE
ROW(
  "blanco",    INT(BLANK()),
  "es_blanco", ISBLANK(INT(BLANK())),
  "cero",      INT(0),
  "cero_neg",  INT(-0.0)
)
```

```result
blanco | es_blanco | cero | cero_neg
(blank) | True | 0 | 0
```

See [`trunc`](./trunc.md) for the version that cuts towards zero, and
[`quotient`](./quotient.md) for integer division, which carries the same decision inside.
