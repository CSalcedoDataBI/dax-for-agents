---
name: FACT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/fact-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# FACT

Returns the factorial of a number, equal to the series 1*2\*3\*...\* , ending in the given number.

## Syntax

```dax
FACT(<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The non-negative number for which you want to calculate the factorial.|

## Return value

A decimal number.

## Remarks

- If the number is not an integer, it is truncated and an error is returned. If the result is too large, an error is returned.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula returns the factorial for the series of integers in the column, `[Values]`.

```dax
= FACT([Values])
```

The following table shows the expected results:

|Values|Results|
|----------|-----------|
|0|1|
|1|1|
|2|2|
|3|6|
|4|24|
|5|120|
|170|7.257415615308E+306|

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [TRUNC function](./trunc.md)
