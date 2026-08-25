---
function: ISSTRING
model: ninguno
---

# ISSTRING — ejemplos

## 1. Es un alias exacto de `ISTEXT`

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

Cada columna compara las dos funciones sobre el mismo valor. Todas verdaderas: no hay ningún
caso probado en el que difieran.

## 2. Los valores, por si no quieres saltar a la otra ficha

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

La cadena vacía **sí** es texto y el blanco **no**. Es lo que más confunde de este predicado, y
está desarrollado en [`istext`](./istext.md).

## 3. Cuál de los dos nombres usar

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

`ISTEXT` es el nombre que comparte con Excel, así que es el que reconoce más gente. `ISSTRING`
es el que encaja con el vocabulario de tipos del motor. Lo que no conviene es mezclarlos en un
mismo modelo — igual que con [`isnumber`](./isnumber.md)/[`isnumeric`](./isnumeric.md).

Ver [`istext`](./istext.md).
