---
function: FIND
model: ninguno
---

# FIND — ejemplos

> La nota de campo [`find`](../../notes/find.md) cubre la diferencia con `SEARCH` en
> mayúsculas. Aquí van los bordes: qué pasa cuando no encuentra, y desde dónde busca.

## 1. Si no encuentra, ABORTA — salvo que le des el cuarto argumento

Es la diferencia práctica que más rompe informes. Un `FIND` sin cuarto argumento sobre una
columna donde el separador falta en una sola fila tumba la medida entera.

```dax
EVALUATE ROW("sin_encontrar", FIND("z", "Contoso"))
```

```result
ERROR: The search Text provided to function 'FIND' could not be found in the given text.
```

Con el cuarto argumento devuelve lo que le digas, y ya se puede decidir:

```dax
EVALUATE
ROW(
  "encontrado",     FIND("t", "Contoso"),
  "no_encontrado",  FIND("z", "Contoso", 1, -1),
  "alternativa_0",  FIND("z", "Contoso", 1, 0),
  "alternativa_blank", ISBLANK(FIND("z", "Contoso", 1, BLANK()))
)
```

```result
encontrado | no_encontrado | alternativa_0 | alternativa_blank
4 | -1 | 0 | True
```

## 2. Distingue mayúsculas, y por eso encuentra menos de lo que parece

```dax
EVALUATE
ROW(
  "exacta",      FIND("Con", "Contoso"),
  "minuscula",   FIND("con", "Contoso", 1, -1),
  "search_igual", SEARCH("con", "Contoso"),
  "acento",      FIND("e", "café", 1, -1)
)
```

```result
exacta | minuscula | search_igual | acento
1 | -1 | 1 | -1
```

`FIND` con `"con"` no encuentra nada donde [`search`](./search.md) sí. Cambiar una por otra
«porque hacen lo mismo» cambia el resultado.

## 3. El tercer argumento es desde dónde, y sirve para encontrar la segunda aparición

El patrón para partir por el **último** separador en vez de por el primero.

```dax
EVALUATE
VAR Ruta = "a.b.c"
VAR Primero = FIND(".", Ruta)
VAR Segundo = FIND(".", Ruta, Primero + 1)
RETURN
ROW(
  "primero", Primero,
  "segundo", Segundo,
  "tercero", FIND(".", Ruta, Segundo + 1, -1)
)
```

```result
primero | segundo | tercero
2 | 4 | -1
```

Empezar en 0 no es «desde el principio»: aborta, igual que en [`mid`](./mid.md). Y el cuarto
argumento **no** rescata de eso — solo cubre el «no encontrado», no el argumento inválido:

```dax
EVALUATE ROW("desde_0", FIND(".", "a.b.c", 0, -1))
```

```result
ERROR: An argument of function 'FIND' has the wrong data type or has an invalid value.
```

Ver [`mid`](./mid.md), que es con lo que se corta después.
