---
name: ENDOFYEAR
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/endofyear-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ENDOFYEAR

For date column input, returns the last date of year in the current context for the specified column of dates.  
For calendar input, returns a table that contains all primary tagged columns and all time related columns for last date of year, in the current context.

## Syntax

```
ENDOFYEAR(<dates> or <calendar> [,<year_end_date>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|
|`year_end_date`|(optional) A literal string with a date that defines the year-end date. The default is December 31. This parameter is permitted only when the date column syntax is used.|

## Return value

For date column input, a table containing a single column and single row with a date value.  
For calendar input, a table that contains all primary tagged columns and all time related columns for last date of year, in the current context.

## Remarks

- The `dates` argument can be any of the following:
  - A reference to a date/time column,
  - A table expression that returns a single column of date/time values,
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- The `year_end_date` parameter is a string literal of a date, in the same locale as the locale of the client where the workbook was created. The year portion of the date is ignored.

- The `year_end_date` parameter is permitted only when the date column syntax is used.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that returns the end of the fiscal year that ends on June 30, for the current context.

```dax
= ENDOFYEAR(DateTime[DateKey],"06/30/2004")
```

## Example for calendar based time intelligence

The following sample formula returns tagged primary columns that corresponds to end of year, for the fiscal calendar.

```dax
= ENDOFYEAR(FiscalCalendar)
```

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [ENDOFWEEK function](./endofweek.md)
- [ENDOFMONTH function](./endofmonth.md)
- [ENDOFQUARTER function](./endofquarter.md)
