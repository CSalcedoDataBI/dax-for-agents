---
name: ISDATETIME
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isdatetime-function-dax.md@323524c
sourceDate: 
notes: false
examples: 3
---
# ISDATETIME

Checks whether a value is a date / time, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISDATETIME(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to test.|

## Return value

`TRUE` if the value is a date / time; otherwise `FALSE`.

## Remarks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/isdatetime.md`](../../examples/information/isdatetime.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query shows the behavior of ISDATETIME.

```dax
EVALUATE
{
    IF ( ISDATETIME ( 42 ), "Is datetime", "Is not datetime" ), // RETURNS: Is not datetime
    IF ( ISDATETIME ( "42" ), "Is datetime", "Is not datetime" ), // RETURNS: Is not datetime
    IF ( ISDATETIME ( "2025-07-01" ), "Is datetime", "Is not datetime" ), // RETURNS: Is not datetime
    IF ( ISDATETIME ( dt"2025-07-01" ), "Is datetime", "Is not datetime" ), // RETURNS: Is datetime
    IF ( ISDATETIME ( DATE ( 2025, 7, 1 ) ), "Is datetime", "Is not datetime" ) // RETURNS: Is datetime
}
```

## Related content

- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
