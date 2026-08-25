---
name: ASINH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/asinh-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ASINH

Returns the inverse hyperbolic sine of a number. The inverse hyperbolic sine is the value whose hyperbolic sine is `number`, so ASINH(SINH(number)) equals `number`.

## Syntax

```dax
ASINH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Any real number.|

## Return value

Returns the inverse hyperbolic sine of a number.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ASINH(-2.5)`|Inverse hyperbolic sine of -2.5|-1.647231146|
|`= ASINH(10)`|Inverse hyperbolic sine of 10|2.99822295|
