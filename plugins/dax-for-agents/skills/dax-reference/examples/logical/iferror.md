---
function: IFERROR
model: ninguno
---

# IFERROR — examples

## 1. It swallows the error you wanted to see

That is its job and also its danger. An `IFERROR` placed around a large expression hides any
failure occurring inside, including the ones that had nothing to do with the case you meant to
cover.

```dax
EVALUATE
ROW(
  "division_por_cero", IFERROR(1 / 0, "capturado"),
  "texto_a_numero",    IFERROR(VALUE("no soy un número"), "capturado"),
  "sin_error",         IFERROR(10 / 2, "capturado")
)
```

```result
division_por_cero | texto_a_numero | sin_error
capturado | capturado | 5
```

The first two return the same thing, and they are different problems: one is arithmetic, the
other is data of the wrong shape. With an `IFERROR` around both, the report cannot tell them
apart.

## 2. For division, DIVIDE is better

`DIVIDE` solves the specific case without switching off every other error, and the engine
understands it better than an `IFERROR` wrapped around a division.

```dax
EVALUATE
ROW(
  "iferror",        IFERROR(1 / 0, 0),
  "divide",         DIVIDE(1, 0, 0),
  "divide_sin_alt", ISBLANK(DIVIDE(1, 0)),
  "cero_entre_cero", DIVIDE(0, 0, -1)
)
```

```result
iferror | divide | divide_sin_alt | cero_entre_cero
0 | 0 | True | -1
```

`DIVIDE` without a third argument returns blank, not zero. The same decision again.

## 3. The alternative value does not have to be of the same type

And there the next problem starts: what it returns may not serve whatever came after.

```dax
EVALUATE
ROW(
  "numero_o_texto", IFERROR(1 / 0, "sin dato"),
  "suma_despues",   IFERROR(1 / 0, 0) + 100,
  "anidado",        IFERROR(IFERROR(1 / 0, VALUE("x")), "los dos fallaron")
)
```

```result
numero_o_texto | suma_despues | anidado
sin dato | 100 | los dos fallaron
```

See [`coalesce`](./coalesce.md), which is usually what whoever writes an `IFERROR` actually
wants: not to catch an error, but to substitute a blank.
