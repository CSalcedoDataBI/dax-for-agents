---
name: NONVISUAL
category: [information]
primaryCategory: information
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/nonvisual-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NONVISUAL

Marks a value filter in a [SUMMARIZECOLUMNS](./summarizecolumns.md) expression as non-visual. This function can only be used within a [SUMMARIZECOLUMNS](./summarizecolumns.md) expression.

## Syntax

```dax
NONVISUAL(<expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|Any DAX expression that returns a single value (not a table).|

## Return value

A table of values.

## Remarks

- Marks a value filter in [SUMMARIZECOLUMNS](./summarizecolumns.md) as not affecting measure values, but only applying to group-by columns.

- This function can only be used within a [SUMMARIZECOLUMNS](./summarizecolumns.md) expression. It's used as either a filterTable argument of the [SUMMARIZECOLUMNS](./summarizecolumns.md) function or a groupLevelFilter argument of the [ROLLUPADDISSUBTOTAL](./rollupaddissubtotal.md) or [ROLLUPISSUBTOTAL](./rollupissubtotal.md) function.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [SUMMARIZECOLUMNS](./summarizecolumns.md).
