---
function: ABS
model: ninguno
---

# ABS — examples

## 1. The predictable part, and the text that converts itself

```dax
EVALUATE
ROW(
  "negativo", ABS(-7.5),
  "positivo", ABS(7.5),
  "cero", ABS(0),
  "texto", ABS("-3")
)
```

```result
negativo | positivo | cero | texto
7.5 | 7.5 | 0 | 3
```

The fourth column is an implicit conversion: the string `"-3"` is read as a number. It works,
but it depends on the model's culture — see [`convert`](./convert.md), where `"1.5"` comes out
as **15** in a Spanish model.

## 2. A blank comes out blank, and still equals zero

```dax
EVALUATE
ROW(
  "abs_blanco", ABS(BLANK()),
  "es_blanco", ISBLANK(ABS(BLANK())),
  "compara_con_cero", ABS(BLANK()) = 0,
  "abs_cero", ABS(0),
  "cero_es_blanco", ISBLANK(ABS(0))
)
```

```result
abs_blanco | es_blanco | compara_con_cero | abs_cero | cero_es_blanco
(blank) | True | True | 0 | False
```

The two middle claims look like they contradict each other and they do not. The blank goes in as
zero, `ABS(0)` is zero, and a zero that came from a blank comes back out as blank. A `0` written
by hand returns a zero that is **not** blank.

It matters when filtering: `FILTER(T, ABS(T[x]) = 0)` also keeps the rows where `x` is empty, not
only the ones that are zero.

## 3. It is what separates "deviation" from "error"

The real use of `ABS` is almost always this: a difference whose sign is beside the point, and a
sum that without it cancels itself out.

```dax
EVALUATE
VAR Desviaciones = { -3, 5, -2 }
RETURN
ROW(
  "suma_con_signo", SUMX(Desviaciones, [Value]),
  "suma_absoluta", SUMX(Desviaciones, ABS([Value])),
  "media_absoluta", ROUND(AVERAGEX(Desviaciones, ABS([Value])), 6)
)
```

```result
suma_con_signo | suma_absoluta | media_absoluta
0 | 10 | 3.333333
```

The first column says **0** and that does not mean there is no error: it means the errors
cancelled each other. That is the difference between a bias and a magnitude.

See [`sign`](./sign.md), which answers the other half of the question.
