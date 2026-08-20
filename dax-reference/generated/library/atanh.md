---
name: ATANH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/atanh-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ATANH

Returns the inverse hyperbolic tangent of a number. Number must be between -1 and 1 (excluding -1 and 1). The inverse hyperbolic tangent is the value whose hyperbolic tangent is `number`, so ATANH(TANH(number)) equals `number`.

## Syntax

```dax
ATANH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Any real number between 1 and -1.|

## Return value

Returns the inverse hyperbolic tangent of a number.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ATANH(0.76159416)`|Inverse hyperbolic tangent of 0.76159416|1.00000001|
|`= ATANH(-0.1)`||-0.100335348|

## Related content

- [ATAN function](./atan.md)
