---
function: LN
model: ninguno
---

# LN — ejemplos

## 1. Es logaritmo natural: la base es *e*, no 10

Confundirla con [`log10`](./log10.md) es el error que no da error — devuelve un número
perfectamente creíble, solo que 2,3 veces el que querías.

```dax
EVALUATE
ROW(
  "ln_1000", ROUND(LN(1000), 6),
  "log10_1000", LOG10(1000),
  "factor", ROUND(LN(1000) / LOG10(1000), 6),
  "ln_de_e", ROUND(LN(EXP(1)), 10)
)
```

```result
ln_1000 | log10_1000 | factor | ln_de_e
6.907755 | 3 | 2.302585 | 1
```

Ese 2,302585 es `LN(10)`, el factor fijo entre las dos bases. `LN(EXP(1)) = 1` es la definición.

## 2. El cero y los negativos abortan la consulta, no devuelven blanco

El logaritmo no está definido ahí, y DAX no lo disimula.

```dax
EVALUATE ROW("ln_cero", LN(0))
```

```result
ERROR: An argument of function 'LN' has the wrong data type or the result is too large or too small.
```

En un modelo real esto llega desde una columna, no desde una constante. Y aquí está lo que no
es evidente: **envolver el iterador en `IFERROR` no sirve.**

```dax
EVALUATE
VAR Valores = { 100, 0, -5 }
RETURN ROW("por_fuera", IFERROR(SUMX(Valores, LN([Value])), -1))
```

```result
ERROR: An argument of function 'LN' has the wrong data type or the result is too large or too small.
```

El `IFERROR` está ahí y la consulta muere igual. No es que `IFERROR` no funcione con `LN` —
`IFERROR(LN(0), -1)` devuelve -1 sin problema. Es que **alrededor de un iterador no alcanza al
error que se levanta dentro**. La protección tiene que ir en la expresión iterada:

```dax
EVALUATE
VAR Valores = { 100, 0, -5 }
RETURN
ROW(
  "iferror_dentro", ROUND(SUMX(Valores, IFERROR(LN([Value]), 0)), 6),
  "con_if", ROUND(SUMX(Valores, IF([Value] > 0, LN([Value]))), 6),
  "filtrando_antes", ROUND(SUMX(FILTER(Valores, [Value] > 0), LN([Value])), 6),
  "iferror_suelto", IFERROR(LN(0), -1)
)
```

```result
iferror_dentro | con_if | filtrando_antes | iferror_suelto
4.60517 | 4.60517 | 4.60517 | -1
```

Las tres primeras funcionan. Una sola fila con cero tumba la agregación entera si la protección
está en el sitio equivocado, y el sitio equivocado es justo el que parece más natural.

## 3. Convierte crecimiento multiplicativo en algo que se puede sumar

Es la razón de usarla en un informe: la suma de logaritmos es el logaritmo del producto, así
que un crecimiento compuesto se vuelve aditivo.

```dax
EVALUATE
VAR Factores = { 1.10, 1.05, 1.20 }
RETURN
ROW(
  "producto", ROUND(PRODUCTX(Factores, [Value]), 6),
  "exp_de_suma_ln", ROUND(EXP(SUMX(Factores, LN([Value]))), 6),
  "media_geometrica", ROUND(EXP(AVERAGEX(Factores, LN([Value]))), 6)
)
```

```result
producto | exp_de_suma_ln | media_geometrica
1.386 | 1.386 | 1.114947
```

Las dos primeras columnas coinciden porque es la misma cuenta por dos caminos. La tercera es la
media **geométrica** —el crecimiento medio real, 11,49 %— que no es la media aritmética de
1,10, 1,05 y 1,20.

Ver [`exp`](./exp.md), su inversa, y [`log`](./log.md) para otras bases.
