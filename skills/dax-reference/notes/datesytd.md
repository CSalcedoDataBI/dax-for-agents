## Trap: a date filter in the SAME `CALCULATE` survives the accumulation

`DATESYTD` returns the dates from 1 January to the end of the current period. It is just another
filter argument, so it coexists with the other arguments of the same `CALCULATE`: if you add a
condition on the date table there, it **intersects** with the accumulated range and the result
stops accumulating.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[YTD] = CALCULATE([Unidades], DATESYTD(DimDate[Date]))
  MEASURE _Measures[YTD con filtro de mes] =
    CALCULATE([Unidades], DATESYTD(DimDate[Date]), DimDate[Month] = 2)
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(VALUES(DimDate[YearMonth]), "unidades", [Unidades],
             "YTD", [YTD], "YTD_con_filtro_mes", [YTD con filtro de mes]),
  DimDate[Year] = 2024, DimDate[Month] IN {1,2,3}
)
```

| month | units | YTD | YTD with month filter |
|---|---|---|---|
| 2024-01 | 7,483 | **7,483** | (blank) |
| 2024-02 | 7,059 | **14,542** | 7,059 |
| 2024-03 | 7,978 | **22,520** | 7,059 |

The correct YTD grows; the other is stuck on February.

What is measured here is the filter written **inside the same `CALCULATE`**. The visual's own row
filter (the `YearMonth` column) does not get in the way: it is what defines "up to when" to
accumulate, and that is why the YTD column does advance. The trap is adding date conditions by
hand next to the function, not the visual filtering.

## Trap: with the fact's date it stops accumulating, without warning

Passing it the fact table's date instead of the date table's raises no error and no blank: it
returns the period's value **without accumulating**.

```dax
DEFINE
  MEASURE _Measures[Unidades] = SUM(FactSales[Quantity])
  MEASURE _Measures[YTD con DimDate]  = CALCULATE([Unidades], DATESYTD(DimDate[Date]))
  MEASURE _Measures[YTD con el hecho] = CALCULATE([Unidades], DATESYTD(FactSales[OrderDate]))
EVALUATE
CALCULATETABLE(
  ADDCOLUMNS(VALUES(DimDate[YearMonth]),
             "unidades", [Unidades],
             "YTD_DimDate", [YTD con DimDate],
             "YTD_FactSales", [YTD con el hecho]),
  DimDate[Year] = 2024, DimDate[Month] IN {1,2,3}
)
ORDER BY DimDate[YearMonth]
```

| month | units | `DATESYTD(DimDate[Date])` | `DATESYTD(FactSales[OrderDate])` |
|---|---|---|---|
| 2024-01 | 7,483 | 7,483 | 7,483 |
| 2024-02 | 7,059 | **14,542** | **7,059** |
| 2024-03 | 7,978 | **22,520** | **7,978** |

In January they agree, which is the worst thing that could happen: if you check the first month, it
looks right.

## Not to be confused with
An incomplete date table. See also [`SAMEPERIODLASTYEAR`](./sameperiodlastyear.md), where the same
mistake does produce a blank: the cause is the same and the symptom is not.

> Measured against [`lab/contoso`](../../../lab/contoso/) — Contoso Retail, FactSales 126,524
> rows, 137 products, DimDate 2023-01-01 to 2024-12-31 — on 2026-08-12. The query is read-only:
> it defines its measures with `DEFINE` and does not touch the model. It runs and compares itself
> with `python lab/check_lab.py contoso localhost:<port>`.
