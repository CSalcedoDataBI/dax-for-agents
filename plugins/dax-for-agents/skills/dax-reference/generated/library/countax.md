---
name: COUNTAX
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/countax-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# COUNTAX

The COUNTAX function counts non-blank results when evaluating the result of an expression over a table. That is, it works just like the COUNTA function, but is used to iterate through the rows in a table and count rows where the specified expressions results in a non-blank result.

## Syntax

```dax
COUNTAX(<table>,<expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table containing the rows for which the expression will be evaluated.|
|`expression`|The expression to be evaluated for each row of the table.|

## Return value

A whole number.

## Remarks

- Like the COUNTA function, the COUNTAX function counts cells containing any type of information, including other expressions. For example, if the column contains an expression that evaluates to an empty string, the COUNTAX function treats that result as non-blank. Usually the COUNTAX function does not count empty cells but in this case the cell contains a formula, so it is counted.

- Whenever the function finds no rows to aggregate, the function returns a blank.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example counts the number of nonblank rows in the column, Phone, using the table that results from filtering the Reseller table on `[Status] = Active`.

```dax
= COUNTAX(FILTER('Reseller',[Status]="Active"),[Phone])
```

## Related content

- [COUNT function](./count.md)
- [COUNTA function](./counta.md)
- [COUNTX function](./countx.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
