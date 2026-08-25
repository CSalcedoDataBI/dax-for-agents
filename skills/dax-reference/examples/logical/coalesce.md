---
function: COALESCE
model: ninguno
---

# COALESCE — examples

## 1. It returns the first one that is NOT blank, and zero does count

Zero is not blank. It is the confusion that makes a `COALESCE` added "to be safe" return the zero
that came from the data instead of the default that was wanted.

```dax
EVALUATE
ROW(
  "blanco_luego_diez", COALESCE(BLANK(), 10),
  "cero_luego_diez",   COALESCE(0, 10),
  "vacio_luego_diez",  COALESCE("", 10),
  "todos_blancos",     ISBLANK(COALESCE(BLANK(), BLANK()))
)
```

```result
blanco_luego_diez | cero_luego_diez | vacio_luego_diez | todos_blancos
10 | 0 | (empty) | True
```

The empty string is not blank either: `COALESCE("", 10)` returns the empty string. If the source
brings `""` instead of nulls, `COALESCE` will do nothing and the problem will still be there.

## 2. It takes many arguments, but never just one

Unlike `AND` and `OR`, which are limited to two, `COALESCE` chains as many as needed. The limit is
at the other end:

```dax
EVALUATE
ROW(
  "tres_argumentos",  COALESCE(BLANK(), BLANK(), "tercero"),
  "cinco_argumentos", COALESCE(BLANK(), BLANK(), BLANK(), BLANK(), 5)
)
```

```result
tres_argumentos | cinco_argumentos
tercero | 5
```

With only one it aborts, and the message says so plainly:

```dax
EVALUATE ROW("uno_solo", COALESCE(BLANK()))
```

```result
ERROR: Too few arguments were passed to the COALESCE function. The minimum argument count for the function is 2.
```

## 3. It mixes types without complaining

You can give a numeric default to a text expression. It runs, and the problem shows up later,
when something tries to format or add up whatever came out.

```dax
EVALUATE
ROW(
  "texto_o_numero", COALESCE(BLANK(), 42),
  "numero_o_texto", COALESCE(BLANK(), "sin dato"),
  "suma_despues",   COALESCE(BLANK(), 42) + 1
)
```

```result
texto_o_numero | numero_o_texto | suma_despues
42 | sin dato | 43
```

It is the direct replacement for `IF(ISBLANK(x), y, x)` — shorter and without evaluating `x`
twice. See [`if`](./if.md).
