---
name: NEXTWEEK
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/nextweek-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NEXTWEEK

> [!NOTE]
> Week functions only work with calendar based time intelligence. 

Returns a table of all dates from the next week, based on the last date in the current context. The table contains all primary tagged columns and all time related columns.


## Syntax

```
NEXTWEEK(<calendar>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`calendar`|A calendar reference|

## Return value

A table contains all primary tagged columns and all time related columns.

## Remarks

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following sample formula creates a measure that calculates the 'next week sales' for Internet sales.

```dax
=
CALCULATE (
    SUM ( InternetSales_USD[SalesAmount_USD] ),
    NEXTWEEK ( FiscalCalendar )
)
```

## Related content

- [Time intelligence functions](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [NEXTDAY function](./nextday.md)
- [NEXTMONTH function](./nextmonth.md)
- [NEXTQUARTER function](./nextquarter.md)
- [NEXTYEAR function](./nextyear.md)
