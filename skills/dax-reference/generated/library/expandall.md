---
name: EXPANDALL
category: []
primaryCategory: 
returns: scalar
appliesTo: [visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/expandall-function-dax.md@323524c
sourceDate: 02/21/2024
notes: false
examples: 0
---
# EXPANDALL

Retrieves a context at the most detailed level. If an expression is provided, returns its value in the new context, allowing for navigation in hierarchies and calculation at the most detailed level.

## Syntax

The syntax that performs both navigation and calculation.
```dax
EXPANDALL ( <expression>, <axis> )
```

The syntax that performs navigation only.
```dax
EXPANDALL ( <axis> )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|The expression to be evaluated in the new context.|
|`axis`|An axis reference.|

## Return value

For the version that performs both navigation and calculation, the function returns the value of the expression in the new context after navigating to the lowest level of the hierarchy.
For the version that performs navigation only, the function modifies the evaluation context by navigating to the lowest level of the hierarchy.

## Remarks

* This function can be used only in visual calculations.
* The navigation-only version of the function can be used inside the CALCULATE function.
* The levels of the hierarchy are determined by all columns in each axis referenced by the axis reference.
* Often, there are multiple descendent cells at a lower level; therefore, some form of aggregation is required for the expression argument.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

Given a table that summarizes the total sales for a hierarchy with levels for total, year, quarter and month, the following DAX calculation calculates the maximum value of [SalesAmount] at the lowest level, [Month].

```dax
MaxOfLeafLevel = EXPANDALL(MAX([SalesAmount]), ROWS)
```

The screenshot below shows the matrix with the visual calculation.

![DAX visual calculation](https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/query-languages/dax/media/dax-queries/dax-visualcalc-expandall.png)

## See also

[EXPAND](./expand.md)
[COLLAPSE](./collapse.md)
[COLLAPSEALL](./collapseall.md)

