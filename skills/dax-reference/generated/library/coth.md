---
name: COTH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/coth-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# COTH

Returns the hyperbolic cotangent of a hyperbolic angle.

## Syntax

```dax
COTH (<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The hyperbolic angle in radians for which you want the hyperbolic cotangent.|

## Return value

The hyperbolic cotangent of the given angle.

## Remarks

- The hyperbolic cotangent is an analog of the ordinary (circular) cotangent.

- The absolute value of number must be less than $2^{27}$ and cannot be 0.

- If number is outside its constraints, an error is returned

- If number is a non-numeric value, an error is returned.

- The following equation is used:

    $$\text{COTH}(N) = \frac{1}{\text{TANH}(N)} = \frac{\text{COSH(N)}}{\text{SINH(N)}} = \frac{e^{N} + e^{-N}}{e^{N} - e^{-N}}$$

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query,

```dax
EVALUATE { COTH(2) }
```

Returns

|[Value] |
|---------|
|1.03731472072755   |
