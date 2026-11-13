---
function: COT
model: ninguno
---

# COT — examples

## 1. It is 1/TAN, and that is why it blows up where `TAN` is zero

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

`COT(π/4)` is exactly 1, which is the 45-degree angle. The argument is in **radians**: `COT(45)`
is not that — see [`radians`](./radians.md).

## 2. Zero aborts the query, and so does the blank

`TAN(0)` is zero, so its reciprocal does not exist. DAX returns neither infinity nor blank: it
kills the query.

```dax
EVALUATE ROW("cot_de_cero", COT(0))
```

```result
ERROR: Division by zero has occurred when evaluating function 'COT'.
```

The message says **division by zero** and not the generic argument error: internally `COT` is
`1 / TAN`, and there it shows. And the blank goes in as zero, so it does the same:

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

The third column is the interesting one and it is not what you would expect: **`COT(PI())` does
not abort.** π is also a zero of the tangent, but `PI()` is not π — it is the nearest `double`,
and `TAN(PI())` is -1.2 × 10⁻¹⁶ rather than zero. Dividing one by that gives eight quadrillion
negative, a perfectly well-formed and perfectly useless number.

So the only point where `COT` complains is the **exact** zero. At the other poles it returns huge
garbage and says nothing, which is a good deal worse than aborting.

## 3. It is odd and periodic with period π, not 2π

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

It repeats every π, half of what the sine and cosine do. If you are modelling something cyclical
with `COT`, the cycle lasts half as long as you think.

See [`coth`](./coth.md), [`acot`](./acot.md) and [`radians`](./radians.md).
