---
function: ISNUMERIC
model: ninguno
---

# ISNUMERIC — examples

## 1. It is NOT an exact alias of `ISNUMBER`: they differ on dates

The documentation declares them aliases. Measured, they are not. A date is a number to `ISNUMBER`
and **is not** one to `ISNUMERIC`.

```dax
EVALUATE
ROW(
  "fecha_isnumber", ISNUMBER(DATE(2024, 1, 1)),
  "fecha_isnumeric", ISNUMERIC(DATE(2024, 1, 1)),
  "hora_isnumber", ISNUMBER(TIME(12, 0, 0)),
  "hora_isnumeric", ISNUMERIC(TIME(12, 0, 0))
)
```

```result
fecha_isnumber | fecha_isnumeric | hora_isnumber | hora_isnumeric
True | False | True | False
```

Swapping one for the other in a model that handles dates changes the result. It is not a matter
of style.

## 2. On everything else they do agree

The disagreement is confined to `datetime` values, and only to those.

```dax
EVALUATE
ROW(
  "entero", ISNUMERIC(42) = ISNUMBER(42),
  "decimal", ISNUMERIC(1.5) = ISNUMBER(1.5),
  "moneda", ISNUMERIC(CURRENCY(2)) = ISNUMBER(CURRENCY(2)),
  "texto", ISNUMERIC("42") = ISNUMBER("42"),
  "blanco", ISNUMERIC(BLANK()) = ISNUMBER(BLANK()),
  "fecha", ISNUMERIC(DATE(2024,1,1)) = ISNUMBER(DATE(2024,1,1))
)
```

```result
entero | decimal | moneda | texto | blanco | fecha
True | True | True | True | True | False
```

Each column compares the two functions on the same value. The first five agree; the sixth is the
only one that does not.

## 3. Which to use, now that it is known to matter

```dax
EVALUATE
ROW(
  "numero", ISNUMERIC(42),
  "texto_numerico", ISNUMERIC("42"),
  "fecha", ISNUMERIC(DATE(2024, 1, 1)),
  "booleano", ISNUMERIC(TRUE),
  "blanco", ISNUMERIC(BLANK())
)
```

```result
numero | texto_numerico | fecha | booleano | blanco
True | False | False | False | False
```

`ISNUMERIC` is the one that answers "a number, and not a date in disguise". If what you want is
to separate dates from quantities, it is the right one and `ISNUMBER` mixes them. If you want the
dates to count, the right one is [`isnumber`](./isnumber.md).

What **neither** answers is "can the engine do arithmetic with this?". `ISNUMBER("42")` is false
and yet `"42" + 1` gives 43: DAX converts when operating, and the type predicate does not know it.
For that question there is no predicate — you have to attempt the operation and guard it.

The [`istext`](./istext.md)/[`isstring`](./isstring.md) pair did turn out identical in every
tested case. Two functions being documented as aliases does not make them so.

See [`isnumber`](./isnumber.md) and [`isdatetime`](./isdatetime.md).
