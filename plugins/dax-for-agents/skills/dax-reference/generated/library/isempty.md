---
name: ISEMPTY
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isempty-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISEMPTY

Checks if a table is empty.

## Syntax

```dax
ISEMPTY(<table_expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table_expression`|A table reference or a DAX expression that returns a table.|

## Return value

True if the table is empty (has no rows), if else, False.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

For the below table named 'Info':

|Country/Region|State|County|Total|
|-----------|---------|----------|---------|
|IND|JK|20|800|
|IND|MH|25|1000|
|IND|WB|10|900|
|USA|CA|5|500|
|USA|WA|10|900|

```dax
EVALUATE
ROW("Any countries with count > 25?", NOT(ISEMPTY(FILTER(Info, [County]>25))))
```

Return value: `FALSE``
