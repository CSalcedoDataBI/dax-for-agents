---
function: UPPER
model: ninguno
---

# UPPER — ejemplos

## 1. No sirve para comparar, porque `=` ya ignora mayúsculas

El patrón `UPPER(a) = UPPER(b)` viene de lenguajes donde la comparación distingue. En DAX no
hace falta — y peor, **oculta** que la comparación nunca distinguió.

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

Si de verdad quieres distinguir, la función es [`exact`](./exact.md). Si no, sobra el `UPPER`.

## 2. Números y signos pasan tal cual — y alguna letra, también

Que no toque números ni signos era lo esperado. Lo que no lo era: la **ß** alemana sale sin
convertir, porque su mayúscula son dos letras (`SS`) y `UPPER` no cambia la longitud del
texto. Un normalizador que dé por hecho «todo a mayúsculas» deja esa fila fuera del grupo.

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

## 3. Con blanco y con números

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

Que la longitud se conserve **no está garantizado en general** —hay letras cuya mayúscula
ocupa dos— y por eso conviene comprobarlo antes de cortar por posición sobre el resultado.

Ver [`lower`](./lower.md), que tiene las mismas tres.
