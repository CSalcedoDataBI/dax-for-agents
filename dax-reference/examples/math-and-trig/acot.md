---
function: ACOT
model: ninguno
---

# ACOT — ejemplos

## 1. Devuelve entre 0 y π, así que NO es simétrica como `ATAN`

Esta es la trampa, y es fácil de pisar porque `ATAN` sí es impar. `ACOT(-1)` **no** es
`-ACOT(1)`.

```dax
EVALUATE
ROW(
  "acot_1", ROUND(ACOT(1), 6),
  "acot_menos_1", ROUND(ACOT(-1), 6),
  "suma", ROUND(ACOT(1) + ACOT(-1), 6),
  "atan_menos_1", ROUND(ATAN(-1), 6)
)
```

```result
acot_1 | acot_menos_1 | suma | atan_menos_1
0.785398 | 2.356194 | 3.141593 | -0.785398
```

`ACOT(-1)` es 3π/4 y no -π/4. La suma da π, que es la propiedad real: `ACOT(-x) = π - ACOT(x)`.
Si conviertes a grados esperando -45 obtienes 135, y el signo del ángulo cambia el cuadrante.

## 2. En el cero vale π/2 — no aborta y no es blanco

Es la única de la familia que trata bien el cero, y por eso también trata bien el blanco.

```dax
EVALUATE
ROW(
  "acot_0", ROUND(ACOT(0), 6),
  "medio_pi", ROUND(PI() / 2, 6),
  "acot_blanco", ROUND(ACOT(BLANK()), 6),
  "cot_0_aborta", IFERROR(COT(0), "aborta")
)
```

```result
acot_0 | medio_pi | acot_blanco | cot_0_aborta
1.570796 | 1.570796 | 1.570796 | aborta
```

`ACOT(BLANK())` devuelve **π/2**, no blanco: el blanco entra como cero y `ACOT(0)` no es cero,
así que no hay nada que colapsar. En una columna calculada, los huecos se rellenan con 1,5708
en silencio. Mientras tanto [`cot`](./cot.md) aborta con el mismo blanco.

## 3. Complementa a `ATAN`: las dos suman π/2

```dax
EVALUATE
ROW(
  "acot_2", ROUND(ACOT(2), 6),
  "atan_2", ROUND(ATAN(2), 6),
  "suma", ROUND(ACOT(2) + ATAN(2), 6),
  "medio_pi", ROUND(PI() / 2, 6)
)
```

```result
acot_2 | atan_2 | suma | medio_pi
0.463648 | 1.107149 | 1.570796 | 1.570796
```

`ACOT(x) = π/2 - ATAN(x)` para cualquier x. Es la forma de escribirla si prefieres quedarte con
una sola función inversa, y además deja explícito el rango que estás usando.

Ver [`cot`](./cot.md), [`acoth`](./acoth.md) y [`degrees`](./degrees.md).
