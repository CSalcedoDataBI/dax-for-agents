---
function: EVEN
model: ninguno
---

# EVEN — ejemplos

## 1. No comprueba si un número es par: lo redondea al par siguiente

El nombre engaña a todo el mundo una vez. `EVEN` no devuelve verdadero ni falso — devuelve
**otro número**.

```dax
EVALUATE
ROW(
  "even_3", EVEN(3),
  "even_2", EVEN(2),
  "even_1", EVEN(1),
  "even_0", EVEN(0)
)
```

```result
even_3 | even_2 | even_1 | even_0
4 | 2 | 2 | 0
```

Para preguntar si algo es par, la forma es `MOD(n, 2) = 0`. Ojo con los negativos, que en
[`mod`](./mod.md) no se comportan como en otros lenguajes.

## 2. Redondea ALEJÁNDOSE del cero, no hacia arriba

Con positivos «al par siguiente» y «hacia arriba» son lo mismo. Con negativos no.

```dax
EVALUATE
ROW(
  "even_m3", EVEN(-3),
  "even_m1", EVEN(-1),
  "even_m2", EVEN(-2),
  "ceiling_m3", CEILING(-3, 2)
)
```

```result
even_m3 | even_m1 | even_m2 | ceiling_m3
-4 | -2 | -2 | -2
```

`EVEN(-3)` es **-4** y `CEILING(-3, 2)` es -2. Van en direcciones opuestas: `EVEN` se aleja del
cero y [`ceiling`](./ceiling.md) sube hacia el infinito positivo.

## 3. Con decimales sube al par, aunque el salto sea mínimo

```dax
EVALUATE
ROW(
  "even_1_5", EVEN(1.5),
  "even_2_0001", EVEN(2.0001),
  "even_blanco", EVEN(BLANK()),
  "even_texto", EVEN("3")
)
```

```result
even_1_5 | even_2_0001 | even_blanco | even_texto
2 | 4 | (blank) | 4
```

`EVEN(2.0001)` da **4**: cualquier cosa por encima de 2 ya necesita el par siguiente.

La columna del blanco merece pararse. `EVEN(BLANK())` sale **en blanco**, y `EVEN(0)` sale
**0**. No es incoherencia: el blanco entra como cero, `EVEN(0)` es cero, y un cero que viene de
un blanco vuelve a salir como blanco. Compara con [`odd`](./odd.md), donde `ODD(BLANK())` es
**1** por esto mismo — su resultado en cero no es cero, así que no hay nada que colapsar.

Ver [`odd`](./odd.md), [`ceiling`](./ceiling.md) y [`mround`](./mround.md).
