---
name: ROUNDDOWN
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/rounddown-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ROUNDDOWN

Rounds a number down, toward zero.

## Syntax

```dax
ROUNDDOWN(<number>, <num_digits>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|A real number that you want rounded down.|
|`num_digits`|The number of digits to which you want to round. Negative rounds to the left of the decimal point; zero to the nearest integer.|

## Return value

A decimal number.

## Remarks

- If `num_digits` is greater than 0 (zero), then the value in `number` is rounded down to the specified number of decimal places.

- If `num_digits` is 0, then the value in `number` is rounded down to the nearest integer.

- If `num_digits` is less than 0, then the value in `number` is rounded down to the left of the decimal point.

- ROUNDDOWN behaves like ROUND, except that it always rounds a number down. The INT function also rounds down, but with INT the result is always an integer, whereas with ROUNDDOWN you can control the precision of the result.

## Example 1

The following example rounds 3.14159 down to three decimal places. The expected result is 3.141.

```dax
= ROUNDDOWN(3.14159,3)
```

## Example 2

The following example rounds the value of 31415.92654 down to 2 decimal places to the left of the decimal. The expected result is 31400.

```dax
= ROUNDDOWN(31415.92654, -2)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [ROUND](./round.md)
- [ROUNDUP](./roundup.md)
- [ROUNDDOWN](./rounddown.md)
- [MROUND](./mround.md)
- [INT](./int.md)

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/rounddown.md`](../../examples/math-and-trig/rounddown.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
