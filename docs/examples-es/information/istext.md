---
function: ISTEXT
model: ninguno
---

# ISTEXT — ejemplos

## 1. La cadena vacía SÍ es texto; el blanco no

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

`""` y `BLANK()` se ven igual en un visual y aquí se separan. Una columna importada de un CSV
suele traer cadenas vacías donde uno espera blancos, y todas las reglas escritas con `ISBLANK`
se caen en silencio.

## 2. Un número escrito como texto es texto, y ahí está el uso real

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

La última columna es la trampa completa: `"42" + 1` da **43** porque DAX convierte al operar,
pero `ISTEXT("42")` sigue diciendo que es texto. El tipo y lo que se puede hacer con el valor
son dos preguntas distintas.

## 3. `ISSTRING` es su alias exacto, y `ISNONTEXT` sí es su negación en todo lo probado

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

[`isstring`](./isstring.md) da lo mismo siempre. Y [`isnontext`](./isnontext.md) coincide con
`NOT ISTEXT` en los cinco casos de arriba, y también en booleano, moneda y texto numérico. No
se encontró ningún valor donde difieran: **la elección entre las dos es de legibilidad, no de
comportamiento.**

Ver [`isstring`](./isstring.md), [`isnontext`](./isnontext.md) y [`isnumber`](./isnumber.md).
