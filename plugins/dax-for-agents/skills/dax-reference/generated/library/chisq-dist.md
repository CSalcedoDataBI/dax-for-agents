---
name: CHISQ.DIST
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/chisq-dist-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CHISQ.DIST

Returns the chi-squared distribution.

The chi-squared distribution is commonly used to study variation in the percentage of something across samples, such as the fraction of the day people spend watching television.

## Syntax

```dax
CHISQ.DIST(<x>, <deg_freedom>, <cumulative>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`x`|The value at which you want to evaluate the distribution.|
|`Deg_freedom`|The number of degrees of freedom.| 
|`cumulative`|A logical value that determines the form of the function. If cumulative is `TRUE`, CHISQ.DIST returns the cumulative distribution function; if `FALSE`, it returns the probability density function.|

## Return value

The chi-squared distribution.

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
EVALUATE { CHISQ.DIST(2, 2, TRUE) }
```

Returns

|[Value] |
|---------|
|0.632120558828558     |
