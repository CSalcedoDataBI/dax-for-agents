---
name: ROLLUP
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/rollup-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ROLLUP

Modifies the behavior of the [SUMMARIZE](./summarize.md) function by adding rollup rows to the result on columns defined by the groupBy_columnName parameter. This function can only be used within a [SUMMARIZE](./summarize.md) expression.

## Syntax

```dax
ROLLUP ( <groupBy_columnName> [, <groupBy_columnName> [, … ] ] )
```

With SUMMARIZE,

```dax
SUMMARIZE(<table>, <groupBy_columnName>[, <groupBy_columnName>]…[, ROLLUP(<groupBy_columnName>[,< groupBy_columnName>…])][, <name>, <expression>]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
| groupBy_columnName | The qualified name of an existing column or ROLLUPGROUP function to be used to create summary groups based on the values found in it. This parameter cannot be an expression.  |

## Return value

This function does not return a value. It only specifies the set of columns to be subtotaled.

## Remarks

This function can only be used within a [SUMMARIZE](./summarize.md) expression.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [SUMMARIZE](./summarize.md).
