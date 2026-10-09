---
name: MATCHBY
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/matchby-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# MATCHBY

In window functions, defines the columns that are used to determine how to match data and identify the current row.

## Syntax

```dax
MATCHBY ( [<matchBy_columnName>[, matchBy_columnName [, …]]] )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`matchBy_columnName`| (Optional) The name of an existing column to be used to identify current row in the window function’s `relation`.</br> RELATED() may also be used to refer to a column in a table related to `relation`.|

## Return value

This function does not return a value.

## Remarks

This function can only be used within a window function expression.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [OFFSET](./offset.md).

## Related content

- [Understanding ORDERBY, PARTITIONBY, and MATCHBY functions](https://learn.microsoft.com/en-us/dax/best-practices/dax-understand-orderby)
- [INDEX](./index.md)
- [OFFSET](./offset.md)
- [ORDERBY](./orderby.md)
- [PARTITIONBY](./partitionby.md)
- [WINDOW](./window.md)
- [RANK](./rank.md)
- [ROWNUMBER](./rownumber.md)
