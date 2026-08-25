---
function: ASIN
model: ninguno
---

# ASIN — ejemplos

## 1. Su dominio es [-1, 1], y fuera de ahí ABORTA

No devuelve blanco: tumba la consulta. Y el valor que se le pasa suele venir de una división,
así que el `1.0000001` de un redondeo basta para romperlo.

```dax
EVALUATE ROW("fuera_de_rango", ASIN(2))
```

```result
ERROR: An argument of function 'ASIN' has the wrong data type or the result is too large or too small.
```

Dentro del dominio:

```dax
EVALUATE
ROW(
  "asin_1",  ROUND(ASIN(1), 6),
  "asin_0",  ASIN(0),
  "asin_m1", ROUND(ASIN(-1), 6),
  "pi_medios", ROUND(PI() / 2, 6)
)
```

```result
asin_1 | asin_0 | asin_m1 | pi_medios
1.570796 | 0 | -1.570796 | 1.570796
```

`ASIN(1)` es exactamente π/2. El rango de salida es **[-π/2, π/2]**.

## 2. Devuelve RADIANES, no grados

Simétrico al problema de [`sin`](./sin.md): si el resultado va a un informe donde se leen
grados, hay que convertirlo con [`degrees`](./degrees.md).

```dax
EVALUATE
ROW(
  "en_radianes", ROUND(ASIN(0.5), 6),
  "en_grados",   ROUND(DEGREES(ASIN(0.5)), 6),
  "vuelta",      ROUND(SIN(ASIN(0.5)), 6),
  "medio",       ROUND(ASIN(SIN(RADIANS(30))), 6)
)
```

```result
en_radianes | en_grados | vuelta | medio
0.523599 | 30 | 0.5 | 0.523599
```

## 3. El viaje de ida y vuelta solo funciona dentro del rango

`ASIN(SIN(x))` devuelve `x` únicamente si `x` está en [-π/2, π/2]. Fuera, devuelve el ángulo
equivalente dentro del rango, sin avisar de que no es el que entró.

```dax
EVALUATE
ROW(
  "dentro",  ROUND(ASIN(SIN(1)), 6),
  "fuera",   ROUND(ASIN(SIN(3)), 6),
  "original", 3,
  "coinciden", ROUND(ASIN(SIN(3)), 6) = 3
)
```

```result
dentro | fuera | original | coinciden
1 | 0.141593 | 3 | False
```

Ver [`acos`](./acos.md), que tiene el mismo dominio y otro rango de salida.
