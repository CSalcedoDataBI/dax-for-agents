---
name: MOD
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/mod-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# MOD

Returns the remainder after a number is divided by a divisor. The result always has the same sign as the divisor.

## Syntax

```dax
MOD(<number>, <divisor>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The number for which you want to find the remainder after the division is performed.|
|`divisor`|The number by which you want to divide.|

## Return value

A whole number.

## Remarks

- If the divisor is 0 (zero), MOD returns an error. You cannot divide by 0.

- The MOD function can be expressed in terms of the INT function: MOD(n, d) = n - d*INT(n/d)

## Example 1

The following formula returns 1, the remainder of 3 divided by 2.

```dax
= MOD(3,2)
```

## Example 2

The following formula returns -1, the remainder of 3 divided by 2. Note that the sign is always the same as the sign of the divisor.

```dax
= MOD(-3,-2)
```

## Related content

- [Math and Trig functions](https://learn.microsoft.com/en-us/dax/math-and-trig-functions-dax)
- [ROUND function](./round.md)
- [ROUNDUP function](./roundup.md)
- [ROUNDDOWN function](./rounddown.md)
- [MROUND function](./mround.md)
- [INT function](./int.md)

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/mod.md`](../../examples/math-and-trig/mod.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
