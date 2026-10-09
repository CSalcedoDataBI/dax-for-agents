---
name: SELECTEDMEASURENAME
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/selectedmeasurename-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SELECTEDMEASURENAME

Used by expressions for calculation items to determine the measure that is in context by name.

## Syntax

```dax
SELECTEDMEASURENAME()
```

### Parameters

None

## Return value

A string value holding the name of the measure that is currently in context when the calculation item is evaluated. 

## Remarks

- Can only be referenced in the expression for a calculation item.

- This function is often used for debugging purposes when authoring calculation groups.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following calculation item expression checks if the current measure is Expense Ratio and conditionally applies calculation logic. Since the check is based on a string comparison, it is not subject to formula fixup and will not benefit from object renaming being automatically reflected. For a similar comparison that would benefit from formula fixup, please see the ISSLECTEDMEASURE function instead. 

```dax
IF (
    SELECTEDMEASURENAME = "Expense Ratio",
    SELECTEDMEASURE (),
    DIVIDE ( SELECTEDMEASURE (), COUNTROWS ( DimDate ) )
)
```

## Related content

- [SELECTEDMEASURE](./selectedmeasure.md)
- [ISSELECTEDMEASURE](./isselectedmeasure.md) 
