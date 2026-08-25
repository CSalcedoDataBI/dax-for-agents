---
function: TRIM
model: ninguno
---

# TRIM — examples

## 1. It removes the surplus spaces, not all of them

It leaves **one** space between words and removes the ones at the ends. It is not "remove
spaces": it is "normalise the spacing".

```dax
EVALUATE
ROW(
  "extremos",   "[" & TRIM("   hola   ") & "]",
  "en_medio",   TRIM("hola     mundo"),
  "mezcla",     TRIM("  hola     mundo   "),
  "solo_espacios", "[" & TRIM("      ") & "]"
)
```

```result
extremos | en_medio | mezcla | solo_espacios
[hola] | hola mundo | hola mundo | []
```

## 2. It does NOT remove the non-breaking space, and that is what breaks joins

`TRIM` only handles the ASCII space (code 32). The **non-breaking space** (code 160) survives
intact — and it is exactly the one that arrives stuck to data coming from a web page, from Excel
or from a copy-paste.

```dax
EVALUATE
VAR ConDuro = "hola" & UNICHAR(160)
RETURN
ROW(
  "longitud_original",   LEN(ConDuro),
  "longitud_tras_trim",  LEN(TRIM(ConDuro)),
  "igual_a_hola",        TRIM(ConDuro) = "hola",
  "codigo_del_sobrante", UNICODE(RIGHT(TRIM(ConDuro), 1))
)
```

```result
longitud_original | longitud_tras_trim | igual_a_hola | codigo_del_sobrante
5 | 5 | False | 160
```

The text **looks** clean in the visual and does not join with `"hola"`. To remove it you have to
name it: `SUBSTITUTE(text, UNICHAR(160), " ")` before the `TRIM`.

## 3. It does not remove tabs or line breaks either

Same problem, other codes. A `TRIM` does not put the text on a single line.

```dax
EVALUATE
VAR ConTab = "hola" & UNICHAR(9) & "mundo"
VAR ConSalto = "hola" & UNICHAR(10) & "mundo"
RETURN
ROW(
  "tab_longitud",   LEN(TRIM(ConTab)),
  "salto_longitud", LEN(TRIM(ConSalto)),
  "tab_sigue",      UNICODE(MID(TRIM(ConTab), 5, 1)),
  "salto_sigue",    UNICODE(MID(TRIM(ConSalto), 5, 1))
)
```

```result
tab_longitud | salto_longitud | tab_sigue | salto_sigue
10 | 10 | 9 | 10
```

See [`substitute`](./substitute.md), which is what actually cleans them out.
