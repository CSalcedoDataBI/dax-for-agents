---
name: LASTNONBLANKVALUE
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/lastnonblankvalue-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# LASTNONBLANKVALUE

Evaluates an expression filtered by the sorted values of a column and returns the last value of the expression that is not blank.

## Syntax

```dax
LASTNONBLANKVALUE(<column>, <expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|A column or an expression that returns a single-column table.|
|`expression`|An expression evaluated for each value of `column`.|

## Return value

The last non-blank value of `expression` corresponding to the sorted values of `column`.

## Remarks

- The column argument can be any of the following:
  - A reference to any column.
  - A table with a single column.

- This function is different from LASTNONBLANK in that the `column` is added to the filter context for the evaluation of `expression`.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query,

```dax
EVALUATE
SUMMARIZECOLUMNS(
  DimProduct[Class],
  "LNBV",
  LASTNONBLANKVALUE(
    DimDate[Date],
    SUM(FactInternetSales[SalesAmount])
   )
)
```

Returns,

|DimProduct[Class]|[LNBV]|
|-----------|---------------|----------|
|L|132.44|
|H|137.6|
|M|84.97|
||2288.6|
