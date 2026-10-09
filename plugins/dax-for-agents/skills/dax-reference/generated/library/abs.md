---
name: ABS
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/abs-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ABS

Returns the absolute value of a number.

## Syntax

```dax
ABS(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number for which you want the absolute value.|

## Return value

A decimal number.

## Remarks

The absolute value of a number is a decimal number, whole or decimal, without its sign. You can use the ABS function to ensure that only non-negative numbers are returned from expressions when nested in functions that require a positive number.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/abs.md`](../../examples/math-and-trig/abs.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns the absolute value of the difference between the list price and the dealer price, which you might use in a new calculated column, **DealerMarkup**.

```dax
= ABS([DealerPrice]-[ListPrice])
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [SIGN function](./sign.md)
