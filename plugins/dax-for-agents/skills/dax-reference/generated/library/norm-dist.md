---
name: NORM.DIST
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/norm-dist-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NORM.DIST

Returns the normal distribution for the specified mean and standard deviation.

## Syntax

```dax
NORM.DIST(X, Mean, Standard_dev, Cumulative)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`X`|The value for which you want the distribution.|
|`Mean`|The arithmetic mean of the distribution.|
|`Standard_dev`|The standard deviation of the distribution.|
|`Cumulative*`|A logical value that determines the form of the function. If cumulative is `TRUE`, NORM.DIST returns the cumulative distribution function; if `FALSE`, it returns the probability density function.|

## Return value

The normal distribution for the specified mean and standard deviation.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { NORM.DIST(42, 40, 1.5, TRUE) }
```

Returns

|[Value]  |
|---------|
|0.908788780274132     |

## Related content

- [NORM.S.DIST function](./norm-s-dist.md)
- [NORM.INV function](./norm-inv.md)
- [NORM.S.INV](./norm-s-inv.md)
