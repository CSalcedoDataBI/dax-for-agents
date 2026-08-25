---
function: TANH
model: ninguno
---

# TANH — ejemplos

## 1. Se satura entre -1 y 1, y por eso no desborda

Es la única de las tres hiperbólicas básicas que **no** tiene techo de desbordamiento:
[`sinh`](./sinh.md) y [`cosh`](./cosh.md) mueren cerca de 710, y `TANH` simplemente se aplana.

```dax
EVALUATE
ROW(
  "tanh_0",   TANH(0),
  "tanh_1",   ROUND(TANH(1), 6),
  "tanh_100", TANH(100),
  "tanh_1000", TANH(1000)
)
```

```result
tanh_0 | tanh_1 | tanh_100 | tanh_1000
0 | 0.761594 | 1 | 1
```

A partir de un valor moderado devuelve **exactamente 1**. La saturación no es aproximada: el
resultado deja de distinguir entradas distintas, y eso importa si lo usas para normalizar.

## 2. Esa saturación borra información

Dos valores muy separados dan el mismo resultado. Como normalizador es cómodo hasta que las
entradas grandes dejan de ordenarse entre sí.

```dax
EVALUATE
ROW(
  "tanh_20",    TANH(20),
  "tanh_50",    TANH(50),
  "son_iguales", TANH(20) = TANH(50),
  "tanh_3",     ROUND(TANH(3), 6)
)
```

```result
tanh_20 | tanh_50 | son_iguales | tanh_3
1 | 1 | True | 0.995055
```

Si necesitas que los extremos sigan distinguiéndose, la escala tiene que ir antes: `TANH(x/k)`
con `k` grande.

## 3. Es impar, y es el cociente de las otras dos

```dax
EVALUATE
ROW(
  "impar",      ROUND(TANH(2) + TANH(-2), 10),
  "cociente",   ROUND(TANH(2) - DIVIDE(SINH(2), COSH(2)), 10),
  "blanco",     TANH(BLANK()),
  "en_rango",   ABS(TANH(-1000)) <= 1
)
```

```result
impar | cociente | blanco | en_rango
0 | 0 | (blank) | True
```

`TANH(BLANK())` sale **en blanco**, igual que [`sinh`](./sinh.md) y por la misma razón: el
blanco entra como cero, `TANH(0)` es cero, y ese cero vuelve a salir como blanco. `TANH(0)`
escrito a mano devuelve un **0** normal.

Ver [`sinh`](./sinh.md) y [`cosh`](./cosh.md), de cuyo cociente sale.
