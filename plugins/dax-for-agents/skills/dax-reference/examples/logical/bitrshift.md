---
function: BITRSHIFT
model: ninguno
---

# BITRSHIFT — examples

## 1. Shifting right is dividing by two, and it TRUNCATES

It does not round. The bits falling off the right are lost, so the operation is not reversible:
shifting right and back left does not return the original number.

```dax
EVALUATE
ROW(
  "diez_entre_2",     BITRSHIFT(10, 1),
  "once_entre_2",     BITRSHIFT(11, 1),
  "ida_y_vuelta",     BITLSHIFT(BITRSHIFT(11, 1), 1),
  "uno_entre_2",      BITRSHIFT(1, 1)
)
```

```result
diez_entre_2 | once_entre_2 | ida_y_vuelta | uno_entre_2
5 | 5 | 10 | 0
```

`11 >> 1` gives 5, and shifting back left gives 10: the lost bit does not come back.

## 2. Reading a field packed inside a number

The real use: several values packed into a single integer. You shift to bring the field down and
mask it with [`bitand`](./bitand.md) to keep only that one.

```dax
EVALUATE
VAR Empaquetado = 5 * 256 + 3 * 16 + 7
RETURN
ROW(
  "valor",       Empaquetado,
  "campo_bajo",  BITAND(Empaquetado, 15),
  "campo_medio", BITAND(BITRSHIFT(Empaquetado, 4), 15),
  "campo_alto",  BITRSHIFT(Empaquetado, 8)
)
```

```result
valor | campo_bajo | campo_medio | campo_alto
1335 | 7 | 3 | 5
```

## 3. With negatives the sign is dragged along

A zero does not come in from the left: the sign bit does. A negative shifted right stays negative
however far it is shifted, and tends towards `-1` rather than `0`.

```dax
EVALUATE
ROW(
  "menos_ocho_1",  BITRSHIFT(-8, 1),
  "menos_ocho_3",  BITRSHIFT(-8, 3),
  "menos_ocho_10", BITRSHIFT(-8, 10),
  "menos_uno_5",   BITRSHIFT(-1, 5)
)
```

```result
menos_ocho_1 | menos_ocho_3 | menos_ocho_10 | menos_uno_5
-4 | -1 | -1 | -1
```
