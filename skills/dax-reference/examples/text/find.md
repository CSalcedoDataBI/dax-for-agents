---
function: FIND
model: ninguno
---

# FIND — examples

> The [`find`](../../notes/find.md) field note covers the difference from `SEARCH` on case. Here
> are the edges: what happens when it does not find, and where it searches from.

## 1. If it does not find, it ABORTS — unless you give it the fourth argument

It is the practical difference that breaks the most reports. A `FIND` with no fourth argument over
a column where the separator is missing on a single row brings the whole measure down.

```dax
EVALUATE ROW("sin_encontrar", FIND("z", "Contoso"))
```

```result
ERROR: The search Text provided to function 'FIND' could not be found in the given text.
```

With the fourth argument it returns whatever you tell it, and then you can decide:

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

## 2. It distinguishes case, and that is why it finds less than it seems

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

`FIND` with `"con"` finds nothing where [`search`](./search.md) does. Swapping one for the other
"because they do the same" changes the result.

## 3. The third argument is where from, and it is how you find the second occurrence

The pattern for splitting on the **last** separator instead of the first.

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

Starting at 0 is not "from the beginning": it aborts, just as in [`mid`](./mid.md). And the
fourth argument does **not** rescue you from that — it only covers "not found", not an invalid
argument:

```dax
EVALUATE ROW("desde_0", FIND(".", "a.b.c", 0, -1))
```

```result
ERROR: An argument of function 'FIND' has the wrong data type or has an invalid value.
```

See [`mid`](./mid.md), which is what you cut with afterwards.
