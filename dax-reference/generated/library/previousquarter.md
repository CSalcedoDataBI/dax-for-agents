---
name: PREVIOUSQUARTER
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/previousquarter-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PREVIOUSQUARTER

For date column input, returns a table that contains a column of all dates from the previous quarter, based on the first date in the `dates` column, in the current context.

For calendar input, returns a table of all dates from the previous quarter, based on the first date in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
PREVIOUSQUARTER(<dates> or <calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|

## Return value

For date column input, a table containing a single column of date values.  
For calendar input, a table for previous quarter. The table contains all primary tagged columns and all time related columns.

## Remarks

- This function returns all dates from the previous quarter, using the first date in the input column. For example, if the first date in the `dates` argument refers to June 10, 2009,  this function returns all dates for the quarter January to March, 2009.

- The `dates` argument can be any of the following:
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

The following sample formula creates a measure that calculates the 'previous quarter sales' for Internet sales.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    PREVIOUSQUARTER ( 'DateTime'[DateKey] )
)
```

## Example for calendar

The following sample formula creates a measure that calculates the 'previous quarter sales' for Internet sales in terms of fiscal calendar.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    PREVIOUSQUARTER ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [PREVIOUSDAY](./previousday.md)
- [PREVIOUSWEEK](./previousweek.md)
- [PREVIOUSMONTH](./previousmonth.md)
- [PREVIOUSYEAR](./previousyear.md)
