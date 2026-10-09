---
name: OPENINGBALANCEMONTH
category: [time-intelligence]
primaryCategory: time-intelligence
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/openingbalancemonth-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# OPENINGBALANCEMONTH

Evaluates the `expression` at the date corresponding to the end of the previous month in the current context.

## Syntax

```
OPENINGBALANCEMONTH(<expression>,<dates> or <calendar>[,<filter>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|An expression that returns a scalar value.|
|`dates or calendar`|A column that contains dates or a calendar reference.|
|`filter`|(optional) An expression that specifies a filter to apply to the current context.|

## Return value

A scalar value that represents the `expression` at the end of the previous month in the current context.

## Remarks

- The `dates` argument can be any of the following:
  - A reference to a date/time column.
  - A table expression that returns a single column of date/time values.
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- The `filter` expression has restrictions described in the topic, [CALCULATE function](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that calculates the 'Month Start Inventory Value' of the product inventory.

```dax
= OPENINGBALANCEMONTH (
    SUMX (
        ProductInventory,
        ProductInventory[UnitCost] * ProductInventory[UnitsBalance]
    ),
    DateTime[DateKey]
)
```

## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'Month Start Inventory Value' of the product inventory in terms of fiscal calendar.

```dax
=
OPENINGBALANCEMONTH (
    SUMX (
        ProductInventory,
        ProductInventory[UnitCost] * ProductInventory[UnitsBalance]
    ),
    FiscalCalendar
)
```

## Related content

- [OPENINGBALANCEWEEK function](./openingbalanceweek.md)
- [OPENINGBALANCEYEAR function](./openingbalanceyear.md)
- [OPENINGBALANCEQUARTER function](./openingbalancequarter.md)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [CLOSINGBALANCEMONTH function](./closingbalancemonth.md)
