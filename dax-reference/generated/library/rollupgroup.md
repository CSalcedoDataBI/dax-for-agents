---
name: ROLLUPGROUP
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/rollupgroup-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ROLLUPGROUP

Modifies the behavior of the [SUMMARIZE](./summarize.md) and [SUMMARIZECOLUMNS](./summarizecolumns.md) functions by adding rollup rows to the result on columns defined by the the groupBy_columnName parameter. This function can only be used within a [SUMMARIZE](./summarize.md) or [SUMMARIZECOLUMNS](./summarizecolumns.md) expression.

## Syntax

```dax
ROLLUPGROUP ( <groupBy_columnName> [, <groupBy_columnName> [, … ] ] )
```

### Parameters

|Term|Definition|
|--------|--------------|
| groupBy_columnName | The qualified name of an existing column or ROLLUPGROUP function to be used to create summary groups based on the values found in it. This parameter cannot be an expression.  |

## Return value

This function does not return a value. It marks a set of columns to be treated as a single group during subtotaling by [ROLLUP](./rollup.md) or [ROLLUPADDISSUBTOTAL](./rollupaddissubtotal.md).

## Remarks

ROLLUPGROUP can only be used as a groupBy_columnName argument to [ROLLUP](./rollup.md), [ROLLUPADDISSUBTOTAL](./rollupaddissubtotal.md), or [ROLLUPISSUBTOTAL](./rollupissubtotal.md).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [SUMMARIZE](./summarize.md) and [SUMMARIZECOLUMNS](./summarizecolumns.md).
