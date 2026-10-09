---
name: UTCNOW
category: [date-and-time]
primaryCategory: date-and-time
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/utcnow-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# UTCNOW

Returns the current UTC date and time.

## Syntax

```dax
UTCNOW()
```

## Return value

A `datetime`.

## Remarks

The result of the UTCNOW function changes only when the formula is refreshed. It is not continuously updated.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following:

```dax
EVALUATE { FORMAT(UTCNOW(), "General Date") }
```

Returns:

|Value  |
|---------|
|2/2/2018 4:48:08 AM    |

## Related content

- [NOW function](./now.md)
- [UTCTODAY function](./utctoday.md)
