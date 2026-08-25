---
function: INT
model: ninguno
---

# INT — ejemplos

## 1. Es el ÚNICO que va hacia menos infinito

De toda la familia, `INT` es el que hace suelo de verdad. `TRUNC` y `ROUNDDOWN` cortan hacia
cero. Con positivos los tres coinciden; con negativos, `INT` se separa.

```dax
EVALUATE
ROW(
  "int_positivo", INT(2.7),
  "int_negativo", INT(-2.7),
  "trunc",        TRUNC(-2.7),
  "rounddown",    ROUNDDOWN(-2.7, 0)
)
```

```result
int_positivo | int_negativo | trunc | rounddown
2 | -3 | -2 | -2
```

Si estás repartiendo importes negativos —devoluciones, ajustes— elegir mal aquí descuadra el
total en una unidad por fila.

## 2. Sin decimales, no toca nada

```dax
EVALUATE
ROW(
  "entero",      INT(42),
  "negativo_ent", INT(-42),
  "casi_entero", INT(2.9999999),
  "justo_medio", INT(-0.5)
)
```

```result
entero | negativo_ent | casi_entero | justo_medio
42 | -42 | 2 | -1
```

`INT(-0.5)` es `-1`: cualquier parte decimal en un negativo baja un entero.

## 3. Con blanco y con cero

```dax
EVALUATE
ROW(
  "blanco",    INT(BLANK()),
  "es_blanco", ISBLANK(INT(BLANK())),
  "cero",      INT(0),
  "cero_neg",  INT(-0.0)
)
```

```result
blanco | es_blanco | cero | cero_neg
(blank) | True | 0 | 0
```

Ver [`trunc`](./trunc.md) para la versión que corta hacia cero, y
[`quotient`](./quotient.md) para la división entera, que tiene la misma decisión dentro.
