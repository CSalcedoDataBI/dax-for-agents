---
function: UNICODE
model: ninguno
---

# UNICODE — examples

## 1. It only looks at the FIRST character

It is not "the text's code": it is the first one's and nothing more. It is for auditing what sits
at the start of a string, not for comparing strings.

```dax
EVALUATE
ROW(
  "una_letra",    UNICODE("A"),
  "una_palabra",  UNICODE("Abc"),
  "otra_palabra", UNICODE("Azz"),
  "iguales",      UNICODE("Abc") = UNICODE("Azz")
)
```

```result
una_letra | una_palabra | otra_palabra | iguales
65 | 65 | 65 | True
```

## 2. What it is really for: seeing the invisible character

When two texts look the same and do not join, this says so in one line.

```dax
EVALUATE
VAR Sucio = "hola" & UNICHAR(160)
RETURN
ROW(
  "ultimo_de_sucio",  UNICODE(RIGHT(Sucio, 1)),
  "ultimo_de_limpio", UNICODE(RIGHT("hola ", 1)),
  "tras_trim",        UNICODE(RIGHT(TRIM(Sucio), 1)),
  "esperado_a",       UNICODE("a")
)
```

```result
ultimo_de_sucio | ultimo_de_limpio | tras_trim | esperado_a
160 | 32 | 160 | 97
```

160 against 32: the first is the non-breaking space [`trim`](./trim.md) does not remove, the
second the ordinary space. And `tras_trim` is still 160, which is the demonstration in a single
cell.

## 3. With a blank and with an empty string it returns BLANK, not an error

It is the opposite of [`value`](./value.md), which aborts on the empty string. Here there is
nothing to guard — but neither can you tell "there was no text" from "the first character is odd"
without looking first.

```dax
EVALUATE
ROW(
  "numero",       UNICODE("5"),
  "acentuada",    UNICODE("é"),
  "enye",         UNICODE("ñ"),
  "cadena_vacia", UNICODE(""),
  "blanco",       UNICODE(BLANK())
)
```

```result
numero | acentuada | enye | cadena_vacia | blanco
53 | 233 | 241 | (blank) | (blank)
```

Where it does abort is on half a surrogate pair — the half of an emoji cut with `LEFT`. See
[`unichar`](./unichar.md), which is the way back and where that case lives.
