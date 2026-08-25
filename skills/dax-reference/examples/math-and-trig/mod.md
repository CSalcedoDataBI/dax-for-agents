---
function: MOD
model: ninguno
---

# MOD — ejemplos

## 1. El signo lo pone el DIVISOR, no el dividendo

Aquí es donde `MOD` sorprende a quien viene de C, Java, JavaScript o Go, donde el resto se
queda con el signo del dividendo. DAX sigue la convención de Excel: **el resultado tiene el
signo del segundo argumento.**

```dax
EVALUATE
ROW(
  "pos_pos", MOD(10, 3),
  "neg_pos", MOD(-10, 3),
  "pos_neg", MOD(10, -3),
  "neg_neg", MOD(-10, -3)
)
```

```result
pos_pos | neg_pos | pos_neg | neg_neg
1 | 2 | -2 | -1
```

`MOD(-10, 3)` es **2**, no -1. Si estás usando `MOD` para repartir en grupos o para detectar
pares, con dividendos negativos el reparto no es el que crees.

## 2. No cuadra con `QUOTIENT`, y esa es la consecuencia

La identidad `dividendo = divisor × cociente + resto` **se rompe** al mezclar las dos, porque
`QUOTIENT` trunca hacia cero y `MOD` no.

```dax
EVALUATE
ROW(
  "quotient", QUOTIENT(-10, 3),
  "mod", MOD(-10, 3),
  "reconstruido", 3 * QUOTIENT(-10, 3) + MOD(-10, 3),
  "original", -10
)
```

```result
quotient | mod | reconstruido | original
-3 | 2 | -7 | -10
```

Sale **-7** donde debería salir -10. El cociente que sí cuadra con este resto es el de
`INT(-10/3)` = -4, no el de `QUOTIENT`. Escribir las dos juntas y esperar que se cancelen es
un error que no da ningún aviso.

## 3. Acepta decimales, y el divisor cero aborta

El nombre y la costumbre sugieren enteros. No lo es.

```dax
EVALUATE
ROW(
  "decimal", MOD(10.5, 3),
  "divisor_decimal", MOD(10, 2.5),
  "divisor_cero", IFERROR(MOD(10, 0), "aborta"),
  "dividendo_blanco", MOD(BLANK(), 3)
)
```

```result
decimal | divisor_decimal | divisor_cero | dividendo_blanco
1.5 | 0 | aborta | (blank)
```

El divisor cero **no** devuelve blanco como haría [`divide`](./divide.md): aborta. Si el
divisor puede venir de datos, envuélvelo.

Ver [`quotient`](./quotient.md), [`even`](./even.md) y [`odd`](./odd.md).
