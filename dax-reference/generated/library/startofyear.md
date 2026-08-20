---
name: STARTOFYEAR
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/startofyear-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# STARTOFYEAR

For date column input, returns the first date of year in the current context for the specified column of dates.  
For calendar input, returns a table for first date of year, in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
STARTOFYEAR(<dates> or <calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference.|
|`YearEndDate`|(Optional) A year end date value. Only applies for date column input.|

## Return value

For date column input, a table containing a single column and single row with a date value.  
For calendar input, a table for first date of year, in the current context. The table contains all primary tagged columns and all time related columns.

## Remarks

- The `dates` argument can be any of the following:
  - A reference to a date/time column.
  - A table expression that returns a single column of date/time values.
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE](./calculate.md).

- The `year_end_date` parameter must not be specified when a calendar is used.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that returns the start of the year, for the current context.

```dax
= STARTOFYEAR(DateTime[DateKey])
```

## Example for calendar based time intelligence

The following sample formula creates a table that returns tagged columns that corresponds to the start of the year, for the fiscal calendar.

```dax
= STARTOFYEAR(FiscalCalendar)
```

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [STARTOFQUARTER](./startofquarter.md)
- [STARTOFMONTH](./startofmonth.md)
- [STARTOFWEEK](./startofweek.md)
