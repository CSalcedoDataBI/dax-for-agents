---
function: EXP
model: ninguno
---

# EXP — ejemplos

## 1. Un blanco sale como 1, no en blanco

Es la trampa que separa a `EXP` de casi todas sus vecinas. El blanco entra como cero, y `e⁰` es
**uno**, así que no hay ningún cero que colapsar de vuelta a blanco.

```dax
EVALUATE
ROW(
  "exp_blanco", EXP(BLANK()),
  "exp_cero", EXP(0),
  "sqrt_blanco", SQRT(BLANK()),
  "abs_blanco", ABS(BLANK())
)
```

```result
exp_blanco | exp_cero | sqrt_blanco | abs_blanco
1 | 1 | (blank) | (blank)
```

En una columna calculada sobre datos con huecos, `EXP` **rellena** cada hueco con un 1 y las
otras dos los dejan pasar. Es la misma mecánica que separa a [`cosh`](./cosh.md) de
[`sinh`](./sinh.md).

## 2. El muro está en 710, y es un muro de verdad

```dax
EVALUATE ROW("desbordado", EXP(710))
```

```result
ERROR: An argument of function 'EXP' has the wrong data type or the result is too large or too small.
```

Justo por debajo todavía cabe, y por poco:

```dax
EVALUATE
ROW(
  "exp_709_enorme", EXP(709) > POWER(10, 307),
  "exp_1", ROUND(EXP(1), 6),
  "exp_menos_1", ROUND(EXP(-1), 6),
  "producto_es_1", ROUND(EXP(1) * EXP(-1), 10)
)
```

```result
exp_709_enorme | exp_1 | exp_menos_1 | producto_es_1
True | 2.718282 | 0.367879 | 1
```

709 y 710 son la frontera del `double`. Un exponente que venga de datos y crezca sin techo
—una tasa acumulada, por ejemplo— llega ahí antes de lo que parece.

## 3. Es la inversa de `LN`, y por eso deshace una suma de logaritmos

```dax
EVALUATE
VAR Factores = { 1.10, 1.05, 1.20 }
RETURN
ROW(
  "ln_ida_vuelta", ROUND(EXP(LN(7)), 10),
  "producto", ROUND(PRODUCTX(Factores, [Value]), 6),
  "por_logaritmos", ROUND(EXP(SUMX(Factores, LN([Value]))), 6)
)
```

```result
ln_ida_vuelta | producto | por_logaritmos
7 | 1.386 | 1.386
```

Las dos últimas columnas son la misma cuenta por dos caminos. Ese rodeo es lo que permite
calcular una media geométrica con las herramientas que hay — ver [`ln`](./ln.md).

Ver [`ln`](./ln.md), [`power`](./power.md) y [`sinh`](./sinh.md).
