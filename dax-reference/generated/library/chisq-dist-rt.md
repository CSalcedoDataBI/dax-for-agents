---
name: CHISQ.DIST.RT
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/chisq-dist-rt-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CHISQ.DIST.RT

Returns the right-tailed probability of the chi-squared distribution. 

The chi-squared distribution is associated with a chi-squared test. Use the chi-squared test to compare observed and expected values. For example, a genetic experiment might hypothesize that the next generation of plants will exhibit a certain set of colors. By comparing the observed results with the expected ones, you can decide whether your original hypothesis is valid.

## Syntax

```dax
CHISQ.DIST.RT(<x>, <deg_freedom>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`x`|The value at which you want to evaluate the distribution.|
|`Deg_freedom`|The number of degrees of freedom.|

## Return value

The right-tailed probability of the chi-squared distribution.

## Remarks

- If `x` or `deg_freedom` is nonnumeric, an error is returned.

- If `deg_freedom` is not an integer, it is rounded.

- If `x` < 0, an error is returned.

- If `deg_freedom` < 1 or `deg_freedom` > 10^10, an error is returned.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query,

```dax
EVALUATE { CHISQ.DIST.RT(2, 5) }
```

Returns

|[Value] |
|---------|
|0.84914503608461    |
