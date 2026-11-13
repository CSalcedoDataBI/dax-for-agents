---
function: REPT
model: ninguno
---

# REPT — examples

## 1. Zero repetitions gives an empty string, not blank

It matters because the typical use of `REPT` is drawing a bar in a table, and the row with a zero
value has to come out empty without disappearing.

```dax
EVALUATE
ROW(
  "tres",       REPT("*", 3),
  "cero",       "[" & REPT("*", 0) & "]",
  "es_blanco",  ISBLANK(REPT("*", 0)),
  "uno",        REPT("ab", 1)
)
```

```result
tres | cero | es_blanco | uno
*** | [] | False | ab
```

## 2. The number is ROUNDED, not truncated

What matters when the count comes out of a division: `2.5` does not draw 2 bars.

```dax
EVALUATE
ROW(
  "dos_coma_cuatro", LEN(REPT("*", 2.4)),
  "dos_coma_cinco",  LEN(REPT("*", 2.5)),
  "dos_coma_seis",   LEN(REPT("*", 2.6)),
  "casi_uno",        LEN(REPT("*", 0.6))
)
```

```result
dos_coma_cuatro | dos_coma_cinco | dos_coma_seis | casi_uno
2 | 3 | 3 | 1
```

## 3. The real case: a proportional bar inside a table

With the usual trap — if the value can be negative, it aborts.

```dax
EVALUATE
VAR Maximo = 20
RETURN
ROW(
  "barra_de_5",  REPT("█", DIVIDE(5, Maximo) * 10),
  "barra_de_20", REPT("█", DIVIDE(20, Maximo) * 10),
  "barra_de_0",  "[" & REPT("█", DIVIDE(0, Maximo) * 10) & "]"
)
```

```result
barra_de_5 | barra_de_20 | barra_de_0
███ | ██████████ | []
```

```dax
EVALUATE ROW("negativo", REPT("*", -1))
```

```result
ERROR: An argument of function 'REPT' has the wrong data type or has an invalid value.
```

That is why the count goes wrapped in `MAX(0, ...)` when the data can come in below zero.
