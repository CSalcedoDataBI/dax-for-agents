---
name: COS
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/cos-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# COS

Returns the cosine of the given angle.

## Syntax

```dax
COS(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. The angle in radians for which you want the cosine.|

## Return value

Returns the cosine of the given angle.

## Remarks

If the angle is in degrees, either multiply the angle by PI()/180 or use the RADIANS function to convert the angle to radians.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/cos.md`](../../examples/math-and-trig/cos.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= COS(1.047)`|Cosine of 1.047 radians|0.5001711|
|`= COS(60*PI()/180)`|Cosine of 60 degrees|0.5|
|`= COS(RADIANS(60))`|Cosine of 60 degrees|0.5|
