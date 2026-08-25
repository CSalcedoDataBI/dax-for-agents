---
function: RANDBETWEEN
model: ninguno
---

# RANDBETWEEN — ejemplos

> Igual que [`rand`](./rand.md), los bloques `result` afirman **propiedades** y no valores
> concretos.

## 1. Los dos extremos entran, y el resultado siempre es entero

```dax
EVALUATE
VAR Tirada = RANDBETWEEN(1, 6)
RETURN
ROW(
  "dentro_del_rango", Tirada >= 1 && Tirada <= 6,
  "es_entero", Tirada = INT(Tirada),
  "sin_variable_no", RANDBETWEEN(1, 6) = INT(RANDBETWEEN(1, 6)),
  "extremos_iguales", RANDBETWEEN(5, 5),
  "negativos_valen", RANDBETWEEN(-3, -3)
)
```

```result
dentro_del_rango | es_entero | sin_variable_no | extremos_iguales | negativos_valen
True | True | False | 5 | -3
```

A diferencia de [`rand`](./rand.md), que excluye el 1, aquí el intervalo es **cerrado por los
dos lados**. Con los extremos iguales el resultado es constante, que es la forma de comprobarlo
sin depender del azar.

La tercera columna es la trampa de [`rand`](./rand.md) otra vez, y sale **falsa**: no está
comparando una tirada consigo misma, está comparando **dos tiradas distintas**. Con el `VAR`
la segunda columna sí dice lo que quiere decir. Escribir esa línea sin variable y leer el
`False` como «no devuelve enteros» es la conclusión equivocada del experimento equivocado.

## 2. Con los extremos al revés aborta la consulta

```dax
EVALUATE ROW("del_seis_al_uno", RANDBETWEEN(6, 1))
```

```result
ERROR: An argument of function 'RANDBETWEEN' has the wrong data type or the result is too large or too small.
```

Si los límites vienen de medidas, el orden no está garantizado. `RANDBETWEEN(MIN(a, b), MAX(a, b))`
es la forma que no se cae.

## 3. Sube el mínimo y baja el máximo — y así un intervalo decimal se puede quedar vacío

Esta es la parte que no dice la firma. Con decimales, el límite inferior se redondea **hacia
arriba** y el superior **hacia abajo**, así que el intervalo se encoge a los enteros que caen
estrictamente dentro. Si no queda ninguno, la consulta muere.

```dax
EVALUATE
ROW(
  "de_1_2_a_2_9", RANDBETWEEN(1.2, 2.9) = 2,
  "de_1_5_a_2_5", RANDBETWEEN(1.5, 2.5) = 2,
  "de_2_2_a_2_8", IFERROR(RANDBETWEEN(2.2, 2.8), "aborta"),
  "de_1_2_a_1_2", IFERROR(RANDBETWEEN(1.2, 1.2), "aborta"),
  "blancos", RANDBETWEEN(BLANK(), BLANK())
)
```

```result
de_1_2_a_2_9 | de_1_5_a_2_5 | de_2_2_a_2_8 | de_1_2_a_1_2 | blancos
True | True | aborta | aborta | 0
```

`RANDBETWEEN(1.2, 2.9)` devuelve **siempre 2**: es el único entero dentro. Y `(2.2, 2.8)` se
convierte en `[3, 2]`, que está invertido, así que aborta — el mismo error del punto 2, con
unos límites que a la vista parecían perfectamente ordenados.

Ver [`rand`](./rand.md) y [`int`](./int.md).
