---
function: ISEVEN
model: ninguno
---

# ISEVEN — examples

## 1. Not to be confused with `EVEN`, which returns a number

Two functions with almost the same name and different return types. `ISEVEN` asks;
[`even`](../math-and-trig/even.md) rounds.

```dax
EVALUATE
ROW(
  "iseven_3", ISEVEN(3),
  "even_3", EVEN(3),
  "iseven_4", ISEVEN(4),
  "even_4", EVEN(4)
)
```

```result
iseven_3 | even_3 | iseven_4 | even_4
False | 4 | True | 4
```

`EVEN(3)` and `EVEN(4)` give the same thing; `ISEVEN` tells them apart. If the goal is to ask,
this is the right one.

## 2. With decimals it ROUNDS, it does not truncate — and that is why 2.5 is odd

Here is what the signature does not say, and it contradicts what `FACT` does in the same
repertoire.

```dax
EVALUATE
ROW(
  "dos_coma_tres", ISEVEN(2.3),
  "dos_coma_cinco", ISEVEN(2.5),
  "tres_coma_cinco", ISEVEN(3.5),
  "impar_de_dos_coma_cinco", ISODD(2.5)
)
```

```result
dos_coma_tres | dos_coma_cinco | tres_coma_cinco | impar_de_dos_coma_cinco
True | False | True | True
```

2.3 behaves like 2 (even) and 2.5 like **3** (odd): it rounds to the nearest integer, and the
exact half **moves away from zero**. 3.5 goes to 4 and is even again; `ISEVEN(-2.5)` looks at -3,
not -2, so it is odd too. Saying "upwards" is only right for positives — it is the same
distinction that separates [`even`](../math-and-trig/even.md) from `CEILING`. It is the opposite
of what [`fact`](../math-and-trig/fact.md) does.

## 3. A blank counts as EVEN

```dax
EVALUATE
ROW(
  "blanco_es_par", ISEVEN(BLANK()),
  "blanco_es_impar", ISODD(BLANK()),
  "cero_es_par", ISEVEN(0),
  "texto_numerico", ISEVEN("4")
)
```

```result
blanco_es_par | blanco_es_impar | cero_es_par | texto_numerico
True | False | True | True
```

The blank goes in as zero, and zero is even. If you split rows into two groups with
`IF(ISEVEN([x]), "par", "impar")`, every row with no data ends up in the even group without
anybody asking for it.

See [`isodd`](./isodd.md) and [`even`](../math-and-trig/even.md).
