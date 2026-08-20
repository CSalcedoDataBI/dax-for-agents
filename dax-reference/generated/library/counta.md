---
name: COUNTA
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/counta-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# COUNTA

Counts the number of rows in the specified column that contain non-blank values.

## Syntax

```dax
COUNTA(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column that contains the values to be counted.|

## Return value

A whole number.

## Remarks

- When the function does not find any rows to count, the function returns a blank.
- Unlike [COUNT](./count.md), COUNTA supports Boolean data type.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns the number of all rows in the `Reseller` table that have any kind of value in the column that stores phone numbers. 

```dax
= COUNTA(Reseller[Phone])
```

## Related content

- [COUNT function](./count.md)
- [COUNTAX function](./countax.md)
- [COUNTX function](./countx.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
