---
name: MEDIANX
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/medianx-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# MEDIANX

Returns the median number of an expression evaluated for each row in a table.

To return the median of numbers in a column, use [MEDIAN function](./median.md).

## Syntax

```dax
MEDIANX(<table>, <expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table containing the rows for which the expression will be evaluated.|
|`expression`|The expression to be evaluated for each row of the table.|

## Return value

A decimal number.

## Remarks

- The MEDIANX function takes as its first argument a table, or an expression that returns a table. The second argument is a column that contains the numbers for which you want to compute the median, or an expression that evaluates to a column.

- Only the numbers in the column are counted. 

- Logical values and text are ignored.

- MEDIANX does not ignore blanks; however, MEDIAN does ignore blanks

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following computes the median age of customers who live in the USA.

```dax
= MEDIANX( FILTER(Customers, RELATED( Geography[Country]="USA" ) ), Customers[Age] )
```

## Related content

- [MEDIAN function](./median.md)
