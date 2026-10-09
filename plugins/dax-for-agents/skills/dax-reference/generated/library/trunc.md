---
name: TRUNC
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/trunc-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# TRUNC

Truncates a number to an integer by removing the decimal, or fractional, part of the number.

## Syntax

```dax
TRUNC(<number>,<num_digits>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number you want to truncate.|
|`num_digits`|A number specifying the precision of the truncation; if omitted, 0 (zero)|

## Return value

A whole number.

## Remarks

TRUNC and INT are similar in that both return integers. TRUNC removes the fractional part of the number. INT rounds numbers down to the nearest integer based on the value of the fractional part of the number. INT and TRUNC are different only when using negative numbers: `TRUNC(-4.3)` returns -4, but `INT(-4.3)` returns -5 because -5 is the smaller number.

## Example 1

The following formula returns 3, the integer part of pi.

```dax
= TRUNC(PI())
```

## Example 2

The following formula returns -8, the integer part of -8.9.

```dax
= TRUNC(-8.9)
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
[`examples/math-and-trig/trunc.md`](../../examples/math-and-trig/trunc.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
