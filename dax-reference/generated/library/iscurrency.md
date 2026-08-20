---
name: ISCURRENCY
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/iscurrency-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISCURRENCY

Checks whether a value is a decimal number, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISCURRENCY(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to test.|

## Return value

`TRUE` if the value is a a decimal number; otherwise `FALSE`.

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.
- This functions is an alias of [ISDECIMAL](./isdecimal.md).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of ISCURRENCY.

```dax
EVALUATE
{
    IF ( ISCURRENCY ( 3.1E-1 ), "Is currency", "Is not currency" ), // RETURNS: Is not currency
    IF ( ISCURRENCY ( "42" ), "Is currency", "Is not currency" ), // RETURNS: Is not currency
    IF ( ISCURRENCY ( 42 ), "Is currency", "Is not currency" ), // RETURNS: Is not currency
    IF ( ISCURRENCY ( CURRENCY ( 4.2421 ) ), "Is currency", "Is not currency" ) // RETURNS: Is currency
}
```

## Related content

- [ISDECIMAL](./isdecimal.md)
- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
