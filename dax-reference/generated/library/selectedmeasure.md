---
name: SELECTEDMEASURE
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/selectedmeasure-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SELECTEDMEASURE

Used by expressions for calculation items or dynamic format strings to reference the measure that is in context.

## Syntax

```dax
SELECTEDMEASURE()
```

### Parameters

None

## Return value

A reference to the measure that is currently in context when the calculation item or format string is evaluated.

## Remarks

- Can only be referenced in the expression for a calculation item or format string.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following calculation item expression calculates the year-to-date for whatever the measure is in context.

```dax
CALCULATE(SELECTEDMEASURE(), DATESYTD(DimDate[Date]))
```

The following expression can be used to dynamically adjust the format string of a measure based upon whether a value is the hundreds, thousands, or millions.

```dax
SWITCH(
TRUE(),
SELECTEDMEASURE() < 1000,"$#,##0",            //Values less than 1000 have no text after them
SELECTEDMEASURE() < 1000000, "$#,##0,.0 K",   //Values between 1000 and 1000000 are formatted as #.## K
"$#,##0,,.0 M"                                //Values greater than 1000000 are formatted as #.## M
)
```

## Related content

- [SELECTEDMEASURENAME](./selectedmeasurename.md)
- [ISSELECTEDMEASURE](./isselectedmeasure.md) 
