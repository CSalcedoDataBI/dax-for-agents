---
function: ISNUMBER
model: ninguno
---

# ISNUMBER — examples

## 1. A DATE is also a number

It is the result that breaks type classifications written carelessly. Internally a date is a
serial number, and `ISNUMBER` sees it.

```dax
EVALUATE
ROW(
  "entero", ISNUMBER(42),
  "decimal", ISNUMBER(1.5),
  "moneda", ISNUMBER(CURRENCY(1.5)),
  "fecha", ISNUMBER(DATE(2024, 1, 1)),
  "fecha_tambien_es_fecha", ISDATETIME(DATE(2024, 1, 1))
)
```

```result
entero | decimal | moneda | fecha | fecha_tambien_es_fecha
True | True | True | True | True
```

If you order a ladder of `IF(ISNUMBER(x), ..., IF(ISDATETIME(x), ...))`, dates never reach the
second branch. Ask [`isdatetime`](./isdatetime.md) first.

## 2. A number written as text is NOT a number

```dax
EVALUATE
ROW(
  "numero", ISNUMBER(42),
  "texto_que_parece_numero", ISNUMBER("42"),
  "booleano", ISNUMBER(TRUE),
  "blanco", ISNUMBER(BLANK())
)
```

```result
numero | texto_que_parece_numero | booleano | blanco
True | False | False | False
```

`ISNUMBER("42")` is **false** even though `ABS("42")` works: the implicit conversion happens when
operating, not when asking about the type. And a boolean does not count as a number either, even
though it adds up as 0 and 1.

## 3. `ISNUMERIC` is documented as its alias and is NOT one

```dax
EVALUATE
ROW(
  "entero", ISNUMBER(42) = ISNUMERIC(42),
  "texto", ISNUMBER("42") = ISNUMERIC("42"),
  "moneda", ISNUMBER(CURRENCY(2)) = ISNUMERIC(CURRENCY(2)),
  "fecha", ISNUMBER(DATE(2024,1,1)) = ISNUMERIC(DATE(2024,1,1)),
  "fecha_con_isnumeric", ISNUMERIC(DATE(2024,1,1))
)
```

```result
entero | texto | moneda | fecha | fecha_con_isnumeric
True | True | True | False | False
```

The first three columns compare the two functions and they agree. The fourth says that on a
**date they do not**: `ISNUMBER` accepts it and [`isnumeric`](./isnumeric.md) rejects it. The
disagreement is confined to `datetime` values, and swapping one for the other in a model with
dates changes the result.

See [`isnumeric`](./isnumeric.md), [`isdatetime`](./isdatetime.md) and [`istext`](./istext.md).
