## Trap: it returns the **whole** previous month, whatever you are looking at

`PREVIOUSMONTH` does not shift your selection: it ignores it, anchors on the **first** date in the
context, and returns the complete calendar month before that one. With a whole month selected that
is what you want. With a partial month — the current month, half a month, a working-days filter —
you are comparing a slice against a whole month.

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
  ("periodo actual (1-15 mar 2024)", CALCULATE([Dias], Quincena),               CALCULATE([Ventas], Quincena)),
  ("PREVIOUSMONTH",                  CALCULATE([Dias], PREVIOUSMONTH(Quincena)), CALCULATE([Ventas], PREVIOUSMONTH(Quincena))),
  ("DATEADD -1 MONTH",               CALCULATE([Dias], DATEADD(Quincena, -1, MONTH)), CALCULATE([Ventas], DATEADD(Quincena, -1, MONTH)))
}
```

| period compared | days | sales |
|---|---|---|
| current (1-15 Mar 2024) | 15 | 436,666.83 |
| `PREVIOUSMONTH` | **29** ❌ | 802,337.00 |
| [`DATEADD(-1, MONTH)`](./dateadd.md) | **15** ✅ | 421,591.51 |

29 days, not 28: February 2024 was a leap year. That detail is the other half of the problem —
months do not measure the same, so "previous month" is never a clean comparison unless both are
complete.

## Straddling two months it returns the one before the **first**

With a selection from 15 February to 10 March, "the previous month" is not February:

```dax
EVALUATE
VAR ACaballo =
  CALCULATETABLE(VALUES(DimDate[Date]), ALL(DimDate),
                 DimDate[Date] >= DATE(2024,2,15), DimDate[Date] <= DATE(2024,3,10))
VAR Prev = CALCULATETABLE(VALUES(DimDate[Date]), PREVIOUSMONTH(ACaballo))
RETURN
{
  ("contexto: min",       FORMAT(MINX(ACaballo, DimDate[Date]), "yyyy-MM-dd")),
  ("contexto: max",       FORMAT(MAXX(ACaballo, DimDate[Date]), "yyyy-MM-dd")),
  ("PREVIOUSMONTH: min",  FORMAT(MINX(Prev, DimDate[Date]), "yyyy-MM-dd")),
  ("PREVIOUSMONTH: max",  FORMAT(MAXX(Prev, DimDate[Date]), "yyyy-MM-dd")),
  ("PREVIOUSMONTH: días", FORMAT(COUNTROWS(Prev), "0"))
}
```

| | date |
|---|---|
| context, first | 2024-02-15 |
| context, last | 2024-03-10 |
| `PREVIOUSMONTH`, first | **2024-01-01** |
| `PREVIOUSMONTH`, last | **2024-01-31** |
| days returned | **31** |

January. Neither February nor March, the two months the user has in front of them. A range crossing
a month boundary — a slicer selection, a "last 30 days" — turns the comparison into something
nobody asked for, and still returns a number.

## Where it is the right function

When the current period **is closed**: a monthly report on last month, a to-close running total.
There `PREVIOUSMONTH` says exactly what you mean and reads better than a `DATEADD` with parameters.

For the current month, the honest comparison is month-to-date against month-to-date, and that is
what `DATEADD` over the selected dates gives you.

## Not to be confused with
- [`DATEADD`](./dateadd.md) — shifts the selection as it is, without completing the period.
- `PREVIOUSYEAR` / `PREVIOUSQUARTER` / `PREVIOUSDAY` — same family, same whole-period behaviour.
- `DATESMTD` — the month up to the context's date, which is usually what people mean by "the
  current month".

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-13. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
