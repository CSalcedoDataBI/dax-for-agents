---
name: ISONORAFTER
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isonorafter-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISONORAFTER

A boolean function that emulates the behavior of a Start At clause and returns true for a row that meets all of the condition parameters.

Based on the sort order, the first parameter is compared with the second parameter. If the sort order is ascending, the comparison to be done is first parameter greater than the second parameter. If the sort order is descending, the comparison to be done is second parameter less than the first parameter.

## Syntax

```DAX
ISONORAFTER(<scalar_expression>, <scalar_expression>[, sort_order [, <scalar_expression>, <scalar_expression>[, sort_order]]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`scalar expression`|Any expression that returns a scalar value like a column reference or integer or string value. Typically the first parameter is a column reference and the second parameter is a scalar value.|
|`sort order`|(optional) The order in which the column is sorted. Can be ascending (ASC) or descending (DESC). By default the sort order is ascending.|

## Return value

True or false.

## Remarks

This function is similar to [ISAFTER](./isafter.md). The difference is ISONORAFTER returns true for values sorted *on or after* the filter values, where ISAFTER returns true for values sorted strictly *after* the filter values.

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

For the following table named, Info:

|Country/Region|State|Count|Total|
|-----------|---------|---------|---------|
|IND|JK|20|800|
|IND|MH|25|1000|
|IND|WB|10|900|
|USA|CA|5|500|
|USA|WA|10|900|

The following expression:

```dax
FILTER (
    Info,
    ISONORAFTER (
        Info[Country], "IND", ASC,
        Info[State], "MH", ASC )
)
```

Returns:

|Country/Region|State|Count|Total|
|-----------|---------|---------|---------|
|IND|MH|25|1000|
|IND|WB|10|900|
|USA|CA|5|500|
|USA|WA|10|900|

## Related content

- [ISAFTER](./isafter.md)
