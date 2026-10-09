---
name: NORM.S.DIST
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/norm-s-dist-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NORM.S.DIST

Returns the standard normal distribution (has a mean of zero and a standard deviation of one).

## Syntax

```dax
NORM.S.DIST(Z, Cumulative)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Z`|The value for which you want the distribution.|
|`Cumulative`|Cumulative is a logical value that determines the form of the function. If cumulative is `TRUE`, NORM.S.DIST returns the cumulative distribution function; if `FALSE`, it returns the probability density function.|

## Return value

The standard normal distribution (has a mean of zero and a standard deviation of one.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { NORM.S.DIST(1.333333, TRUE) }
```

Returns

|[Value]  |
|---------|
|0.908788725604095    |

## Related content

- [NORM.INV function](./norm-inv.md)
- [NORM.DIST function](./norm-dist.md)
- [NORM.S.INV](./norm-s-inv.md)
