---
name: MROUND
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/mround-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# MROUND

Returns a number rounded to the desired multiple.

## Syntax

```dax
MROUND(<number>, <multiple>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number to round.|
|`multiple`|The multiple of significance to which you want to round the number.|

## Return value

A decimal number.

## Remarks

MROUND rounds up, away from zero, if the remainder of dividing `number` by the specified `multiple` is greater than or equal to half the value of `multiple`.

## Example: Decimal Places

The following expression rounds 1.3 to the nearest multiple of .2. The expected result is 1.4.

```dax
= MROUND(1.3,0.2)
```

## Example: Negative Numbers

The following expression rounds -10 to the nearest multiple of -3. The expected result is -9.

```dax
= MROUND(-10,-3)
```

## Example: Error

The following expression returns an error, because the numbers have different signs.

```dax
= MROUND(5,-2)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [ROUND function](./round.md)
- [ROUNDUP function](./roundup.md)
- [ROUNDDOWN function](./rounddown.md)
- [MROUND function](./mround.md)
- [INT function](./int.md)

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/mround.md`](../../examples/math-and-trig/mround.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
