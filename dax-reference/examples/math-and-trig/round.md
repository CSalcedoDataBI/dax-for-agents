---
function: ROUND
model: ninguno
---

# ROUND — ejemplos

## 1. El medio se va SIEMPRE hacia afuera, no al par

DAX no usa redondeo bancario. `2.5` sube a 3 y `3.5` sube a 4 — los dos se alejan del cero. Si
vienes de Python, de R o de SQL Server con `ROUND` bancario, esta es la diferencia que hace
que los totales no cuadren entre sistemas.

```dax
EVALUATE
ROW(
  "dos_y_medio",  ROUND(2.5, 0),
  "tres_y_medio", ROUND(3.5, 0),
  "negativo",     ROUND(-2.5, 0),
  "menos_medio",  ROUND(-0.5, 0)
)
```

```result
dos_y_medio | tres_y_medio | negativo | menos_medio
3 | 4 | -3 | -1
```

Con redondeo al par, `2.5` daría 2 y `3.5` daría 4. Aquí dan 3 y 4.

## 2. Decimales negativos redondean a la izquierda de la coma

Poco conocido y útil para agrupar magnitudes sin dividir.

```dax
EVALUATE
ROW(
  "dos_decimales", ROUND(1234.5678, 2),
  "a_decenas",     ROUND(1234.5678, -1),
  "a_millares",    ROUND(1234.5678, -3),
  "mas_alla",      ROUND(1234.5678, -9)
)
```

```result
dos_decimales | a_decenas | a_millares | mas_alla
1234.57 | 1230 | 1000 | 0
```

Redondear más allá de la magnitud del número da cero, no error.

## 3. Con blanco devuelve blanco, y no cero

Así que un `ROUND` sobre una columna con huecos no los rellena — que es lo correcto, y a la vez
la razón por la que el resultado sigue desapareciendo del visual.

```dax
EVALUATE
ROW(
  "blanco",    ROUND(BLANK(), 2),
  "es_blanco", ISBLANK(ROUND(BLANK(), 2)),
  "cero",      ROUND(0, 2),
  "ya_entero", ROUND(42, 2)
)
```

```result
blanco | es_blanco | cero | ya_entero
(blank) | True | 0 | 42
```

Ver [`rounddown`](./rounddown.md) y [`roundup`](./roundup.md), que **no** son «hacia abajo» y
«hacia arriba» en el sentido que parece, y [`int`](./int.md), que sí lo es.
