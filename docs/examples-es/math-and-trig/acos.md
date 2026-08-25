---
function: ACOS
model: ninguno
---

# ACOS — ejemplos

## 1. Mismo dominio que ASIN, [-1, 1], y también aborta fuera

```dax
EVALUATE ROW("fuera_de_rango", ACOS(2))
```

```result
ERROR: An argument of function 'ACOS' has the wrong data type or the result is too large or too small.
```

Es el error que aparece al calcular ángulos a partir de un producto escalar: la división da
`1.0000000002` por acumulación de coma flotante y la consulta muere. La defensa es acotar el
argumento con `MIN(1, MAX(-1, x))` antes de llamarla.

```dax
EVALUATE
ROW(
  "acos_1",   ACOS(1),
  "acos_0",   ROUND(ACOS(0), 6),
  "acos_m1",  ROUND(ACOS(-1), 6),
  "pi",       ROUND(PI(), 6)
)
```

```result
acos_1 | acos_0 | acos_m1 | pi
0 | 1.570796 | 3.141593 | 3.141593
```

## 2. Su rango de salida es [0, π] — distinto al de ASIN

Ahí está la diferencia práctica entre las dos: `ASIN` devuelve ángulos con signo, `ACOS`
nunca devuelve negativos. Para un ángulo entre vectores es lo que se quiere.

```dax
EVALUATE
ROW(
  "acos_de_neg", ROUND(ACOS(-0.5), 6),
  "asin_de_neg", ROUND(ASIN(-0.5), 6),
  "acos_positivo_siempre", ACOS(-0.5) > 0,
  "suma_constante", ROUND(ACOS(0.3) + ASIN(0.3), 6)
)
```

```result
acos_de_neg | asin_de_neg | acos_positivo_siempre | suma_constante
2.094395 | -0.523599 | True | 1.570796
```

`ACOS(x) + ASIN(x)` es siempre π/2. Es la comprobación rápida de que ninguna de las dos está
mal usada.

## 3. En radianes, como todo aquí

```dax
EVALUATE
ROW(
  "radianes", ROUND(ACOS(0.5), 6),
  "grados",   ROUND(DEGREES(ACOS(0.5)), 6),
  "vuelta",   ROUND(COS(ACOS(0.5)), 6),
  "blanco",   ROUND(ACOS(BLANK()), 6)
)
```

```result
radianes | grados | vuelta | blanco
1.047198 | 60 | 0.5 | 1.570796
```

`ACOS(BLANK())` no es blanco: el blanco entra como 0 y el resultado es π/2.
