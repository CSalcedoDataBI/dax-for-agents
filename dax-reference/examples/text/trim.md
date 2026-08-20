---
function: TRIM
model: ninguno
---

# TRIM — ejemplos

## 1. Quita los espacios de sobra, no todos

Deja **un** espacio entre palabras y elimina los de los extremos. No es «quitar espacios»:
es «normalizar el espaciado».

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

## 2. NO quita el espacio duro, y eso es lo que rompe los cruces

`TRIM` solo trata el espacio ASCII (código 32). El **espacio de no separación** (código 160)
sobrevive intacto — y es exactamente el que llega pegado a los datos que vienen de una web,
de Excel o de un copiar-pegar.

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

El texto **parece** limpio en el visual y no cruza con `"hola"`. Para quitarlo hace falta
nombrarlo: `SUBSTITUTE(texto, UNICHAR(160), " ")` antes del `TRIM`.

## 3. Tampoco quita tabuladores ni saltos de línea

Mismo problema, otros códigos. Un `TRIM` no deja el texto en una sola línea.

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

Ver [`substitute`](./substitute.md), que es con lo que se limpian de verdad.
