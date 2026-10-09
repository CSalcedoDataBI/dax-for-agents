---
name: CONTAINS
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/contains-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# CONTAINS

Returns true if values for all referred columns exist, or are contained, in those columns; otherwise, the function returns false.

## Syntax

```dax
CONTAINS(<table>, <columnName>, <value>[, <columnName>, <value>]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|Any DAX expression that returns a table of data.|
|`columnName`|The name of an existing column, using standard DAX syntax. It cannot be an expression. |
|`value`|Any DAX expression that returns a single scalar value, that is to be sought in `columnName`. The expression is to be evaluated exactly once and before it is passed to the argument list.  |

## Return value

A value of `TRUE` if each specified `value` can be found in the corresponding `columnName`, or are contained, in those columns; otherwise, the function returns `FALSE`.

## Remarks

- The arguments `columnName` and `value` must come in pairs; otherwise an error is returned.

- `columnName` must belong to the specified `table`, or to a table that is related to `table`.

- If `columnName` refers to a column in a related table then it must be fully qualified; otherwise, an error is returned.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/information/contains.md`](../../examples/information/contains.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example creates a measure that tells you whether there were any Internet sales of product 214 and to customer 11185 at the same time.

```dax
= CONTAINS(InternetSales, [ProductKey], 214, [CustomerKey], 11185)
```
