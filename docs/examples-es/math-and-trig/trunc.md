---
function: TRUNC
model: ninguno
---

# TRUNC — ejemplos

## 1. Corta hacia cero, y por eso NO es INT

Es la misma distinción de toda la familia, vista desde el otro lado: `TRUNC` quita los
decimales sin mirar el signo. `INT` baja al entero inferior.

```dax
EVALUATE
ROW(
  "positivo",     TRUNC(2.7),
  "negativo",     TRUNC(-2.7),
  "int_negativo", INT(-2.7),
  "coinciden_en_positivo", TRUNC(2.7) = INT(2.7)
)
```

```result
positivo | negativo | int_negativo | coinciden_en_positivo
2 | -2 | -3 | True
```

## 2. Acepta un segundo argumento, como ROUND

Lo que la separa de `INT`, que solo hace enteros. `TRUNC` puede cortar en cualquier posición.

```dax
EVALUATE
ROW(
  "sin_segundo",   TRUNC(2.789),
  "dos_decimales", TRUNC(2.789, 2),
  "a_decenas",     TRUNC(1999, -1),
  "negativo_dos",  TRUNC(-2.789, 2)
)
```

```result
sin_segundo | dos_decimales | a_decenas | negativo_dos
2 | 2.78 | 1990 | -2.78
```

`TRUNC(-2.789, 2)` da `-2,78`, no `-2,79`: corta, no redondea.

## 3. Con blanco y con cero

```dax
EVALUATE
ROW(
  "blanco",    TRUNC(BLANK()),
  "es_blanco", ISBLANK(TRUNC(BLANK())),
  "cero",      TRUNC(0.9999),
  "cero_neg",  TRUNC(-0.9999)
)
```

```result
blanco | es_blanco | cero | cero_neg
(blank) | True | 0 | 0
```

Los dos últimos son la señal de que esto no es redondeo: `0,9999` da 0 y `-0,9999` da 0
también — el mismo cero por los dos lados.

Ver [`int`](./int.md) y [`rounddown`](./rounddown.md), que hace lo mismo que `TRUNC` pero se
llama de otra manera.
