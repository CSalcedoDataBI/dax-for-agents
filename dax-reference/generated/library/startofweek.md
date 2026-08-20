---
name: STARTOFWEEK
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/startofweek-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# STARTOFWEEK

Returns a table for the first date of week in the current context, based on the calendar. The table contains all primary tagged columns and all time related columns.

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

## Syntax

```
STARTOFWEEK(<calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`calendar`|A calendar reference|

## Return value

A table that contains all primary tagged columns and all time related columns.

## Remarks

- Constraints on Boolean expressions are described in the topic, [CALCULATE](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.


## Example for calendar based time intelligence

The following sample formula returns primary tagged columns for the first date of the week, for the fiscal calendar.

```dax
= STARTOFWEEK(FiscalCalendar)
```

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [STARTOFYEAR](./startofyear.md)
- [STARTOFQUARTER](./startofquarter.md)
- [STARTOFMONTH](./startofmonth.md)
