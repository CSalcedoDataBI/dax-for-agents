---
function: SEARCH
model: ninguno
---

# SEARCH — ejemplos

> La nota de campo [`search`](../../notes/search.md) cubre la diferencia con `FIND`. Aquí van
> los comodines y el borde de «no encontrado».

## 1. Acepta comodines, y eso la vuelve peligrosa con datos reales

`?` es un carácter cualquiera y `*` es cualquier cosa. Está bien hasta que el texto que
buscas **contiene** uno de los dos: entonces deja de buscarlo literalmente.

```dax
EVALUATE
ROW(
  "interrogante", SEARCH("Cont?so", "Contoso"),
  "asterisco",    SEARCH("Con*so", "Contoso"),
  "literal_asterisco", SEARCH("*", "a*b"),
  "escapado",     SEARCH("~*", "a*b")
)
```

```result
interrogante | asterisco | literal_asterisco | escapado
1 | 1 | 1 | 2
```

Buscar un asterisco literal exige escaparlo con `~`. Un filtro «contiene» construido sobre
`SEARCH` con texto que viene del usuario es, en la práctica, una inyección de comodines.

## 2. Si no encuentra, aborta igual que FIND

El comodín no salva de eso.

```dax
EVALUATE ROW("sin_encontrar", SEARCH("z", "Contoso"))
```

```result
ERROR: The search Text provided to function 'SEARCH' could not be found in the given text.
```

```dax
EVALUATE
ROW(
  "encontrado",    SEARCH("oso", "Contoso"),
  "no_encontrado", SEARCH("z", "Contoso", 1, -1),
  "mayusculas",    SEARCH("CONTOSO", "Contoso"),
  "acento",        SEARCH("cafe", "café", 1, -1)
)
```

```result
encontrado | no_encontrado | mayusculas | acento
5 | -1 | 1 | -1
```

`SEARCH("cafe", "café")` no encuentra: ignora las mayúsculas, **no** los acentos.

## 3. El uso real: un «contiene» que no tumbe el informe

El cuarto argumento convierte la búsqueda en una condición, que es como debería escribirse
siempre.

```dax
EVALUATE
VAR Texto = "Sony Bravia"
RETURN
ROW(
  "contiene_sony",  SEARCH("sony", Texto, 1, 0) > 0,
  "contiene_lg",    SEARCH("lg", Texto, 1, 0) > 0,
  "posicion_lg",    SEARCH("lg", Texto, 1, 0),
  "empieza_por",    SEARCH("sony", Texto, 1, 0) = 1
)
```

```result
contiene_sony | contiene_lg | posicion_lg | empieza_por
True | False | 0 | True
```
