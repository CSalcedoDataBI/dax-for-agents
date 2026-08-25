---
function: COTH
model: ninguno
---

# COTH — ejemplos

## 1. Es 1/TANH, y se aplana en ±1 enseguida

Nada que ver con la cotangente circular de [`cot`](./cot.md): esta no oscila. Tiende a 1 por
arriba y a -1 por abajo, y llega rápido.

```dax
EVALUATE
ROW(
  "coth_1", ROUND(COTH(1), 6),
  "uno_entre_tanh", ROUND(1 / TANH(1), 6),
  "coth_3", ROUND(COTH(3), 6),
  "coth_20", ROUND(COTH(20), 10)
)
```

```result
coth_1 | uno_entre_tanh | coth_3 | coth_20
1.313035 | 1.313035 | 1.00497 | 1
```

En 3 ya está a cinco milésimas de 1, y en 20 es indistinguible de 1 con la precisión que
imprime este informe. Para valores grandes, `COTH(x)` es 1 a efectos prácticos.

## 2. Solo hay un punto prohibido, y es el cero

```dax
EVALUATE ROW("coth_de_cero", COTH(0))
```

```result
ERROR: Division by zero has occurred when evaluating function 'COTH'.
```

A diferencia de [`cot`](./cot.md), que aborta en cada múltiplo de π, aquí el único agujero es
el cero — porque `TANH` solo vale cero ahí. Y el blanco cae en el agujero:

```dax
EVALUATE
ROW(
  "blanco", IFERROR(COTH(BLANK()), "aborta"),
  "cero", IFERROR(COTH(0), "aborta"),
  "casi_cero", ROUND(COTH(0.001), 4),
  "casi_cero_neg", ROUND(COTH(-0.001), 4)
)
```

```result
blanco | cero | casi_cero | casi_cero_neg
aborta | aborta | 1000.0003 | -1000.0003
```

El salto en el cero va de -1000 a +1000. Cualquier hueco en los datos tumba la consulta, y ese
es el caso que llega de verdad.

## 3. Es impar, y nunca vale entre -1 y 1

```dax
EVALUATE
ROW(
  "impar", ROUND(COTH(2) + COTH(-2), 10),
  "coth_2", ROUND(COTH(2), 6),
  "fuera_del_intervalo", ABS(COTH(0.5)) > 1,
  "tanh_dentro", ABS(TANH(0.5)) < 1
)
```

```result
impar | coth_2 | fuera_del_intervalo | tanh_dentro
0 | 1.037315 | True | True
```

`TANH` vive dentro de (-1, 1) y `COTH`, su inverso, vive fuera. Las dos últimas columnas son la
misma afirmación vista desde los dos lados.

Ver [`cot`](./cot.md), [`acoth`](./acoth.md) y [`tanh`](./tanh.md).
