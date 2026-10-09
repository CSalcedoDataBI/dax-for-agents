---
name: ISSELECTEDMEASURE
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/isselectedmeasure-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISSELECTEDMEASURE

Used by expressions for calculation items to determine the measure that is in context is one of those specified in a list of measures. 

## Syntax

```dax
ISSELECTEDMEASURE( M1, M2, ... )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`M1, M2, ...`|A list of measures.|

## Return value

A Boolean indicating whether the measure that is currently in context is one of those specified in the list of parameters. 

## Remarks

- Can only be referenced in the expression for a calculation item.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following calculation item expression checks if the current measure is one of those specified in the list of parameters. If the measures are renamed, formula fixup will reflect the name changes in the expression.

```dax
IF (
    ISSELECTEDMEASURE ( [Expense Ratio 1], [Expense Ratio 2] ),
    SELECTEDMEASURE (),
    DIVIDE ( SELECTEDMEASURE (), COUNTROWS ( DimDate ) )
)

```

## Related content

- [SELECTEDMEASURE](./selectedmeasure.md)
- [SELECTEDMEASURENAME](./selectedmeasurename.md)
