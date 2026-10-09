---
name: CONFIDENCE.T
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/confidence-t-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# CONFIDENCE.T

Returns the confidence interval for a population mean, using a Student's t distribution.

## Syntax

```dax
CONFIDENCE.T(alpha,standard_dev,size)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`alpha`|The significance level used to compute the confidence level. The confidence level equals 100*(1 - alpha)%, or in other words, an alpha of 0.05 indicates a 95 percent confidence level.|
|`standard_dev`|The population standard deviation for the data range and is assumed to be known.|
|`size`|The sample size.|

## Return value

Returns the confidence interval for a population mean, using a Student's t distribution.

## Remarks

- If any argument is nonnumeric, CONFIDENCE.T returns the `#VALUE!` error value.

- If `alpha ≤ 0` or `alpha ≥ 1`, CONFIDENCE.T returns the `#NUM!` error value.

- If `standard_dev ≤ 0`, CONFIDENCE.T returns the `#NUM!` error value.

- If size is not an integer, it is rounded.

- If size equals 1, CONFIDENCE.T returns #DIV/0! error value.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

|Formula|Description|Result|
|-----------|---------------|----------|
|`= CONFIDENCE.T(0.05,1,50)`|Confidence interval for the mean of a population based on a sample size of 50, with a 5% significance level and a standard deviation of 1. This is based on a Student's t-distribution.|0.284196855|
