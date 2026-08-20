---
name: CALENDARAUTO
category: [date-and-time]
primaryCategory: date-and-time
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/calendarauto-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CALENDARAUTO

Returns a table with a single column named "Date" that contains a contiguous set of dates. The range of dates is calculated automatically based on data in the model.

## Syntax

```dax
CALENDARAUTO([fiscal_year_end_month])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`fiscal_year_end_month`|Any DAX expression that returns an integer from 1 to 12. If omitted, defaults to the value specified in the calendar table template for the current user, if present; otherwise, defaults to 12.|

## Return value

Returns a table with a single column named "Date" that contains a contiguous set of dates. The range of dates is calculated automatically based on data in the model.

## Remarks

- The date range is calculated as follows:

  - The earliest date in the model which is not in a calculated column or calculated table is taken as the MinDate.
  - The latest date in the model which is not in a calculated column or calculated table is taken as the MaxDate.
  - The date range returned is dates between the beginning of the fiscal year associated with MinDate and the end of the fiscal year associated with MaxDate.

- An error is returned if the model does not contain any datetime values which are not in calculated columns or calculated tables.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

In this example, the MinDate and MaxDate in the data model are July 1, 2018 and June 30, 2019. This model contains two calculated tables:

- **CalendarAuto**. Defined as `CALENDARAUTO()`. Returns all dates between January 1, 2018 and December 31, 2019.
- **CalendarAuto3**. Defined as `CALENDARAUTO(3)`. Returns all dates between April 1, 2018 and March 31, 2020. As in this example `fiscal_year_end_month` is 3, the first years starts on April 1st and ends on March 31st. As a result, the range is determined by selecting the first day of the fiscal year on or before the MinDate's year (April 1, 2018) and the last day of the fiscal year after or within the MaxDate's year (March 31, 2020).

Below are measure definitions and their return values on the example model:

```dax
MinDate = MIN('Date'[Date]) //returns July 1, 2018
MaxDate = MAX('Date'[Date]) //returns June 30, 2019
MinCalendarAuto = MIN('CalendarAuto'[Date]) //returns January 1, 2018
MaxCalendarAuto = MAX('CalendarAuto'[Date]) //returns December 31, 2019
MinCalendarAuto3 = MIN('CalendarAuto3'[Date]) //returns April 1, 2018
MaxCalendarAuto3 = MAX('CalendarAuto3'[Date]) //returns March 31, 2020
```
