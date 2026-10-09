---
name: ACOT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/acot-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ACOT

Returns the principal value of the arccotangent, or inverse cotangent of a number.

## Syntax

```dax
ACOT(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Number`|The cosine of the angle you want. Must be a real number.|

## Return value

A single decimal value.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/acot.md`](../../examples/math-and-trig/acot.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
