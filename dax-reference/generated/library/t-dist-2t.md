---
name: T.DIST.2T
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/t-dist-2t-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# T.DIST.2T

Returns the two-tailed Student's t-distribution.

## Syntax

```dax
T.DIST.2T(X,Deg_freedom)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`X`|The numeric value at which to evaluate the distribution.|
|`Deg_freedom` |An integer indicating the number of degrees of freedom.|

## Return value

The two-tailed Student's t-distribution.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { T.DIST.2T(1.959999998, 60) }
```

Returns

|[Value]  |
|---------|
|0.054644929975921     |

## Related content

- [T.DIST](./t-dist.md)
- [T.DIST.RT](./t-dist-rt.md)
- [T.INV](./t-inv.md)
- [T.INV.2t](./t-inv-2t.md)

