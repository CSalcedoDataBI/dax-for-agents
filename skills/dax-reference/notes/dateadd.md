## Trap: it shifts what is selected, not the whole period

`DATEADD` takes the dates from the context and moves them. If the context is 15 days, it returns
15 days. That is exactly what you want to compare month against month **in progress** — and it is
exactly what [`PREVIOUSMONTH`](./previousmonth.md) does not do, even though over a complete month
both give the same thing and look interchangeable.

With the first half of March 2024 selected:

```dax
DEFINE
  MEASURE _Measures[Ventas] = SUMX(FactSales, FactSales[Quantity] * FactSales[NetPrice])
  MEASURE _Measures[Dias] = COUNTROWS(DimDate)
EVALUATE
VAR Quincena =
  CALCULATETABLE(VALUES(DimDate[Date]), ALL(DimDate),
                 DimDate[Year] = 2024, DimDate[Month] = 3, DimDate[DayOfMonth] <= 15)
RETURN
{
  ("periodo actual (1-15 mar 2024)", CALCULATE([Dias], Quincena),                    CALCULATE([Ventas], Quincena)),
  ("DATEADD -1 MONTH",               CALCULATE([Dias], DATEADD(Quincena, -1, MONTH)), CALCULATE([Ventas], DATEADD(Quincena, -1, MONTH))),
  ("PREVIOUSMONTH",                  CALCULATE([Dias], PREVIOUSMONTH(Quincena)),      CALCULATE([Ventas], PREVIOUSMONTH(Quincena)))
}
```

| period compared | days | sales |
|---|---|---|
| current (1-15 Mar 2024) | 15 | 436,666.83 |
| `DATEADD(-1, MONTH)` | **15** | 421,591.51 ✅ comparable |
| `PREVIOUSMONTH` | **29** | 802,337.00 ❌ whole month |

802,337 against 436,666 is not a 46% drop: it is half a month against a whole one. The report does
not warn you, because both numbers are correct — what is wrong is comparing them.

## It needs a real date table

`DATEADD` requires a **continuous** date column: no gaps and whole years. Over a date column from
the fact table it returns incomplete results at the edges, and in some models it does not even
warn.

The first period always comes out **blank**, because there is nothing before it to shift. A
`Ventas YoY %` over the model's first year is blank, not zero, and that is correct: there is no
comparison to make.

## Not to be confused with
- [`SAMEPERIODLASTYEAR`](./sameperiodlastyear.md) — it is `DATEADD(-1, YEAR)` with its own name.
- [`PREVIOUSMONTH`](./previousmonth.md) / `PREVIOUSYEAR` — the **complete** previous period.
- Subtracting days by hand (`Fecha - 365`): it loses leap years and does not line the weekdays up.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
