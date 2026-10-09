---
name: T.DIST
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/t-dist-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# T.DIST

Returns the Student's left-tailed t-distribution.

## Syntax

```dax
T.DIST(X,Deg_freedom,Cumulative)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`X`|The numeric value at which to evaluate the distribution.|
|`Deg_freedom` |An integer indicating the number of degrees of freedom.|
|`Cumulative`|A logical value that determines the form of the function. If cumulative is `TRUE`, T.DIST returns the cumulative distribution function; if `FALSE`, it returns the probability density function.|

## Return value

The Student's left-tailed t-distribution.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { T.DIST(60, 1, TRUE) }
```

Returns,

|[Value]  |
|---------|
|0.994695326367377     |

## Related content

- [T.DIST.2T](./t-dist-2t.md)
- [T.DIST.RT](./t-dist-rt.md)
- [T.INV](./t-inv.md)
- [T.INV.2t](./t-inv-2t.md)

