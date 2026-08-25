---
function: ISSTRING
model: ninguno
---

# ISSTRING — examples

## 1. It is an exact alias of `ISTEXT`

```dax
EVALUATE
ROW(
  "cadena", ISSTRING("hola") = ISTEXT("hola"),
  "cadena_vacia", ISSTRING("") = ISTEXT(""),
  "numero", ISSTRING(42) = ISTEXT(42),
  "texto_numerico", ISSTRING("42") = ISTEXT("42"),
  "blanco", ISSTRING(BLANK()) = ISTEXT(BLANK())
)
```

```result
cadena | cadena_vacia | numero | texto_numerico | blanco
True | True | True | True | True
```

Each column compares the two functions on the same value. All true: there is no tested case in
which they differ.

## 2. The values, in case you would rather not jump to the other card

```dax
EVALUATE
ROW(
  "cadena", ISSTRING("hola"),
  "cadena_vacia", ISSTRING(""),
  "numero", ISSTRING(42),
  "texto_numerico", ISSTRING("42"),
  "blanco", ISSTRING(BLANK())
)
```

```result
cadena | cadena_vacia | numero | texto_numerico | blanco
True | True | False | True | False
```

The empty string **is** text and the blank is **not**. It is the most confusing thing about this
predicate, and it is worked through in [`istext`](./istext.md).

## 3. Which of the two names to use

```dax
EVALUATE
ROW(
  "misma_respuesta", ISSTRING(CURRENCY(2)) = ISTEXT(CURRENCY(2)),
  "isstring", ISSTRING(CURRENCY(2)),
  "istext", ISTEXT(CURRENCY(2))
)
```

```result
misma_respuesta | isstring | istext
True | False | False
```

`ISTEXT` is the name it shares with Excel, so it is the one more people recognise. `ISSTRING` is
the one that fits the engine's type vocabulary. What is unwise is mixing them in the same model —
just as with [`isnumber`](./isnumber.md)/[`isnumeric`](./isnumeric.md).

See [`istext`](./istext.md).
