---
function: BITRSHIFT
model: ninguno
---

# BITRSHIFT — ejemplos

## 1. Desplazar a la derecha es dividir por dos, y TRUNCA

No redondea. Los bits que salen por la derecha se pierden, así que la operación no es
reversible: desplazar a la derecha y volver a la izquierda no devuelve el número original.

```dax
EVALUATE
ROW(
  "diez_entre_2",     BITRSHIFT(10, 1),
  "once_entre_2",     BITRSHIFT(11, 1),
  "ida_y_vuelta",     BITLSHIFT(BITRSHIFT(11, 1), 1),
  "uno_entre_2",      BITRSHIFT(1, 1)
)
```

```result
diez_entre_2 | once_entre_2 | ida_y_vuelta | uno_entre_2
5 | 5 | 10 | 0
```

`11 >> 1` da 5, y volver a la izquierda da 10: el bit perdido no vuelve.

## 2. Leer un campo empaquetado dentro de un número

El uso real: varios valores metidos en un solo entero. Se desplaza para traer el campo abajo
y se enmascara con [`bitand`](./bitand.md) para quedarse solo con él.

```dax
EVALUATE
VAR Empaquetado = 5 * 256 + 3 * 16 + 7
RETURN
ROW(
  "valor",       Empaquetado,
  "campo_bajo",  BITAND(Empaquetado, 15),
  "campo_medio", BITAND(BITRSHIFT(Empaquetado, 4), 15),
  "campo_alto",  BITRSHIFT(Empaquetado, 8)
)
```

```result
valor | campo_bajo | campo_medio | campo_alto
1335 | 7 | 3 | 5
```

## 3. Con negativos el signo se arrastra

No entra un cero por la izquierda: entra el bit de signo. Un negativo desplazado a la derecha
sigue siendo negativo, por mucho que se desplace, y tiende a `-1` en vez de a `0`.

```dax
EVALUATE
ROW(
  "menos_ocho_1",  BITRSHIFT(-8, 1),
  "menos_ocho_3",  BITRSHIFT(-8, 3),
  "menos_ocho_10", BITRSHIFT(-8, 10),
  "menos_uno_5",   BITRSHIFT(-1, 5)
)
```

```result
menos_ocho_1 | menos_ocho_3 | menos_ocho_10 | menos_uno_5
-4 | -1 | -1 | -1
```
