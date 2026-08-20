---
name: DEGREES
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/degrees-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DEGREES

Converts radians into degrees.

## Syntax

```dax
DEGREES(angle)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`angle`|Required. The angle in radians that you want to convert.|

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= DEGREES(PI())`|Degrees of pi radians|180|
