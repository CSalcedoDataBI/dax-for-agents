---
name: T.INV.2T
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/t-inv-2t-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# T.INV.2T

Returns the two-tailed inverse of the Student's t-distribution.
 
## Syntax

```dax
T.INV.2T(Probability,Deg_freedom)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Probability`|The probability associated with the Student's t-distribution.|
|`Deg_freedom`|The number of degrees of freedom with which to characterize the distribution.|

## Return value

The two-tailed inverse of the Student's t-distribution.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { T.INV.2T(0.546449, 60) }
```

Returns

|[Value]  |
|---------|
|0.606533075825759    |

## Related content

- [T.INV](./t-inv.md)
- [T.DIST](./t-dist.md)
- [T.DIST.2T](./t-dist-2t.md)
- [T.DIST.RT](./t-dist-rt.md)
