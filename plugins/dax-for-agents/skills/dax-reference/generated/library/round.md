---
name: ROUND
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/round-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ROUND

Rounds a number to the specified number of digits.

## Syntax

```dax
ROUND(<number>, <num_digits>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number you want to round.|
|`num_digits`|The number of digits to which you want to round. A negative value rounds digits to the left of the decimal point; a value of zero rounds to the nearest integer.|

## Return value

A decimal number.

## Remarks

- If `num_digits` is greater than 0 (zero), then number is rounded to the specified number of decimal places.

- If `num_digits` is 0, the number is rounded to the nearest integer.

- If `num_digits` is less than 0, the number is rounded to the left of the decimal point.

- Ties are broken by rounding half away from zero (also known as commercial rounding).
  | Examples | Result |
  | --- | --- |
  | `= ROUND(1.15, 1)` | 1.2 |
  | `= ROUND(-1.15, 1)` | -1.2 |

- Related functions
  - To always round up (away from zero), use the ROUNDUP function.
  - To always round down (toward zero), use the ROUNDDOWN function.
  - To round a number to a specific multiple (for example, to round to the nearest multiple of 0.5), use the MROUND function.
  - Use the functions TRUNC and INT to obtain the integer portion of the number.

## Example 1

The following formula rounds 2.15 up, to one decimal place. The expected result is 2.2.

```dax
= ROUND(2.15,1)
```

## Example 2

The following formula rounds 21.5 to one decimal place to the left of the decimal point. The expected result is 20.

```dax
= ROUND(21.5,-1)
```

## Related content
- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [ROUND](./round.md)
- [ROUNDDOWN](./rounddown.md)
- [MROUND](./mround.md)
- [INT](./int.md)
- [TRUNC](./trunc.md)

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/round.md`](../../examples/math-and-trig/round.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
