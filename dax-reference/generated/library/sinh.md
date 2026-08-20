---
name: SINH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sinh-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# SINH

Returns the hyperbolic sine of a number.

## Syntax

```dax
SINH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. Any real number.|

## Return value

Returns the hyperbolic sine of a number.

## Remarks

- The formula for the hyperbolic sine is:

    $$\text{SINH}(z) = \frac{e^{z} - e^{-z}}{2}$$

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/sinh.md`](../../examples/math-and-trig/sinh.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

Probability of obtaining a result of less than 1.03 seconds.

```dax
= 2.868*SINH(0.0342\*1.03)
```

Returns, 0.1010491
