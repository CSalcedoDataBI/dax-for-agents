---
name: ENDOFMONTH
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/endofmonth-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ENDOFMONTH

For date column input, returns the last date of the month in the current context for the specified column of dates.  
For calendar input, returns a table for the last date of the month, in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
ENDOFMONTH(<dates> or <calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|

## Return value

For date column input, a table containing a single column and single row with a date value.  
For calendar input, a table with a single row that contains all primary tagged columns and all time related columns.

## Remarks

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

The following sample formula creates a measure that returns the end of the month, for the current context.

```dax
= ENDOFMONTH(DateTime[DateKey])
```

## Example for calendar based time intelligence

The following sample formula returns tagged primary columns that corresponds to the end of the month, for the fiscal calendar.

```dax
= ENDOFMONTH(FiscalCalendar)
```

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [ENDOFYEAR function](./endofyear.md)
- [ENDOFQUARTER function](./endofquarter.md)
- [ENDOFWEEK function](./endofweek.md)

