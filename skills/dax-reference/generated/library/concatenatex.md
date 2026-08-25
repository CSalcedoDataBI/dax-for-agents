---
name: CONCATENATEX
category: [text]
primaryCategory: text
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/concatenatex-function-dax.md@323524c
sourceDate: 
notes: true
examples: 3
---
# CONCATENATEX

Concatenates the result of an expression evaluated for each row in a table.

## Syntax

```dax
CONCATENATEX(<table>, <expression>[, <delimiter> [, <orderBy_expression> [, <order>]]...])
```

### Parameters

|Term|Definition|
|-----|-----|
|`table`|The table containing the rows for which the expression will be evaluated.|
|`expression`|The expression to be evaluated for each row of `table`.|
|`delimiter`|(Optional) A separator to use during concatenation.|
|`orderBy_expression`|(Optional) Any DAX expression where the result value is used to sort the concatenated values in the output string. It is evaluated for each row of `table`.|
|`order`|(Optional) A value that specifies how to sort `orderBy_expression` values, ascending or descending.|

The optional `order` parameter accepts the following values:

|Value|Alternate Values|Description|
|-----|-----|-----|
|0 (zero)|`FALSE`, `DESC`|Sorts in descending order of values of `orderBy_expression`. This is the default value when the `order` parameter is omitted.|
|1|`TRUE`, `ASC`|Sorts in ascending order of values of `orderBy_expression`.|

## Return value

A concatenated string.

## Remarks

- This function takes as its first argument a table or an expression that returns a table. The second argument is a column that contains the values you want to concatenate, or an expression that returns a value.

- Concatenated values are not necessarily sorted in any particular order, unless `orderBy_expression` is specified.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**3** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/text/concatenatex.md`](../../examples/text/concatenatex.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

Employees table

|FirstName|LastName|
|-------------|------------|
|Alan|Brewer|
|Michael|Blythe|

The following formula:

```dax
= CONCATENATEX(Employees, [FirstName] & " " & [LastName], ",")
```

Returns:
"Alan Brewer, Michael Blythe"
