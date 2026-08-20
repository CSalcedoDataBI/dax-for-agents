---
name: PERCENTILEX.EXC
category: [statistical]
primaryCategory: statistical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/percentilex-exc-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PERCENTILEX.EXC

Returns the percentile number of an expression evaluated for each row in a table.

To return the percentile of numbers in a column, use [PERCENTILE.EXC function](./percentile-exc.md).

## Syntax

```dax
PERCENTILEX.EXC(<table>, <expression>, k)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table containing the rows for which the expression will be evaluated.|
|`expression`|The expression to be evaluated for each row of the table.|
|`k`|The desired percentile value in the range 0 to 1 exclusive.|

## Return value

The percentile number of an expression evaluated for each row in a table.

## Remarks

- If k is zero or blank, percentile rank of 1/(n+1) returns the smallest value. If zero, it is out of range and an error is returned.

- If k is nonnumeric or outside the range 0 to 1, an error is returned.

- If k is not a multiple of 1/(n + 1), PERCENTILEX.EXC will interpolate to determine the value at the k-th percentile.

- PERCENTILEX.EXC will interpolate when the value for the specified percentile is between two values in the array. If it cannot interpolate for the k percentile specified, an error is returned.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Related content

- [PERCENTILE.EXC](./percentile-exc.md)
