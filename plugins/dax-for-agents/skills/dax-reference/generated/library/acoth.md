---
name: ACOTH
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/acoth-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# ACOTH

Returns the inverse hyperbolic cotangent of a number.

## Syntax

```dax
ACOTH(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Number`|The absolute value of Number must be greater than 1.|

## Return value

A single decimal value.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/acoth.md`](../../examples/math-and-trig/acoth.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
