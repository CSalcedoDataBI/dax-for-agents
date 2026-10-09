---
name: TOTALWTD
category: [time-intelligence]
primaryCategory: time-intelligence
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/totalwtd-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# TOTALWTD

Evaluates the value of the `expression` for the week to date, in the current context.  

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

## Syntax

```
TOTALWTD(<expression>,<calendar>[,<filter>])
```

### Parameters

|Parameter|Definition|
|-------------|--------------|
|`expression`|An expression that returns a scalar value.|
|`calendar`|A calendar reference.|
|`filter`|(optional) An expression that specifies a filter to apply to the current context.|

## Return value

A scalar value that represents the `expression` evaluated for the dates in the current week-to-date, given the dates in `dates` or `calendar`.

## Remarks

- Constraints on Boolean expressions are described in the topic, [CALCULATE](./calculate.md).

- The `filter` expression has restrictions described in the topic, [CALCULATE](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.


## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'week running total' or 'week running sum' for Internet sales in terms of fiscal calendar.

```dax
= TOTALWTD(SUM(InternetSales_USD[SalesAmount_USD]), FiscalCalendar)
```

## Related content

- [ALL](./all.md)
- [CALCULATE](./calculate.md)
- [TOTALYTD](./totalytd.md)
- [TOTALQTD](./totalqtd.md)
- [TOTALMTD](./totalmtd.md)
