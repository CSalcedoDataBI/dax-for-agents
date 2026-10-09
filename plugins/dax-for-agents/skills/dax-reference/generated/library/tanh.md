---
name: TANH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/tanh-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# TANH

Returns the hyperbolic tangent of a number.

## Syntax

```dax
TANH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. Any real number.|

## Return value

Returns the hyperbolic tangent of a number.

## Remarks

- The formula for the hyperbolic tangent is:

    $$\text{TANH}(z) = \frac{\text{SINH}(z)}{\text{COSH}(z)}$$

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/tanh.md`](../../examples/math-and-trig/tanh.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= TANH(-2)`|Hyperbolic tangent of -2 (-0.96403)|-0.964028|
|`= TANH(0)`|Hyperbolic tangent of 0 (0)|0|
|`= TANH(0.5)`|Hyperbolic tangent of 0.5 (0.462117)|0.462117|
