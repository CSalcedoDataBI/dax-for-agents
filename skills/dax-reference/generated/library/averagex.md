---
name: AVERAGEX
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/averagex-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# AVERAGEX

Calculates the average (arithmetic mean) of a set of expressions evaluated over a table.

## Syntax

```dax
AVERAGEX(<table>,<expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|Name of a table, or an expression that specifies the table over which the aggregation can be performed.|
|`expression`|An expression with a scalar result, which will be evaluated for each row of the table in the first argument.|

## Return value

A decimal number.

## Remarks

- The AVERAGEX function enables you to evaluate expressions for each row of a table, and then take the resulting set of values and calculate its arithmetic mean. Therefore, the function takes a table as its first argument, and an expression as the second argument.

- In all other respects, AVERAGEX follows the same rules as AVERAGE. You cannot include non-numeric or null cells. Both the table and expression arguments are required.

- When there are no rows to aggregate, the function returns a blank.  When there are rows, but none of them meet the specified criteria, then the function returns 0.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example calculates the average freight and tax on each order in the InternetSales table, by first summing Freight plus TaxAmt in each row, and then averaging those sums.

```dax
= AVERAGEX(InternetSales, InternetSales[Freight]+ InternetSales[TaxAmt])
```

If you use multiple operations in the expression used as the second argument, you must use parentheses to control the order of calculations. For more information, see [DAX Syntax Reference](https://learn.microsoft.com/en-us/dax/dax-syntax-reference).

## Related content

- [AVERAGE function](./average.md)
- [AVERAGEA function](./averagea.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
