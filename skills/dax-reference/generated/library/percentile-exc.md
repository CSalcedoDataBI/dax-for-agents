---
name: PERCENTILE.EXC
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/percentile-exc-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PERCENTILE.EXC

Returns the k-th percentile of values in a range, where k is in the range 0..1, exclusive.

To return the percentile number of an expression evaluated for each row in a table, use [PERCENTILEX.EXC function](./percentilex-exc.md).

## Syntax

```dax
PERCENTILE.EXC(<column>, <k>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|A column containing the values that define relative standing.|
|`k`|The percentile value in the range 0..1, exclusive.|

## Return value

The k-th percentile of values in a range, where k is in the range 0..1, exclusive.

## Remarks

- If column is empty, BLANK() is returned.

- If k is zero or blank, percentile rank of 1/(n+1) returns the smallest value. If zero, it is out of range and an error is returned.

- If k is nonnumeric or outside the range 0 to 1, an error is returned.

- If k is not a multiple of 1/(n + 1), PERCENTILE.EXC will interpolate to determine the value at the k-th percentile.

- PERCENTILE.EXC will interpolate when the value for the specified percentile is between two values in the array. If it cannot interpolate for the k percentile specified, an error is returned.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Related content

- [PERCENTILEX.EXC](./percentilex-exc.md)
