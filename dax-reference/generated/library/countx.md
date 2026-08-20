---
name: COUNTX
category: [aggregation]
primaryCategory: aggregation
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/countx-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# COUNTX

Counts the number of rows that contain a non-blank value or an expression that evaluates to a non-blank value, when evaluating an expression over a table.

## Syntax

```dax
COUNTX(<table>,<expression>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table containing the rows to be counted.|
|`expression`|An expression that returns the set of values that contains the values you want to count.|

## Return value

An integer.

## Remarks

- The COUNTX function takes two arguments. The first argument must always be a table, or any expression that returns a table. The second argument is the column or expression that is searched by COUNTX.

- The COUNTX function counts only values, dates, or strings. If the function finds no rows to count, it returns a blank. 

- If you want to count logical values, use the COUNTAX function.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example 1

The following formula returns a count of all rows in the Product table that have a list price.

```dax
= COUNTX(Product,[ListPrice])
```

## Example 2

The following formula illustrates how to pass a filtered table to COUNTX for the first argument. The formula uses a filter expression to get only the rows in the Product table that meet the condition, ProductSubCategory = "Caps", and then counts the rows in the resulting table that have a list price. The FILTER expression applies to the table Products but uses a value that you look up in the related table, ProductSubCategory.

```dax
= COUNTX(FILTER(Product,RELATED(ProductSubcategory[EnglishProductSubcategoryName])="Caps"), Product[ListPrice])
```

## Related content

- [COUNT function](./count.md)
- [COUNTA function](./counta.md)
- [COUNTAX function](./countax.md)
- [Statistical functions](https://learn.microsoft.com/en-us/dax/statistical-functions-dax)
