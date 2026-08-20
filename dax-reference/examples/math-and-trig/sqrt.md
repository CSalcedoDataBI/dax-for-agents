---
function: SQRT
model: ninguno
---

# SQRT — ejemplos

## 1. Un negativo aborta la consulta entera

No devuelve blanco ni un error de celda: mata la consulta. Con una constante se ve venir; con
una columna que a veces trae un negativo, no.

```dax
EVALUATE ROW("raiz_de_menos_uno", SQRT(-1))
```

```result
ERROR: An argument of function 'SQRT' has the wrong data type or the result is too large or too small.
```

La protección, y dónde ponerla:

```dax
EVALUATE
VAR Valores = { 9, 4, -1 }
RETURN
ROW(
  "protegido", SUMX(Valores, IF([Value] >= 0, SQRT([Value]))),
  "iferror_dentro", SUMX(Valores, IFERROR(SQRT([Value]), 0)),
  "filtrando", SUMX(FILTER(Valores, [Value] >= 0), SQRT([Value]))
)
```

```result
protegido | iferror_dentro | filtrando
5 | 5 | 5
```

Las tres funcionan porque la protección va **dentro** del iterador. Envolver el `SUMX` entero
en `IFERROR` no basta — medido en [`ln`](./ln.md).

## 2. El blanco sí pasa, y sale en blanco

```dax
EVALUATE
ROW(
  "blanco", SQRT(BLANK()),
  "es_blanco", ISBLANK(SQRT(BLANK())),
  "compara_cero", SQRT(BLANK()) = 0,
  "cero", SQRT(0)
)
```

```result
blanco | es_blanco | compara_cero | cero
(blank) | True | True | 0
```

El cero no es negativo, así que no aborta: entra, sale cero, y ese cero que venía de un blanco
vuelve a salir blanco. Es la misma mecánica de [`abs`](./abs.md) y [`sign`](./sign.md).

## 3. Es `POWER(n, 0.5)`, con la precisión que eso implica

```dax
EVALUATE
ROW(
  "sqrt_2", ROUND(SQRT(2), 6),
  "power_2", ROUND(POWER(2, 0.5), 6),
  "identicos", SQRT(2) = POWER(2, 0.5),
  "cuadrado", ROUND(SQRT(2) * SQRT(2), 10),
  "exacto", SQRT(2) * SQRT(2) = 2
)
```

```result
sqrt_2 | power_2 | identicos | cuadrado | exacto
1.414214 | 1.414214 | True | 2 | False
```

Las dos últimas columnas son el punto. `SQRT(2) * SQRT(2)` **se imprime como 2** y **no es 2**:
sobran 4,4 × 10⁻¹⁶. El formato de salida redondea, la comparación no, y un `IF(x = 2, ...)`
sobre eso se va por la rama equivocada sin dar ninguna señal.

La tercera columna, en cambio, sí es verdadera: `SQRT(2)` y `POWER(2, 0.5)` devuelven
exactamente el mismo `double`. Que dos cálculos coincidan bit a bit no implica que el ida y
vuelta cuadre — es la misma trampa que [`currency`](./currency.md) resuelve para el dinero.

Ver [`power`](./power.md), [`sqrtpi`](./sqrtpi.md) y [`abs`](./abs.md).
