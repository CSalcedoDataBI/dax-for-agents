---
function: LEFT
model: ninguno
---

# LEFT — examples

## 1. Asking for more than there is gives no error

It returns whatever is there. It sounds convenient and it is exactly what stops you noticing the
data came in short: a 3-letter code and an 8-letter one both come out "fine".

```dax
EVALUATE
ROW(
  "normal",       LEFT("Contoso", 3),
  "mas_de_largo", LEFT("ab", 10),
  "cero",         "[" & LEFT("Contoso", 0) & "]",
  "sin_segundo",  LEFT("Contoso")
)
```

```result
normal | mas_de_largo | cero | sin_segundo
Con | ab | [] | C
```

Without the second argument it returns **one** character, not the whole string.

## 2. A negative number does abort

It is the only way it warns you, and it arrives through a calculated variable, not a constant.

```dax
EVALUATE ROW("negativo", LEFT("Contoso", -1))
```

```result
ERROR: An argument of function 'LEFT' has the wrong data type or has an invalid value.
```

## 3. Over a blank and over a number

```dax
EVALUATE
ROW(
  "blanco",     "[" & LEFT(BLANK(), 3) & "]",
  "es_blanco",  ISBLANK(LEFT(BLANK(), 3)),
  "numero",     LEFT(12345, 2),
  "decimal",    LEFT(1.75, 3)
)
```

```result
blanco | es_blanco | numero | decimal
[] | True | 12 | 1,7
```

Over a number it converts to text first, with the model's culture — so the cut depends on whether
the decimal separator is a comma or a dot.

See [`right`](./right.md), [`mid`](./mid.md) and [`len`](./len.md), which counts code units and
not visible characters: that is where an emoji gets split in half.
