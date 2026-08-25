---
name: FLOOR
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/floor-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# FLOOR

Rounds a number down, toward zero, to the nearest multiple of significance.

## Syntax

```dax
FLOOR(<number>, <significance>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The numeric value you want to round.|
|`significance`|The multiple to which you want to round. The arguments`number` and `significance` must either both be positive, or both be negative.|

## Return value

A decimal number.

## Remarks

- If either argument is nonnumeric, FLOOR returns `#VALUE!` error value.

- If number and significance have different signs, FLOOR returns the `#NUM!` error value.

- Regardless of the sign of the number, a value is rounded down when adjusted away from zero. If the number is an exact multiple of significance, no rounding occurs.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/floor.md`](../../examples/math-and-trig/floor.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula takes the values in the [Total Product Cost] column from the table, InternetSales, and rounds down to the nearest multiple of .1.

```dax
= FLOOR(InternetSales[Total Product Cost],.1)
```

The following table shows the expected results for some sample values:

|Values|Expected Result|
|----------|-------------------|
|10.8423|10.8|
|8.0373|8|
|2.9733|2.9|

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
