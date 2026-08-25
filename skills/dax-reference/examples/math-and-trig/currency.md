---
function: CURRENCY
model: ninguno
---

# CURRENCY — examples

## 1. It exists so that sums of money reconcile, and that difference can be seen

A `double` does not represent 0.1 exactly. `CURRENCY` uses fixed point with four decimals, and
there money arithmetic behaves the way you expect.

```dax
EVALUATE
ROW(
  "en_coma_flotante", 0.1 + 0.2 = 0.3,
  "en_currency", CURRENCY(0.1) + CURRENCY(0.2) = CURRENCY(0.3),
  "residuo_flotante_x1e17", ROUND((0.1 + 0.2 - 0.3) * POWER(10, 17), 4)
)
```

```result
en_coma_flotante | en_currency | residuo_flotante_x1e17
False | True | 5.5511
```

The first column is false. The third shows why: there is 5.55 × 10⁻¹⁷ left over, which the output
format does not show but the comparison does see. With `CURRENCY` the equality holds.

## 2. Four decimals, rounding away from zero

It is not a display format: **it clips the value**.

```dax
EVALUATE
ROW(
  "hacia_arriba", CURRENCY(0.33335),
  "hacia_abajo", CURRENCY(0.33334),
  "negativo", CURRENCY(-0.33335),
  "un_tercio", CURRENCY(1/3)
)
```

```result
hacia_arriba | hacia_abajo | negativo | un_tercio
0.3334 | 0.3333 | -0.3334 | 0.3333
```

The fifth decimal decides and is then lost. On a unit price with more than four decimals —
exchange rates, cost per thousand — that is a real loss multiplied by the quantity.

## 3. With text it inherits the culture trap

```dax
EVALUATE
ROW(
  "cadena_con_coma", CURRENCY("12,3456"),
  "cadena_con_punto", CURRENCY("12.3456"),
  "numero_directo", CURRENCY(12.3456)
)
```

```result
cadena_con_coma | cadena_con_punto | numero_directo
12.3456 | 123456 | 12.3456
```

In this model, which is **es-ES**, `CURRENCY("12.3456")` returns **123456**: the dot is read as a
thousands separator and the four decimals become four whole digits. It is the same hole as
[`convert`](./convert.md), multiplied by ten thousand.

The practical rule: do not convert text to money. Convert to a number at the source, where the
culture is yours to control.

See [`convert`](./convert.md) and [`round`](./round.md).
