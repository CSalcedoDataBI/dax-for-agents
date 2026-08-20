---
name: BETA.INV
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/beta-inv-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# BETA.INV

Returns the inverse of the beta cumulative probability density function (BETA.DIST).

If probability `= BETA.DIST(x,...TRUE)`, then `BETA.INV(probability,...) = x`. The beta distribution can be used in project planning to model probable completion times given an expected completion time and variability.

## Syntax

```dax
BETA.INV(probability,alpha,beta,[A],[B])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Probability`|A probability associated with the beta distribution.|
|`Alpha`|A parameter of the distribution.|
|`Beta`|A parameter the distribution.|
|`A`|Optional. A lower bound to the interval of x.|
|`B`|Optional. An upper bound to the interval of x.|

## Return value

Returns the inverse of the beta cumulative probability density function (BETA.DIST).

## Remarks

- If any argument is nonnumeric, `BETA.INV` returns the `#VALUE!` error value.

- If any argument is not an integer, it is rounded.

- If `alpha` ≤ 0 or `beta` ≤ 0, `BETA.INV` returns the `#NUM!` error value.

- If probability ≤ 0 or probability &gt; 1, `BETA.INV` returns the #NUM! error value.

- If you omit values for A and B, `BETA.INV` uses the standard cumulative beta distribution, so that A = 0 and B = 1.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.
