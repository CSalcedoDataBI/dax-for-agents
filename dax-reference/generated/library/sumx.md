---
name: SUMX
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sumx-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# SUMX

Returns the sum of an expression evaluated for each row in a table.

## Syntax

```dax
SUMX(<table>, <expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table containing the rows for which the expression will be evaluated.|
|`expression`|The expression to be evaluated for each row of the table.|

## Return value

A decimal number.

## Remarks

- The SUMX function takes as its first argument a table, or an expression that returns a table. The second argument is a column that contains the numbers you want to sum, or an expression that evaluates to a column.

- The SUMX is an [iterator function](https://learn.microsoft.com/en-us/dax/dax-glossary#iterator-function).

- Only the numbers in the column are counted. Blanks, logical values, and text are ignored.

- For more complex examples of SUMX in formulas, see [ALL](./all.md) and [CALCULATETABLE](./calculatetable.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example first filters the table, InternetSales, on the expression, 'InternetSales[SalesTerritoryID] = 5`, and then returns the sum of all values in the Freight column. In other words, the expression returns the sum of freight charges for only the specified sales area.

```dax
= SUMX(FILTER(InternetSales, InternetSales[SalesTerritoryID]=5),[Freight])
```

If you do not need to filter the column, use the SUM function. The SUM function is similar to the Excel function of the same name, except that it takes a column as a reference.

## Related content

- [SUM](./sum.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
