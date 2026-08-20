---
function: LCM
model: ninguno
---

# LCM — ejemplos

## 1. Dos argumentos como máximo, igual que `GCD`

```dax
EVALUATE
ROW(
  "dos", LCM(4, 6),
  "tres_anidada", LCM(LCM(4, 6), 10),
  "coprimos", LCM(7, 9),
  "uno_multiplo_del_otro", LCM(4, 12)
)
```

```result
dos | tres_anidada | coprimos | uno_multiplo_del_otro
12 | 60 | 63 | 12
```

Con coprimos el mínimo común múltiplo es el producto; cuando uno divide al otro, es el mayor.
Para más de dos números hay que anidar, como en [`gcd`](./gcd.md).

## 2. Redondea los decimales, no los trunca

```dax
EVALUATE
ROW(
  "cuatro_coma_cuatro", LCM(4.4, 6),
  "cuatro_coma_seis", LCM(4.6, 6),
  "cuatro", LCM(4, 6),
  "cinco", LCM(5, 6)
)
```

```result
cuatro_coma_cuatro | cuatro_coma_seis | cuatro | cinco
12 | 30 | 12 | 30
```

4,6 se comporta como 5 y devuelve 30 en vez de 12. Es la misma regla de [`gcd`](./gcd.md) y la
contraria de [`fact`](./fact.md).

## 3. El cero absorbe, los negativos abortan, y el resultado crece rápido

```dax
EVALUATE
ROW(
  "con_cero", LCM(0, 5),
  "con_blanco", LCM(BLANK(), 5),
  "negativo", IFERROR(LCM(-4, 6), "aborta"),
  "grandes", LCM(123456, 789012)
)
```

```result
con_cero | con_blanco | negativo | grandes
0 | 0 | aborta | 8117355456
```

`LCM(0, n)` es **0**, no `n` — al revés que [`gcd`](./gcd.md), donde el cero es el elemento
neutro. Un blanco en los datos convierte todo el cálculo en cero sin avisar.

Y con dos números de seis cifras el resultado ya pasa de 8.000 millones: `LCM(a, b)` es
`a × b / GCD(a, b)`, así que con coprimos grandes desborda antes de lo que parece.

Ver [`gcd`](./gcd.md) y [`mod`](./mod.md).
