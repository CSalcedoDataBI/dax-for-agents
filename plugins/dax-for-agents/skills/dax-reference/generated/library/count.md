---
name: COUNT
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/count-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# COUNT

Counts the number of rows in the specified column that contain non-blank values.

## Syntax

```dax
COUNT(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column that contains the values to be counted.|

## Return value

A whole number.

## Remarks

- The only argument allowed to this function is a column. The COUNT function counts rows that contain the following kinds of values:

  - Numbers
  - Dates
  - Strings

- When the function finds no rows to count, it returns a blank.

- Blank values are skipped. `TRUE`/`FALSE` values are not supported.

- If you want to evaluate a column of `TRUE`/`FALSE` values, use the COUNTA function.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

- For best practices when using COUNT, see [Use COUNTROWS instead of COUNT](https://learn.microsoft.com/en-us/dax/best-practices/dax-countrows).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example shows how to count the number of values in the column, ShipDate.

```dax
= COUNT([ShipDate])
```

To count logical values or text, use the COUNTA or COUNTAX functions.

## Related content

- [COUNTA function](./counta.md)
- [COUNTAX function](./countax.md)
- [COUNTX function](./countx.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
