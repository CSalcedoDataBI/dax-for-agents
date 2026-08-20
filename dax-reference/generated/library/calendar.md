---
name: CALENDAR
category: [date-and-time]
primaryCategory: date-and-time
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/calendar-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CALENDAR

Returns a table with a single column named "Date" that contains a contiguous set of dates. The range of dates is from the specified start date to the specified end date, inclusive of those two dates.

## Syntax

```dax
CALENDAR(<start_date>, <end_date>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`start_date`|Any DAX expression that returns a datetime value.|
|`end_date`|Any DAX expression that returns a datetime value.|

## Return value

Returns a table with a single column named "Date" containing a contiguous set of dates. The range of dates is from the specified start date to the specified end date, inclusive of those two dates.

## Remarks

- An error is returned if start_date is greater than end_date.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula returns a table with dates between January 1st, 2015 and December 31st, 2021.

```dax
= CALENDAR (DATE (2015, 1, 1), DATE (2021, 12, 31))
```

For a data model which includes actual sales data and future sales forecasts, the following expression returns a date table covering the range of dates in both the Sales and Forecast tables.

```dax
= CALENDAR (MINX (Sales, [Date]), MAXX (Forecast, [Date]))
```
