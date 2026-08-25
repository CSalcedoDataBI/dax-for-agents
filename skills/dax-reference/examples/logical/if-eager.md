---
function: IF.EAGER
model: ninguno
---

# IF.EAGER — examples

## 1. It returns exactly the same as IF

And that is the first thing to understand: **it does not exist to change the result**. If it ever
returns something different from `IF`, that is a bug, not a function.

```dax
EVALUATE
ROW(
  "if_verdadero",       IF(1 = 1, "sí", "no"),
  "if_eager_verdadero", IF.EAGER(1 = 1, "sí", "no"),
  "if_falso",           IF(1 = 2, "sí", "no"),
  "if_eager_falso",     IF.EAGER(1 = 2, "sí", "no")
)
```

```result
if_verdadero | if_eager_verdadero | if_falso | if_eager_falso
sí | sí | no | no
```

## 2. The difference is WHEN the branches are evaluated

`IF` may skip the branch that is not taken. `IF.EAGER` always evaluates both. The reason it
exists is the query plan: sometimes evaluating both at once is cheaper than branching.

**That difference does not show in the result**, and this example demonstrates it that way on
purpose: both forms return the same thing even though the discarded branch contains a division by
zero guarded with `DIVIDE`. Anyone looking for a difference in value will not find one, and that
is what has to be known before swapping one for the other.

```dax
EVALUATE
ROW(
  "if_rama_muerta",       IF(1 = 1, "tomada", DIVIDE(1, 0)),
  "if_eager_rama_muerta", IF.EAGER(1 = 1, "tomada", DIVIDE(1, 0)),
  "ambas_validas",        IF.EAGER(1 = 2, DIVIDE(10, 2), DIVIDE(20, 2))
)
```

```result
if_rama_muerta | if_eager_rama_muerta | ambas_validas
tomada | tomada | 10
```

## 3. The branch not taken can still cost you

If the discarded branch is expensive, `IF.EAGER` pays for it anyway. Here both branches return
the same thing and the difference is in the work, not the number — which is why this example
shows identical values: **it is the proof that the only thing that changes is the cost**.

```dax
EVALUATE
ROW(
  "if_barato",       IF(1 = 1, 1, SUMX(GENERATESERIES(1, 100000), [Value])),
  "if_eager_caro",   IF.EAGER(1 = 1, 1, SUMX(GENERATESERIES(1, 100000), [Value])),
  "lo_que_costaba",  SUMX(GENERATESERIES(1, 100000), [Value])
)
```

```result
if_barato | if_eager_caro | lo_que_costaba
1 | 1 | 5000050000
```

Measuring that difference needs volume and a cold engine: that lives in
[`lab/rendimiento`](../../../../lab/rendimiento/), not here.
