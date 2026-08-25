---
function: OR
model: ninguno
---

# OR — ejemplos

## 1. Dos argumentos, igual que AND

```dax
EVALUATE
ROW(
  "dos_condiciones", OR(1 = 2, 2 = 2),
  "anidada",         OR(1 = 2, OR(2 = 3, 3 = 3)),
  "operador",        1 = 2 || 2 = 3 || 3 = 3
)
```

```result
dos_condiciones | anidada | operador
True | True | True
```

Y con tres, aborta:

```dax
EVALUATE ROW("tres_argumentos", OR(1 = 2, 2 = 3, 3 = 3))
```

```result
ERROR: Too many arguments were passed to the OR function. The maximum argument count for the function is 2.
```

Con más de dos condiciones, `||` se lee mejor que un `OR` anidado tres niveles.

## 2. El blanco no rescata: cuenta como falso

Un `OR` entre un blanco y un falso da falso. Donde suele doler es al revés de lo que se
espera: se escribe `OR(columna, otra)` pensando «si alguna tiene dato», y lo que se pregunta
en realidad es si alguna es distinta de cero.

```dax
EVALUATE
ROW(
  "blanco_o_falso",  OR(BLANK(), FALSE()),
  "blanco_o_cierto", OR(BLANK(), TRUE()),
  "cero_o_cero",     OR(0, 0),
  "cero_o_uno",      OR(0, 1)
)
```

```result
blanco_o_falso | blanco_o_cierto | cero_o_cero | cero_o_uno
False | True | False | True
```

## 3. No te apoyes en el cortocircuito

No conviene dar por hecho que `OR` deja de evaluar el segundo argumento cuando el primero ya
es cierto. Si el segundo puede fallar, protégelo tú — aquí con `DIVIDE`, que no lanza error,
en vez de con una división cruda.

```dax
EVALUATE
ROW(
  "primera_cierta", OR(TRUE(), 1 = 1),
  "con_divide",     OR(TRUE(), DIVIDE(1, 0) = 0),
  "con_iserror",    OR(TRUE(), ISERROR(1 / 0))
)
```

```result
primera_cierta | con_divide | con_iserror
True | True | True
```

Ver [`and`](./and.md) y [`if-eager`](./if-eager.md), donde esto mismo es el tema central.
