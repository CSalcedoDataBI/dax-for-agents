---
name: ATAN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/atan-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ATAN

Returns the arctangent, or inverse tangent, of a number. The arctangent is the angle whose tangent is `number`. The returned angle is given in radians in the range -pi/2 to pi/2.

## Syntax

```dax
ATAN(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The tangent of the angle you want.|

## Return value

Returns the inverse tangent of a number.

## Remarks

To express the arctangent in degrees, multiply the result by 180/PI( ) or use the DEGREES function.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/atan.md`](../../examples/math-and-trig/atan.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ATAN(1)`|Arctangent of 1 in radians, pi/4|0.785398163|
|`= ATAN(1)*180/PI()`|Arctangent of 1 in degrees|45|
