---
name: COT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/cot-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# COT

Returns the cotangent of an angle specified in radians.

## Syntax

```dax
COT (<number>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The angle in radians for which you want the cotangent.|

## Return value

The cotangent of the given angle.

## Remarks

- The absolute value of number must be less than 2^27 and cannot be 0.

- If number is outside its constraints, an error is returned.

- If number is a non-numeric value, an error is returned.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/cot.md`](../../examples/math-and-trig/cot.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query,

```dax
EVALUATE { COT(30) }
```

Returns

|[Value] |
|---------|
|-0.156119952161659    |
