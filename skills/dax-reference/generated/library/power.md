---
name: POWER
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/power-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# POWER

Returns the result of a number raised to a power.

## Syntax

```dax
POWER(<number>, <power>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The base number, which can be any real number.|
|`power`|The exponent to which the base number is raised.|

## Return value

A decimal number.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns 25.

```dax
= POWER(5,2)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
