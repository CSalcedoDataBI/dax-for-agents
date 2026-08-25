---
name: LOOKUP
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/lookup-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# LOOKUP

Returns the value or evaluates the expression from the visual matrix using absolute navigation. Filters can be provided for any axis on the visual matrix. Any omitted filters are inferred from the context. If no single value can be determined, an error is returned.

## Syntax

```dax
LOOKUP(<expression>, <colref>, <expression>[, <colref>, <expression>]...)
```

### Parameters

|Term|Definition|
|--------|--------------|
|expression| The expression to evaluate. |
|colref|(Optional) The column to be filtered.|
|expression|(Optional) The value to filter.|

## Return value

The value of **expression** after filters are applied.

If there isn't a match, an error is returned.

If multiple rows match the filters, an error is returned.

## Example 1

In this example, LOOKUP retrieves the sum of sales for Bikes Category.
The first argument could be a column or a scalar expression.

```dax
Lookup Example 1 = LOOKUP(SUM([Sales Amount]),  [Category], "Bikes")
Lookup Example 2 = LOOKUP([Sales Amount], [Category], "Bikes")
```

The screenshot below shows the matrix with two visual calculations.

![lookup example 1](https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/query-languages/dax/media/dax-queries/dax-visualcalc-lookup.png)

## Example 2
In this example, the **LookupExample2** visual calculation retrieves the sum of Sales for Fiscal Year **FY2018**. Notice that quarter filter from the row will be used since its not specified explicitly, resulting in no results being returned for **FY2019 Q1** to **FY2019 Q4** since the combination of **FY2018** and **FY2019 Q1** to **FY2019 Q4** does not exist. **LookupExample3** explicitly specifies the quarter so does not take into account the current quarter on the row.

```dax
LookupExample2 = LOOKUP([Sales Amount], [Fiscal Year], "FY2018")
LookupExample3 = LOOKUP([Sales Amount], [Fiscal Year], "FY2018", [Fiscal Quarter], "FY2018 Q1")
```

![lookup example 2](https://raw.githubusercontent.com/MicrosoftDocs/query-docs/main/query-languages/dax/media/dax-queries/dax-visualcalc-lookup-example2.png)


## Related content

- [LOOKUPWITHTOTALS](./lookupwithtotals.md)
