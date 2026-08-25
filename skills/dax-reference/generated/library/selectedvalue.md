---
name: SELECTEDVALUE
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/selectedvalue-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# SELECTEDVALUE

Returns the value when the context for columnName has been filtered down to one distinct value only. Otherwise returns alternateResult.

## Syntax

```dax
SELECTEDVALUE(<columnName>[, <alternateResult>])
```

### Parameters

|Term|Definition|
|----------|--------------|
| `columnName` |The name of an existing column, using standard DAX syntax. It cannot be an expression. |
| `alternateResult` |(Optional) The value returned when the context for columnName has been filtered down to zero or more than one distinct value. When not provided, the default value is BLANK().|

## Return value

The value when the context for columnName has been filtered down to one distinct value only. Else, alternateResult.

## Remarks

- An equivalent expression for `SELECTEDVALUE(<columnName>, <alternateResult>)` is `IF(HASONEVALUE(<columnName>), VALUES(<columnName>), <alternateResult>)`.

- To learn more about best practices when using SELECTEDVALUE, see [Use SELECTEDVALUE instead of VALUES in DAX](https://learn.microsoft.com/en-us/dax/best-practices/dax-selectedvalue).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query:

```dax
DEFINE
 MEASURE DimProduct[Selected Color] = SELECTEDVALUE(DimProduct[Color], "No Single Selection")
EVALUATE
 SUMMARIZECOLUMNS
   (ROLLUPADDISSUBTOTAL(DimProduct[Color], "Is Total"),
   "Selected Color", [Selected Color])ORDER BY [Is Total] ASC,
   [Color] ASC
```

Returns the following:

DimProduct[Color]  |[Is Total]  |[Selected Color]
---------|---------|---------|
Black     |  `FALSE`       |   Black      |
Blue     |   `FALSE`      |    Blue     |
Grey     |  `FALSE`       |   Grey      |
Multi     |   `FALSE`      |   Multi     |
NA     |   `FALSE`      |      NA   |
Red     |  `FALSE`       |   Red     |
Silver     |  `FALSE`       |  Silver   |
Silver/Black     | `FALSE`        |   Silver/Black |
White     |   `FALSE`      |  White       |
Yellow    | `FALSE`        |  Yellow       |
|``| `TRUE` | No Single Selection|
