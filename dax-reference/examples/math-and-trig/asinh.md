---
function: ASINH
model: ninguno
---

# ASINH — ejemplos

## 1. Acepta cualquier número, que la hace la excepción de la familia

Ni dominio ni agujeros. Es la única de las inversas hiperbólicas que no aborta nunca.

```dax
EVALUATE
ROW(
  "cero", ASINH(0),
  "negativo", ROUND(ASINH(-1), 6),
  "positivo", ROUND(ASINH(1), 6),
  "enorme", ROUND(ASINH(1000000), 6)
)
```

```result
cero | negativo | positivo | enorme
0 | -0.881374 | 0.881374 | 14.508658
```

Compara con [`acosh`](./acosh.md), que exige 1 o más, y con [`atanh`](./atanh.md), que exige
estar dentro de (-1, 1). `ASINH` se traga todo.

## 2. El blanco sale en blanco, y eso también la separa de sus vecinas

```dax
EVALUATE
ROW(
  "blanco", ASINH(BLANK()),
  "es_blanco", ISBLANK(ASINH(BLANK())),
  "cero", ASINH(0),
  "acosh_blanco", IFERROR(ACOSH(BLANK()), "aborta")
)
```

```result
blanco | es_blanco | cero | acosh_blanco
(blank) | True | 0 | aborta
```

El blanco entra como cero, `ASINH(0)` es cero, y ese cero vuelve a salir blanco. En la misma
familia, `ACOSH` con un blanco **mata la consulta**. Elegir mal entre las dos cambia el
resultado de un hueco de «se ignora» a «no hay informe».

## 3. Es impar, es la inversa exacta de `SINH`, y es un logaritmo

```dax
EVALUATE
ROW(
  "impar", ROUND(ASINH(2) + ASINH(-2), 10),
  "ida_y_vuelta", ROUND(ASINH(SINH(3)), 10),
  "formula_cerrada", ROUND(ASINH(2) - LN(2 + SQRT(5)), 10),
  "asinh_2", ROUND(ASINH(2), 6)
)
```

```result
impar | ida_y_vuelta | formula_cerrada | asinh_2
0 | 3 | 0 | 1.443635
```

`ASINH(x) = LN(x + √(x² + 1))`. El `+1` en vez del `-1` de [`acosh`](./acosh.md) es justo lo que
elimina el dominio: la raíz nunca se queda sin argumento.

Ver [`sinh`](./sinh.md), [`acosh`](./acosh.md) y [`atanh`](./atanh.md).
