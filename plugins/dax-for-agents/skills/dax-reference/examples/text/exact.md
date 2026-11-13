---
function: EXACT
model: ninguno
---

# EXACT — examples

## 1. It is the comparison that DOES distinguish case

DAX's `=` operator does not. `EXACT` is the only way to ask without inventing a trick with
[`unicode`](./unicode.md).

```dax
EVALUATE
ROW(
  "igual_operador", "Sony" = "SONY",
  "exact",          EXACT("Sony", "SONY"),
  "exact_iguales",  EXACT("Sony", "Sony"),
  "acentos",        EXACT("café", "cafe")
)
```

```result
igual_operador | exact | exact_iguales | acentos
True | False | True | False
```

That `"Sony" = "SONY"` is true explains why a `SUBSTITUTE` — which **does** distinguish — behaves
differently from the filter preceding it.

## 2. With blanks and empty strings

```dax
EVALUATE
ROW(
  "blanco_vs_vacia",  EXACT(BLANK(), ""),
  "blanco_vs_blanco", EXACT(BLANK(), BLANK()),
  "vacia_vs_vacia",   EXACT("", ""),
  "blanco_vs_texto",  EXACT(BLANK(), "x")
)
```

```result
blanco_vs_vacia | blanco_vs_blanco | vacia_vs_vacia | blanco_vs_texto
True | True | True | False
```

`EXACT(BLANK(), "")` is **true**: to `EXACT`, the blank and the empty string are the same text. It
distinguishes case but not that, so it is no use for auditing a source that mixes nulls with empty
strings — for that, `ISBLANK`.

## 3. The space counts, and the invisible one too

Two texts that look identical in the visual may not be. `EXACT` says so; the eye does not.

```dax
EVALUATE
ROW(
  "espacio_final",   EXACT("hola", "hola "),
  "espacio_duro",    EXACT("hola", "hola" & UNICHAR(160)),
  "tras_trim",       EXACT("hola", TRIM("  hola  ")),
  "duro_tras_trim",  EXACT("hola", TRIM("hola" & UNICHAR(160)))
)
```

```result
espacio_final | espacio_duro | tras_trim | duro_tras_trim
False | False | True | False
```

The last one is what matters: [`trim`](./trim.md) does not save you from the non-breaking space,
and `EXACT` demonstrates it in one line.
