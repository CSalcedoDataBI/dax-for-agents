---
name: ISDOUBLE
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isdouble-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISDOUBLE

Checks whether a value is a floating-point number, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISDOUBLE(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to test.|

## Return value

`TRUE` if the value is a floating-point number; otherwise `FALSE`.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of ISDOUBLE.

```dax
EVALUATE
{
    IF ( ISDOUBLE ( 4.2 ), "Is double", "Is not double" ), // RETURNS: Is double
    IF ( ISDOUBLE ( 3.1E-1 ), "Is double", "Is not double" ), // RETURNS: Is double
    IF ( ISDOUBLE ( "42" ), "Is double", "Is not double" ), // RETURNS: Is not double
    IF ( ISDOUBLE ( 42 ), "Is double", "Is not double" ), // RETURNS: Is not double
}
```

## Related content

- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
