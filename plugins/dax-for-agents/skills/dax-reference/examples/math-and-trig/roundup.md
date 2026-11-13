---
function: ROUNDUP
model: ninguno
---

# ROUNDUP — examples

## 1. "Up" means AWAY FROM ZERO

The mirror of [`rounddown`](./rounddown.md), with the same confusion in reverse:
`ROUNDUP(-2.1)` is `-3`, not `-2`. A negative becomes **more negative**.

```dax
EVALUATE
ROW(
  "positivo",  ROUNDUP(2.1, 0),
  "negativo",  ROUNDUP(-2.1, 0),
  "ceiling",   CEILING(-2.1, 1),
  "iso",       ISO.CEILING(-2.1, 1)
)
```

```result
positivo | negativo | ceiling | iso
3 | -3 | -2 | -2
```

`CEILING` with a positive significance does go towards positive infinity, so it gives `-2`. The
two functions that sound like "upwards" do not agree on negatives.

## 2. Any remainder rounds up, however small

It is what you want for working out boxes, licences or batches: a little is left over, one more
is needed.

```dax
EVALUATE
ROW(
  "justo",       ROUNDUP(2.0, 0),
  "un_pelin",    ROUNDUP(2.0001, 0),
  "cajas_de_12", ROUNDUP(DIVIDE(25, 12), 0),
  "dos_dec",     ROUNDUP(2.001, 2)
)
```

```result
justo | un_pelin | cajas_de_12 | dos_dec
2 | 3 | 3 | 2.01
```

## 3. Negative decimals, and the blank

```dax
EVALUATE
ROW(
  "a_decenas",  ROUNDUP(1001, -1),
  "a_millares", ROUNDUP(1001, -3),
  "blanco",     ROUNDUP(BLANK(), 2),
  "es_blanco",  ISBLANK(ROUNDUP(BLANK(), 2))
)
```

```result
a_decenas | a_millares | blanco | es_blanco
1010 | 2000 | (blank) | True
```
