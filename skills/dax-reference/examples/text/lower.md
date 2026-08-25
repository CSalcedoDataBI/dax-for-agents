---
function: LOWER
model: ninguno
---

# LOWER — ejemplos

## 1. Como en UPPER, comparar con ella no aporta nada

`=` ya ignora las mayúsculas. Un `LOWER` a los dos lados es ruido que además esconde esa
propiedad al siguiente que lea el código.

```dax
EVALUATE
ROW(
  "sin_lower", "SONY" = "sony",
  "con_lower", LOWER("SONY") = LOWER("sony"),
  "exact",     EXACT("SONY", "sony")
)
```

```result
sin_lower | con_lower | exact
True | True | False
```

## 2. Donde sí sirve: normalizar antes de agrupar o de construir una clave

Aquí el objetivo no es comparar, es que dos escrituras distintas produzcan **el mismo texto**.

```dax
EVALUATE
ROW(
  "clave_1",    LOWER(TRIM("  Sony  ")),
  "clave_2",    LOWER(TRIM("SONY")),
  "coinciden",  EXACT(LOWER(TRIM("  Sony  ")), LOWER(TRIM("SONY"))),
  "con_duro",   EXACT(LOWER(TRIM("Sony" & UNICHAR(160))), "sony")
)
```

```result
clave_1 | clave_2 | coinciden | con_duro
sony | sony | True | False
```

El último recuerda que `TRIM` no quita el espacio duro: la clave sale distinta y el grupo se
parte en dos. Ver [`trim`](./trim.md) y [`substitute`](./substitute.md).

## 3. Con blanco, números y signos

```dax
EVALUATE
ROW(
  "blanco",      "[" & LOWER(BLANK()) & "]",
  "es_blanco",   ISBLANK(LOWER(BLANK())),
  "con_numeros", LOWER("ABC-123"),
  "acentos",     LOWER("CAFÉ AÑO")
)
```

```result
blanco | es_blanco | con_numeros | acentos
[] | True | abc-123 | café año
```
