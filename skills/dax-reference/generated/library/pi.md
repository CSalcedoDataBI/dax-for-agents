---
name: PI
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/pi-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PI

Returns the value of Pi, 3.14159265358979, accurate to 15 digits.

## Syntax

```dax
PI()
```

## Return value

A decimal number with the value of Pi, 3.14159265358979, accurate to 15 digits.

## Remarks

Pi is a mathematical constant. In DAX, Pi is represented as a real number accurate to 15 digits, the same as Excel.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula calculates the area of a circle given the radius in the column, `[Radius]`.

```dax
= PI()*([Radius]*2)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
