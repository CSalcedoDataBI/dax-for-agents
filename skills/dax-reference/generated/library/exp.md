---
name: EXP
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/exp-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# EXP

Returns e raised to the power of a given number. The constant e equals 2.71828182845904, the base of the natural logarithm.

## Syntax

```dax
EXP(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The exponent applied to the base e. The constant e equals 2.71828182845904, the base of the natural logarithm.|

## Return value

A decimal number.

## Exceptions

## Remarks

- EXP is the inverse of LN, which is the natural logarithm of the given number.

- To calculate powers of bases other than e, use the exponentiation operator (^). For more information, see [DAX Operator Reference](https://learn.microsoft.com/en-us/dax/dax-operator-reference).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula calculates e raised to the power of the number contained in the column, `[Power]`.

```dax
= EXP([Power])
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [LN function](./ln.md)
- [EXP function](./exp.md)
- [LOG function](./log.md)
- [LOG function](./log.md)
