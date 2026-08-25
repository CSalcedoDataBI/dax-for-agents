---
name: SQRT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sqrt-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SQRT

Returns the square root of a number.

## Syntax

```dax
SQRT(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number for which you want the square root, a column that contains numbers, or an expression that evaluates to a number.|

## Return value

A decimal number.

## Remarks

If the number is negative, the SQRT function returns an error.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula,

```dax
= SQRT(25)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
