---
name: STDEVX.S
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/stdevx-s-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# STDEVX.S

Returns the standard deviation of a sample population.

## Syntax

```dax
STDEVX.S(<table>, <expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`  | Any DAX expression that returns a single scalar value, where the expression is to be evaluated multiple times (for each row/context).  |
|`expression`   | Any DAX expression that returns a single scalar value, where the expression is to be evaluated multiple times (for each row/context).   |

## Return value

A number with the standard deviation of a sample population.

## Exceptions

## Remarks

- STDEVX.S evaluates `expression` for each row of `table` and returns the standard deviation of `expression` assuming that `table` refers to a sample of the population. If `table` represents the entire population, then compute the standard deviation by using STDEVX.P.

- STDEVX.S uses the following formula:

    √[∑(x - x̃)<sup>2</sup>/(n-1)]

    where x̃ is the average value of x for the entire population and n is the population size.

- Blank rows are filtered out from `columnName` and not considered in the calculations.

- An error is returned if `columnName` contains less than 2 non-blank rows.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example shows the formula for a calculated column that estimates the standard deviation of the unit price per product for a sample population, when the formula is used in the Product table.

```dax
= STDEVX.S(RELATEDTABLE(InternetSales_USD), InternetSales_USD[UnitPrice_USD] – (InternetSales_USD[DiscountAmount_USD]/InternetSales_USD[OrderQuantity]))
```
