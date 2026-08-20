---
function: ODD
model: ninguno
---

# ODD — ejemplos

## 1. No comprueba si un número es impar: lo redondea al impar siguiente

Igual que [`even`](./even.md), el nombre promete una pregunta y la función devuelve **otro
número**.

```dax
EVALUATE
ROW(
  "odd_2", ODD(2),
  "odd_3", ODD(3),
  "odd_1", ODD(1),
  "odd_1_5", ODD(1.5)
)
```

```result
odd_2 | odd_3 | odd_1 | odd_1_5
3 | 3 | 1 | 3
```

Para preguntar si algo es impar, la forma es `MOD(n, 2) <> 0`, con el cuidado que pide
[`mod`](./mod.md) cuando hay negativos.

## 2. Se aleja del cero, y el cero **no** se queda quieto

Esta es la diferencia real con `EVEN`, y la que hace que el blanco se comporte distinto.

```dax
EVALUATE
ROW(
  "odd_0", ODD(0),
  "even_0", EVEN(0),
  "odd_m2", ODD(-2),
  "odd_m1", ODD(-1)
)
```

```result
odd_0 | even_0 | odd_m2 | odd_m1
1 | 0 | -3 | -1
```

`ODD(0)` es **1**: el cero no es impar, así que hay que moverse. `EVEN(0)` es 0 porque ya
estaba donde tenía que estar. Ese detalle, que parece trivia, decide el punto siguiente.

## 3. Un blanco sale como 1, no en blanco

```dax
EVALUATE
ROW(
  "odd_blanco", ODD(BLANK()),
  "even_blanco", EVEN(BLANK()),
  "odd_texto", ODD("2"),
  "odd_m0_5", ODD(-0.5)
)
```

```result
odd_blanco | even_blanco | odd_texto | odd_m0_5
1 | (blank) | 3 | -1
```

El blanco entra como cero en las dos. `EVEN(0)` es cero, y un cero que viene de un blanco
vuelve a salir en blanco; `ODD(0)` es **1**, que no es cero, así que no hay nada que colapsar y
el 1 se queda. Es la misma mecánica que separa a [`sinh`](./sinh.md) de [`cosh`](./cosh.md).

En una columna calculada sobre datos con huecos, eso significa que `ODD` **rellena** los huecos
con un 1 y `EVEN` los deja pasar. Rara vez es lo que se quería.

Ver [`even`](./even.md), [`mround`](./mround.md) y [`ceiling`](./ceiling.md).
