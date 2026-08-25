---
function: ISTEXT
model: ninguno
---

# ISTEXT — examples

## 1. The empty string IS text; the blank is not

```dax
EVALUATE
ROW(
  "cadena", ISTEXT("hola"),
  "cadena_vacia", ISTEXT(""),
  "blanco", ISTEXT(BLANK()),
  "cadena_vacia_es_blanco", ISBLANK("")
)
```

```result
cadena | cadena_vacia | blanco | cadena_vacia_es_blanco
True | True | False | False
```

`""` and `BLANK()` look the same in a visual and here they part. A column imported from a CSV
usually brings empty strings where you expect blanks, and every rule written with `ISBLANK` falls
over in silence.

## 2. A number written as text is text, and there is the real use

```dax
EVALUATE
ROW(
  "texto_numerico", ISTEXT("42"),
  "numero", ISTEXT(42),
  "es_numero", ISNUMBER("42"),
  "pero_suma", "42" + 1
)
```

```result
texto_numerico | numero | es_numero | pero_suma
True | False | False | 43
```

The last column is the whole trap: `"42" + 1` gives **43** because DAX converts when operating,
but `ISTEXT("42")` still says it is text. The type and what can be done with the value are two
different questions.

## 3. `ISSTRING` is its exact alias, and `ISNONTEXT` is its negation in everything tested

```dax
EVALUATE
ROW(
  "alias_cadena", ISTEXT("x") = ISSTRING("x"),
  "alias_numero", ISTEXT(42) = ISSTRING(42),
  "alias_blanco", ISTEXT(BLANK()) = ISSTRING(BLANK()),
  "negacion_en_blanco", ISNONTEXT(BLANK()) = NOT ISTEXT(BLANK()),
  "negacion_en_numero", ISNONTEXT(42) = NOT ISTEXT(42)
)
```

```result
alias_cadena | alias_numero | alias_blanco | negacion_en_blanco | negacion_en_numero
True | True | True | True | True
```

[`isstring`](./isstring.md) always gives the same. And [`isnontext`](./isnontext.md) agrees with
`NOT ISTEXT` in the five cases above, and also on booleans, currency and numeric text. No value
was found where they differ: **the choice between the two is about readability, not behaviour.**

See [`isstring`](./isstring.md), [`isnontext`](./isnontext.md) and [`isnumber`](./isnumber.md).
