---
name: TODAY
category: [date-and-time]
primaryCategory: date-and-time
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/today-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# TODAY

Returns the current date.

## Syntax

```dax
TODAY()
```

## Return value

A date (`datetime`).

## Remarks

- The TODAY function is useful when you need to have the current date displayed in a report, regardless of when you open it. It is also useful for calculating intervals.

- If the TODAY function does not update the date when you expect it to, you might need to change the settings that control when the report or semantic model is refreshed.

- The NOW function is similar but returns the exact time, whereas TODAY returns the time value 12:00:00 AM (midnight) for all dates.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

If you know that someone was born in 1963, you might use the following formula to find that person's age as of this year's birthday:

```dax
= YEAR(TODAY())-1963
```

This formula uses the TODAY function as an argument for the YEAR function to obtain the current year, and then subtracts 1963, returning the person's age.

## Related content

- [Date and time functions](https://learn.microsoft.com/en-us/dax/date-and-time-functions-dax)
- [NOW](./now.md)
