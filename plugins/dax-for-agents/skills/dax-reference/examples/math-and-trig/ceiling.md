---
function: CEILING
model: ninguno
---

# CEILING — examples

## 1. With a positive significance it goes towards PLUS infinity

So with a negative it moves towards zero — the opposite of [`roundup`](./roundup.md), which moves
away. Both sound like "upwards" and they do not agree.

```dax
EVALUATE
ROW(
  "positivo",  CEILING(2.1, 1),
  "negativo",  CEILING(-2.1, 1),
  "roundup",   ROUNDUP(-2.1, 0),
  "a_medios",  CEILING(2.3, 0.5)
)
```

```result
positivo | negativo | roundup | a_medios
3 | -2 | -3 | 2.5
```

## 2. With a NEGATIVE significance it changes direction, and there it parts from ISO.CEILING

It is the only real difference between the two, and it only shows up when the signs cross.

```dax
EVALUATE
ROW(
  "ceiling_sig_neg", CEILING(-2.3, -1),
  "iso_sig_neg",     ISO.CEILING(-2.3, -1),
  "ceiling_sig_pos", CEILING(-2.3, 1),
  "iso_sig_pos",     ISO.CEILING(-2.3, 1)
)
```

```result
ceiling_sig_neg | iso_sig_neg | ceiling_sig_pos | iso_sig_pos
-3 | -2 | -2 | -2
```

`ISO.CEILING` **always** goes towards plus infinity, whatever happens to the significance's sign.
`CEILING` does not. If the multiple comes out of a calculation and can be negative, that
difference is a silent mismatch.

## 3. A zero significance gives zero, not an error

Just like [`mround`](./mround.md), and with the same risk: a calculated multiple that comes out
zero takes the value with it without warning.

```dax
EVALUATE
ROW(
  "sig_cero",  CEILING(5, 0),
  "blanco",    CEILING(BLANK(), 1),
  "es_blanco", ISBLANK(CEILING(BLANK(), 1)),
  "ya_multiplo", CEILING(6, 3)
)
```

```result
sig_cero | blanco | es_blanco | ya_multiplo
0 | (blank) | True | 6
```
