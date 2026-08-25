---
function: BITXOR
model: ninguno
---

# BITXOR — ejemplos

## 1. Cambia la bandera: la enciende si estaba apagada y al revés

Es lo que distingue `BITXOR` de [`bitor`](./bitor.md), que solo enciende.

```dax
EVALUATE
VAR Permisos = 5
RETURN
ROW(
  "valor",          Permisos,
  "cambia_el_1",    BITXOR(Permisos, 1),
  "cambia_el_2",    BITXOR(Permisos, 2),
  "cambia_dos_veces", BITXOR(BITXOR(Permisos, 1), 1)
)
```

```result
valor | cambia_el_1 | cambia_el_2 | cambia_dos_veces
5 | 4 | 7 | 5
```

Aplicarlo dos veces devuelve el valor original. Esa propiedad es la que lo hace útil para
alternar un estado, y también la que lo hace peligroso si se ejecuta dos veces sin querer.

## 2. Consigo mismo siempre da cero

De ahí el truco clásico de comparar dos números: si el `BITXOR` es cero, son idénticos bit a
bit.

```dax
EVALUATE
ROW(
  "consigo_mismo",   BITXOR(12345, 12345),
  "con_cero",        BITXOR(12345, 0),
  "difieren_en_uno", BITXOR(12, 13),
  "negativos",       BITXOR(-5, -5)
)
```

```result
consigo_mismo | con_cero | difieren_en_uno | negativos
0 | 12345 | 1 | 0
```

## 3. Con signos distintos el resultado es negativo

El bit de signo también se opera, así que `BITXOR` de un positivo y un negativo sale negativo.
Un cálculo que dé por hecho que el resultado es una máscara positiva se rompe aquí.

```dax
EVALUATE
ROW(
  "positivo_negativo", BITXOR(5, -1),
  "negativo_negativo", BITXOR(-5, -3),
  "positivo_positivo", BITXOR(5, 3),
  "menos_uno_cero",    BITXOR(-1, 0)
)
```

```result
positivo_negativo | negativo_negativo | positivo_positivo | menos_uno_cero
-6 | 6 | 6 | -1
```
