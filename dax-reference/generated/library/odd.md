---
name: ODD
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/odd-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ODD

Returns number rounded up to the nearest odd integer.

## Syntax

```dax
ODD(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|Required. The value to round.|

## Return value

Returns number rounded up to the nearest odd integer.

## Remarks

- If `number` is nonnumeric, ODD returns the `#VALUE!` error value.

- Regardless of the sign of number, a value is rounded up when adjusted away from zero. If number is an odd integer, no rounding occurs.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= ODD(1.5)`|Rounds 1.5 up to the nearest odd integer.|3|
|`= ODD(3)`|Rounds 3 up to the nearest odd integer.|3|
|`= ODD(2)`|Rounds 2 up to the nearest odd integer.|3|
|`= ODD(-1)`|Rounds -1 up to the nearest odd integer.|-1|
|`= ODD(-2)`|Rounds -2 up (away from 0) to the nearest odd integer.|-3|
