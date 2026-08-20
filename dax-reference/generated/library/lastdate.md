---
name: LASTDATE
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/lastdate-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# LASTDATE

For date column input, returns the last date in the current context for the specified column of dates.  

For calendar input, returns the last date based on the calendar.

## Syntax

```
LASTDATE(<dates> or <calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|

## Return value

For date column input, a table containing a single column and single row with a date value.

For calendar input, a single row table that contains all primary tagged columns and all time related columns.

## Remarks

- The `dates` argument can be any of the following: 
  - A reference to a date/time column,
  - A table expression that returns a single column of date/time values,
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- When the current context is a single date, the date returned by the FIRSTDATE and LASTDATE functions will be equal.

- For date column input, the Return value is a table that contains a single column and single value. Therefore, this function can be used as an argument to any function that requires a table in its arguments. Also, the returned value can be used whenever a date value is required.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that obtains the last date, for the current context, when a sale was made in the Internet sales channel.

```dax
= LASTDATE('InternetSales_USD'[SaleDateKey])
```

## Example for calendar based time intelligence

The following sample formula creates a measure that obtains the last date, for the current context, when a sale was made in the Internet sales channel.

```dax
= LASTDATE(FiscalCalendar)
```

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [FIRSTDATE function](./firstdate.md)
- [LASTNONBLANK function](./lastnonblank.md)
