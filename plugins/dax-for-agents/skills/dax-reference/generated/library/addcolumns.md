---
name: ADDCOLUMNS
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/addcolumns-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ADDCOLUMNS

Adds calculated columns to the given table or table expression.

## Syntax

```dax
ADDCOLUMNS(<table>, <name>, <expression>[, <name>, <expression>]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|Any DAX expression that returns a table of data.| 
|`name`|The name given to the column, enclosed in double quotes.  |
|`expression`|Any DAX expression that returns a scalar expression, evaluated for each row of `table`. | 

## Return value

A table with all its original columns and the added ones.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns an extended version of the Product Category table that includes total sales values from the reseller channel and the internet sales.

```dax
ADDCOLUMNS(ProductCategory
               , "Internet Sales", SUMX(RELATEDTABLE(InternetSales_USD), InternetSales_USD[SalesAmount_USD])
               , "Reseller Sales", SUMX(RELATEDTABLE(ResellerSales_USD), ResellerSales_USD[SalesAmount_USD]))
```

The following table shows a preview of the data as it would be received by any function expecting to receive a table:

|ProductCategory[ProductCategoryName]|ProductCategory[ProductCategoryAlternateKey]|ProductCategory[ProductCategoryKey]|[Internet Sales]|[Reseller Sales]|
|-----|-----|-----|-----|-----|
|Bikes|1|1|25107749.77|63084675.04|
|Components|2|2||11205837.96|
|Clothing|3|3|306157.5829|1669943.267|
|Accessories|4|4|640920.1338|534301.9888|
