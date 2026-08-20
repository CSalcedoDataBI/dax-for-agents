---
name: ISNUMERIC
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isnumeric-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISNUMERIC

Checks whether a value is a number, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISNUMERIC(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to test.|

## Return value

`TRUE` if the value is numeric; otherwise `FALSE`.

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.
- This function is an alias of [ISNUMBER](./isnumber.md).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of ISNUMERIC.

```dax
EVALUATE
{
    IF ( ISNUMERIC ( 0 ), "Is number", "Is Not number" ), // RETURNS: Is number
    IF ( ISNUMERIC ( 3.1E-1 ), "Is number", "Is Not number" ), // RETURNS: Is number
    IF ( ISNUMERIC ( "42" ), "Is number", "Is Not number" ) // RETURNS: Is Not number
}
```

## Related content

- [ISNUMBER](./isnumber.md)
- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
