---
function: ISEVEN
model: ninguno
---

# ISEVEN — ejemplos

## 1. No confundir con `EVEN`, que devuelve un número

Dos funciones con casi el mismo nombre y tipos de retorno distintos. `ISEVEN` pregunta;
[`even`](../math-and-trig/even.md) redondea.

```dax
EVALUATE
ROW(
  "iseven_3", ISEVEN(3),
  "even_3", EVEN(3),
  "iseven_4", ISEVEN(4),
  "even_4", EVEN(4)
)
```

```result
iseven_3 | even_3 | iseven_4 | even_4
False | 4 | True | 4
```

`EVEN(3)` y `EVEN(4)` dan lo mismo; `ISEVEN` los distingue. Si el objetivo es preguntar, esta
es la buena.

## 2. Con decimales REDONDEA, no trunca — y por eso 2,5 es impar

Aquí está lo que no dice la firma, y contradice lo que hace `FACT` en el mismo repertorio.

```dax
EVALUATE
ROW(
  "dos_coma_tres", ISEVEN(2.3),
  "dos_coma_cinco", ISEVEN(2.5),
  "tres_coma_cinco", ISEVEN(3.5),
  "impar_de_dos_coma_cinco", ISODD(2.5)
)
```

```result
dos_coma_tres | dos_coma_cinco | tres_coma_cinco | impar_de_dos_coma_cinco
True | False | True | True
```

2,3 se comporta como 2 (par) y 2,5 como **3** (impar): redondea al entero más cercano, y el
medio exacto **se aleja del cero**. 3,5 va a 4 y vuelve a ser par; `ISEVEN(-2.5)` mira -3, no
-2, así que también es impar. Decir «hacia arriba» acierta solo con positivos — es la misma
distinción que separa a [`even`](../math-and-trig/even.md) de `CEILING`. Es la contraria de lo
que hace [`fact`](../math-and-trig/fact.md).

## 3. Un blanco cuenta como PAR

```dax
EVALUATE
ROW(
  "blanco_es_par", ISEVEN(BLANK()),
  "blanco_es_impar", ISODD(BLANK()),
  "cero_es_par", ISEVEN(0),
  "texto_numerico", ISEVEN("4")
)
```

```result
blanco_es_par | blanco_es_impar | cero_es_par | texto_numerico
True | False | True | True
```

El blanco entra como cero, y el cero es par. Si repartes filas en dos grupos con
`IF(ISEVEN([x]), "par", "impar")`, todas las filas sin dato acaban en el grupo de los pares sin
que nadie lo pida.

Ver [`isodd`](./isodd.md) y [`even`](../math-and-trig/even.md).
