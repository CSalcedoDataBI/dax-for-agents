---
name: NORM.INV
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/norm-inv-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NORM.INV

The inverse of the normal cumulative distribution for the specified mean and standard deviation.
 

## Syntax

```dax
NORM.INV(Probability, Mean, Standard_dev)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Probability`|A probability corresponding to the normal distribution.|
|`Mean`|The arithmetic mean of the distribution.|
|`Standard_dev`|The standard deviation of the distribution.|

## Return value

Returns the inverse of the normal cumulative distribution for the specified mean and standard deviation.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
EVALUATE { NORM.INV(0.908789, 40, 1.5) }
```

Returns

|[Value]  |
|---------|
|42.00000200956628780274132    |

## Related content

- [NORM.S.INV](./norm-s-inv.md) 
- [NORM.S.DIST function](./norm-s-dist.md) 
- [NORM.DIST function](./norm-dist.md) 
