---
name: CURRENTGROUP
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/currentgroup-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CURRENTGROUP

Returns a set of rows from the table argument of a [GROUPBY](./groupby.md) expression that belong to the current row of the [GROUPBY](./groupby.md) result.

## Syntax

```dax
CURRENTGROUP ( )
```

### Parameters

None

## Return value

The rows in the table argument of the [GROUPBY](./groupby.md) function corresponding to one group of values of the groupBy_columnName arguments.

## Remarks

- This function can only be used within a [GROUPBY](./groupby.md) expression.

- This function takes no arguments and is only supported as the first argument to one of the following aggregation functions: [AVERAGEX](./averagex.md), [COUNTAX](./countax.md), [COUNTX](./countx.md), [GEOMEANX](./geomeanx.md), [MAXX](./maxx.md), [MINX](./minx.md), [PRODUCTX](./productx.md), [STDEVX.S](./stdevx-s.md), [STDEVX.P](./stdevx-s.md), [SUMX](./sumx.md), [VARX.S](./varx-s.md), [VARX.P](./varx-p.md).

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

See [GROUPBY](./groupby.md).
