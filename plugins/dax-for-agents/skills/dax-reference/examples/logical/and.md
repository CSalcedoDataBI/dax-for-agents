---
function: AND
model: ninguno
---

# AND — examples

## 1. It only accepts TWO arguments

It is the difference from Excel that costs the most time. With three conditions you have to nest
it, or use `&&`, which does chain.

```dax
EVALUATE
ROW(
  "dos_condiciones", AND(1 = 1, 2 = 2),
  "anidada",         AND(1 = 1, AND(2 = 2, 3 = 3)),
  "operador",        1 = 1 && 2 = 2 && 3 = 3
)
```

```result
dos_condiciones | anidada | operador
True | True | True
```

With three arguments it does not give a strange result: it **aborts**, and the message says
exactly how many it expected.

```dax
EVALUATE ROW("tres_argumentos", AND(1 = 1, 2 = 2, 3 = 3))
```

```result
ERROR: Too many arguments were passed to the AND function. The maximum argument count for the function is 2.
```

## 2. A blank is FALSE, and it cannot be told from a real false

`AND` converts to boolean before operating, so a blank goes in as `FALSE`. The result does not
say whether the condition was false or whether there was no data.

```dax
EVALUATE
ROW(
  "blanco_y_cierto", AND(BLANK(), TRUE()),
  "falso_y_cierto",  AND(FALSE(), TRUE()),
  "blanco_y_blanco", AND(BLANK(), BLANK()),
  "cero_y_cierto",   AND(0, TRUE())
)
```

```result
blanco_y_cierto | falso_y_cierto | blanco_y_blanco | cero_y_cierto
False | False | False | False
```

If you need to tell "not applicable" from "no", `AND` is not the tool: an explicit `ISBLANK` has
to come first.

## 3. With numbers it does not compare, it converts

Any non-zero value is true. An `AND` over numeric columns is not comparing magnitudes: it is
asking whether they are different from zero.

```dax
EVALUATE
ROW(
  "dos_positivos",   AND(5, 3),
  "uno_negativo",    AND(-1, 1),
  "con_cero",        AND(5, 0),
  "decimal_pequeno", AND(0.0001, 1)
)
```

```result
dos_positivos | uno_negativo | con_cero | decimal_pequeno
True | True | False | True
```

See [`or`](./or.md), which has exactly the same three traps.
