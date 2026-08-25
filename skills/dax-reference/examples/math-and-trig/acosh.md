---
function: ACOSH
model: ninguno
---

# ACOSH — ejemplos

## 1. Solo acepta 1 o más, y el blanco cae fuera

`COSH` nunca baja de 1, así que su inversa no tiene nada que devolver por debajo de ahí.

```dax
EVALUATE ROW("por_debajo_de_uno", ACOSH(0.5))
```

```result
ERROR: An argument of function 'ACOSH' has the wrong data type or the result is too large or too small.
```

```dax
EVALUATE
ROW(
  "uno", ACOSH(1),
  "medio", IFERROR(ACOSH(0.5), "aborta"),
  "cero", IFERROR(ACOSH(0), "aborta"),
  "blanco", IFERROR(ACOSH(BLANK()), "aborta")
)
```

```result
uno | medio | cero | blanco
0 | aborta | aborta | aborta
```

`ACOSH(1)` es exactamente **0** — es el suelo del dominio y el cero de la función. El blanco
entra como cero y el cero está prohibido, así que un hueco en los datos tumba la consulta.
Compara con [`asinh`](./asinh.md), que acepta cualquier número.

## 2. No es simétrica: pierde el signo que `COSH` ya había perdido

```dax
EVALUATE
ROW(
  "cosh_2", ROUND(COSH(2), 6),
  "cosh_menos_2", ROUND(COSH(-2), 6),
  "acosh_de_eso", ROUND(ACOSH(COSH(-2)), 10),
  "no_recupera_el_signo", ACOSH(COSH(-2)) = -2
)
```

```result
cosh_2 | cosh_menos_2 | acosh_de_eso | no_recupera_el_signo
3.762196 | 3.762196 | 2 | False
```

`COSH(-2)` y `COSH(2)` son el mismo número, así que `ACOSH` devuelve **2** y no -2. El ida y
vuelta solo cierra para valores no negativos, que es lo que significa que `COSH` no sea
inyectiva.

## 3. Es un logaritmo disfrazado

```dax
EVALUATE
ROW(
  "acosh_2", ROUND(ACOSH(2), 6),
  "formula_cerrada", ROUND(LN(2 + SQRT(3)), 6),
  "identicos", ROUND(ACOSH(2) - LN(2 + SQRT(3)), 10),
  "crece_despacio", ROUND(ACOSH(1000), 6)
)
```

```result
acosh_2 | formula_cerrada | identicos | crece_despacio
1.316958 | 1.316958 | 0 | 7.600902
```

`ACOSH(x) = LN(x + √(x² - 1))`. Como todo logaritmo, crece muy despacio: para x = 1000 apenas
llega a 7,6.

Ver [`cosh`](./cosh.md), [`asinh`](./asinh.md) y [`ln`](./ln.md).
