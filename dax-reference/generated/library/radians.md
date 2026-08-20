---
name: RADIANS
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/radians-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# RADIANS

Converts degrees to radians.

## Syntax

```dax
RADIANS(angle)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`angle`|Required. An angle in degrees that you want to convert.|

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= RADIANS(270)`|270 degrees as radians (4.712389 or 3π/2 radians)|4.712389|
