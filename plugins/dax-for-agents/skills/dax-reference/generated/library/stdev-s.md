---
name: STDEV.S
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/stdev-s-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# STDEV.S

Returns the standard deviation of a sample population.

## Syntax

```dax
STDEV.S(<ColumnName>)
```

### Parameters

|Term|Definition|
|--------|--------------|
| `columnName` | The name of an existing column using standard DAX syntax, usually fully qualified. It cannot be an expression.   |

## Return value

A number that represents the standard deviation of a sample population.

## Exceptions

## Remarks

- STDEV.S assumes that the column refers to a sample of the population. If your data represents the entire population, then compute the standard deviation by using STDEV.P.

- STDEV.S uses the following formula:

    √[∑(x - x̃)<sup>2</sup>/(n-1)]

    where x̃ is the average value of x for the sample population and n is the population size.

- Blank rows are filtered out from `columnName` and not considered in the calculations.

- An error is returned if `columnName` contains less than 2 non-blank rows.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example shows the formula for a measure that calculates the standard deviation of the column, SalesAmount_USD, when the table InternetSales_USD is the sample population.

```dax
= STDEV.S(InternetSales_USD[SalesAmount_USD])
```
