---
name: LASTNONBLANK
category: [filter]
primaryCategory: filter
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/lastnonblank-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# LASTNONBLANK

Returns the last value in the column, `column`, filtered by the current context, where the expression is not blank.

## Syntax

```dax
LASTNONBLANK(<column>,<expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|A column expression.|
|`expression`|An expression evaluated for blanks for each value of `column`.|

## Return value

A table containing a single column and single row with the computed last value.

## Remarks

- The `column` argument can be any of the following:
  - A reference to any column.
  - A table with a single column.
  - A Boolean expression that defines a single-column table

- Constraints on Boolean expressions are described in the topic, [CALCULATE function](./calculate.md).

- This function is typically used to return the last value of a column for which the expression is not blank. For example, you could get the last value for which there were sales of a product.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Related content

- [FIRSTNONBLANK function](./firstnonblank.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
