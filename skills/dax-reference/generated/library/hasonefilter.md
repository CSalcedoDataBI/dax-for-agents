---
name: HASONEFILTER
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/hasonefilter-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# HASONEFILTER

Returns `TRUE` when the number of directly filtered values on `columnName` is one; otherwise returns `FALSE`.

## Syntax

```dax
HASONEFILTER(<columnName>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`columnName`|  The name of an existing column, using standard DAX syntax. It cannot be an expression.  |

## Return value

`TRUE` when the number of directly filtered values on `columnName` is one; otherwise returns `FALSE`.

## Remarks

- This function is similar to HASONEVALUE() with the difference that HASONEVALUE() works based on cross-filters while HASONEFILTER() works by a direct filter.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example shows how to use HASONEFILTER() to return the filter for   ResellerSales_USD[ProductKey]) if there is one filter, or to return BLANK if there are no filters or more than one filter on ResellerSales_USD[ProductKey]).

```dax
= IF(HASONEFILTER(ResellerSales_USD[ProductKey]),FILTERS(ResellerSales_USD[ProductKey]),BLANK())
```
