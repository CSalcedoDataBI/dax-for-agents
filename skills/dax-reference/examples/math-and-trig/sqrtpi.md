---
function: SQRTPI
model: ninguno
---

# SQRTPI — ejemplos

## 1. Es `SQRT(n × π)`, no `SQRT(n) × π` ni `SQRT(π)`

El nombre admite tres lecturas y solo una es la correcta. La multiplicación va **dentro** de la
raíz.

```dax
EVALUATE
ROW(
  "sqrtpi_4", ROUND(SQRTPI(4), 6),
  "raiz_de_4_por_pi", ROUND(SQRT(4 * PI()), 6),
  "raiz_de_4_por_pi_fuera", ROUND(SQRT(4) * PI(), 6),
  "sqrtpi_1", ROUND(SQRTPI(1), 6)
)
```

```result
sqrtpi_4 | raiz_de_4_por_pi | raiz_de_4_por_pi_fuera | sqrtpi_1
3.544908 | 3.544908 | 6.283185 | 1.772454
```

Las columnas 1 y 2 coinciden; la 3 es casi el doble. Y `SQRTPI(1)` es `SQRT(π)` = 1,772454, que
es de donde sale la confusión del nombre.

## 2. Hereda el dominio de `SQRT`: un negativo aborta

```dax
EVALUATE ROW("negativo", SQRTPI(-1))
```

```result
ERROR: An argument of function 'SQRTPI' has the wrong data type or the result is too large or too small.
```

Y el cero y el blanco se comportan como en [`sqrt`](./sqrt.md):

```dax
EVALUATE
ROW(
  "cero", SQRTPI(0),
  "blanco", SQRTPI(BLANK()),
  "es_blanco", ISBLANK(SQRTPI(BLANK()))
)
```

```result
cero | blanco | es_blanco
0 | (blank) | True
```

El blanco entra como cero, `SQRTPI(0)` es cero, y ese cero vuelve a salir blanco.

## 3. Para qué existe: la constante de la distribución normal

Prácticamente su único uso es la fórmula de la densidad normal, donde `√(2π)` aparece como
denominador. Escribirla con `SQRTPI(2)` ahorra un paréntesis y poco más.

```dax
EVALUATE
ROW(
  "raiz_2pi", ROUND(SQRTPI(2), 6),
  "escrita_larga", ROUND(SQRT(2 * PI()), 6),
  "densidad_en_cero", ROUND(1 / SQRTPI(2), 6)
)
```

```result
raiz_2pi | escrita_larga | densidad_en_cero
2.506628 | 2.506628 | 0.398942
```

0,398942 es la altura de la campana en su centro. Si no estás escribiendo estadística a mano,
`SQRT(n * PI())` se lee mejor y hace lo mismo.

Ver [`sqrt`](./sqrt.md) y [`pi`](./pi.md).
