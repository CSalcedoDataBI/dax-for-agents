---
name: QUOTIENT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/quotient-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# QUOTIENT

Performs division and returns only the integer portion of the division result. Use this function when you want to discard the remainder of division.

## Syntax

```dax
QUOTIENT(<numerator>, <denominator>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`numerator`|The dividend, or number to divide.|
|`denominator`|The divisor, or number to divide by.|

## Return value

A whole number.

## Remarks

- If either argument is non-numeric, QUOTIENT returns the `#VALUE!` error value.

- You can use a column reference instead of a literal value for either argument. However, if the column that you reference contains a 0 (zero), an error is returned for the entire column of values.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/quotient.md`](../../examples/math-and-trig/quotient.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formulas return the same result, 2.

```dax
= QUOTIENT(5,2)
```

```dax
= QUOTIENT(10/2,2)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
