---
name: ACOS
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/acos-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# ACOS

Returns the arccosine, or inverse cosine, of a number. The arccosine is the angle whose cosine is`number`. The returned angle is given in radians in the range 0 (zero) to pi.

## Syntax

```dax
ACOS(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Number`|The cosine of the angle you want and must be from -1 to 1.|

## Return value

Returns the arccosine, or inverse cosine, of a number.

## Remarks

If you want to convert the result from radians to degrees, multiply it by 180/PI() or use the DEGREES function.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/acos.md`](../../examples/math-and-trig/acos.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ACOS(-0.5)`|Arccosine of -0.5 in radians, 2*pi/3.|2.094395102|
|`= ACOS(-0.5)*180/PI()`|Arccosine of -0.5 in degrees.|120|
