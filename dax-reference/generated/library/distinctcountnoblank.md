---
name: DISTINCTCOUNTNOBLANK
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/distinctcountnoblank-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DISTINCTCOUNTNOBLANK

Counts the number of distinct values in a column.

## Syntax

```dax
DISTINCTCOUNTNOBLANK(<column>)
```

### Parameters

|Term  |Description|
|---------|---------|
|`column`| The column that contains the values to be counted |

## Return value

The number of distinct values in `column`.

## Remarks

- Unlike [DISTINCTCOUNT](./distinctcount.md) function, DISTINCTCOUNTNOBLANK does not count the BLANK value.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example shows how to count the number of distinct sales orders in the column ResellerSales_USD[SalesOrderNumber].

```dax
= DISTINCTCOUNT(ResellerSales_USD[SalesOrderNumber])
```

DAX query

```DAX
EVALUATE
    ROW(
        "DistinctCountNoBlank", DISTINCTCOUNTNOBLANK(DimProduct[EndDate]),
        "DistinctCount", DISTINCTCOUNT(DimProduct[EndDate])
    )
```

|[DistinctCountNoBlank]  |[DistinctCount]  |
|---------|---------|
|2     |     3    |

## Related content

- [DISTINCTCOUNT](./distinctcount.md)
