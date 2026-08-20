---
function: ACOTH
model: ninguno
---

# ACOTH — ejemplos

## 1. Su dominio es lo de FUERA de [-1, 1], al revés que `ATANH`

Es lo contrario de lo que sugiere la costumbre: aquí los valores pequeños son los prohibidos.

```dax
EVALUATE
ROW(
  "acoth_2", ROUND(ACOTH(2), 6),
  "acoth_menos_2", ROUND(ACOTH(-2), 6),
  "acoth_1_01", ROUND(ACOTH(1.01), 6),
  "dentro_del_intervalo", IFERROR(ACOTH(0.5), "aborta")
)
```

```result
acoth_2 | acoth_menos_2 | acoth_1_01 | dentro_del_intervalo
0.549306 | -0.549306 | 2.651652 | aborta
```

`ACOTH(0.5)` aborta. Y en 1,01 —justo fuera del intervalo— el valor ya es 2,65 y sigue
creciendo: la función se dispara al acercarse a ±1 desde fuera.

## 2. El 1, el -1, el cero y el blanco abortan todos

```dax
EVALUATE ROW("acoth_de_uno", ACOTH(1))
```

```result
ERROR: An argument of function 'ACOTH' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE
ROW(
  "uno", IFERROR(ACOTH(1), "aborta"),
  "menos_uno", IFERROR(ACOTH(-1), "aborta"),
  "cero", IFERROR(ACOTH(0), "aborta"),
  "blanco", IFERROR(ACOTH(BLANK()), "aborta")
)
```

```result
uno | menos_uno | cero | blanco
aborta | aborta | aborta | aborta
```

El blanco entra como cero y el cero está dentro del intervalo prohibido. Cualquier hueco en la
columna tumba la consulta entera, así que la protección hay que escribirla — y dentro del
iterador, no alrededor, como está medido en [`ln`](./ln.md).

## 3. Es `ATANH` del inverso, y esa es la forma práctica de recordarla

```dax
EVALUATE
ROW(
  "acoth_2", ROUND(ACOTH(2), 6),
  "atanh_de_un_medio", ROUND(ATANH(1/2), 6),
  "identicos", ROUND(ACOTH(2) - ATANH(0.5), 10),
  "coth_ida_vuelta", ROUND(COTH(ACOTH(3)), 10)
)
```

```result
acoth_2 | atanh_de_un_medio | identicos | coth_ida_vuelta
0.549306 | 0.549306 | 0 | 3
```

`ACOTH(x) = ATANH(1/x)`, y el dominio sale solo de ahí: para que `1/x` caiga dentro de (-1, 1),
`x` tiene que estar fuera.

Ver [`coth`](./coth.md), [`atanh`](./atanh.md) y [`acot`](./acot.md).
