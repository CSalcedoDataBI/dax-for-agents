---
function: VALUE
model: ninguno
---

# VALUE — examples

## 1. Anything that is not a number ABORTS the query

It does not return blank: it throws an error that takes the whole measure with it. A text column
with a single dirty row brings the entire visual down, not just that row.

```dax
EVALUATE
ROW(
  "entero",       VALUE("42"),
  "con_espacios", VALUE("  42  "),
  "negativo",     VALUE("-7"),
  "notacion_e",   VALUE("1E3")
)
```

```result
entero | con_espacios | negativo | notacion_e
42 | 42 | -7 | 1000
```

With rubbish inside:

```dax
EVALUATE ROW("texto", VALUE("cuarenta y dos"))
```

```result
ERROR: Cannot convert value 'cuarenta y dos' of type Text to type Number.
```

To survive that you have to wrap it, and there [`iferror`](../logical/iferror.md)'s problem
begins: it catches that error and also the ones you were not expecting.

## 2. The empty string aborts; the blank does not

Two forms of "no data" that behave in opposite ways.

```dax
EVALUATE
ROW(
  "blanco",       VALUE(BLANK()),
  "es_blanco",    ISBLANK(VALUE(BLANK())),
  "ya_es_numero", VALUE(42)
)
```

```result
blanco | es_blanco | ya_es_numero
(blank) | True | 42
```

```dax
EVALUATE ROW("cadena_vacia", VALUE(""))
```

```result
ERROR: Cannot convert value '' of type Text to type Number.
```

If the source mixes nulls and empty strings — which is common — half the rows pass and the other
half bring the query down.

## 3. The decimal separator is the CULTURE's, and here it is the comma

This model is `es-ES`. `"3.5"` is not read as three and a half: the dot is a thousands separator,
so it comes out as **35**. The same literals in an `en-US` model give different numbers.

```dax
EVALUATE
ROW(
  "con_coma",    VALUE("3,5"),
  "con_punto",   VALUE("3.5"),
  "miles_punto", VALUE("1.234"),
  "miles_coma",  VALUE("1,234")
)
```

```result
con_coma | con_punto | miles_punto | miles_coma
3.5 | 35 | 1234 | 1.234
```

It is why converting text to a number on the fly is fragile: the same report opened under another
regional setting returns different figures with no warning. It is solved at the source, by typing
the column.
