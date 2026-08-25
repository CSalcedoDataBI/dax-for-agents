---
function: VALUE
model: ninguno
---

# VALUE — ejemplos

## 1. Lo que no es un número ABORTA la consulta

No devuelve blanco: lanza un error que se lleva por delante la medida entera. Una columna de
texto con una sola fila sucia tumba el visual completo, no solo esa fila.

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

Con basura dentro:

```dax
EVALUATE ROW("texto", VALUE("cuarenta y dos"))
```

```result
ERROR: Cannot convert value 'cuarenta y dos' of type Text to type Number.
```

Para sobrevivir a eso hay que envolverlo, y ahí empieza el problema de
[`iferror`](../logical/iferror.md): captura ese error y también los que no esperabas.

## 2. La cadena vacía aborta; el blanco no

Dos formas de «no hay dato» que se comportan al revés la una de la otra.

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

Si el origen mezcla nulos y cadenas vacías —cosa habitual— la mitad de las filas pasa y la
otra mitad tumba la consulta.

## 3. El separador decimal es el de la CULTURA, y aquí es la coma

Este modelo es `es-ES`. `"3.5"` no se lee como tres y medio: el punto es separador de miles,
así que sale **35**. Los mismos literales en un modelo `en-US` dan otros números.

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

Es la razón por la que convertir texto a número al vuelo es frágil: el mismo informe abierto
con otra configuración regional devuelve cifras distintas sin avisar. Se resuelve en el
origen, tipando la columna.
