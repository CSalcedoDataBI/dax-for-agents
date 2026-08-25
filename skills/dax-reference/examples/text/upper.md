---
function: UPPER
model: ninguno
---

# UPPER — examples

## 1. It is no use for comparing, because `=` already ignores case

The `UPPER(a) = UPPER(b)` pattern comes from languages where comparison is case-sensitive. In DAX
it is not needed — and worse, it **hides** the fact that the comparison never was.

```dax
EVALUATE
ROW(
  "sin_upper",   "Sony" = "sony",
  "con_upper",   UPPER("Sony") = UPPER("sony"),
  "exact",       EXACT("Sony", "sony"),
  "exact_upper", EXACT(UPPER("Sony"), UPPER("sony"))
)
```

```result
sin_upper | con_upper | exact | exact_upper
True | True | False | True
```

If you really do want to distinguish, the function is [`exact`](./exact.md). If not, the `UPPER`
is redundant.

## 2. Numbers and signs pass straight through — and so does one letter

That it leaves numbers and signs alone was expected. What was not: the German **ß** comes out
unconverted, because its uppercase is two letters (`SS`) and `UPPER` does not change the text's
length. A normaliser assuming "everything to uppercase" leaves that row out of the group.

```dax
EVALUATE
ROW(
  "con_numeros", UPPER("abc-123"),
  "con_acentos", UPPER("café año"),
  "ya_mayuscula", UPPER("YA ESTÁ"),
  "eszett",      UPPER("straße")
)
```

```result
con_numeros | con_acentos | ya_mayuscula | eszett
ABC-123 | CAFÉ AÑO | YA ESTÁ | STRAßE
```

## 3. With a blank and with numbers

```dax
EVALUATE
ROW(
  "blanco",     "[" & UPPER(BLANK()) & "]",
  "es_blanco",  ISBLANK(UPPER(BLANK())),
  "numero",     UPPER(1.5),
  "longitud",   LEN(UPPER("café")) = LEN("café")
)
```

```result
blanco | es_blanco | numero | longitud
[] | True | 1,5 | True
```

That the length is preserved is **not guaranteed in general** — there are letters whose uppercase
takes two — which is why it is worth checking before cutting by position over the result.

See [`lower`](./lower.md), which has the same three.
