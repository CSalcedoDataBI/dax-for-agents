---
name: PDURATION
category: [financial]
primaryCategory: financial
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/pduration-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# PDURATION

Returns the number of periods required by an investment to reach a specified value.

## Syntax

```dax
PDURATION(<rate>, <pv>, <fv>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`rate`|The interest rate per period.|
|`pv`|The present value of the investment.|
|`fv`|The desired future value of the investment.|

## Return Value

The number of periods.

## Remarks

- PDURATION uses the following equation:

    $$\text{PDURATION} = \frac{log(\text{fv}) - log(\text{pv})}{log(1 + \text{rate})}$$

- An error is returned if:
  - rate ≤ 0.
  - pv ≤ 0.
  - fv ≤ 0.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example 1

The following DAX query:

```dax
EVALUATE
{
  PDURATION(0.025, 2000, 2200)
}
```

Returns the number of years required for an investment of \\$2000, earning 2.5% annually, to reach \\$2200.

| **[Value]**    |
| ---------------- |
| 3.85986616262266 |

## Example 2

The following DAX query:

```dax
EVALUATE
{
  PDURATION(0.025/12, 1000, 1200)
}
```

Returns the number of months required for an investment of \\$1000, earning 2.5% annually, to reach \\$1200.

| **[Value]**    |
| ---------------- |
| 87.6054764193714 |
