---
name: ROUNDUP
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/roundup-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ROUNDUP

Rounds a number up, away from 0 (zero).

## Syntax

```dax
ROUNDUP(<number>, <num_digits>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|A real number that you want to round up.|
|`num_digits`|The number of digits to which you want to round. A negative value for `num_digits` rounds to the left of the decimal point; if `num_digits` is zero or is omitted, `number` is rounded to the nearest integer.|

## Return value

A decimal number.

## Remarks

- If `num_digits` is greater than 0 (zero), then the number is rounded up to the specified number of decimal places.

- If `num_digits` is 0, then number is rounded up to the nearest integer.

- If `num_digits` is less than 0, then number is rounded up to the left of the decimal point.

- ROUNDUP behaves like ROUND, except that it always rounds a number up.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/roundup.md`](../../examples/math-and-trig/roundup.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following formula rounds Pi to four decimal places. The expected result is 3.1416.

```dax
= ROUNDUP(PI(),4)
```

## Example: Decimals as Second Argument

The following formula rounds 1.3 to the nearest multiple of 0.2. The expected result is 2.

```dax
= ROUNDUP(1.3,0.2)
```

## Example: Negative Number as Second Argument

The following formula rounds the value in the column, **FreightCost**, with the expected results shown in the following table:

```dax
= ROUNDUP([Values],-1)
```

When `num_digits` is less than zero, the number of places to the left of the decimal sign is increased by the value you specify.

|FreightCost|Expected Result|
|---------------|-------------------|
|13.25|20|
|2.45|10|
|25.56|30|
|1.34|10|
|345.01|350|

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [ROUND](./round.md)
- [ROUNDDOWN](./rounddown.md)
- [MROUND](./mround.md)
- [INT](./int.md)
