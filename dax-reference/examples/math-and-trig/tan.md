---
function: TAN
model: ninguno
---

# TAN — ejemplos

## 1. Radianes otra vez, y aquí el error es más grande

`TAN(45)` da 1,62 en vez de 1. No es un desvío pequeño: la tangente crece rápido, así que
confundir grados con radianes puede dar un número de otro orden de magnitud.

```dax
EVALUATE
ROW(
  "tan_45_grados",   ROUND(TAN(45), 6),
  "tan_45_radianes", ROUND(TAN(RADIANS(45)), 6),
  "tan_0",           TAN(0),
  "tan_30_bien",     ROUND(TAN(RADIANS(30)), 6)
)
```

```result
tan_45_grados | tan_45_radianes | tan_0 | tan_30_bien
1.619775 | 1 | 0 | 0.57735
```

## 2. En π/2 no da infinito ni error: da un número enorme

Matemáticamente la tangente no existe ahí. Numéricamente, `PI()/2` es una aproximación, así
que el motor devuelve un número gigantesco y sigue como si nada. Una división por ese valor
da casi cero y nadie se entera.

```dax
EVALUATE
ROW(
  "cerca_del_polo", ROUND(TAN(PI() / 2), 0),
  "es_muy_grande",  TAN(PI() / 2) > 1000000000,
  "hay_error",      ISERROR(TAN(PI() / 2)),
  "justo_despues",  ROUND(TAN(PI() / 2 + 0.1), 6)
)
```

```result
cerca_del_polo | es_muy_grande | hay_error | justo_despues
16324552277619100 | True | False | -9.966644
```

Si el ángulo sale de un cálculo y puede acercarse a 90°, hay que acotarlo a mano: no hay
error que avise.

## 3. Es impar, y periódica con período π

```dax
EVALUATE
ROW(
  "tan_1",       ROUND(TAN(1), 6),
  "tan_menos_1", ROUND(TAN(-1), 6),
  "impar",       ROUND(TAN(1) + TAN(-1), 10),
  "periodo",     ROUND(TAN(1) - TAN(1 + PI()), 6)
)
```

```result
tan_1 | tan_menos_1 | impar | periodo
1.557408 | -1.557408 | 0 | 0
```

El período es **π**, no 2π como en [`sin`](./sin.md) y [`cos`](./cos.md).

Ver [`atan`](./atan.md), su inversa, que no tiene dominio.
