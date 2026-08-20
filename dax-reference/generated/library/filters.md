---
name: FILTERS
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/filters-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# FILTERS

Returns the values that are directly applied as filters to `columnName`.

## Syntax

```dax
FILTERS(<columnName>)
```

### Parameters

|Term  |Description|
|---------|---------|
|`columnName`| The name of an existing column, using standard DAX syntax. It cannot be an expression.  |

## Return value

The values that are directly applied as filters to `columnName`.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example shows how to determine the number of direct filters a column has.

```dax
= COUNTROWS(FILTERS(ResellerSales_USD[ProductKey]))
```

This example lets you know how many direct filters on ResellerSales_USD[ProductKey] have been applied to the context where the expression is being evaluated.
