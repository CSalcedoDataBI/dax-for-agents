---
function: COT
model: ninguno
---

# COT — ejemplos

## 1. Es 1/TAN, y por eso explota donde `TAN` vale cero

```dax
EVALUATE
ROW(
  "cot_1", ROUND(COT(1), 6),
  "uno_entre_tan_1", ROUND(1 / TAN(1), 6),
  "identicos", ROUND(COT(1) - 1 / TAN(1), 10),
  "cot_pi_4", ROUND(COT(PI() / 4), 10)
)
```

```result
cot_1 | uno_entre_tan_1 | identicos | cot_pi_4
0.642093 | 0.642093 | 0 | 1
```

`COT(π/4)` es exactamente 1, que es el ángulo de 45 grados. El argumento va en **radianes**:
`COT(45)` no es eso — ver [`radians`](./radians.md).

## 2. El cero aborta la consulta, y el blanco también

`TAN(0)` es cero, así que su inverso no existe. DAX no devuelve infinito ni blanco: mata la
consulta.

```dax
EVALUATE ROW("cot_de_cero", COT(0))
```

```result
ERROR: Division by zero has occurred when evaluating function 'COT'.
```

El mensaje dice **división por cero** y no el error genérico de argumento: internamente `COT`
es `1 / TAN`, y ahí se ve. Y el blanco entra como cero, así que hace lo mismo:

```dax
EVALUATE
ROW(
  "blanco", IFERROR(COT(BLANK()), "aborta"),
  "cero", IFERROR(COT(0), "aborta"),
  "en_pi", COT(PI()),
  "tan_de_pi_x1e16", ROUND(TAN(PI()) * POWER(10, 16), 6),
  "casi_cero", ROUND(COT(0.001), 4)
)
```

```result
blanco | cero | en_pi | tan_de_pi_x1e16 | casi_cero
aborta | aborta | -8162276138809536 | -1.225148 | 999.9997
```

La tercera columna es lo interesante y no es lo que uno espera: **`COT(PI())` no aborta.** π
también es un cero de la tangente, pero `PI()` no es π — es el `double` más cercano, y
`TAN(PI())` vale -1,2 × 10⁻¹⁶ en vez de cero. Dividir uno entre eso da ocho mil billones en
negativo, un número perfectamente formado y perfectamente inútil.

O sea que el único punto donde `COT` protesta es el cero **exacto**. En los demás polos
devuelve basura enorme sin decir nada, que es bastante peor que abortar.

## 3. Es impar y periódica con período π, no 2π

```dax
EVALUATE
ROW(
  "cot_1", ROUND(COT(1), 6),
  "cot_1_mas_pi", ROUND(COT(1 + PI()), 6),
  "impar", ROUND(COT(1) + COT(-1), 10),
  "periodo_2pi_tambien", ROUND(COT(1 + 2 * PI()), 6)
)
```

```result
cot_1 | cot_1_mas_pi | impar | periodo_2pi_tambien
0.642093 | 0.642093 | 0 | 0.642093
```

Se repite cada π, la mitad que el seno y el coseno. Si estás modelando algo cíclico con `COT`,
el ciclo dura la mitad de lo que crees.

Ver [`coth`](./coth.md), [`acot`](./acot.md) y [`radians`](./radians.md).
