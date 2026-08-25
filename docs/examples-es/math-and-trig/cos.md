---
function: COS
model: ninguno
---

# COS — ejemplos

## 1. Radianes, como toda la familia

`COS(60)` no es 0,5. El coseno de 60 **grados** sí lo es, y para eso hay que decirlo con
[`radians`](./radians.md).

```dax
EVALUATE
ROW(
  "cos_60_grados",   ROUND(COS(60), 6),
  "cos_60_radianes", ROUND(COS(RADIANS(60)), 6),
  "cos_0",           COS(0),
  "cos_pi",          COS(PI())
)
```

```result
cos_60_grados | cos_60_radianes | cos_0 | cos_pi
-0.952413 | 0.5 | 1 | -1
```

## 2. Es par: el signo del argumento no importa

Lo contrario que [`sin`](./sin.md), que es impar. Útil para comprobar de un vistazo que estás
usando la función que crees.

```dax
EVALUATE
ROW(
  "cos_1",       ROUND(COS(1), 6),
  "cos_menos_1", ROUND(COS(-1), 6),
  "coinciden",   COS(1) = COS(-1),
  "sin_no",      SIN(1) = SIN(-1)
)
```

```result
cos_1 | cos_menos_1 | coinciden | sin_no
0.540302 | 0.540302 | True | False
```

## 3. Sin dominio, y siempre entre -1 y 1

```dax
EVALUATE
ROW(
  "muy_grande", ROUND(COS(1000), 6),
  "en_rango",   ABS(COS(1000)) <= 1,
  "identidad",  ROUND(COS(2) * COS(2) + SIN(2) * SIN(2), 10),
  "blanco",     ISBLANK(COS(BLANK()))
)
```

```result
muy_grande | en_rango | identidad | blanco
0.562379 | True | 1 | False
```

`COS(BLANK())` **no** es blanco: el blanco se convierte en 0 y el coseno de 0 es 1. Es la
excepción a la regla de que el blanco se propaga, y conviene verla antes de fiarse.

Ver [`acos`](./acos.md), que sí tiene dominio.
