---
name: ENDOFWEEK
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/endofweek-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ENDOFWEEK

Returns all primary tagged columns and all time related columns for last date of week, in the current context.  

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

## Syntax

```
ENDOFWEEK(<calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`calendar`|A calendar reference|

## Return value

A table that contains all primary tagged columns and all time related columns for end of week, in the current context.

## Remarks

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example for calendar based time intelligence

The following sample formula returns tagged primary columns that corresponds to the end of the week, for the fiscal calendar.

```dax
= ENDOFWEEK(FiscalCalendar)
```

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [ENDOFYEAR function](./endofyear.md)
- [ENDOFQUARTER function](./endofquarter.md)
- [ENDOFMONTH function](./endofmonth.md)

