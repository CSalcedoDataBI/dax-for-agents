---
name: ISODD
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isodd-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ISODD

Returns `TRUE` if number is odd, or `FALSE` if number is even.

## Syntax

```dax
ISODD(number)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`number`|The value to test. If number is not an integer, it is truncated.|

## Return value

Returns `TRUE` if number is odd, or `FALSE` if number is even.

## Remarks

- If number is nonnumeric, ISODD returns the `#VALUE!` error value.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/isodd.md`](../../examples/information/isodd.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
