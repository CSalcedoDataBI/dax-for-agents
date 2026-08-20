---
name: SELECTEDMEASUREFORMATSTRING
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/selectedmeasureformatstring-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SELECTEDMEASUREFORMATSTRING

Used by expressions for calculation items to retrieve the format string of the measure that is in context.

## Syntax

```dax
SELECTEDMEASUREFORMATSTRING()
```

### Parameters

None

## Return value

A string holding the format string of the measure that is currently in context when the calculation item is evaluated.

## Remarks

- This function can only be referenced in expressions for calculation items in calculation groups. It is designed to be used by the **Format String Expression** property of calculation items.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following expression is evaluated by the Format String Expression property for a calculation item. If there is a single currency in filter context, the format string is retrieved from the DimCurrency[FormatString] column; otherwise the format string of the measure in context is used.

```dax
SELECTEDVALUE( DimCurrency[FormatString], SELECTEDMEASUREFORMATSTRING() )
```

## Related content

- [SELECTEDMEASURE](./selectedmeasure.md)
- [ISSELECTEDMEASURE](./isselectedmeasure.md) 
