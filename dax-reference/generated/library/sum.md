---
name: SUM
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sum-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SUM

Adds all the numbers in a column.

## Syntax

```dax
SUM(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column that contains the numbers to sum.|

## Return value

A decimal number.

## Remarks

If you want to filter the values that you are summing, you can use the SUMX function and specify an expression to sum over.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example adds all the numbers that are contained in the column, Amt, from the table, Sales.

```dax
= SUM(Sales[Amt])
```

## Related content

- [SUMX](./sumx.md)
