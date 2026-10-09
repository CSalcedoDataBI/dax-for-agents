---
function: SEARCH
model: ninguno
---

# SEARCH — examples

> The [`search`](../../notes/search.md) field note covers the difference from `FIND`. Here are the
> wildcards and the "not found" edge.

## 1. It accepts wildcards, and that makes it dangerous with real data

`?` is any single character and `*` is anything. That is fine until the text you are looking for
**contains** one of the two: then it stops being searched for literally.

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

Searching for a literal asterisk requires escaping it with `~`. A "contains" filter built on
`SEARCH` with text coming from the user is, in practice, a wildcard injection.

## 2. If it does not find, it aborts just like FIND

The wildcard does not save you from that.

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

`SEARCH("cafe", "café")` does not find: it ignores case, **not** accents.

## 3. The real use: a "contains" that does not bring the report down

The fourth argument turns the search into a condition, which is how it should always be written.

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
