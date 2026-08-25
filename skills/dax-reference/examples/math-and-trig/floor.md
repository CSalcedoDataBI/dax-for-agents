---
function: FLOOR
model: ninguno
---

# FLOOR — ejemplos

## 1. Va hacia menos infinito, así que con negativos se ALEJA del cero

El espejo de [`ceiling`](./ceiling.md). Con un negativo, `FLOOR` baja — al contrario que
[`rounddown`](./rounddown.md), que corta hacia cero.

```dax
EVALUATE
ROW(
  "positivo",   FLOOR(2.9, 1),
  "negativo",   FLOOR(-2.1, 1),
  "rounddown",  ROUNDDOWN(-2.1, 0),
  "int",        INT(-2.1)
)
```

```result
positivo | negativo | rounddown | int
2 | -3 | -2 | -3
```

`FLOOR(x, 1)` e `INT(x)` coinciden; `ROUNDDOWN` no. Tres funciones, dos comportamientos.

## 2. Con significancia, agrupa en tramos por abajo

El uso real: meter un valor en su escalón.

```dax
EVALUATE
ROW(
  "a_medios",     FLOOR(2.3, 0.5),
  "a_centenas",   FLOOR(1234, 100),
  "a_cuartos",    FLOOR(0.37, 0.25),
  "ya_en_tramo",  FLOOR(6, 3)
)
```

```result
a_medios | a_centenas | a_cuartos | ya_en_tramo
2 | 1200 | 0.25 | 6
```

## 3. Significancia cero: aquí SÍ aborta, y sus hermanas no

Es la asimetría que no está documentada en ningún sitio. Con múltiplo cero,
[`ceiling`](./ceiling.md) y [`mround`](./mround.md) devuelven 0; `FLOOR` lanza división por
cero. Tres funciones de la misma familia, dos comportamientos distintos ante el mismo dato
malo.

```dax
EVALUATE ROW("sig_cero", FLOOR(5, 0))
```

```result
ERROR: Division by zero has occurred when evaluating function 'FLOOR'.
```

Lo demás se comporta como el resto de la familia:

```dax
EVALUATE
ROW(
  "blanco",    FLOOR(BLANK(), 1),
  "es_blanco", ISBLANK(FLOOR(BLANK(), 1)),
  "cero",      FLOOR(0, 1)
)
```

```result
blanco | es_blanco | cero
(blank) | True | 0
```

Ver [`mround`](./mround.md), que redondea al múltiplo **más cercano** en vez de siempre hacia
un lado — y que aborta cuando los signos no coinciden.
