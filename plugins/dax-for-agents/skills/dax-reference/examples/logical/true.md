---
function: TRUE
model: ninguno
---

# TRUE — examples

## 1. It is a function, and it takes parentheses

`TRUE` is not a reserved word: it is a function with no arguments. Without `()` DAX tries to
resolve it as a name and fails.

```dax
EVALUATE
ROW(
  "con_parentesis", TRUE(),
  "comparada",      TRUE() = TRUE(),
  "dentro_de_if",   IF(TRUE(), "rama SI", "rama NO")
)
```

```result
con_parentesis | comparada | dentro_de_if
True | True | rama SI
```

## 2. It is worth 1 in arithmetic, but it canNOT be compared to 1

This is what you discover by running it. `TRUE() + 0` gives 1 without trouble, so intuition says
`TRUE() = 1` ought to work too. It does not: DAX refuses to compare a boolean with an integer.

```dax
EVALUATE
ROW(
  "true_mas_cero",  TRUE() + 0,
  "false_mas_cero", FALSE() + 0,
  "suma_de_tres",   (1 = 1) + (2 = 2) + (3 = 4)
)
```

```result
true_mas_cero | false_mas_cero | suma_de_tres
1 | 0 | 2
```

`(1=1) + (2=2) + (3=4)` counts how many conditions hold without writing three `IF`s. The
conversion happens because the `+` forces it; the comparison does not force it, and that is why it
aborts:

```dax
EVALUATE ROW("comparado_con_uno", TRUE() = 1)
```

```result
ERROR: DAX comparison operations do not support comparing values of type True/False with values of type Integer. Consider using the VALUE or FORMAT function to convert one of the values.
```

If you need to compare, convert first yourself:

```dax
EVALUATE ROW("convertido_antes", TRUE() + 0 = 1)
```

```result
convertido_antes
True
```

## 3. Comparing against TRUE() with `=` or with `==` is not the same

```dax
EVALUATE
ROW(
  "sin_comparar",     IF(1 = 1, "sí", "no"),
  "comparado_simple", IF((1 = 1) = TRUE(), "sí", "no"),
  "blanco_simple",    IF(BLANK() = TRUE(), "sí", "no"),
  "blanco_estricto",  IF(BLANK() == TRUE(), "sí", "no")
)
```

```result
sin_comparar | comparado_simple | blanco_simple | blanco_estricto
sí | sí | no | no
```

See [`false`](./false.md), and the [`blank`](../../notes/blank.md) field note for the mechanism
behind `=` versus `==`.
