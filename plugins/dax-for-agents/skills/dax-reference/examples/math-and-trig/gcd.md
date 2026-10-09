---
function: GCD
model: ninguno
---

# GCD — examples

## 1. It takes only TWO arguments, not Excel's 255

This is the first thing that breaks when porting a formula. In Excel `GCD` accepts up to 255
numbers; in DAX, two.

```dax
EVALUATE ROW("tres_numeros", GCD(24, 36, 60))
```

```result
ERROR: Too many arguments were passed to the GCD function. The maximum argument count for the function is 2.
```

With more than two you have to nest, and this does work because the greatest common divisor is
associative:

```dax
EVALUATE
ROW(
  "dos", GCD(24, 36),
  "tres_anidada", GCD(GCD(24, 36), 60),
  "coprimos", GCD(7, 9),
  "iguales", GCD(7, 7)
)
```

```result
dos | tres_anidada | coprimos | iguales
12 | 12 | 1 | 7
```

## 2. It rounds decimals — Excel truncates them

Same formula, different answer on migration. And `FACT`, in the same repertoire, does truncate.

```dax
EVALUATE
ROW(
  "cuatro_coma_cuatro", GCD(4.4, 6),
  "cuatro_coma_cinco", GCD(4.5, 6),
  "cuatro_coma_seis", GCD(4.6, 6),
  "cuatro", GCD(4, 6),
  "cinco", GCD(5, 6)
)
```

```result
cuatro_coma_cuatro | cuatro_coma_cinco | cuatro_coma_seis | cuatro | cinco
2 | 1 | 1 | 2 | 1
```

4.4 behaves like 4 and 4.5 like 5. If you expected truncation, 4.5 gives you 1 where you thought
you had 2. Round it yourself beforehand with whatever rule you want, and stop depending on this
one.

## 3. Negatives abort; zero and blank do not

```dax
EVALUATE
ROW(
  "cero", GCD(0, 5),
  "blanco", GCD(BLANK(), 5),
  "ambos_cero", GCD(0, 0),
  "negativo", IFERROR(GCD(-4, 6), "aborta")
)
```

```result
cero | blanco | ambos_cero | negativo
5 | 5 | 0 | aborta
```

`GCD(0, n)` is `n`, which is the correct definition. The blank goes in as zero and behaves the
same. A negative, on the other hand, kills the query — and in real data the negative arrives
before the zero does.

See [`lcm`](./lcm.md), which shares these rules, and [`fact`](./fact.md), which does not.
