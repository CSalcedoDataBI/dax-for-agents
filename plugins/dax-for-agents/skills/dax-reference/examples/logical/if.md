---
function: IF
model: ninguno
---

# IF — examples

## 1. Without the third argument the result is BLANK, not zero

Leaving out the `else` does not mean "zero". It means **blank**, which is a different thing: it
does not appear in the visual, it does not count in a `COUNT`, and the moment somebody adds zero
to it, it stops being blank.

```dax
EVALUATE
ROW(
  "sin_else",        IF(1 = 2, 10),
  "es_blanco",       ISBLANK(IF(1 = 2, 10)),
  "sin_else_mas_0",  IF(1 = 2, 10) + 0,
  "con_else_cero",   IF(1 = 2, 10, 0)
)
```

```result
sin_else | es_blanco | sin_else_mas_0 | con_else_cero
(blank) | True | 0 | 0
```

`sin_else + 0` and `con_else_cero` give the same thing — and that is precisely the confusion. The
first turns a blank into a zero without saying so; the second decides it.

## 2. A blank condition is FALSE

`IF` does not tell "false" from "no data". A blank takes the `else` branch without warning, so a
column with gaps is classified wholesale as if it were `FALSE`.

```dax
EVALUATE
ROW(
  "condicion_blanca", IF(BLANK(), "rama SI", "rama NO"),
  "condicion_cero",   IF(0, "rama SI", "rama NO"),
  "condicion_uno",    IF(1, "rama SI", "rama NO"),
  "cero_es_falso",    BLANK() = FALSE()
)
```

```result
condicion_blanca | condicion_cero | condicion_uno | cero_es_falso
rama NO | rama NO | rama SI | True
```

Zero is false too, and for the same reason: `IF` converts to boolean, and in DAX both zero and
blank convert to `FALSE`.

## 3. The two branches do not have to return the same type

`IF` can return text down one branch and a number down the other. What comes out is a variant
value, and whoever consumes it afterwards — a comparison, a `SUM`, a format — is the one who gets
the surprise.

```dax
EVALUATE
ROW(
  "rama_numero", IF(1 = 1, 42, "cuarenta y dos"),
  "rama_texto",  IF(1 = 2, 42, "cuarenta y dos"),
  "suma_mixta",  IF(1 = 1, 42, "x") + 1
)
```

```result
rama_numero | rama_texto | suma_mixta
42 | cuarenta y dos | 43
```

See [`coalesce`](./coalesce.md) for the specific "if it is blank, use this other one" case, which
is where an unnecessary `IF` almost always ends up.
