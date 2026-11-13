---
function: BITXOR
model: ninguno
---

# BITXOR — examples

## 1. It toggles the flag: on if it was off and the other way round

That is what distinguishes `BITXOR` from [`bitor`](./bitor.md), which only turns on.

```dax
EVALUATE
VAR Permisos = 5
RETURN
ROW(
  "valor",          Permisos,
  "cambia_el_1",    BITXOR(Permisos, 1),
  "cambia_el_2",    BITXOR(Permisos, 2),
  "cambia_dos_veces", BITXOR(BITXOR(Permisos, 1), 1)
)
```

```result
valor | cambia_el_1 | cambia_el_2 | cambia_dos_veces
5 | 4 | 7 | 5
```

Applying it twice returns the original value. That property is what makes it useful for toggling
a state, and also what makes it dangerous if it runs twice by accident.

## 2. With itself it always gives zero

Hence the classic trick for comparing two numbers: if the `BITXOR` is zero, they are identical bit
for bit.

```dax
EVALUATE
ROW(
  "consigo_mismo",   BITXOR(12345, 12345),
  "con_cero",        BITXOR(12345, 0),
  "difieren_en_uno", BITXOR(12, 13),
  "negativos",       BITXOR(-5, -5)
)
```

```result
consigo_mismo | con_cero | difieren_en_uno | negativos
0 | 12345 | 1 | 0
```

## 3. With different signs the result is negative

The sign bit is operated on too, so `BITXOR` of a positive and a negative comes out negative. A
calculation assuming the result is a positive mask breaks here.

```dax
EVALUATE
ROW(
  "positivo_negativo", BITXOR(5, -1),
  "negativo_negativo", BITXOR(-5, -3),
  "positivo_positivo", BITXOR(5, 3),
  "menos_uno_cero",    BITXOR(-1, 0)
)
```

```result
positivo_negativo | negativo_negativo | positivo_positivo | menos_uno_cero
-6 | 6 | 6 | -1
```
