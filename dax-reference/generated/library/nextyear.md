---
name: NEXTYEAR
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/nextyear-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NEXTYEAR

For date column input, returns a table that contains a column of all dates in the next year, based on the last date in the `dates` column, in the current context.

For calendar input, returns a table of all dates from the next year, based on the last date in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
NEXTYEAR(<dates> or <calendar>[,<year_end_date>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|
|`year_end_date`|(optional) A literal string with a date that defines the year-end date. The default is December 31. This parameter is permitted only when the date column syntax is used. |

## Return value

For date column input, a table containing a single column of date values.  
For calendar input, a table that contains all primary tagged columns and all time related columns.

## Remarks

- This function returns all dates in the next year, based on the last date in the input column. For example, if the last date in the `dates` column refers to the year 2007, this function returns all dates for the year 2008.

- The `dates` argument can be any of the following:
  - A reference to a date/time column.
  - A table expression that returns a single column of date/time values.
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- The `year_end_date` parameter is a string literal of a date, in the same locale as the locale of the client where the workbook was created. The year portion of the date is ignored. This parameter does not apply when calendar is used.

- The `year_end_date` parameter is permitted only when the date column syntax is used.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that calculates the 'next year sales' for Internet sales.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    NEXTYEAR ( 'DateTime'[DateKey] )
)
```

## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'next year sales' for Internet sales.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    NEXTYEAR ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [NEXTDAY function](./nextday.md)
- [NEXTQUARTER function](./nextquarter.md)
- [NEXTMONTH function](./nextmonth.md)
