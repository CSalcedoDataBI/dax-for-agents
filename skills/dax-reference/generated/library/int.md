---
name: INT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/int-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# INT

Rounds a number down to the nearest integer.

## Syntax

```dax
INT(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number you want to round down to an integer|

## Return value

A whole number.

## Remarks

TRUNC and INT are similar in that both return integers. TRUNC removes the fractional part of the number. INT rounds numbers down to the nearest integer based on the value of the fractional part of the number. INT and TRUNC are different only when using negative numbers: `TRUNC(-4.3)` returns -4, but `INT(-4.3)` returns -5 because -5 is the lower number.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/int.md`](../../examples/math-and-trig/int.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following expression rounds the value to 1. If you use the ROUND function, the result would be 2.

```dax
= INT(1.5)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [ROUND function](./round.md)
- [ROUNDUP function](./roundup.md)
- [ROUNDDOWN function](./rounddown.md)
- [MROUND function](./mround.md)
