---
name: LCM
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/lcm-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# LCM

Returns the least common multiple of integers. The least common multiple is the smallest positive integer that is a multiple of all integer arguments number1, number2, and so on. Use LCM to add fractions with different denominators.

## Syntax

```dax
LCM(number1, number2)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number1, number2`|The two integers for which you want the least common multiple. If a value is not an integer, it is truncated.|

## Return value

Returns the least common multiple of integers.

## Remarks

- If any argument is nonnumeric, LCM returns the `#VALUE!` error value.

- If any argument is less than zero, LCM returns the `#NUM!` error value.

- If LCM(a,b) &gt;=2^53, LCM returns the `#NUM!` error value.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= LCM(5, 2)`|Least common multiple of 5 and 2.|10|
|`= LCM(24, 36)`|Least common multiple of 24 and 36.|72|
