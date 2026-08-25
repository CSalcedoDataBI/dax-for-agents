---
function: COSH
model: ninguno
---

# COSH — ejemplos

## 1. Nunca baja de 1

Al contrario que [`cos`](./cos.md), que va de -1 a 1. `COSH` tiene su mínimo en `COSH(0) = 1` y
crece desde ahí en las dos direcciones. Un `COSH` negativo es imposible, así que si tu cálculo
lo produce, la función no es la que crees.

```dax
EVALUATE
ROW(
  "cosh_0",  COSH(0),
  "cosh_1",  ROUND(COSH(1), 6),
  "cosh_m1", ROUND(COSH(-1), 6),
  "minimo",  COSH(0.5) >= 1
)
```

```result
cosh_0 | cosh_1 | cosh_m1 | minimo
1 | 1.543081 | 1.543081 | True
```

## 2. Es par: el signo se pierde

`COSH(x) = COSH(-x)`. Es la diferencia estructural con [`sinh`](./sinh.md), que es impar, y la
razón por la que `COSH` no se puede invertir sobre todo el eje — ver [`acosh`](./acosh.md),
cuyo dominio empieza en 1 justamente por esto.

```dax
EVALUATE
ROW(
  "cosh_2",     ROUND(COSH(2), 6),
  "cosh_m2",    ROUND(COSH(-2), 6),
  "coinciden",  COSH(2) = COSH(-2),
  "sinh_no",    SINH(2) = SINH(-2)
)
```

```result
cosh_2 | cosh_m2 | coinciden | sinh_no
3.762196 | 3.762196 | True | False
```

## 3. El mismo techo que SINH, por la misma razón

```dax
EVALUATE ROW("desbordado", COSH(710))
```

```result
ERROR: An argument of function 'COSH' has the wrong data type or the result is too large or too small.
```

Y la definición, comprobada:

```dax
EVALUATE
ROW(
  "definicion",  ROUND(COSH(3) - (EXP(3) + EXP(-3)) / 2, 10),
  "blanco",      COSH(BLANK()),
  "suma_con_sinh", ROUND(COSH(2) + SINH(2) - EXP(2), 10)
)
```

```result
definicion | blanco | suma_con_sinh
0 | 1 | 0
```

`COSH(x) + SINH(x) = eˣ` — la comprobación en una línea de que las dos son las mitades par e
impar de la exponencial.

Y `COSH(BLANK())` es **1**, no blanco: el blanco entra como cero y `COSH(0)` vale 1. Cuidado con
generalizarlo, porque [`sinh`](./sinh.md) y [`tanh`](./tanh.md) **sí** devuelven blanco con la
misma entrada — no porque el blanco entre distinto, sino porque su resultado en cero es cero, y
un cero que sale de un blanco vuelve a salir como blanco.
