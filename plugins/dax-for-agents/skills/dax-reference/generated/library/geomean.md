---
name: GEOMEAN
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/geomean-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# GEOMEAN

Returns the geometric mean of the numbers in a column.

To return the geometric mean of an expression evaluated for each row in a table, use [GEOMEANX function](./geomeanx.md).

## Syntax

```dax
GEOMEAN(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column that contains the numbers for which the geometric mean is to be computed.|

## Return value

A decimal number.

## Remarks

- Only the numbers in the column are counted. Blanks, logical values, and text are ignored.

- GEOMEAN( Table[Column] ) is equivalent to GEOMEANX( Table, Table[Column] )

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following computes the geometric mean of the Return column in the Investment table:

```dax
= GEOMEAN( Investment[Return] )
```

## Related content

- [GEOMEANX function](./geomeanx.md)
