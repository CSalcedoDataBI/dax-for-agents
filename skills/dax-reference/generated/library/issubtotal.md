---
name: ISSUBTOTAL
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/issubtotal-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISSUBTOTAL

Creates another column in a [SUMMARIZE](./summarize.md) expression that returns True if the row contains subtotal values for the column given as argument, otherwise returns False.

## Syntax

```dax
ISSUBTOTAL(<columnName>)
```

With [SUMMARIZE](./summarize.md),

```dax
SUMMARIZE(<table>, <groupBy_columnName>[, <groupBy_columnName>]…[, ROLLUP(<groupBy_columnName>[,< groupBy_columnName>…])][, <name>, {<expression>|ISSUBTOTAL(<columnName>)}]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`columnName`  |The name of any column in table of the SUMMARIZE function or any column in a related table to table.  |

## Return value

A True value if the row contains a subtotal value for the column given as argument, otherwise returns False.

## Remarks

- This function can only be used in the expression of a [SUMMARIZE](./summarize.md) function.

- This function must be preceded by the name of the Boolean column.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [SUMMARIZE](./summarize.md).
