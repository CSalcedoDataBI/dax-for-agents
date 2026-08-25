---
name: ALLCROSSFILTERED
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/allcrossfiltered-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ALLCROSSFILTERED

Clear all filters which are applied to a table.

## Syntax

```dax
ALLCROSSFILTERED(<table>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table that you want to clear filters on. |

## Return value

N/A. See remarks.

## Remarks

- ALLCROSSFILTERED can only be used to clear filters but not to return a table.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
DEFINE
MEASURE FactInternetSales[TotalQuantity1] =
    CALCULATE(SUM(FactInternetSales[OrderQuantity]), ALLCROSSFILTERED(FactInternetSales))
MEASURE FactInternetSales[TotalQuantity2] =
    CALCULATE(SUM(FactInternetSales[OrderQuantity]), ALL(FactInternetSales))
EVALUATE
    SUMMARIZECOLUMNS(DimSalesReason[SalesReasonName], 
        "TotalQuantity1", [TotalQuantity1],
        "TotalQuantity2", [TotalQuantity2])
    ORDER BY DimSalesReason[SalesReasonName]

```

Returns,

|DimSalesReason[SalesReasonName]  |[TotalQuantity1]  |[TotalQuantity2] |
|---------|---------|---------|
|Demo Event    |    60398     |         |
|Magazine Advertisement    |    60398     |         |
|Manufacturer     |   60398      |   1818      |
|On Promotion     |   60398      |   7390      |
|Other     |   60398      |    3653     |
|Price     |   60398      |    47733     |
|Quality     |   60398      |   1551      |
|Review     |   60398      |    1640     |
|Sponsorship   |   60398      |         |
|Television  Advertisement    |   60398      |     730    |
|||

> [!NOTE]
> There is a direct or indirect many-to-many relationship between FactInternetSales table and DimSalesReason table.
