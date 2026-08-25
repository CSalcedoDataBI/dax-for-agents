---
name: MAXA
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/maxa-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# MAXA

Returns the largest value in a column.

## Syntax

```dax
MAXA(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column in which you want to find the largest value.|

## Return value

The largest value.

## Remarks

- The MAXA function takes as argument a column, and looks for the largest value among the following types of values:
  - Numbers
  - Dates

- Logical values, such as `TRUE` and `FALSE`. Rows that evaluate to `TRUE` count as 1; rows that evaluate to `FALSE` count as 0 (zero).

- Empty cells are ignored. If the column contains no values that can be used, MAXA returns 0 (zero).

- If you want to compare text values, use the MAX function.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example 1

The following example returns the greatest value from a calculated column, named **ResellerMargin**, that computes the difference between list price and reseller price.

```dax
= MAXA([ResellerMargin])
```

## Example 2

The following example returns the largest value from a column that contains dates and times. Therefore, this formula gets the most recent transaction date.

```dax
= MAXA([TransactionDate])
```

## Related content

- [MAX function](./max.md)
- [MAXX function](./maxx.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
