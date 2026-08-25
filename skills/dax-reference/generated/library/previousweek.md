---
name: PREVIOUSWEEK
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/previousweek-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PREVIOUSWEEK

Returns a table of all dates from the previous week, based on the first date in the current context. The table contains all primary tagged columns and all time related columns.

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

## Syntax

```dax
PREVIOUSWEEK(<calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`calendar`|A calendar reference|

## Return value

A table that contains all primary tagged columns and all time related columns.

## Remarks

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.


## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'previous week sales' for Internet sales in terms of fiscal calendar.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    PREVIOUSWEEK ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [PREVIOUSDAY function](./previousday.md)
- [PREVIOUSMONTH function](./previousmonth.md)
- [PREVIOUSQUARTER function](./previousquarter.md)
- [PREVIOUSYEAR function](./previousyear.md)

