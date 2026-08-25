## Trap: with the fact's date the result comes out blank, with no error

The function returns a set of dates shifted by a year, and that set filters **the column you
passed it**. If you pass it the fact table's date, the filter lands on `FactSales[OrderDate]` —
while the visual's context is still filtering `DimDate`. Both conditions have to hold at once:
2023 dates on the fact **and** 2024 on the dimension. No row is like that, and the result is
blank.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[LY bien] = CALCULATE([Unidades], SAMEPERIODLASTYEAR(DimDate[Date]))
  MEASURE _Measures[LY mal]  = CALCULATE([Unidades], SAMEPERIODLASTYEAR(FactSales[OrderDate]))
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(VALUES(DimDate[YearMonth]), "unidades", [Unidades],
             "LY_DimDate", [LY bien], "LY_FactSales", [LY mal]),
  DimDate[Year] = 2024, DimDate[Month] IN {1,2}
)
```

| month | units | LY with DimDate | LY with FactSales |
|---|---|---|---|
| 2024-01 | 7,483 | **7,272** ✅ | **(blank)** ❌ |
| 2024-02 | 7,059 | **6,782** ✅ | **(blank)** ❌ |

With `DimDate[Date]` the shifted filter replaces the context's own, because it lands on the same
column. That is why the whole family asks for the date table's column: it is not an arbitrary
rule, it is that the filter has to land where the visual is already filtering.

An entire year-over-year column of blanks is almost always this, not missing history.

**The blank is not the only shape of the failure.** The same mistake with `DATESYTD` does not
return blank: it returns the period's value **without accumulating**, which is harder to spot
because it looks like a reasonable number. The query that measures it is in
[`datesytd`](./datesytd.md) and gives:

| month | YTD with `DimDate[Date]` | YTD with `FactSales[OrderDate]` |
|---|---|---|
| 2024-01 | 7,483 | 7,483 |
| 2024-02 | **14,542** | **7,059** |
| 2024-03 | **22,520** | **7,978** |

`DATESYTD` does not shift to the previous year, so there is no contradiction to leave the
intersection empty: the filter simply lands on the wrong column and does not accumulate. Each
function in the family fails in its own way; what they share is the cause, not the symptom.

## Not to be confused with
Missing history. Check which column the function points at; the data is usually there.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
