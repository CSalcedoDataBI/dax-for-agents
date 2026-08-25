---
name: COSH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/cosh-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# COSH

Returns the hyperbolic cosine of a number.

## Syntax

```dax
COSH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. Any real number for which you want to find the hyperbolic cosine.|

## Return value

The hyperbolic cosine of a number.

## Remarks

- The formula for the hyperbolic cosine is:

    $$\text{COSH}(z) = \frac{e^{z} + e^{-z}}{2}$$

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/cosh.md`](../../examples/math-and-trig/cosh.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|DAX expression|Description|Result|
|-----------|---------------|----------|
|`= COSH(4)`|Hyperbolic cosine of 4|27.308233|
|`= COSH(EXP(1))`|Hyperbolic cosine of the base of the natural logarithm.|7.6101251|
