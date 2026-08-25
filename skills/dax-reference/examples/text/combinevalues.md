---
function: COMBINEVALUES
model: ninguno
---

# COMBINEVALUES — examples

## 1. It exists for composite keys, and it does not check for collisions

It joins values with a delimiter so two tables can be related on more than one column. What it
does **not** do is make sure the delimiter does not appear inside the values — and there two
different rows produce the same key.

```dax
EVALUATE
ROW(
  "normal",     COMBINEVALUES("-", "ES", "2024"),
  "colision_a", COMBINEVALUES("-", "ES-2", "024"),
  "colision_b", COMBINEVALUES("-", "ES", "2-024"),
  "iguales",    COMBINEVALUES("-", "ES-2", "024") = COMBINEVALUES("-", "ES", "2-024")
)
```

```result
normal | colision_a | colision_b | iguales
ES-2024 | ES-2-024 | ES-2-024 | True
```

Two **different** pairs of values give the same key. The relationship joins them as if they were
the same, and there is no error: there are extra rows.

That is why the delimiter has to be a character the data cannot contain. And here comes the
restriction that is not in the signature: **it has to be a literal constant**. It cannot be
computed, so the obvious route — `UNICHAR(31)`, a control character no data carries — is closed:

```dax
EVALUATE ROW("delimitador_calculado", COMBINEVALUES(UNICHAR(31), "a", "b"))
```

```result
ERROR: The delimiter value in the 'COMBINEVALUES' function can only be a constant non empty string.
```

That leaves writing it literally, with a sequence odd enough. `raro` comes out **false**: with
`||#||` the two pairs of values stop producing the same key, which was the problem.

```dax
EVALUATE
ROW(
  "raro",     COMBINEVALUES("||#||", "ES-2", "024") = COMBINEVALUES("||#||", "ES", "2-024"),
  "resultado", COMBINEVALUES("||#||", "ES", "2024")
)
```

```result
raro | resultado
False | ES||#||2024
```

## 2. It accepts more than two values, and converts anything that is not text

```dax
EVALUATE
ROW(
  "tres",     COMBINEVALUES("|", "a", "b", "c"),
  "con_numero", COMBINEVALUES("|", "ES", 2024),
  "decimal",  COMBINEVALUES("|", "x", 1.5),
  "booleano", COMBINEVALUES("|", "x", TRUE())
)
```

```result
tres | con_numero | decimal | booleano
a|b|c | ES|2024 | x|1,5 | x|TRUE
```

The conversion uses the model's culture, so a key built with a decimal **is not portable** between
models with different regional settings.

## 3. With blanks

```dax
EVALUATE
ROW(
  "blanco_en_medio", COMBINEVALUES("-", "a", BLANK(), "c"),
  "blanco_al_final", COMBINEVALUES("-", "a", BLANK()),
  "todos_blancos",   COMBINEVALUES("-", BLANK(), BLANK()),
  "es_blanco",       ISBLANK(COMBINEVALUES("-", BLANK(), BLANK()))
)
```

```result
blanco_en_medio | blanco_al_final | todos_blancos | es_blanco
a--c | a- | - | False
```

The delimiter is written anyway, so a blank leaves a visible gap in the key — which, for once, is
good: a collision with a genuinely empty value is visible.
