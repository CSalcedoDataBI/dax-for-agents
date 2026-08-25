---
name: ACOSH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/acosh-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ACOSH

Returns the inverse hyperbolic cosine of a number. The number must be greater than or equal to 1. The inverse hyperbolic cosine is the value whose hyperbolic cosine is `number`, so ACOSH(COSH(number)) equals number.

## Syntax

```dax
ACOSH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Any real number equal to or greater than 1.|

## Return value

Returns the inverse hyperbolic cosine of a number.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ACOSH(1)`|Inverse hyperbolic cosine of 1.|0|
|`= ACOSH(10)`|Inverse hyperbolic cosine of 10.|2.993228|

