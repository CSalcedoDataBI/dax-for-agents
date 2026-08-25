---
name: MEDIAN
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/median-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# MEDIAN

Returns the median of numbers in a column.

To return the median of an expresssion evaluated for each row in a table, use [MEDIANX function](./medianx.md).

## Syntax

```dax
MEDIAN(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column that contains the numbers for which the median is to be computed.|

## Return value

A decimal number.

## Remarks

- Only the numbers in the column are counted. Blanks are ignored. Logical values, dates, and text are not supported. 

- MEDIAN( Table[Column] ) is equivalent to MEDIANX( Table, Table[Column] ).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following computes the median of a column named Age in a table named Customers:

```dax
= MEDIAN( Customers[Age] )
```

## Related content

- [MEDIANX function](./medianx.md)
