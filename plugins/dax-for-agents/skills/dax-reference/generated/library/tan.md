---
name: TAN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/tan-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# TAN

Returns the tangent of the given angle.

## Syntax

```dax
TAN(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. The angle in radians for which you want the tangent.|

## Return value

Returns the tangent of the given angle.

## Remarks

If your argument is in degrees, multiply it by PI()/180 or use the RADIANS function to convert it to radians.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/tan.md`](../../examples/math-and-trig/tan.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= TAN(0.785)`|Tangent of 0.785 radians (0.99920)|0.99920|
|`= TAN(45*PI()/180)`|Tangent of 45 degrees (1)|1|
|`= TAN(RADIANS(45))`|Tangent of 45 degrees (1)|1|
