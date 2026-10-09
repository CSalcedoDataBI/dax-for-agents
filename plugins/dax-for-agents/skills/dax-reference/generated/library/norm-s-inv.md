---
name: NORM.S.INV
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/norm-s-inv-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NORM.S.INV

Returns the inverse of the standard normal cumulative distribution. The distribution has a mean of zero and a standard deviation of one.

## Syntax

```dax
NORM.S.INV(Probability)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Probability`|A probability corresponding to the normal distribution.|

## Return value

The inverse of the standard normal cumulative distribution. The distribution has a mean of zero and a standard deviation of one.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { NORM.S.INV(0.908789) }
```

Returns

|[Value]  |
|---------|
|1.33333467304411    |

## Related content

- [NORM.INV](./norm-inv.md)
- [NORM.S.DIST function](./norm-s-dist.md)
- [NORM.DIST function](./norm-dist.md)
