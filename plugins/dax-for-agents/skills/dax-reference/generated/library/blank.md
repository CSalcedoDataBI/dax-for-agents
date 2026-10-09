---
name: BLANK
category: [other]
primaryCategory: other
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/blank-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# BLANK

Returns a blank.

## Syntax

```dax
BLANK()
```

## Return value

A blank.

## Remarks

- Blanks are not equivalent to nulls. DAX uses blanks for both database nulls and for blank cells in Excel.

- Some DAX functions treat blank cells somewhat differently from Microsoft Excel. Blanks and empty strings ("") are not always equivalent, but some operations may treat them as such.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example illustrates how you can work with blanks in formulas. The formula calculates the ratio of sales between the Resellers and the Internet channels. However, before attempting to calculate the ratio the denominator should be checked for zero values. If the denominator is zero then a blank value should be returned; otherwise, the ratio is calculated.

```dax
=
IF (
    SUM ( InternetSales_USD[SalesAmount_USD] ) = 0,
    BLANK (),
    SUM ( ResellerSales_USD[SalesAmount_USD] )
        / SUM ( InternetSales_USD[SalesAmount_USD] )
)
```

The table shows the expected results when this formula is used to create a table visualization. Blank cells indicate where Internet sales were zero, so the ratio could not be calculated.

|Row Labels|Accessories|Bikes|Clothing|
|----|----|----|----| 
|2005||2.65||
|2006||3.33||
|2007|1.04|2.92|6.63|
|2008|0.41|1.53|2.00|

In the original data source, the column evaluated by the BLANK function might have included text, empty strings, or nulls. If the original data source was a SQL Server database, nulls and empty strings are different kinds of data. However, for this operation an implicit type cast is performed and DAX treats them as the same.

## Related content

- [Text functions](https://learn.microsoft.com/en-us/dax/text-functions-dax)
- [ISBLANK function](./isblank.md)

