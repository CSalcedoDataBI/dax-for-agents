---
name: ISSTRING
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isstring-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ISSTRING

Checks if a value is text, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISSTRING(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to check.|

## Return value

`TRUE` if the value is text; otherwise `FALSE`.

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.
- This function is an alias of [ISTEXT](./istext.md).

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/isstring.md`](../../examples/information/isstring.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of the ISSTRING function.


```dax
EVALUATE
{
    IF ( ISSTRING ( "text" ), "Is Text", "Is Non-Text" ), // RETURNS: Is Text
    IF ( ISSTRING ( "" ), "Is Text", "Is Non-Text" ), // RETURNS: Is Text
    IF ( ISSTRING ( 42 ), "Is Text", "Is Non-Text" ), // RETURNS: Is Non-Text
    IF ( ISSTRING ( BLANK () ), "Is Text", "Is Non-Text" ) // RETURNS: Is Non-Text
}
```

## Related content

- [ISTEXT](./istext.md)
- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
