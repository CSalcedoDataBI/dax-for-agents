---
function: ISO.CEILING
model: ninguno
---

# ISO.CEILING — examples

## 1. Always towards plus infinity, whatever happens to the sign

That is its whole reason for existing. [`ceiling`](./ceiling.md) changes direction when the
significance is negative; this one does not.

```dax
EVALUATE
ROW(
  "iso_sig_neg",     ISO.CEILING(-2.3, -1),
  "ceiling_sig_neg", CEILING(-2.3, -1),
  "iso_sig_pos",     ISO.CEILING(-2.3, 1),
  "ceiling_sig_pos", CEILING(-2.3, 1)
)
```

```result
iso_sig_neg | ceiling_sig_neg | iso_sig_pos | ceiling_sig_pos
-2 | -3 | -2 | -2
```

The first two columns are the entire difference between the two functions. With a positive
significance they always agree, and that is why the problem does not show up in testing.

## 2. With a positive significance it behaves like CEILING

```dax
EVALUATE
ROW(
  "positivo",  ISO.CEILING(2.1, 1),
  "negativo",  ISO.CEILING(-2.1, 1),
  "a_medios",  ISO.CEILING(2.3, 0.5),
  "ya_multiplo", ISO.CEILING(6, 3)
)
```

```result
positivo | negativo | a_medios | ya_multiplo
3 | -2 | 2.5 | 6
```

## 3. The second argument is optional

Without it, significance 1 — which is the case you want 90% of the time.

```dax
EVALUATE
ROW(
  "sin_segundo",  ISO.CEILING(2.1),
  "con_uno",      ISO.CEILING(2.1, 1),
  "negativo_sin", ISO.CEILING(-2.1),
  "blanco",       ISBLANK(ISO.CEILING(BLANK()))
)
```

```result
sin_segundo | con_uno | negativo_sin | blanco
3 | 3 | -2 | True
```

The name carries a dot (`ISO.CEILING`), so its card's file is `iso-ceiling.md` and not
`iso.ceiling.md`.
