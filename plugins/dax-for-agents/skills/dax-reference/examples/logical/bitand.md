---
function: BITAND
model: ninguno
---

# BITAND — examples

## 1. What it is really for: asking whether a permission is set

The real use of the bit functions is a column where each bit is a flag. `BITAND` with the mask
answers "is this one on?" without taking the number apart.

```dax
EVALUATE
VAR Permisos = 13
RETURN
ROW(
  "valor",          Permisos,
  "tiene_bit_1",    BITAND(Permisos, 1),
  "tiene_bit_2",    BITAND(Permisos, 2),
  "tiene_bit_4",    BITAND(Permisos, 4),
  "tiene_bit_8",    BITAND(Permisos, 8)
)
```

```result
valor | tiene_bit_1 | tiene_bit_2 | tiene_bit_4 | tiene_bit_8
13 | 1 | 0 | 4 | 8
```

13 is `1101` in binary: bits 1, 4 and 8 set, 2 not. The result is **not true or false**, it is the
mask's value or zero — and that is why it has to be compared, not used as it is inside an `IF`.

## 2. With negatives, two's complement comes in

DAX integers are 64-bit signed, so `-1` has every bit set and acts as the identity.

```dax
EVALUATE
ROW(
  "menos_uno_con_5",  BITAND(-1, 5),
  "menos_dos_con_5",  BITAND(-2, 5),
  "negativo_negativo", BITAND(-4, -2),
  "cero_con_todo",    BITAND(0, -1)
)
```

```result
menos_uno_con_5 | menos_dos_con_5 | negativo_negativo | cero_con_todo
5 | 4 | -4 | 0
```

## 3. Decimals are ROUNDED before operating, not truncated

This was written the other way round and the engine corrected it. Intuition says "truncate", the
way bitwise operators do in almost every language. DAX **rounds**: `12.9` goes in as `13`, not as
`12`.

```dax
EVALUATE
ROW(
  "entero",     BITAND(12, 10),
  "decimal",    BITAND(12.9, 10.9),
  "negativo_decimal", BITAND(-12.9, 10),
  "casi_uno",   BITAND(0.9, 1)
)
```

```result
entero | decimal | negativo_decimal | casi_uno
8 | 9 | 2 | 1
```

See [`bitor`](./bitor.md) for turning a flag on and [`bitxor`](./bitxor.md) for toggling it.
