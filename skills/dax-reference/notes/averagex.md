## Trap: a `+ 0` changes the denominator

`AVERAGEX` **skips blanks**, just like `AVERAGE`: it divides by the rows that have a value, not
by all of them. The intuition that "the iterator walks every row and therefore counts the empty
ones" is false, and it is measured.

What does change the result is any expression that turns the blank into a zero. A `COALESCE`
added for safety, or a plain `+ 0`, moves the denominator.

Over five stores of which **two have blank square metres** (100 + 200 + 300 = 600; over 3 that is
200, over 5 it is 120):

```dax
EVALUATE
ROW(
  "AVERAGE",               AVERAGE(Tiendas[Metros]),
  "AVERAGEX_columna",      AVERAGEX(Tiendas, Tiendas[Metros]),
  "AVERAGEX_con_COALESCE", AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0)),
  "AVERAGEX_con_mas_cero", AVERAGEX(Tiendas, Tiendas[Metros] + 0)
)
```

| expression | result | divides by |
|---|---|---|
| `AVERAGE(Tiendas[Metros])` | **200** | 3 |
| `AVERAGEX(Tiendas, Tiendas[Metros])` | **200** | 3 |
| `AVERAGEX(Tiendas, COALESCE(Tiendas[Metros], 0))` | **120** | 5 |
| `AVERAGEX(Tiendas, Tiendas[Metros] + 0)` | **120** | 5 |

**`Tiendas[Metros] + 0` drops the average from 200 to 120.** The `+ 0` alters no existing value;
all it does is stop the blank being blank, and with that it enters the denominator.

The `COALESCE` is worse because it looks deliberate: whoever writes it believes they are
preventing an error, and what they are doing is changing the definition of the metric.

Neither number is wrong — it depends on whether "no data" means "not applicable" or "zero". What
is wrong is that the decision ends up hidden inside a `+ 0`.

## Not to be confused with
`AVERAGE`, which here gives exactly the same. The difference between them is not blank handling:
it is that `AVERAGEX` can average an **expression** and `AVERAGE` only a column.

> Model, data and queries in [`lab/blancos`](../../../lab/blancos/) — it opens in Power BI Desktop
> and runs. Measured on 2026-08-12.
