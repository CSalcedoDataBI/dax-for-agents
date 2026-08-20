---
function: BITLSHIFT
model: ninguno
---

# BITLSHIFT — ejemplos

## 1. Desplazar a la izquierda es multiplicar por potencias de dos

Mientras quepa. Ese «mientras quepa» es todo el contenido de esta ficha.

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

## 2. Cerca de los 64 bits deja de ser una multiplicación

El entero de DAX tiene 64 bits con signo. Al llegar arriba, el bit que sale por el borde no
se pierde en silencio de la forma que uno espera: cambia el signo o desborda.

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

Si tu máscara de banderas puede crecer, este es el techo real, y conviene conocerlo antes de
que un informe empiece a dar negativos.

## 3. Un corrimiento negativo desplaza al otro lado

No da error: `BITLSHIFT(x, -n)` hace lo mismo que `BITRSHIFT(x, n)`. Está bien saberlo, porque
significa que un signo equivocado en una variable no se detecta — el cálculo sigue y devuelve
un número perfectamente creíble en la dirección contraria.

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

Ver [`bitrshift`](./bitrshift.md) para el sentido contrario.
