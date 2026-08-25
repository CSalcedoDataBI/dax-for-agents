---
name: ISATLEVEL
category: []
primaryCategory: 
returns: scalar
appliesTo: [visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isatlevel-function-dax.md@323524c
sourceDate: 02/20/2024
notes: false
examples: 0
---
# ISATLEVEL

Reports whether the column is present at the current level.

## Syntax

```dax
ISATLEVEL ( <column> )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|A grouping column in the data grid.|

## Return value

`TRUE` or `FALSE` that indicates whether the grouping column is at the current level in the context.

## Remarks

* This function can be used only in visual calculations.
* Unlike other functions with similar functionality, such as ISINSCOPE, ISFILTERED, HASONEVALUE, and so on, ISATLEVEL is a function specialized for visual calculations, therefore it is guaranteed to be compatible with functions that navigate the levels of a hierarchy in the data matrix, such as EXPAND and COLLAPSE.
* A hierarchy level can contain more than one column. For example, in a [Year], [Quarter], [Month] hierarchy, the level that contains the [Quarter] column also includes the [Year] column at the same level.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

Consider a table that includes a hierarchy with levels for total, year, quarter, and month. The following DAX calculations can be used to determine whether a specific column is at the current level in the original context or at the new level after a navigation operation.

```dax
IsYearLevel = ISATLEVEL([Fiscal Year])
IsQuarterLevel = ISATLEVEL([Fiscal Quarter])
IsMonthLevel = ISATLEVEL([Month])
IsQuarterLevelAfterExpand = EXPAND(ISATLEVEL([Fiscal Quarter]), ROWS)
IsQuarterLevelAfterCollapse = COLLAPSE(ISATLEVEL([Fiscal Quarter]), ROWS)
```

The screenshot below shows the matrix with the five visual calculations.

![DAX visual calculation](https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/query-languages/dax/media/dax-queries/dax-visualcalc-isatlevel.png)

## See also

[EXPAND](./expand.md)
[EXPANDALL](./expandall.md)
[COLLAPSE](./collapse.md)
[COLLAPSEALL](./collapseall.md)
[ISINSCOPE](./isinscope.md)
[ISFILTERED](./isfiltered.md)
[HASONEVALUE](./hasonevalue.md)

