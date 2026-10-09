---
name: SIN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sin-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# SIN

Returns the sine of the given angle.

## Syntax

```dax
SIN(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. The angle in radians for which you want the sine.|

## Return value

Returns the sine of the given angle.

## Remarks

If an argument is in degrees, multiply it by `PI()/180` or use the RADIANS function to convert it to radians.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/sin.md`](../../examples/math-and-trig/sin.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= SIN(PI())`|Sine of pi radians (0, approximately).|0.0|
|`= SIN(PI()/2)`|Sine of pi/2 radians.|1.0|
|`= SIN(30*PI()/180)`|Sine of 30 degrees.|0.5|
|`= SIN(RADIANS(30))`|Sine of 30 degrees.|0.5|
