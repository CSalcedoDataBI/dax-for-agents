---
function: OR
model: ninguno
---

# OR — examples

## 1. Two arguments, just like AND

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

And with three, it aborts:

```dax
EVALUATE ROW("tres_argumentos", OR(1 = 2, 2 = 3, 3 = 3))
```

```result
ERROR: Too many arguments were passed to the OR function. The maximum argument count for the function is 2.
```

With more than two conditions, `||` reads better than an `OR` nested three levels deep.

## 2. The blank does not rescue: it counts as false

An `OR` between a blank and a false gives false. Where it usually hurts is the opposite of what
you expect: you write `OR(column, other)` thinking "if either has data", and what you are actually
asking is whether either is different from zero.

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

## 3. Do not lean on short-circuiting

It is unwise to assume `OR` stops evaluating the second argument once the first is already true.
If the second can fail, guard it yourself — here with `DIVIDE`, which raises no error, rather than
with a raw division.

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

See [`and`](./and.md) and [`if-eager`](./if-eager.md), where this is the central subject.
