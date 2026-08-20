---
function: FACT
model: ninguno
---

# FACT — ejemplos

## 1. Trunca los decimales, y ahí se separa de `GCD` y `LCM`

Las tres reciben números que deberían ser enteros. `FACT` **trunca** y las otras dos
**redondean**, así que la misma entrada da respuestas distintas según la función.

```dax
EVALUATE
ROW(
  "fact_4_9", FACT(4.9),
  "fact_4_1", FACT(4.1),
  "fact_4", FACT(4),
  "gcd_4_9_con_6", GCD(4.9, 6)
)
```

```result
fact_4_9 | fact_4_1 | fact_4 | gcd_4_9_con_6
24 | 24 | 24 | 1
```

`FACT(4.9)` es 24, o sea 4!. Pero `GCD(4.9, 6)` trata el 4,9 como **5** y devuelve 1 en vez del
2 que daría con 4. Dos reglas distintas en la misma familia — está medido en [`gcd`](./gcd.md).

## 2. El techo está en 170, y el blanco vale 1

```dax
EVALUATE ROW("desbordado", FACT(171))
```

```result
ERROR: An argument of function 'FACT' has the wrong data type or the result is too large or too small.
```

Justo debajo todavía cabe, y el blanco tiene una respuesta que sorprende:

```dax
EVALUATE
ROW(
  "fact_170_enorme", FACT(170) > POWER(10, 300),
  "fact_0", FACT(0),
  "fact_blanco", FACT(BLANK()),
  "negativo", IFERROR(FACT(-1), "aborta")
)
```

```result
fact_170_enorme | fact_0 | fact_blanco | negativo
True | 1 | 1 | aborta
```

`FACT(BLANK())` es **1**, no blanco: el blanco entra como cero y `0!` es uno, que no es cero,
así que no hay nada que colapsar. Misma mecánica que [`exp`](./exp.md) y [`cosh`](./cosh.md).
En una columna calculada eso significa que los huecos se rellenan con un 1 en silencio.

## 3. Crece tan rápido que 170 es poco margen

```dax
EVALUATE
ROW(
  "fact_10", FACT(10),
  "fact_20", FACT(20),
  "fact_50_orden", ROUND(LOG10(FACT(50)), 4),
  "fact_100_orden", ROUND(LOG10(FACT(100)), 4)
)
```

```result
fact_10 | fact_20 | fact_50_orden | fact_100_orden
3628800 | 2432902008176640000 | 64.4831 | 157.97
```

50! ya tiene 65 dígitos. Para combinatoria sobre datos reales, lo práctico es trabajar con
[`log10`](./log10.md) del factorial y no con el factorial, o el desbordamiento llega enseguida.

Ver [`gcd`](./gcd.md), [`lcm`](./lcm.md) y [`log10`](./log10.md).
