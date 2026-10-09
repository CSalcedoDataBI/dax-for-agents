---
name: DISTINCT
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/distinct-table-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DISTINCT (table)

Returns a table by removing duplicate rows from another table or expression.

## Syntax

```dax
DISTINCT(<table>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table from which unique rows are to be returned. The table can also be an expression that results in a table.|

## Return value

A table containing only distinct rows.

## Related functions

There is another version of the DISTINCT function, [DISTINCT (column)](./distinct.md), that takes a column name as input parameter.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following query:

```dax
EVALUATE DISTINCT( { (1, "A"), (2, "B"), (1, "A") } )
```

Returns table:

|[Value1]    |[Value2]  |
|---------|---------|
|1    |     A    |
|2    |     B    |

## Related content

- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)
- [DISTINCT (column)](./distinct.md)
- [FILTER function](./filter.md)
- [RELATED function](./related.md)
- [VALUES function](./values.md)
