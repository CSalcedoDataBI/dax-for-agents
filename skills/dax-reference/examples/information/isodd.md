---
function: ISODD
model: ninguno
---

# ISODD — examples

## 1. It is the exact complement of `ISEVEN`, decimals included

```dax
EVALUATE
ROW(
  "siete", ISODD(7),
  "ocho", ISODD(8),
  "complementarios_7", ISODD(7) = NOT ISEVEN(7),
  "complementarios_2_5", ISODD(2.5) = NOT ISEVEN(2.5),
  "complementarios_blanco", ISODD(BLANK()) = NOT ISEVEN(BLANK())
)
```

```result
siete | ocho | complementarios_7 | complementarios_2_5 | complementarios_blanco
True | False | True | True | True
```

There is never a value that is both or neither. That is not obvious: in
[`sign`](../math-and-trig/sign.md), for instance, there is a fourth case.

## 2. It rounds decimals, and that is why 2.5 is odd and 3.5 is not

```dax
EVALUATE
ROW(
  "dos_coma_cinco", ISODD(2.5),
  "tres_coma_cinco", ISODD(3.5),
  "dos_coma_tres", ISODD(2.3),
  "tres_coma_siete", ISODD(3.7)
)
```

```result
dos_coma_cinco | tres_coma_cinco | dos_coma_tres | tres_coma_siete
True | False | False | False
```

2.5 behaves like 3 and 3.5 like 4; 3.7 goes up to 4 and also comes out even. The half does not
"go up": it **moves away from zero**, and with negatives that means down. Measured,
`ISODD(-2.5)` is true because it looks at -3, not -2; `ISODD(-1.5)` is false because it looks at
-2, not -1. With positives the two rules coincide, and that is why the confusion goes unnoticed
until a negative appears. Same rule as [`iseven`](./iseven.md).

## 3. A blank is NOT odd, and that is the gap it leaves

```dax
EVALUATE
ROW(
  "blanco", ISODD(BLANK()),
  "blanco_es_par", ISEVEN(BLANK()),
  "cero", ISODD(0),
  "menos_tres", ISODD(-3)
)
```

```result
blanco | blanco_es_par | cero | menos_tres
False | True | False | True
```

Filtering with `ISODD` discards the rows with no data; filtering with `ISEVEN` keeps them. Two
filters that look like they split the table in half and do not — they always send the gaps to the
same side.

See [`iseven`](./iseven.md) and [`odd`](../math-and-trig/odd.md).
