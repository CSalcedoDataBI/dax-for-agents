---
function: ISODD
model: ninguno
---

# ISODD — ejemplos

## 1. Es el complemento exacto de `ISEVEN`, también con decimales

```dax
EVALUATE
ROW(
  "siete", ISODD(7),
  "ocho", ISODD(8),
  "complementarios_7", ISODD(7) = NOT ISEVEN(7),
  "complementarios_2_5", ISODD(2.5) = NOT ISEVEN(2.5),
  "complementarios_blanco", ISODD(BLANK()) = NOT ISEVEN(BLANK())
)
```

```result
siete | ocho | complementarios_7 | complementarios_2_5 | complementarios_blanco
True | False | True | True | True
```

Nunca hay un valor que sea las dos cosas ni ninguna de las dos. Eso no es obvio: en
[`sign`](../math-and-trig/sign.md), por ejemplo, sí hay un cuarto caso.

## 2. Redondea los decimales, y por eso 2,5 es impar y 3,5 no

```dax
EVALUATE
ROW(
  "dos_coma_cinco", ISODD(2.5),
  "tres_coma_cinco", ISODD(3.5),
  "dos_coma_tres", ISODD(2.3),
  "tres_coma_siete", ISODD(3.7)
)
```

```result
dos_coma_cinco | tres_coma_cinco | dos_coma_tres | tres_coma_siete
True | False | False | False
```

2,5 se comporta como 3 y 3,5 como 4; 3,7 sube a 4 y también sale par. El medio no «sube»: **se
aleja del cero**, y con negativos eso es bajar. Medido, `ISODD(-2.5)` es verdadero porque mira
-3, no -2; `ISODD(-1.5)` es falso porque mira -2, no -1. Con positivos las dos reglas coinciden
y por eso la confusión no se nota hasta que aparece un negativo. Misma regla que
[`iseven`](./iseven.md).

## 3. Un blanco NO es impar, y ese es el hueco que deja

```dax
EVALUATE
ROW(
  "blanco", ISODD(BLANK()),
  "blanco_es_par", ISEVEN(BLANK()),
  "cero", ISODD(0),
  "menos_tres", ISODD(-3)
)
```

```result
blanco | blanco_es_par | cero | menos_tres
False | True | False | True
```

Filtrar con `ISODD` descarta las filas sin dato; filtrar con `ISEVEN` se las queda. Dos filtros
que parecen partir la tabla en dos mitades y no lo hacen — reparten los huecos siempre al mismo
lado.

Ver [`iseven`](./iseven.md) y [`odd`](../math-and-trig/odd.md).
