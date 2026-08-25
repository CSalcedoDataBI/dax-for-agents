---
name: OPENINGBALANCEYEAR
category: [time-intelligence]
primaryCategory: time-intelligence
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/openingbalanceyear-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# OPENINGBALANCEYEAR

Evaluates the `expression` at the date corresponding to the end of the previous year in the current context.

## Syntax

```
OPENINGBALANCEYEAR(<expression>,<dates> or <calendar>[,<filter>][,<year_end_date>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|An expression that returns a scalar value.|
|`dates or calendar`|A column that contains dates or a calendar reference.|
|`filter`|(optional) An expression that specifies a filter to apply to the current context.|
|`year_end_date`|(optional) A literal string with a date that defines the year-end date. The default is December 31. Only applies when date column is used.|

## Return value

A scalar value that represents the `expression` evaluated at the end of the previous year in the current context.

## Remarks

- The `dates` argument can be any of the following:
  - A reference to a date/time column.
  - A table expression that returns a single column of date/time values.
  - A Boolean expression that defines a single-column table of date/time values.

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- The `filter` expression has restrictions described in the topic, [CALCULATE function](./calculate.md).

- The `year_end_date` parameter is a string literal of a date, in the same locale as the locale of the client where the workbook was created. The year portion of the date is ignored.

- The `year_end_date` parameter must not be specified when a calendar is used.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that calculates the 'Year Start Inventory Value' of the product inventory.

```dax
=
OPENINGBALANCEYEAR (
    SUMX (
        ProductInventory,
        ProductInventory[UnitCost] * ProductInventory[UnitsBalance]
    ),
    DateTime[DateKey]
)
```

## Example for calendar based time intelligence

The following sample formula creates a measure that calculates the 'Year Start Inventory Value' of the product inventory in terms of fiscal calendar.

```dax
=
OPENINGBALANCEYEAR (
    SUMX (
        ProductInventory,
        ProductInventory[UnitCost] * ProductInventory[UnitsBalance]
    ),
    FiscalCalendar
)
```

## Related content

- [OPENINGBALANCEWEEK function](./openingbalanceweek.md)
- [OPENINGBALANCEQUARTER function](./openingbalancequarter.md)
- [OPENINGBALANCEMONTH function](./openingbalancemonth.md)
- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [CLOSINGBALANCEYEAR function](./closingbalanceyear.md)
