---
function: EXACT
model: ninguno
---

# EXACT — ejemplos

## 1. Es la comparación que SÍ distingue mayúsculas

El operador `=` de DAX no las distingue. `EXACT` es la única forma de preguntarlo sin
inventar un truco con [`unicode`](./unicode.md).

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

Que `"Sony" = "SONY"` sea verdadero explica por qué un `SUBSTITUTE` —que **sí** distingue—
se comporta distinto que el filtro que lo precede.

## 2. Con blancos y cadenas vacías

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

`EXACT(BLANK(), "")` es **verdadero**: para `EXACT`, el blanco y la cadena vacía son el mismo
texto. Distingue mayúsculas pero no distingue eso, así que no sirve para auditar un origen que
mezcla nulos con cadenas vacías — para eso, `ISBLANK`.

## 3. El espacio cuenta, y el invisible también

Dos textos que se ven idénticos en el visual pueden no serlo. `EXACT` lo dice; el ojo no.

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

El último es el que importa: [`trim`](./trim.md) no salva del espacio duro, y `EXACT` lo
demuestra en una línea.
