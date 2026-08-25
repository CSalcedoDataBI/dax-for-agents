## Trap: `BLANK() = 0` is true, and so is `BLANK() = ""`

In a comparison, the blank is coerced to the type of the other operand. So a filter
`[Importe] = 0` **also captures the blanks**, and `[Texto] = ""` captures the empties.

```dax
EVALUATE
ROW(
  "BLANK_mas_20",        BLANK() + 20,
  "BLANK_igual_0",       BLANK() = 0,
  "BLANK_estricto_0",    BLANK() == 0,
  "BLANK_igual_vacio",   BLANK() = "",
  "BLANK_estricto_vacio", BLANK() == ""
)
```

| expression | result |
|---|---|
| `BLANK() + 20` | **20** |
| `BLANK() = 0` | **TRUE** |
| `BLANK() == 0` | **FALSE** |
| `BLANK() = ""` | **TRUE** |
| `BLANK() == ""` | **FALSE** |

To tell "there is no data" from "the data is zero" you have two tools, and the difference between
them is a single character:

- **`==`** is **strict** equality: it does not coerce the blank, so `[Importe] == 0` leaves the
  blanks out while `[Importe] = 0` pulls them in.
- **`ISBLANK`** asks about the blank directly, and it is what reads best when that is the
  question.

What does not work is a bare `= 0`, which is exactly what gets written without thinking.

## Not to be confused with
SQL. `NULL = 0` is unknown in SQL; in DAX it is true. The right analogy is Excel's empty cell, not
`NULL`.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
