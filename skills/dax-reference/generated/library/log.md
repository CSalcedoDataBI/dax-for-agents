---
name: LOG
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/log-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# LOG

Returns the logarithm of a number to the base you specify.

## Syntax

```dax
LOG(<number>,<base>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The positive number for which you want the logarithm.|
|`base`|The base of the logarithm. If omitted, the base is 10.|

## Return value

A decimal number.

## Remarks

You might receive an error if the value is too large to be displayed.

The function LOG10 is similar, but always returns the common logarithm, meaning the logarithm for the base 10.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formulas return the same result, 2.

```dax
= LOG(100,10)
= LOG(100)
= LOG10(100)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [EXP function](./exp.md)
- [LOG function](./log.md)
- [LOG function](./log.md)
