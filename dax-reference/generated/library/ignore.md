---
name: IGNORE
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/ignore-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# IGNORE

Modifies the behavior of the [SUMMARIZECOLUMNS](./summarizecolumns.md) function by omitting specific expressions from the BLANK/NULL evaluation. Rows for which all expressions not using IGNORE return BLANK/NULL will be excluded independent of whether the expressions which do use IGNORE evaluate to BLANK/NULL or not. This function can only be used within a [SUMMARIZECOLUMNS](./summarizecolumns.md) expression.

## Syntax

```dax
IGNORE(<expression>)
```

With SUMMARIZECOLUMNS,

```dax
SUMMARIZECOLUMNS(<groupBy_columnName>[, < groupBy_columnName >]…, [<filterTable>]…[, <name>, IGNORE(…)]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|Any DAX expression that returns a single value (not a table).|

## Return value

The function does not return a value.

## Remarks

IGNORE can only be used as an expression argument to [SUMMARIZECOLUMNS](./summarizecolumns.md).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [SUMMARIZECOLUMNS](./summarizecolumns.md).
