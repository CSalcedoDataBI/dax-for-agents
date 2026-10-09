---
function: NOT
model: ninguno
---

# NOT — examples

## 1. NOT of a blank is TRUE

It is the trap that turns a "anything that is not X" filter into "anything that is not X, plus
everything with no data". The blank converts to `FALSE`, and its negation is `TRUE`.

```dax
EVALUATE
ROW(
  "not_blanco", NOT(BLANK()),
  "not_falso",  NOT(FALSE()),
  "not_cierto", NOT(TRUE()),
  "not_cero",   NOT(0)
)
```

```result
not_blanco | not_falso | not_cierto | not_cero
True | True | False | True
```

A row with no data passes the filter. If that is not what you want, you need
`NOT(...) && NOT(ISBLANK(...))`.

## 2. With numbers, anything different from zero is true

```dax
EVALUATE
ROW(
  "not_uno",      NOT(1),
  "not_cien",     NOT(100),
  "not_negativo", NOT(-5),
  "not_decimal",  NOT(0.5)
)
```

```result
not_uno | not_cien | not_negativo | not_decimal
False | False | False | False
```

The sign does not matter: only whether it is zero.

## 3. Negating a comparison is not inverting it

With blanks in play, `NOT(a > b)` and `a <= b` stop behaving the way algebra suggests, because
comparison against a blank is not the one you have in mind.

```dax
EVALUATE
ROW(
  "blanco_mayor_cero",     BLANK() > 0,
  "not_blanco_mayor_cero", NOT(BLANK() > 0),
  "blanco_menor_igual",    BLANK() <= 0,
  "blanco_igual_cero",     BLANK() = 0
)
```

```result
blanco_mayor_cero | not_blanco_mayor_cero | blanco_menor_igual | blanco_igual_cero
False | True | True | True
```
