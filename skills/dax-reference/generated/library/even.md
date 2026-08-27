---
name: EVEN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/even-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# EVEN

Returns number rounded up to the nearest even integer. You can use this function for processing items that come in twos. For example, a packing crate accepts rows of one or two items. The crate is full when the number of items, rounded up to the nearest two, matches the crate's capacity.

## Syntax

```dax
EVEN(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The value to round.|

## Return value

Returns number rounded up to the nearest even integer.

## Remarks

- If `number` is nonnumeric, EVEN returns the `#VALUE!` error value.

- Regardless of the sign of number, a value is rounded up when adjusted away from zero. If number is an even integer, no rounding occurs.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/even.md`](../../examples/math-and-trig/even.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= EVEN(1.5)`|Rounds 1.5 to the nearest even integer|2|
|`= EVEN(3)`|Rounds 3 to the nearest even integer|4|
|`= EVEN(2)`|Rounds 2 to the nearest even integer|2|
|`= EVEN(-1)`|Rounds -1 to the nearest even integer|-2|
