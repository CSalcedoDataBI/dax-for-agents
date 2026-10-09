---
name: OPENINGBALANCEWEEK
category: [time-intelligence]
primaryCategory: time-intelligence
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/openingbalanceweek-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# OPENINGBALANCEWEEK

Evaluates the `expression` at the date corresponding to the end of the previous week in the current context.

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

## Syntax

```
OPENINGBALANCEWEEK(<expression>,<calendar>[,<filter>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|An expression that returns a scalar value.|
|`calendar`|A calendar reference.|
|`filter`|(optional) An expression that specifies a filter to apply to the current context.|

## Return value

A scalar value that represents the `expression` evaluated at the end of the previous week in the current context.

## Remarks

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- The `filter` expression has restrictions described in the topic, [CALCULATE function](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.


## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'Week Start Inventory Value' of the product inventory in terms of fiscal calendar.

```dax
=
OPENINGBALANCEWEEK (
    SUMX (
        ProductInventory,
        ProductInventory[UnitCost] * ProductInventory[UnitsBalance]
    ),
    FiscalCalendar
)
```

## Related content

- [OPENINGBALANCEYEAR function](./openingbalanceyear.md)
- [OPENINGBALANCEQUARTER function](./openingbalancequarter.md)
- [OPENINGBALANCEMONTH function](./openingbalancemonth.md)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [CLOSINGBALANCEWEEK function](./closingbalanceweek.md)
