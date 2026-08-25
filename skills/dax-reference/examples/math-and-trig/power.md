---
function: POWER
model: ninguno
---

# POWER — ejemplos

## 1. `POWER(0, 0)` aborta la consulta

Muchos lenguajes devuelven 1 por convención. DAX no: lo trata como indefinido y mata la
consulta.

```dax
EVALUATE ROW("cero_a_la_cero", POWER(0, 0))
```

```result
ERROR: An argument of function 'POWER' has the wrong data type or the result is too large or too small.
```

Los vecinos sí funcionan, lo que hace el agujero más fácil de pisar:

```dax
EVALUATE
ROW(
  "cero_a_la_dos", POWER(0, 2),
  "dos_a_la_cero", POWER(2, 0),
  "cero_a_la_menos_uno", IFERROR(POWER(0, -1), "aborta"),
  "base_blanca", POWER(BLANK(), 2)
)
```

```result
cero_a_la_dos | dos_a_la_cero | cero_a_la_menos_uno | base_blanca
0 | 1 | aborta | (blank)
```

Si el exponente viene de datos y puede ser cero al mismo tiempo que la base, hay que protegerlo.

## 2. La base negativa funciona, incluso con exponente fraccionario

Excel se niega con `(-8)^(1/3)`. DAX lo calcula — y el resultado enseña de paso que esto es
coma flotante.

```dax
EVALUATE
ROW(
  "menos_dos_al_cubo", POWER(-2, 3),
  "menos_dos_al_cuadrado", POWER(-2, 2),
  "raiz_cubica_negativa", POWER(-8, 1/3),
  "es_exactamente_menos_dos", POWER(-8, 1/3) = -2,
  "lo_que_sobra_x1e16", ROUND((POWER(-8, 1/3) + 2) * POWER(10, 16), 6)
)
```

```result
menos_dos_al_cubo | menos_dos_al_cuadrado | raiz_cubica_negativa | es_exactamente_menos_dos | lo_que_sobra_x1e16
-8 | 4 | -2 | False | 2.220446
```

La tercera columna **se imprime** como -2 y la cuarta dice que no lo es. La quinta está
multiplicada por 10¹⁶ justamente porque, sin escalar, el residuo también se imprime como 0:
sobran 2,220446 × 10⁻¹⁶. El formato de salida redondea y la comparación no. `POWER` devuelve un `double`, así que compararlo
con un entero esperado falla en silencio — redondea antes, o compara con una tolerancia.

## 3. Exponentes negativos y fraccionarios, que es donde deja de ser «multiplicar varias veces»

```dax
EVALUATE
ROW(
  "inverso", POWER(2, -2),
  "raiz_cuadrada", ROUND(POWER(9, 0.5), 6),
  "raiz_cubica", ROUND(POWER(27, 1/3), 6),
  "interes_compuesto", ROUND(POWER(1.05, 10), 6)
)
```

```result
inverso | raiz_cuadrada | raiz_cubica | interes_compuesto
0.25 | 3 | 3 | 1.628895
```

El último es el uso real en un informe: un 5 % durante diez periodos es un 62,9 % acumulado, no
un 50 %.

Ver [`sqrt`](./sqrt.md), [`exp`](./exp.md) y [`log`](./log.md), su inversa.
