---
function: RADIANS
model: ninguno
---

# RADIANS — examples

## 1. Without it, the trigonometric functions read degrees as radians

And they do not fail: they return a perfectly believable number that is wrong.

```dax
EVALUATE
ROW(
  "sen_90_bien", ROUND(SIN(RADIANS(90)), 10),
  "sen_90_mal", ROUND(SIN(90), 6),
  "cos_180_bien", ROUND(COS(RADIANS(180)), 10),
  "cos_180_mal", ROUND(COS(180), 6)
)
```

```result
sen_90_bien | sen_90_mal | cos_180_bien | cos_180_mal
1 | 0.893997 | -1 | -0.59846
```

`SIN(90)` returns 0.894 because 90 **radians** is fourteen turns and change. No error, no
warning: just the wrong figure in the report.

## 2. It is `x × π / 180`, and the round trip closes

```dax
EVALUATE
ROW(
  "rad_180", ROUND(RADIANS(180), 10),
  "pi", ROUND(PI(), 10),
  "rad_90", ROUND(RADIANS(90), 10),
  "escrita_a_mano", ROUND(90 * PI() / 180, 10),
  "ida_y_vuelta", ROUND(DEGREES(RADIANS(37)), 10)
)
```

```result
rad_180 | pi | rad_90 | escrita_a_mano | ida_y_vuelta
3.141593 | 3.141593 | 1.570796 | 1.570796 | 37
```

Writing it by hand gives the same thing; `RADIANS` only makes clear what you are doing, which in
a long measure is worth more than saving characters.

## 3. It has no domain, and the blank comes out blank

```dax
EVALUATE
ROW(
  "blanco", RADIANS(BLANK()),
  "es_blanco", ISBLANK(RADIANS(BLANK())),
  "cero", RADIANS(0),
  "negativo", ROUND(RADIANS(-90), 10),
  "mil_grados", ROUND(RADIANS(1000), 6)
)
```

```result
blanco | es_blanco | cero | negativo | mil_grados
(blank) | True | 0 | -1.570796 | 17.453293
```

It accepts any number. A thousand degrees is nearly three turns, and `RADIANS` does not normalise
them — the trigonometric functions do not need it either, because they are periodic.

See [`degrees`](./degrees.md), its inverse, and [`pi`](./pi.md).
