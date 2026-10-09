---
name: ISLOGICAL
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/islogical-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISLOGICAL

Checks whether a value is a logical value, (`TRUE` or `FALSE`), and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISLOGICAL(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value that you want to test.|

## Return value

`TRUE` if the value is a logical value; `FALSE` if any value other than `TRUE` OR `FALSE`.

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.
- This function is an alias of [ISBOOLEAN](./isboolean.md).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of ISLOGICAL.

```dax
EVALUATE
{
    IF ( ISLOGICAL ( TRUE ), "Is Boolean type or Logical", "Is different type" ), // RETURNS: Is Boolean type or Logical
    IF ( ISLOGICAL ( FALSE ), "Is Boolean type or Logical", "Is different type" ), // RETURNS: Is Boolean type or Logical
    IF ( ISLOGICAL ( 42 ), "Is Boolean type or Logical", "Is different type" ) // RETURNS: Is different type
}
```

## Related content
- [ISBOOLEAN](./isboolean.md)
- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
