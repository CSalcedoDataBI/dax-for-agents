---
function: ROUNDUP
model: ninguno
---

# ROUNDUP — ejemplos

## 1. «Arriba» significa ALEJÁNDOSE DE CERO

El espejo de [`rounddown`](./rounddown.md), con la misma confusión al revés:
`ROUNDUP(-2.1)` es `-3`, no `-2`. Un negativo se hace **más negativo**.

```dax
EVALUATE
ROW(
  "positivo",  ROUNDUP(2.1, 0),
  "negativo",  ROUNDUP(-2.1, 0),
  "ceiling",   CEILING(-2.1, 1),
  "iso",       ISO.CEILING(-2.1, 1)
)
```

```result
positivo | negativo | ceiling | iso
3 | -3 | -2 | -2
```

`CEILING` con significancia positiva sí va hacia más infinito, así que da `-2`. Las dos
funciones que suenan a «hacia arriba» no coinciden en los negativos.

## 2. Cualquier resto sube, por pequeño que sea

Es lo que se quiere para calcular cajas, licencias o lotes: sobra un poco, hace falta uno más.

```dax
EVALUATE
ROW(
  "justo",       ROUNDUP(2.0, 0),
  "un_pelin",    ROUNDUP(2.0001, 0),
  "cajas_de_12", ROUNDUP(DIVIDE(25, 12), 0),
  "dos_dec",     ROUNDUP(2.001, 2)
)
```

```result
justo | un_pelin | cajas_de_12 | dos_dec
2 | 3 | 3 | 2.01
```

## 3. Decimales negativos, y el blanco

```dax
EVALUATE
ROW(
  "a_decenas",  ROUNDUP(1001, -1),
  "a_millares", ROUNDUP(1001, -3),
  "blanco",     ROUNDUP(BLANK(), 2),
  "es_blanco",  ISBLANK(ROUNDUP(BLANK(), 2))
)
```

```result
a_decenas | a_millares | blanco | es_blanco
1010 | 2000 | (blank) | True
```
