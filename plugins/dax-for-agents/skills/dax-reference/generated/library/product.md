---
name: PRODUCT
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/product-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PRODUCT

Returns the product of the numbers in a column.

## Syntax

```dax
PRODUCT(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column that contains the numbers for which the product is to be computed.|

## Return value

A decimal number.

## Remarks

- To return the product of an expression evaluated for each row in a table, use [PRODUCTX function](./productx.md).

- Only the numbers in the column are counted. Blanks, logical values, and text are ignored. For example,

  `PRODUCT( Table[Column] )` is equivalent to `PRODUCTX( Table, Table[Column] )`.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.
 
## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following computes the product of the AdjustedRates column in an Annuity table:

```dax
= PRODUCT( Annuity[AdjustedRates] )
```

## Related content

- [PRODUCTX](./productx.md)
