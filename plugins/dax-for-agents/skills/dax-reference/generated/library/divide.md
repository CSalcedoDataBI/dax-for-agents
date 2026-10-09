---
name: DIVIDE
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/divide-function-dax.md@323524c
sourceDate: 
notes: true
examples: 3
---
# DIVIDE

Performs division and returns alternate result or BLANK() on division by 0.

## Syntax

```dax
DIVIDE(<numerator>, <denominator> [,<alternateresult>])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`numerator`|The dividend or number to divide.|
|`denominator`|The divisor or number to divide by.|
|`alternateresult`|(Optional) The value returned when division by zero results in an error. When not provided, the default value is BLANK().|

## Return value

- A decimal number.

## Remarks

- Alternate result on divide by 0 must be a constant.

- For best practices when using DIVIDE, see [DIVIDE function vs. divide operator (/) in DAX](https://learn.microsoft.com/en-us/dax/best-practices/dax-divide-function-operator).

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/divide.md`](../../examples/math-and-trig/divide.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns 2.5.

```dax
= DIVIDE(5,2)
```

## Example 1

The following example returns BLANK.

```dax
= DIVIDE(5,0)
```

## Example 2

The following example returns 1.

```dax
= DIVIDE(5,0,1)
```

## Related content

- [QUOTIENT function](./quotient.md)
- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
