---
function: SINH
model: ninguno
---

# SINH — ejemplos

## 1. No es trigonometría circular: no hay radianes ni período

Es la trampa de leerla por el nombre. `SINH` no oscila entre -1 y 1: **crece sin techo**, de
forma exponencial. Pasarle grados convertidos con `RADIANS` no tiene sentido aquí.

```dax
EVALUATE
ROW(
  "sinh_0",   SINH(0),
  "sinh_1",   ROUND(SINH(1), 6),
  "sinh_5",   ROUND(SINH(5), 6),
  "sinh_10",  ROUND(SINH(10), 6)
)
```

```result
sinh_0 | sinh_1 | sinh_5 | sinh_10
0 | 1.175201 | 74.203211 | 11013.232875
```

De 1 a 10 el valor se multiplica por casi diez mil. Comparar eso con [`sin`](./sin.md), que
nunca sale de [-1, 1], deja clara la diferencia.

## 2. Ese crecimiento tiene un techo, y al pasarlo aborta

Alrededor de 710 el resultado deja de caber en un número de coma flotante y la consulta muere.
Es el mismo muro que [`exp`](./exp.md), porque `SINH` está hecha de exponenciales.

```dax
EVALUATE ROW("desbordado", SINH(710))
```

```result
ERROR: An argument of function 'SINH' has the wrong data type or the result is too large or too small.
```

Justo por debajo todavía funciona:

```dax
EVALUATE
ROW(
  "sinh_700", SINH(700) > 0,
  "es_enorme", SINH(700) > POWER(10, 300),
  "exp_equivale", ROUND(SINH(3) - (EXP(3) - EXP(-3)) / 2, 10)
)
```

```result
sinh_700 | es_enorme | exp_equivale
True | True | 0
```

La última columna es la definición: `SINH(x) = (eˣ - e⁻ˣ) / 2`.

## 3. Es impar, y no tiene dominio por abajo

```dax
EVALUATE
ROW(
  "sinh_m1",  ROUND(SINH(-1), 6),
  "impar",    ROUND(SINH(2) + SINH(-2), 10),
  "blanco",   SINH(BLANK()),
  "identidad", ROUND(COSH(1) * COSH(1) - SINH(1) * SINH(1), 10)
)
```

```result
sinh_m1 | impar | blanco | identidad
-1.175201 | 0 | (blank) | 1
```

`COSH² - SINH² = 1` es la identidad hiperbólica fundamental, el equivalente de `sin² + cos² = 1`.

La columna `blanco` merece un segundo: `SINH(BLANK())` sale **en blanco**, y sin embargo
`SINH(BLANK()) = 0` devuelve **verdadero**. No son dos hechos en conflicto — el blanco entra
como cero, `SINH(0)` es cero, y un cero que viene de un blanco vuelve a salir como blanco.
`SINH(0)` escrito a mano, en cambio, devuelve un **0** que no está en blanco. Compara con
[`cosh`](./cosh.md), donde `COSH(BLANK())` es **1** por esto mismo: su resultado en cero no es
cero, así que no hay nada que colapsar.

Ver [`cosh`](./cosh.md), [`tanh`](./tanh.md) y [`asinh`](./asinh.md), su inversa.
