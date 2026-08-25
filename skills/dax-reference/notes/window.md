## Trap: the window got fixed, not the number being averaged

`WINDOW` takes an explicit `relation` so it does not inherit the default filter over
`ALLSELECTED()` — the trap already documented by
[`dax-window-functions`](../../dax-window-functions/SKILL.md#the-gotchas-read-before-shipping).
But fixing the `relation` only fixes **which rows the window sees**. The metric `AVERAGEX`
averages on each row is still evaluated through a context transition, and that transition
**combines** with any other filter that was already active — it does not replace it.

It is the same trap as [`ALL`](./all.md) — *it clears the filters on its table, and only those* —
one floor further down, where nobody looks: inside each row `AVERAGEX` opens.

### The scenario: a 3-month moving average, with year and month filtered at once

Any report with a `Year` slicer and a matrix at `YearMonth` level leaves **both filters alive at
once** — even though one implies the other. `Year = 2024` and `YearMonth = "2024-02"` are
redundant, but they live in different columns of the same table, and that is enough.

```dax
DEFINE
    FUNCTION Contoso.Lab.MediaMovil3M = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
            metric
        )
    FUNCTION Contoso.Lab.MediaMovil3M_Corregida = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            ADDCOLUMNS(
                WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
                "@p", periodCol
            ),
            VAR _cur = [@p]
            RETURN CALCULATE(metric, REMOVEFILTERS(dateTable), periodCol = _cur)
        )
EVALUATE
CALCULATETABLE(
    ROW(
        "sin_filtro_de_Year_rota",      ROUND(Contoso.Lab.MediaMovil3M(DimDate, DimDate[YearMonth], [Total Sales]), 2),
        "sin_filtro_de_Year_corregida", ROUND(Contoso.Lab.MediaMovil3M_Corregida(DimDate, DimDate[YearMonth], [Total Sales]), 2)
    ),
    DimDate[YearMonth] = "2024-02"
)
```

| column | result |
|---|---|
| `sin_filtro_de_Year_rota` | **805,753.73** |
| `sin_filtro_de_Year_corregida` | **805,753.73** |

With only the month filter, both versions agree: that is the control. Now the year filter is added
— redundant, and from the same table:

```dax
DEFINE
    FUNCTION Contoso.Lab.MediaMovil3M = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
            metric
        )
    FUNCTION Contoso.Lab.MediaMovil3M_Corregida = ( dateTable : ANYREF EXPR, periodCol : ANYREF EXPR, metric : ANYREF EXPR ) =>
        AVERAGEX(
            ADDCOLUMNS(
                WINDOW( -2, REL, 0, REL, SUMMARIZE(ALL(dateTable), periodCol), ORDERBY(periodCol, ASC) ),
                "@p", periodCol
            ),
            VAR _cur = [@p]
            RETURN CALCULATE(metric, REMOVEFILTERS(dateTable), periodCol = _cur)
        )
EVALUATE
CALCULATETABLE(
    ROW(
        "con_filtro_Year2024_rota",      ROUND(Contoso.Lab.MediaMovil3M(DimDate, DimDate[YearMonth], [Total Sales]), 2),
        "con_filtro_Year2024_corregida", ROUND(Contoso.Lab.MediaMovil3M_Corregida(DimDate, DimDate[YearMonth], [Total Sales]), 2)
    ),
    DimDate[Year] = 2024,
    DimDate[YearMonth] = "2024-02"
)
```

| column | result |
|---|---|
| `con_filtro_Year2024_rota` | **834,142.57** ❌ |
| `con_filtro_Year2024_corregida` | **805,753.73** ✅ |

Nothing warns you. No error, no BLANK, no visibly missing row anywhere: the broken figure is a
plausible number, off from the correct one by a fraction anybody would sign without looking twice.

### Why

`ALL(dateTable)` inside `SUMMARIZE` does build the full relation — the 24 `YearMonth`
combinations, December 2023 included — that part is verified and is not what fails:

```dax
EVALUATE
CALCULATETABLE(
  ROW("meses_visibles_con_ALL", COUNTROWS(SUMMARIZE(ALL(DimDate), DimDate[YearMonth]))),
  DimDate[Year] = 2024
)
```
It returns **24**, not 12: the window's relation ignores the year filter, as it was asked to.

What fails is the next step. `AVERAGEX` iterates that relation and, for each row, evaluates
`metric` — and evaluating it triggers a context transition: the row (`YearMonth = "2023-12"`)
becomes a filter that is **added** to the one already there (`Year = 2024`), not substituted for
it. The intersection of `YearMonth = "2023-12"` and `Year = 2024` has no rows, so `[Total Sales]`
for that row gives **BLANK** — and `AVERAGEX`, like `AVERAGE`, discards BLANKs from both the
numerator and the denominator. The broken window does not average 3 months: it averages the 2 that
do not clash with the outside filter, silently.

```dax
EVALUATE
CALCULATETABLE(
  ROW("Diciembre_2023_bajo_Year_2024", CALCULATE([Total Sales], DimDate[YearMonth] = "2023-12")),
  DimDate[Year] = 2024
)
```
It gives **BLANK**. There is the row that vanished: 834,142.57 = (865,948.13 + 802,337.00) / 2 —
January and February 2024 on their own, without December.

### The fix

`ALL` in `WINDOW`'s relation is not enough. You have to **capture each row's period value before
entering `CALCULATE`** — with `ADDCOLUMNS` — and use it as the only filter on the date table, after
clearing them all with `REMOVEFILTERS`:

```
CALCULATE(metric, REMOVEFILTERS(dateTable), periodCol = _cur)
```

`REMOVEFILTERS(dateTable)` does clear the surplus `Year = 2024` — but written without capturing the
value first (a bare `periodCol`, letting the context transition supply it), `REMOVEFILTERS` **would
also take out that very filter** the transition had just created, because both live on the same
table and `REMOVEFILTERS` does not tell one from the other. Materialising the value with
`ADDCOLUMNS` first is what takes it out of the race.

### How this was arrived at

Four queries, in the order an agent would use them: **`dax-lib`** found
`TimeSeries.MovingAverage` (Tate Bowman, v0.1.1 — Simple, Weighted, Exponential and others) already
published for this — but only the index, not the code, so it was not enough on its own.
**`dax-reference`** showed that native `MOVINGAVERAGE` is `appliesTo: [visual-calculation]` — it
cannot be called from a query or from a measure, so it was out for this case.
**`dax-window-functions`** gave the actual pattern (`AVERAGEX` over `WINDOW`) and already warns
about the default `ALLSELECTED` — the top half of this trap. **`dax-udf-authoring`** gave the
mechanics for wrapping it in a reusable function (`ANYREF EXPR`, optional parameters). Writing the
in-house version with that guidance — and measuring it against a filter a real report does put on —
found the layer none of the four had written yet: that `ALL`/`ALLSELECTED` in the `relation` does
not protect the number being averaged. This file is that layer.

## Not to be confused with
- [`ALL`](./all.md) — the same trap one level up: it clears the filters on its table, and only
  those. Here "its table" is the one that had already been filtered from outside.
- [`ALLSELECTED`](./allselected.md) — the other side of the same problem: `WINDOW` without an
  explicit `relation` inherits `ALLSELECTED()` by default, which is where all this starts.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-24. The query is read-only:
> it defines its functions with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
