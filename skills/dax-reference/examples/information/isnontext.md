---
function: ISNONTEXT
model: ninguno
---

# ISNONTEXT — examples

## 1. It says true for a blank — and so does `NOT ISTEXT`

Worth saying before anything else, because the name invites the opposite assumption: `ISNONTEXT`
does not behave differently from `NOT ISTEXT` in any tested case, not even on the blank (section 3
measures it). It exists for compatibility with Excel, where the question is phrased as "does this
cell hold something that is not text?", and an empty cell counts as yes.

```dax
EVALUATE
ROW(
  "blanco", ISNONTEXT(BLANK()),
  "istext_del_blanco", ISTEXT(BLANK()),
  "cadena", ISNONTEXT("hola"),
  "numero", ISNONTEXT(42)
)
```

```result
blanco | istext_del_blanco | cadena | numero
True | False | False | True
```

The blank is not text, so it is "non-text". It sounds like a truism until you use it to filter:
`FILTER(T, ISNONTEXT(T[x]))` also **keeps the empty rows**.

## 2. The empty string goes to the other side

```dax
EVALUATE
ROW(
  "cadena_vacia", ISNONTEXT(""),
  "blanco", ISNONTEXT(BLANK()),
  "cero", ISNONTEXT(0),
  "booleano", ISNONTEXT(TRUE)
)
```

```result
cadena_vacia | blanco | cero | booleano
False | True | True | True
```

`""` is text, so `ISNONTEXT("")` is false — while the blank gives true. Two values a visual paints
identically, split by this predicate into opposite groups.

## 3. It agrees with `NOT ISTEXT` in every tested case

```dax
EVALUATE
ROW(
  "blanco", ISNONTEXT(BLANK()) = NOT ISTEXT(BLANK()),
  "cadena", ISNONTEXT("x") = NOT ISTEXT("x"),
  "cadena_vacia", ISNONTEXT("") = NOT ISTEXT(""),
  "numero", ISNONTEXT(42) = NOT ISTEXT(42),
  "fecha", ISNONTEXT(DATE(2024,1,1)) = NOT ISTEXT(DATE(2024,1,1))
)
```

```result
blanco | cadena | cadena_vacia | numero | fecha
True | True | True | True | True
```

They are equivalent, so the choice is about readability: `ISNONTEXT` reads better when the
intention is "anything but text, nothing included".

See [`istext`](./istext.md) and [`isblank`](./isblank.md).
