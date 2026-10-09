---
function: ISDATETIME
model: ninguno
---

# ISDATETIME — examples

## 1. A date is a date AND a number at the same time

That overlap is what breaks type classifications written in the wrong order.

```dax
EVALUATE
ROW(
  "fecha_es_fecha", ISDATETIME(DATE(2024, 1, 1)),
  "fecha_es_numero", ISNUMBER(DATE(2024, 1, 1)),
  "numero_es_fecha", ISDATETIME(45000),
  "numero_es_numero", ISNUMBER(45000)
)
```

```result
fecha_es_fecha | fecha_es_numero | numero_es_fecha | numero_es_numero
True | True | False | True
```

The asymmetry is the key: a date passes as a number, but a number does **not** pass as a date
even when it is a valid serial number. The type belongs to the value, not to its magnitude. In a
ladder of `IF`s, `ISDATETIME` has to come **before** [`isnumber`](./isnumber.md).

## 2. A date written as text is not a date

```dax
EVALUATE
ROW(
  "fecha", ISDATETIME(DATE(2024, 1, 1)),
  "texto_con_pinta_de_fecha", ISDATETIME("2024-01-01"),
  "es_texto", ISTEXT("2024-01-01"),
  "hora_tambien_cuenta", ISDATETIME(TIME(12, 30, 0))
)
```

```result
fecha | texto_con_pinta_de_fecha | es_texto | hora_tambien_cuenta
True | False | True | True
```

It is the same pattern as `ISNUMBER("42")`. And a time with no date counts too: the type is
`datetime`, not "date".

## 3. The blank has no type, here either

```dax
EVALUATE
ROW(
  "blanco", ISDATETIME(BLANK()),
  "blanco_es_blanco", ISBLANK(BLANK()),
  "fecha_cero", ISDATETIME(DATE(1899, 12, 30)),
  "booleano", ISDATETIME(TRUE)
)
```

```result
blanco | blanco_es_blanco | fecha_cero | booleano
False | True | True | False
```

1899-12-30 is DAX's calendar origin and is still a perfectly valid date — what is not a date is
the blank. For date columns with gaps, the question goes to [`isblank`](./isblank.md).

See [`isnumber`](./isnumber.md) and [`isblank`](./isblank.md).
