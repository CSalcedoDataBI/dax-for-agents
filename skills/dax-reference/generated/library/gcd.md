---
name: GCD
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/gcd-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# GCD

Returns the greatest common divisor of two or more integers. The greatest common divisor is the largest integer that divides both number1 and number2 without a remainder.

## Syntax

```dax
GCD(number1, number2)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number1, number2`|The two integers for which you want the greatest common divisor. If a value is not an integer, it is truncated.|

## Return value

The greatest common divisor of two or more integers.

## Remarks

- If any argument is nonnumeric, GCD returns the `#VALUE!` error value.

- If any argument is less than zero, GCD returns the `#NUM!` error value.

- One divides any value evenly.

- A prime number has only itself and one as even divisors.

- If a parameter to GCD is &gt;=2^53, GCD returns the `#NUM!` error value.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/math-and-trig/gcd.md`](../../examples/math-and-trig/gcd.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|DAX expression|Description|Result|
|-----------|---------------|----------|
|`= GCD(5, 2)`|Greatest common divisor of 5 and 2.|1|
|`= GCD(24, 36)`|Greatest common divisor of 24 and 36.|12|
|`= GCD(7, 1)`|Greatest common divisor of 7 and 1.|1|
