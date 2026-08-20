---
name: MINA
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/mina-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# MINA

Returns the smallest value in a column.

## Syntax

```dax
MINA(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|The column for which you want to find the minimum value.|

## Return value

The smallest value.

## Remarks

- The MINA function takes as argument a column that contains numbers, and determines the smallest value as follows:
  - If the column contains no values, MINA returns 0 (zero).
  - Rows in the column that evaluates to logical values, such as `TRUE` and `FALSE` are treated as 1 if `TRUE` and 0 (zero) if `FALSE`.
  - Empty cells are ignored.

- If you want to compare text values, use the MIN function.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example 1

The following expression returns the minimum freight charge from the table, InternetSales.

```dax
= MINA(InternetSales[Freight])
```

## Example 2

The following expression returns the minimum value in the column, PostalCode. Because the data type of the column is text, the function does not find any values, and the formula returns zero (0).

```dax
= MINA([PostalCode])
```

## Related content

- [MIN function](./min.md)
- [MINX function](./minx.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
