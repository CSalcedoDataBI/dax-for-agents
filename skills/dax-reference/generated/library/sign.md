---
name: SIGN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sign-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# SIGN

Determines the sign of a number, the result of a calculation, or a value in a column. The function returns 1 if the number is positive, 0 (zero) if the number is zero, or -1 if the number is negative.

## Syntax

```dax
SIGN(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Any real number, a column that contains numbers, or an expression that evaluates to a number.|

## Return value

A whole number. The possible Return values are 1, 0, and -1.

|Return value|Description|
|----------------|---------------|
|1|The number is positive|
|0|The number is zero|
|-1|The number is negative|

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/sign.md`](../../examples/math-and-trig/sign.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula returns the sign of the result of the expression that calculates sale price minus cost.

```dax
= SIGN( ([Sale Price] - [Cost]) )
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
