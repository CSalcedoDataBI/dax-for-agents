---
name: NEXTMONTH
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/nextmonth-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NEXTMONTH

For date column input, returns a table that contains a column of all dates from the next month, based on the last date in the `dates` column in the current context.

For calendar input, returns a table for all dates from the next month, based on the last date in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
NEXTMONTH(<dates> or <calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|

## Return value

For date column input, a table containing a single column of date values.
For calendar input, a table that contains all primary tagged columns and all time related columns for next month.

## Remarks

- This function returns all dates from the next month to the last date in the input parameter. For example, if the last date in the `dates` argument refers to June 10, 2009; then this function returns all dates for the month of July, 2009.

- The `dates` argument can be any of the following:
  - A reference to a date/time column.
  - A table expression that returns a single column of date/time values.
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that calculates the 'next month sales' for Internet sales.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    NEXTMONTH ( 'DateTime'[DateKey] )
)
```

## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'next month sales' for Internet sales.

```dax
=
CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    NEXTMONTH ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [NEXTDAY function](./nextday.md)
- [NEXTWEEK function](./nextweek.md)
- [NEXTQUARTER function](./nextquarter.md)
- [NEXTYEAR function](./nextyear.md)
