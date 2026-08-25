---
function: SWITCH
model: ninguno
---

# SWITCH — examples

## 1. With no `else` and no match, it returns blank

Just like `IF`. A `SWITCH` covering five cases that meets the sixth gives neither an error nor a
zero: it disappears from the visual.

```dax
EVALUATE
ROW(
  "coincide",        SWITCH(2, 1, "uno", 2, "dos", 3, "tres"),
  "no_coincide",     SWITCH(9, 1, "uno", 2, "dos", 3, "tres"),
  "es_blanco",       ISBLANK(SWITCH(9, 1, "uno")),
  "con_else",        SWITCH(9, 1, "uno", 2, "dos", "ninguno")
)
```

```result
coincide | no_coincide | es_blanco | con_else
dos | (blank) | True | ninguno
```

## 2. `SWITCH(TRUE(), ...)` is the range pattern

It is how to write a ladder of conditions without nesting five `IF`s. The first one that holds
wins, so **the order matters**: a broad condition placed at the top hides the ones below.

```dax
EVALUATE
VAR Valor = 95
RETURN
ROW(
  "valor",         Valor,
  "bien_ordenado", SWITCH(TRUE(), Valor >= 90, "alto", Valor >= 50, "medio", "bajo"),
  "mal_ordenado",  SWITCH(TRUE(), Valor >= 50, "medio", Valor >= 90, "alto", "bajo"),
  "primera_gana",  SWITCH(TRUE(), TRUE(), "primera", TRUE(), "segunda")
)
```

```result
valor | bien_ordenado | mal_ordenado | primera_gana
95 | alto | medio | primera
```

With 95, `mal_ordenado` returns "medio": the `>= 50` branch comes first and takes everything above
50, so the `>= 90` one is never evaluated. It gives no error — it gives a plausible and wrong
answer, which is worse. With a value between 50 and 90 both forms agree, and that is why this
fault passes testing.

## 3. The blank does NOT match the zero branch

It is the opposite of what an `IF` does, and that is why it surprises: in an `IF` the blank
converts to `FALSE` and follows the `else` branch, but `SWITCH` compares values, and a blank is
not equal to `0` or to `""` for matching purposes. It goes to the `else` without touching any
branch.

```dax
EVALUATE
ROW(
  "cero_con_blanco",  SWITCH(BLANK(), 0, "encontró el cero", "no coincidió"),
  "texto_con_blanco", SWITCH(BLANK(), "", "encontró la cadena vacía", "no coincidió"),
  "cero_con_cero",    SWITCH(0, 0, "encontró el cero", "no coincidió")
)
```

```result
cero_con_blanco | texto_con_blanco | cero_con_cero
no coincidió | no coincidió | encontró el cero
```

So a branch written for zero does **not** capture the rows with no data: they all go to the
`else`, and if there is no `else`, they disappear. Handling them needs a branch of their own with
`ISBLANK`, or a `SWITCH(TRUE(), ...)` where the condition is written out in full.

See [`if`](./if.md) for the same conversions with two branches.
