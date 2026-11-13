---
function: CONVERT
model: ninguno
---

# CONVERT — examples

## 1. Converting text to a number is governed by the model's CULTURE, not by DAX syntax

This is the one that bites. A literal `1.5` written in DAX is always one and a half; the
**string** `"1.5"` depends on the model's language. These results are from an **es-ES** model.

```dax
EVALUATE
ROW(
  "literal_dax", 1.5,
  "cadena_con_punto", CONVERT("1.5", DOUBLE),
  "cadena_con_coma", CONVERT("1,5", DOUBLE),
  "con_separador_de_miles", CONVERT("1.234,5", DOUBLE)
)
```

```result
literal_dax | cadena_con_punto | cadena_con_coma | con_separador_de_miles
1.5 | 15 | 1.5 | 1234.5
```

`CONVERT("1.5", DOUBLE)` returns **15**, not 1.5: the dot is read as a thousands separator. No
error, no warning — just a number ten times bigger. That same model, with an English culture,
would give 1.5, so the formula is correct or incorrect depending on where it is opened.

## 2. To an integer it ROUNDS, it does not truncate — the opposite of `INT`

```dax
EVALUATE
ROW(
  "convert_1_9", CONVERT(1.9, INTEGER),
  "int_1_9", INT(1.9),
  "convert_menos_1_9", CONVERT(-1.9, INTEGER),
  "int_menos_1_9", INT(-1.9),
  "trunc_menos_1_9", TRUNC(-1.9)
)
```

```result
convert_1_9 | int_1_9 | convert_menos_1_9 | int_menos_1_9 | trunc_menos_1_9
2 | 1 | -2 | -2 | -1
```

Three functions and three different results for -1.9. `CONVERT` rounds, [`int`](./int.md) always
goes down, and `TRUNC` goes towards zero. Choosing out of habit means choosing wrong two times
out of three.

## 3. The types it accepts, and what it does with a blank

```dax
EVALUATE
ROW(
  "a_double", CONVERT("123", DOUBLE),
  "a_entero", CONVERT("123", INTEGER),
  "a_booleano", CONVERT(1, BOOLEAN),
  "cero_a_booleano", CONVERT(0, BOOLEAN),
  "blanco_a_entero", CONVERT(BLANK(), INTEGER),
  "sigue_en_blanco", ISBLANK(CONVERT(BLANK(), INTEGER))
)
```

```result
a_double | a_entero | a_booleano | cero_a_booleano | blanco_a_entero | sigue_en_blanco
123 | 123 | True | False | (blank) | True
```

The blank **stays blank**: `CONVERT` forces the type but does not invent a value. Worth knowing
because intuition says otherwise — an integer "cannot be empty" — and because
[`randbetween`](./randbetween.md), given two blanks, does return a 0.

See [`currency`](./currency.md), [`int`](./int.md) and [`value`](../text/value.md).
