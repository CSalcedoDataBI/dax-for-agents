---
function: ISBLANK
model: ninguno
---

# ISBLANK — examples

## 1. Blank is not zero, and it is not the empty string either

Three things that look the same in a visual and are different to the engine.

```dax
EVALUATE
ROW(
  "blanco", ISBLANK(BLANK()),
  "cero", ISBLANK(0),
  "cadena_vacia", ISBLANK(""),
  "cadena_vacia_es_texto", ISTEXT("")
)
```

```result
blanco | cero | cadena_vacia | cadena_vacia_es_texto
True | False | False | True
```

`""` is **not** blank: it is text of length zero. An `ISBLANK` over a column arriving from a CSV
with empty cells can return false on every row and look as though there are no gaps.

## 2. `= 0` and `ISBLANK` do not classify the same, and that is the difference that matters

```dax
EVALUATE
ROW(
  "blanco_es_blanco", ISBLANK(BLANK()),
  "blanco_igual_cero", BLANK() = 0,
  "cero_es_blanco", ISBLANK(0),
  "cero_igual_cero", 0 = 0
)
```

```result
blanco_es_blanco | blanco_igual_cero | cero_es_blanco | cero_igual_cero
True | True | False | True
```

The `= 0` comparison is **true for both**: the blank compares as zero. `ISBLANK` is the only one
of the two that separates them. An `IF([m] = 0, "sin ventas")` also labels the categories where
nothing was measured.

## 3. It is the only type predicate that says yes to a blank

All the others reject it — except [`isnontext`](./isnontext.md), which accepts it for another
reason.

```dax
EVALUATE
ROW(
  "isblank", ISBLANK(BLANK()),
  "isnumber", ISNUMBER(BLANK()),
  "istext", ISTEXT(BLANK()),
  "isnontext", ISNONTEXT(BLANK()),
  "isdatetime", ISDATETIME(BLANK())
)
```

```result
isblank | isnumber | istext | isnontext | isdatetime
True | False | False | True | False
```

A blank **has no type**. If you are classifying a column with a ladder of `ISNUMBER`, `ISTEXT` and
the rest, the gaps fall through every branch and have to be asked about first.

See [`isnontext`](./isnontext.md), [`iserror`](./iserror.md) and
[`divide`](../math-and-trig/divide.md).
