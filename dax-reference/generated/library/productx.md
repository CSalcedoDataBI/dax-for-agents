---
name: PRODUCTX
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/productx-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PRODUCTX

Returns the product of an expression evaluated for each row in a table.

## Syntax

```dax
PRODUCTX(<table>, <expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table containing the rows for which the expression will be evaluated.|
|`expression`|The expression to be evaluated for each row of the table.|

## Return value

A decimal number.

## Remarks

- To return the product of the numbers in a column, use [PRODUCT](./product.md).

- The PRODUCTX function takes as its first argument a table, or an expression that returns a table. The second argument is a column that contains the numbers for which you want to compute the product, or an expression that evaluates to a column.

- Only the numbers in the column are counted. Blanks, logical values, and text are ignored.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following computes the future value of an investment:

```dax
= [PresentValue] * PRODUCTX( AnnuityPeriods, 1+[FixedInterestRate] )
```

## Related content

- [PRODUCT](./product.md)
