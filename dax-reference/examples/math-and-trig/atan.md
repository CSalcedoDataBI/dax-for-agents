---
function: ATAN
model: ninguno
---

# ATAN — ejemplos

## 1. No tiene dominio: acepta cualquier número sin abortar

Es la excepción de la familia inversa. [`asin`](./asin.md) y [`acos`](./acos.md) mueren fuera
de [-1, 1]; `ATAN` no muere nunca. Por eso es la que se usa cuando el argumento sale de una
división que puede desbocarse.

```dax
EVALUATE
ROW(
  "atan_1",     ROUND(ATAN(1), 6),
  "atan_1000",  ROUND(ATAN(1000), 6),
  "atan_m1000", ROUND(ATAN(-1000), 6),
  "pi_medios",  ROUND(PI() / 2, 6)
)
```

```result
atan_1 | atan_1000 | atan_m1000 | pi_medios
0.785398 | 1.569796 | -1.569796 | 1.570796
```

Se acerca a ±π/2 pero no llega: el rango abierto es **(-π/2, π/2)**.

## 2. Ese rango es media vuelta, no una entera

Consecuencia práctica: `ATAN(y/x)` **no** distingue un ángulo del tercer cuadrante de uno del
primero, porque `y/x` es el mismo número en los dos. Es el motivo por el que en otros
lenguajes existe `atan2`, que en DAX no está.

```dax
EVALUATE
ROW(
  "primer_cuadrante",  ROUND(DEGREES(ATAN(DIVIDE(1, 1))), 6),
  "tercer_cuadrante",  ROUND(DEGREES(ATAN(DIVIDE(-1, -1))), 6),
  "son_iguales",       ATAN(DIVIDE(1, 1)) = ATAN(DIVIDE(-1, -1)),
  "division_igual",    DIVIDE(1, 1) = DIVIDE(-1, -1)
)
```

```result
primer_cuadrante | tercer_cuadrante | son_iguales | division_igual
45 | 45 | True | True
```

Hay que reconstruir el cuadrante a mano con el signo de cada componente.

## 3. Es impar, y devuelve radianes

```dax
EVALUATE
ROW(
  "atan_2",     ROUND(ATAN(2), 6),
  "atan_m2",    ROUND(ATAN(-2), 6),
  "impar",      ROUND(ATAN(2) + ATAN(-2), 10),
  "en_grados",  ROUND(DEGREES(ATAN(1)), 6)
)
```

```result
atan_2 | atan_m2 | impar | en_grados
1.107149 | -1.107149 | 0 | 45
```

`ATAN(1)` en grados son 45. Ver [`acot`](./acot.md), su complementaria, que tiene otro rango.
