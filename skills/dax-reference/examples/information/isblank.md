---
function: ISBLANK
model: ninguno
---

# ISBLANK — ejemplos

## 1. Blanco no es cero, y tampoco es la cadena vacía

Tres cosas que se ven igual en un visual y son distintas para el motor.

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

`""` **no** está en blanco: es un texto de longitud cero. Un `ISBLANK` sobre una columna que
llega de un CSV con celdas vacías puede devolver falso en todas las filas y parecer que no hay
huecos.

## 2. `= 0` y `ISBLANK` no clasifican igual, y esa es la diferencia que importa

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

La comparación `= 0` es **verdadera para los dos**: el blanco se compara como cero. `ISBLANK`
es la única de las dos que los separa. Un `IF([m] = 0, "sin ventas")` etiqueta también las
categorías donde no se midió nada.

## 3. Es el único predicado de tipo que dice sí a un blanco

Todos los demás lo rechazan — salvo [`isnontext`](./isnontext.md), que lo acepta por otra
razón.

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

Un blanco **no tiene tipo**. Si estás clasificando una columna con una escalera de `ISNUMBER`,
`ISTEXT` y demás, los huecos se caen por todas las ramas y hay que preguntar por ellos primero.

Ver [`isnontext`](./isnontext.md), [`iserror`](./iserror.md) y [`divide`](../math-and-trig/divide.md).
