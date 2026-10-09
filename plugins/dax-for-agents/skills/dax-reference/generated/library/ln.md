---
name: LN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/ln-function-dax.md@323524c
sourceDate: 
notes: false
examples: 5
---
# LN

Returns the natural logarithm of a number. Natural logarithms are based on the constant e (2.71828182845904).

## Syntax

```dax
LN(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The positive number for which you want the natural logarithm.|

## Return value

A decimal number.

## Remarks

LN is the inverse of the EXP function.

## Ejemplos ejecutables

**5** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/ln.md`](../../examples/math-and-trig/ln.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns the natural logarithm of the number in the column, `[Values]`.

```dax
= LN([Values])
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [EXP function](./exp.md)
