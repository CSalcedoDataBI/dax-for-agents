---
name: CLOSINGBALANCEWEEK
category: [time-intelligence]
primaryCategory: time-intelligence
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/closingbalanceweek-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CLOSINGBALANCEWEEK

Evaluates the `expression` at the last date of the week in the current context. 

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

## Syntax

```
CLOSINGBALANCEWEEK(<expression>, <calendar>[,<filter>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|An expression that returns a scalar value.|
|`calendar`|A calendar reference.|
|`filter`|(optional) An expression that specifies a filter to apply to the current context.|

## Return value

A scalar value that represents the `expression` evaluated at the last date of the week in the current context.

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.


## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'Week End Inventory Value' of the product inventory using a fiscal calendar.

```dax
= CLOSINGBALANCEWEEK (
    SUMX (
        ProductInventory,
        ProductInventory[UnitCost] * ProductInventory[UnitsBalance]
    ),
    FiscalCalendar
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [CLOSINGBALANCEYEAR function](./closingbalanceyear.md)
- [CLOSINGBALANCEQUARTER function](./closingbalancequarter.md)
- [CLOSINGBALANCEMONTH function](./closingbalancemonth.md)
