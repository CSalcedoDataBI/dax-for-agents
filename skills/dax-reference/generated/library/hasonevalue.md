---
name: HASONEVALUE
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/hasonevalue-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# HASONEVALUE

Returns `TRUE` when the context for `columnName` has been filtered down to one distinct value only. Otherwise is `FALSE`.

## Syntax

```html
HASONEVALUE(<columnName>)
```

### Parameters

|Term|Definition|
|--------|--------------|
| columnName   |  The name of an existing column, using standard DAX syntax. It cannot be an expression.  |

## Return value

`TRUE` when the context for `columnName` has been filtered down to one distinct value only. Otherwise is `FALSE`.

## Remarks

- An equivalent expression for HASONEVALUE() is `COUNTROWS(VALUES(<columnName>)) = 1`.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following measure formula verifies if the context is being sliced by one value in order to estimate a percentage against a predefined scenario; in this case you want to compare Reseller Sales against sales in 2007, then you need to know if the context is filtered by single years. Also, if the comparison is meaningless you want to return BLANK.

```dax
= IF(HASONEVALUE(DateTime[CalendarYear]),SUM(ResellerSales_USD[SalesAmount_USD])/CALCULATE(SUM(ResellerSales_USD[SalesAmount_USD]),DateTime[CalendarYear]=2007),BLANK())
```
