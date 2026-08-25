---
function: FIXED
model: ninguno
---

# FIXED — ejemplos

## 1. Devuelve TEXTO, y ahí se acaba la aritmética

Se parece a `ROUND` y no lo es: `ROUND` devuelve un número, `FIXED` devuelve una cadena. Lo
que salga de aquí ya no se suma ni se ordena como número.

```dax
EVALUATE
ROW(
  "fixed",       FIXED(1234.5678, 2),
  "round",       ROUND(1234.5678, 2),
  "fixed_len",   LEN(FIXED(1234.5678, 2)),
  "orden_texto", FIXED(9, 0) < FIXED(10, 0)
)
```

```result
fixed | round | fixed_len | orden_texto
1.234,57 | 1234.57 | 8 | False
```

`"9" < "10"` es falso como texto y verdadero como número. Es la misma trampa que
[`format`](./format.md), y la razón por la que estas funciones van en el visual, no dentro
de la lógica.

## 2. Pone separador de miles salvo que le digas que no

El tercer argumento. Y el separador es el de la **cultura del modelo**, aquí `es-ES`: el
punto para los miles y la coma para los decimales.

```dax
EVALUATE
ROW(
  "con_miles", FIXED(1234567.891, 2),
  "sin_miles", FIXED(1234567.891, 2, TRUE),
  "cero_dec",  FIXED(1234.5, 0),
  "un_dec",    FIXED(1234.55, 1)
)
```

```result
con_miles | sin_miles | cero_dec | un_dec
1.234.567,89 | 1234567,89 | 1.235 | 1.234,6
```

## 3. Un número negativo de decimales redondea a la IZQUIERDA de la coma

Poco conocido y muy útil: `-3` redondea a millares. Y sigue devolviendo texto.

```dax
EVALUATE
ROW(
  "menos_1", FIXED(12345.6, -1),
  "menos_3", FIXED(12345.6, -3),
  "menos_9", FIXED(12345.6, -9),
  "blanco",  FIXED(BLANK(), 2)
)
```

```result
menos_1 | menos_3 | menos_9 | blanco
12.350 | 12.000 | 0 | 0,00
```

Redondear más allá de la magnitud del número da cero, no error.
