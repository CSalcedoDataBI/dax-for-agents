---
name: PREVIOUSMONTH
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/previousmonth-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# PREVIOUSMONTH

For date column input, returns a table that contains a column of all dates from the previous month, based on the first date in the `<Dates>` column, in the current context.

For calendar input, returns a table of all dates from the previous month, based on the first date in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
PREVIOUSMONTH(<dates> or <calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|

## Return value

For date column input, a table containing a single column of date values.  
For calendar input, a table that contains all primary tagged columns and all time related columns.

## Remarks

- This function returns all dates from the previous month, using the first date in the column used as input. For example, if the first date in the `Dates` argument refers to June 10, 2009, this function returns all dates for the month of May, 2009.

- The `Dates` argument can be any of the following:
  - A reference to a date/time column.
  - A table expression that returns a single column of date/time values.
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that calculates the 'previous month sales' for sales.

```dax
= CALCULATE ( SUM ( 'Sales'[Sales Amount] ), PREVIOUSMONTH ( 'Date'[Date] ) )
```

## Example for calendar

The following sample formula creates a measure that calculates the 'previous month sales' for Internet sales in terms of fiscal calendar.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    PREVIOUSMONTH ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [PREVIOUSDAY](./previousday.md)
- [PREVIOUSWEEK](./previousweek.md)
- [PREVIOUSQUARTER](./previousquarter.md)
- [PREVIOUSYEAR](./previousyear.md)
