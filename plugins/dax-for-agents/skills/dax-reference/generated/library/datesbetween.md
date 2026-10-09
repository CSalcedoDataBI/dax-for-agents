---
name: DATESBETWEEN
category: [time-intelligence]
primaryCategory: time-intelligence
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/datesbetween-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 0
---
# DATESBETWEEN

For date column input, returns a table that contains a column of dates that begins with a specified start date and continues until a specified end date.

For calendar input, returns a table that begins with a specified start date and continues until a specified end date. The table contains all primary tagged columns and all time related columns.

This function is suited to pass as a filter to the [CALCULATE](./calculate.md) function. Use it to filter an expression by a custom date range.

> [!NOTE]
> If you're working with standard date intervals such as days, months, quarters, or years, use the better-suited [DATESINPERIOD](./datesinperiod.md) function.

## Syntax

```dax
DATESBETWEEN(<dates or calendar>, <StartDate>, <EndDate>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`dates or calendar`|A column that contains dates or a calendar reference|
|`StartDate`|A date/day expression. If you use calendar syntax, use the same data type as the primary column tagged to the Day category.|
|`EndDate`|A date/day expression. If you use calendar syntax, use the same data type as the primary column tagged to the Day category.|

## Return value

For date column input, a table containing a single column of date values.  
For calendar input, a table that contains all primary tagged columns and all time related columns.

## Remarks

- In the most common use case, `dates` is a reference to the date column of a marked date table.

- If `StartDate` is BLANK, then `StartDate` is the earliest value in the `dates` column. For calendar, it's the first value in a column that's tagged as day.

- If `EndDate` is BLANK, then `EndDate` is the latest value in the `dates` column. For calendar, it's the last value in a column that's tagged as day.

- Dates used as the `StartDate` and `EndDate` are inclusive. So, for example, if the `StartDate` value is July 1, 2019, then that date is included in the returned table (providing the date exists in the `dates` column).

- For date column input, the returned table can only contain dates stored in the `Dates` column. So, for example, if the `Dates` column starts from July 1, 2017, and the `StartDate` value is July 1, 2016, the returned table starts from July 1, 2017.

- For calendar input, if the input date isn't found in the tagged day column, it's treated as BLANK, and the first or last value is used.

- For calendar input, use the same data type and format as the tagged day column for the start date and end date. For example, if the column uses the format YYYY-Sn-Qn-Mnn-Wnn-Dnn (e.g., "2014-S2-Q4-M11-W45-D03"), the start date and end date must follow the same format (e.g., "2015-S2-Q4-M11-W45-D03"). Otherwise, the behavior is undefined.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following **Sales** table measure definition uses the DATESBETWEEN function to produce a _life-to-date_ (LTD) calculation. Life-to-date represents the accumulation of a measure over time since the very beginning of time.

The formula uses the [MAX](./max.md) function. This function returns the latest date that's in the filter context. So, the DATESBETWEEN function returns a table of dates beginning from the earliest date until the latest date being reported.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

```dax
Customers LTD =
CALCULATE (
    DISTINCTCOUNT ( Sales[CustomerKey] ),
    DATESBETWEEN ( 'Date'[Date], BLANK (), MAX ( 'Date'[Date] ) )
)
```

Consider that the earliest date stored in the **Date** table is July 1, 2017. So, when a report filters the measure by the month of June 2020, the DATESBETWEEN function returns a date range from July 1, 2017 until June 30, 2020.

## Example for calendar based time intelligence
The following **Sales** table measure definition uses the DATESBETWEEN function to produce a _life-to-date_ (LTD) calculation. Life-to-date represents the accumulation of a measure over time since the very beginning of time.

The formula uses the [MAX](./max.md) function. This function returns the max datekey that's in the filter context. So, the DATESBETWEEN function returns a table of dates beginning from the earliest date until the latest date being reported. We use DateKey as an example to show that the "Day" category can be tagged with a column that isn't date-typed.

```dax
Customers LTD =
CALCULATE (
    DISTINCTCOUNT ( Sales[CustomerKey] ),
    DATESBETWEEN ( FiscalCalendar, BLANK (), MAX ( 'Date'[DateKey] ) )
)
```

## Related content

- [Time intelligence functions (DAX)](https://learn.microsoft.com/en-us/dax/time-intelligence-functions-dax)
- [Date and time functions (DAX)](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [DATESINPERIOD function (DAX)](./datesinperiod.md)
