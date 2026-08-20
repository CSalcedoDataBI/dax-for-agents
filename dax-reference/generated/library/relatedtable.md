---
name: RELATEDTABLE
category: [relationship]
primaryCategory: relationship
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/relatedtable-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# RELATEDTABLE

Evaluates a table expression in a context modified by the given filters.

## Syntax

```dax
RELATEDTABLE(<tableName>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`tableName`|The name of an existing table using standard DAX syntax. It cannot be an expression.|

## Return value

A table of values.

## Remarks

- The RELATEDTABLE function changes the context in which the data is filtered, and evaluates the expression in the new context that you specify.

- This function is a shortcut for CALCULATETABLE function with no logical expression.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example uses the RELATEDTABLE function to create a calculated column with the Internet Sales in the Product Category table:

```dax
= SUMX( RELATEDTABLE('InternetSales_USD')
     , [SalesAmount_USD])
```

The following table shows the results:

|:::no-loc text="Product Category Key":::|:::no-loc text="Product Category AlternateKey":::|:::no-loc text="Product Category Name":::|:::no-loc text="Internet Sales":::|
|-----|------|------|------|
|1|1|Bikes|$28,318,144.65|
|2|2|Components||
|3|3|Clothing|$339,772.61|
|4|4|Accessories|$700,759.96|



## Related content

- [CALCULATETABLE](./calculatetable.md)
- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)
