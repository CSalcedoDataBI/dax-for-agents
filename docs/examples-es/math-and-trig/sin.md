---
function: SIN
model: ninguno
---

# SIN — ejemplos

## 1. El argumento va en RADIANES, y con grados no falla: miente

Es la trampa número uno de toda la familia. `SIN(90)` no da 1 — da el seno de 90 radianes, que
es un número perfectamente creíble y completamente equivocado. No hay error que lo delate.

```dax
EVALUATE
ROW(
  "sin_90_grados",   ROUND(SIN(90), 6),
  "sin_90_radianes", ROUND(SIN(RADIANS(90)), 6),
  "sin_0",           SIN(0),
  "sin_30_bien",     ROUND(SIN(RADIANS(30)), 6)
)
```

```result
sin_90_grados | sin_90_radianes | sin_0 | sin_30_bien
0.893997 | 1 | 0 | 0.5
```

Si el dato viene en grados —y casi siempre viene en grados— hay que pasarlo por
[`radians`](./radians.md) **siempre**.

## 2. No tiene dominio: acepta cualquier número

A diferencia de su inversa [`asin`](./asin.md), que solo admite [-1, 1]. Aquí el resultado
siempre cae en ese intervalo.

```dax
EVALUATE
ROW(
  "muy_grande",  ROUND(SIN(1000), 6),
  "negativo",    ROUND(SIN(-1), 6),
  "impar",       ROUND(SIN(-1) + SIN(1), 6),
  "en_rango",    ABS(SIN(1000)) <= 1
)
```

```result
muy_grande | negativo | impar | en_rango
0.82688 | -0.841471 | 0 | True
```

`SIN(-x) = -SIN(x)`: la suma da cero exacto, que es la comprobación de que es impar.

## 3. SIN(PI()) se MUESTRA como cero y no es igual a cero

Las dos cosas a la vez, y esa contradicción es el ejemplo. `PI()` es una aproximación, así que
el seno sale del orden de 10⁻¹⁶: cualquier formato lo enseña como `0`, y la comparación `= 0`
devuelve **falso**. Un `IF(SIN(x) = 0, …)` que se ve correcto en el visual nunca entra por esa
rama.

```dax
EVALUATE
ROW(
  "sin_pi",        SIN(PI()),
  "es_cero",       SIN(PI()) = 0,
  "sin_pi_medios", SIN(PI() / 2),
  "identidad",     ROUND(SIN(1) * SIN(1) + COS(1) * COS(1), 10)
)
```

```result
sin_pi | es_cero | sin_pi_medios | identidad
0 | False | 1 | 1
```

Con valores de coma flotante hay que comparar contra una tolerancia —`ABS(x) < 1e-9`— o
redondear antes. Ver [`cos`](./cos.md), [`tan`](./tan.md) y [`asin`](./asin.md).
