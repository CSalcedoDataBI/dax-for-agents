---
name: SQRTPI
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sqrtpi-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# SQRTPI

Returns the square root of (number * pi).

## Syntax

```dax
SQRTPI(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. The number by which pi is multiplied.|

## Return value

Returns the square root of (number * pi).

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/sqrtpi.md`](../../examples/math-and-trig/sqrtpi.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= SQRTPI(1)`|Square root of pi.|1.772454|
|`= SQRTPI(2)`|Square root of 2 * pi.|2.506628|
