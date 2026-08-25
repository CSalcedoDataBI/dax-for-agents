---
function: REPLACE
model: ninguno
---

# REPLACE — examples

## 1. It substitutes by POSITION, not by content

It is the difference from [`substitute`](./substitute.md), and the one that gets it picked wrong.
`REPLACE` searches for nothing: you tell it where to start and how many characters to cover.

```dax
EVALUATE
ROW(
  "por_posicion",  REPLACE("Contoso", 1, 3, "XXX"),
  "por_contenido", SUBSTITUTE("Contoso", "Con", "XXX"),
  "en_medio",      REPLACE("Contoso", 4, 2, "--"),
  "hasta_el_final", REPLACE("Contoso", 4, 99, "!")
)
```

```result
por_posicion | por_contenido | en_medio | hasta_el_final
XXXtoso | XXXtoso | Con--so | Con!
```

Asking for more characters than are left gives no error: it covers up to the end.

## 2. With length 0, it inserts instead of substituting

The least obvious use and the most useful: it is how you put something in the middle of a string.

```dax
EVALUATE
ROW(
  "inserta",      REPLACE("2024", 5, 0, "-01"),
  "al_principio", REPLACE("2024", 1, 0, "AÑO "),
  "mas_alla",     REPLACE("2024", 99, 0, "!"),
  "vacia",        REPLACE("Contoso", 1, 3, "")
)
```

```result
inserta | al_principio | mas_alla | vacia
2024-01 | AÑO 2024 | 2024! | toso
```

Inserting past the end **appends to the end**, rather than failing or leaving a gap.

## 3. Position 0 aborts, just as in MID

```dax
EVALUATE ROW("posicion_0", REPLACE("Contoso", 0, 3, "X"))
```

```result
ERROR: An argument of function 'REPLACE' has the wrong data type or has an invalid value.
```

And over a blank something happens that is worth seeing: `REPLACE(BLANK(), 1, 3, "X")` does
**not** return blank, it returns `"X"`. The blank is treated as an empty string and the new text
is inserted anyway, so a column with gaps fills itself with the replacement.

```dax
EVALUATE
ROW(
  "blanco",     "[" & REPLACE(BLANK(), 1, 3, "X") & "]",
  "es_blanco",  ISBLANK(REPLACE(BLANK(), 1, 3, "X")),
  "numero",     REPLACE(12345, 2, 2, "--")
)
```

```result
blanco | es_blanco | numero
[X] | False | 1--45
```

Over a number it converts to text first — with the model's culture, so the position depends on
whether the decimal separator is a comma or a dot.
