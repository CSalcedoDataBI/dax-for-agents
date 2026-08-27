---
name: RANDBETWEEN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/randbetween-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# RANDBETWEEN

Returns a random number in the range between two numbers you specify.

## Syntax

```dax
RANDBETWEEN(<bottom>,<top>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Bottom`|The smallest integer the function will return.|
|`Top`|The largest integer the function will return.|

## Return value

A whole number.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/randbetween.md`](../../examples/math-and-trig/randbetween.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula returns a random number between 1 and 10.

```dax
= RANDBETWEEN(1,10)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
