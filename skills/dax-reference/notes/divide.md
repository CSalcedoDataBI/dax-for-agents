## Trap: `/` does not protect you, and the "0" you return changes the chart

`DIVIDE` returns **(blank)** when dividing by zero, not an error. That blank is deliberate: it
makes the category disappear from the visual instead of drawing a zero nobody measured.

```dax
EVALUATE
ROW(
  "DIVIDE_1_0_es_blank", ISBLANK(DIVIDE(1,0)),
  "DIVIDE_1_0_alt0",     DIVIDE(1,0,0)
)
```

| expression | result |
|---|---|
| `ISBLANK(DIVIDE(1,0))` | **TRUE** |
| `DIVIDE(1,0,0)` | 0 |

The third argument is a business decision, not a safety measure: use `0` only if "there was no
divisor" and "the result was zero" mean the same thing to whoever reads the report. They almost
never do.

## What Microsoft says, and is not in the card
They recommend `DIVIDE` over `IF(divisor = 0, BLANK(), a/b)` because the `IF` evaluates the
divisor twice. It is in
[their best-practices page](https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator),
not in the function's page, which is why this note exists.

That is **their** recommendation, quoted, not a measurement from this repo: on this model both
forms take the same time within the noise.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
