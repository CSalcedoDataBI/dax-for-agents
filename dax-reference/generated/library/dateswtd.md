---
name: DATESWTD
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/dateswtd-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DATESWTD

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

Returns a table for week to date, in the current context. The table contains all primary tagged columns and all time related columns.

## Syntax

```
DATESWTD(<calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`calendar`|A calendar reference.|

## Return value

A table containing all primary tagged and time-related columns

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.


## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'Week To Date Total' for Internet sales uing fiscal calendar.

```dax
= CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    DATESWTD ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [DATESYTD function](./datesytd.md)
- [DATESQTD function](./datesqtd.md)
- [DATESMTD function](./datesmtd.md)
