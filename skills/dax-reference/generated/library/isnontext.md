---
name: ISNONTEXT
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isnontext-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ISNONTEXT

Checks if a value is not text (blank cells are not text), and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISNONTEXT(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to check.|

## Return value

`TRUE` if the value is not text or blank; `FALSE` if the value is text.

## Remarks

- An empty string is considered text.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/isnontext.md`](../../examples/information/isnontext.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of the ISNONTEXT function.

```dax
EVALUATE {
    IF( ISNONTEXT( 1 ), "Is Non-Text", "Is Text" ), // RETURNS: Is Non-Text
    IF( ISNONTEXT( BLANK ( ) ), "Is Non-Text", "Is Text" ), // RETURNS: Is Non-Text
    IF( ISNONTEXT( ""), "Is Non-Text", "Is Text" ) // RETURNS: Is Text
}
```

## Related content

- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
