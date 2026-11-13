---
function: LOWER
model: ninguno
---

# LOWER — examples

## 1. As with UPPER, comparing with it adds nothing

`=` already ignores case. A `LOWER` on both sides is noise that also hides that property from the
next person who reads the code.

```dax
EVALUATE
ROW(
  "sin_lower", "SONY" = "sony",
  "con_lower", LOWER("SONY") = LOWER("sony"),
  "exact",     EXACT("SONY", "sony")
)
```

```result
sin_lower | con_lower | exact
True | True | False
```

## 2. Where it does help: normalising before grouping or building a key

Here the goal is not to compare, it is to make two different spellings produce **the same text**.

```dax
EVALUATE
ROW(
  "clave_1",    LOWER(TRIM("  Sony  ")),
  "clave_2",    LOWER(TRIM("SONY")),
  "coinciden",  EXACT(LOWER(TRIM("  Sony  ")), LOWER(TRIM("SONY"))),
  "con_duro",   EXACT(LOWER(TRIM("Sony" & UNICHAR(160))), "sony")
)
```

```result
clave_1 | clave_2 | coinciden | con_duro
sony | sony | True | False
```

The last one is a reminder that `TRIM` does not remove the non-breaking space: the key comes out
different and the group splits in two. See [`trim`](./trim.md) and
[`substitute`](./substitute.md).

## 3. With a blank, numbers and signs

```dax
EVALUATE
ROW(
  "blanco",      "[" & LOWER(BLANK()) & "]",
  "es_blanco",   ISBLANK(LOWER(BLANK())),
  "con_numeros", LOWER("ABC-123"),
  "acentos",     LOWER("CAFÉ AÑO")
)
```

```result
blanco | es_blanco | con_numeros | acentos
[] | True | abc-123 | café año
```
