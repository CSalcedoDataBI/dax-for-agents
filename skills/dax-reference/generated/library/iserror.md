---
name: ISERROR
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/iserror-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISERROR

Checks whether a value is an error, and returns `TRUE` or `FALSE`.

## Syntax

```dax
ISERROR(<value>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`value`|The value you want to test.|

## Return value

A Boolean value of `TRUE` if the value is an error; otherwise `FALSE`.

## Remarks

- For best practices when using ISERROR, see [Appropriate use of error functions](https://learn.microsoft.com/en-us/dax/best-practices/dax-error-functions).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example calculates the ratio of total Internet sales to total reseller sales. The ISERROR function is used to check for errors, such as division by zero. If there is an error a blank is returned, otherwise the ratio is returned.

```dax
= IF( ISERROR(
       SUM('ResellerSales_USD'[SalesAmount_USD])
       /SUM('InternetSales_USD'[SalesAmount_USD])
             )
    , BLANK()
    , SUM('ResellerSales_USD'[SalesAmount_USD])
      /SUM('InternetSales_USD'[SalesAmount_USD])
    )
```

## Related content

- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
- [IFERROR function](./iferror.md)
- [IF function](./if.md)
