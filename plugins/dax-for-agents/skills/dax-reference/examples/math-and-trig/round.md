---
function: ROUND
model: ninguno
---

# ROUND — examples

## 1. The half always goes outwards, never to even

DAX does not use banker's rounding. `2.5` goes up to 3 and `3.5` goes up to 4 — both move away
from zero. If you come from Python, from R or from SQL Server with banker's `ROUND`, this is the
difference that makes totals disagree across systems.

```dax
EVALUATE
ROW(
  "dos_y_medio",  ROUND(2.5, 0),
  "tres_y_medio", ROUND(3.5, 0),
  "negativo",     ROUND(-2.5, 0),
  "menos_medio",  ROUND(-0.5, 0)
)
```

```result
dos_y_medio | tres_y_medio | negativo | menos_medio
3 | 4 | -3 | -1
```

With round-half-to-even, `2.5` would give 2 and `3.5` would give 4. Here they give 3 and 4.

## 2. Negative decimals round to the left of the point

Little known, and useful for grouping magnitudes without dividing.

```dax
EVALUATE
ROW(
  "dos_decimales", ROUND(1234.5678, 2),
  "a_decenas",     ROUND(1234.5678, -1),
  "a_millares",    ROUND(1234.5678, -3),
  "mas_alla",      ROUND(1234.5678, -9)
)
```

```result
dos_decimales | a_decenas | a_millares | mas_alla
1234.57 | 1230 | 1000 | 0
```

Rounding beyond the number's own magnitude gives zero, not an error.

## 3. With a blank it returns blank, not zero

So a `ROUND` over a column with gaps does not fill them — which is correct, and at the same time
the reason the result keeps disappearing from the visual.

```dax
EVALUATE
ROW(
  "blanco",    ROUND(BLANK(), 2),
  "es_blanco", ISBLANK(ROUND(BLANK(), 2)),
  "cero",      ROUND(0, 2),
  "ya_entero", ROUND(42, 2)
)
```

```result
blanco | es_blanco | cero | ya_entero
(blank) | True | 0 | 42
```

See [`rounddown`](./rounddown.md) and [`roundup`](./roundup.md), which are **not** "down" and
"up" in the sense they appear to be, and [`int`](./int.md), which is.
