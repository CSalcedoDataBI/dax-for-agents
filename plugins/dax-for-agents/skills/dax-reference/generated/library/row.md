---
name: ROW
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/row-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ROW function

Returns a table with a single row containing values that result from the expressions given to each column.

## Syntax

```dax
ROW(<name>, <expression>[[,<name>, <expression>]…])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`name`|  The name given to the column, enclosed in double quotes. |
|`expression`| Any DAX expression that returns a single scalar value to populate. `name`.  |

## Return value

A single row table

## Remarks

- Arguments must always come in pairs of `name` and `expression`.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns a single row table with the total sales for internet and resellers channels.

```dax
ROW("Internet Total Sales (USD)", SUM(InternetSales_USD[SalesAmount_USD]),
         "Resellers Total Sales (USD)", SUM(ResellerSales_USD[SalesAmount_USD]))
```
