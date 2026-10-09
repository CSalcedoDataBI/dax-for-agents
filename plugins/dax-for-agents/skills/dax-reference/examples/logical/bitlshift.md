---
function: BITLSHIFT
model: ninguno
---

# BITLSHIFT — examples

## 1. Shifting left is multiplying by powers of two

As long as it fits. That "as long as it fits" is this card's entire content.

```dax
EVALUATE
ROW(
  "uno_por_1",   BITLSHIFT(1, 1),
  "uno_por_8",   BITLSHIFT(1, 8),
  "cinco_por_4", BITLSHIFT(5, 4),
  "por_cero",    BITLSHIFT(5, 0)
)
```

```result
uno_por_1 | uno_por_8 | cinco_por_4 | por_cero
2 | 256 | 80 | 5
```

## 2. Near 64 bits it stops being a multiplication

The DAX integer is 64-bit signed. On reaching the top, the bit falling off the edge is not lost
silently in the way you would expect: it flips the sign or overflows.

```dax
EVALUATE
ROW(
  "bit_30", BITLSHIFT(1, 30),
  "bit_40", BITLSHIFT(1, 40),
  "bit_62", BITLSHIFT(1, 62),
  "bit_63", BITLSHIFT(1, 63)
)
```

```result
bit_30 | bit_40 | bit_62 | bit_63
1073741824 | 1099511627776 | 4611686018427387904 | -9223372036854775808
```

If your flag mask can grow, this is the real ceiling, and it is worth knowing before a report
starts returning negatives.

## 3. A negative shift moves the other way

It gives no error: `BITLSHIFT(x, -n)` does the same as `BITRSHIFT(x, n)`. Worth knowing, because
it means a wrong sign in a variable goes undetected — the calculation carries on and returns a
perfectly believable number in the opposite direction.

```dax
EVALUATE
ROW(
  "negativo_1",       BITLSHIFT(-1, 1),
  "negativo_4",       BITLSHIFT(-4, 2),
  "corrimiento_neg",  BITLSHIFT(8, -1),
  "cero_desplazado",  BITLSHIFT(0, 10)
)
```

```result
negativo_1 | negativo_4 | corrimiento_neg | cero_desplazado
-2 | -16 | 4 | 0
```

See [`bitrshift`](./bitrshift.md) for the other direction.
