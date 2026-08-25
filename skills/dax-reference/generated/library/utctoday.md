---
name: UTCTODAY
category: [date-and-time]
primaryCategory: date-and-time
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/utctoday-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# UTCTODAY

Returns the current UTC date.

## Syntax

```dax
UTCTODAY()
```

## Return value

A date.

## Remarks

- UTCTODAY returns the time value 12:00:00 PM for all dates.

- The UTCNOW function is similar but returns the exact time and date.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following:

```dax
EVALUATE { FORMAT(UTCTODAY(), "General Date") }
```

Returns:

|[Value]  |
|---------|
|2/2/2018    |

## Related content

- [NOW function](./now.md)
- [UTCNOW function](./utcnow.md)
