---
name: CUSTOMDATA
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/customdata-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CUSTOMDATA

Returns the content of the `CustomData` property in the connection string.

## Syntax

```dax
CUSTOMDATA()
```

## Return value

The content of the `CustomData` property in the connection string.

Blank, if `CustomData` property was not defined at connection time.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX formula verifies if the CustomData property was set to **`OK`**.

```dax
= IF(CUSTOMDATA()="OK", "Correct Custom data in connection string", "No custom data in connection string property or unexpected value")
```
