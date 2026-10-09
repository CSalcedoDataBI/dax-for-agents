---
name: DATEDIFF
category: [date-and-time]
primaryCategory: date-and-time
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/datediff-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 0
---
# DATEDIFF

Returns the number of interval boundaries between two dates.

## Syntax

```dax
DATEDIFF(<Date1>, <Date2>, <Interval>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Date1`|A scalar datetime value.|
|`Date2`|A scalar datetime value.|
|`Interval`|The interval to use when comparing dates. The value can be one of the following:<br /><br />-   SECOND<br />-   MINUTE<br />-   HOUR<br />-   DAY<br />-   WEEK<br />-  MONTH<br />-   QUARTER<br />-   YEAR|

## Return value

The count of interval boundaries between two dates.

## Remarks

DATEDIFF returns a positive result if Date2 is larger than Date1. It returns a negative result if Date1 is larger than Date2.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

The following DAX query:

```dax
EVALUATE
VAR StartDate =
    DATE ( 2019, 07, 01 )
VAR EndDate =
    DATE ( 2021, 12, 31 )
RETURN
    {
        ( "Year", DATEDIFF ( StartDate, EndDate, YEAR ) ),
        ( "Quarter", DATEDIFF ( StartDate, EndDate, QUARTER ) ),
        ( "Month", DATEDIFF ( StartDate, EndDate, MONTH ) ),
        ( "Week", DATEDIFF ( StartDate, EndDate, WEEK ) ),
        ( "Day", DATEDIFF ( StartDate, EndDate, DAY ) )
    }
```

Returns the following:

|Value1  |Value2  |
|---------|---------|
|Year     |   2      |
|Quarter     |    9     |
|Month     |    29     |
|Week    |    130     |
|Day    |      914   |
