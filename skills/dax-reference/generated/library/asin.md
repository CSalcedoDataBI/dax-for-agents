---
name: ASIN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/asin-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# ASIN

Returns the arcsine, or inverse sine, of a number. The arcsine is the angle whose sine is `number`. The returned angle is given in radians in the range -pi/2 to pi/2.

## Syntax

```dax
ASIN(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The sine of the angle you want and must be from -1 to 1.|

## Return value

Returns the arcsine, or inverse sine, of a number.

## Remarks

To express the arcsine in degrees, multiply the result by 180/PI( ) or use the DEGREES function.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/asin.md`](../../examples/math-and-trig/asin.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ASIN(-0.5)`|Arcsine of -0.5 in radians, -pi/6|-0.523598776|
|`= ASIN(-0.5)*180/PI()`|Arcsine of -0.5 in degrees|-30|
|`= DEGREES(ASIN(-0.5))`|Arcsine of -0.5 in degrees|-30|
