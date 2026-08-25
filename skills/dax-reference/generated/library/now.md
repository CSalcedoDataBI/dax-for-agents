---
name: NOW
category: [date-and-time]
primaryCategory: date-and-time
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/now-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NOW

Returns the current date and time in `datetime` format.

The NOW function is useful when you need to display the current date and time on a worksheet or calculate a value based on the current date and time, and have that value updated each time you open the worksheet.

## Syntax

```dax
NOW()
```

## Return value

A date (`datetime)`.

## Remarks

- The result of the `NOW` function changes only when the column that contains the formula is refreshed. It is not updated continuously.

- In the Power BI Service, the result of the `NOW` function is always in the UTC timezone.

- The `TODAY` function returns the same date but is not precise with regard to time; the time returned is always 12:00:00 AM and only the date is updated.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following example returns the current date and time plus 3.5 days:

```dax
= NOW()+3.5
```

## Related content

- [UTCNOW function](./utcnow.md)
- [TODAY function](./today.md)
