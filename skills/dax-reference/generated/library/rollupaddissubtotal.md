---
name: ROLLUPADDISSUBTOTAL
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/rollupaddissubtotal-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ROLLUPADDISSUBTOTAL

Modifies the behavior of the [SUMMARIZECOLUMNS](./summarizecolumns.md) function by adding rollup/subtotal rows to the result based on the groupBy_columnName columns. This function can only be used within a [SUMMARIZECOLUMNS](./summarizecolumns.md) expression.

## Syntax

```dax
ROLLUPADDISSUBTOTAL ( [<grandtotalFilter>], <groupBy_columnName>, <name> [, [<groupLevelFilter>] [, <groupBy_columnName>, <name> [, [<groupLevelFilter>] [, … ] ] ] ] )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`grandtotalFilter`|(Optional) Filter to be applied to the grandtotal level.|
|`groupBy_columnName`|Name of an existing column used to create summary groups based on the values found in it. Cannot be an expression.|
|name |Name of an ISSUBTOTAL column. The values of the column are calculated using the ISSUBTOTAL function.|
|`groupLevelFilter`|(Optional) Filter to be applied to the current level.|

## Return value

The function does not return a value.

## Remarks

None

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [SUMMARIZECOLUMNS](./summarizecolumns.md).
