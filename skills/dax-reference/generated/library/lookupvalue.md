---
name: LOOKUPVALUE
category: [filter]
primaryCategory: filter
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/lookupvalue-function-dax.md@323524c
sourceDate: 07/08/2026
notes: true
examples: 0
---
# LOOKUPVALUE

Returns the value for the row that meets all criteria specified by one or more search conditions.

## Syntax

```dax
LOOKUPVALUE (
    <result_columnName>,
    <search_columnName>,
    <search_value>
    [, <search2_columnName>, <search2_value>]…
    [, <alternateResult>]
)
```

### Parameters

|Term|Definition|
|--------|--------------|
| `result_columnName`  |  The name of an existing column that contains the value you want to return.  It can't be an expression. |
| `search_columnName`  | The name of an existing column. It can be in the same table as result_columnName or in a related table. It can't be an expression. You can specify multiple pairs of search_columnName and search_value. |
| `search_value` | The value to search for in search_columnName. You can specify multiple pairs of search_columnName and search_value. |
| `alternateResult` | (Optional) The value returned when the context for result_columnName is filtered down to zero or more than one distinct value. If not specified, the function returns BLANK when result_columnName is filtered down to zero values, or an error when the context for result_columnName has more than one distinct value. |

## Return value

The value of `result_columnName` at the row where all pairs of `search_columnName` and `search_value` have an exact match.

If no match satisfies all the search values, the function returns BLANK or `alternateResult` (if specified). In other words, the function doesn't return a lookup value if only some of the criteria match.

If multiple rows match the search values and the values in the `result_columnName` for these rows are identical, that value is returned. However, if `result_columnName` returns different values, the function returns an error or `alternateResult` (if specified).

## Remarks

- If a relationship exists between the table that contains the result column and tables that contain the search columns, in most cases, using the [RELATED](./related.md) function instead of LOOKUPVALUE is more efficient and gives better performance.

- You can specify multiple pairs of `search_columnName` and `search_value`.

- The `search_value` and `alternateResult` parameters are evaluated before the function iterates through the rows of the search table.

- Avoid using ISERROR or IFERROR to capture an error returned by LOOKUPVALUE. If some inputs to the function result in an error when a single output value can't be determined, providing an `alternateResult` parameter is the most reliable and highest-performing way to handle the error.

- The `alternateResult` parameter returns an error if specified in a Power Pivot calculated column.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

## Example 1

In this example, LOOKUPVALUE searches Average Rate for the currency used to pay for the order on the day the order was placed:

```dax
Exchange Rate =
LOOKUPVALUE (
    'Currency Rate'[Average Rate],
    'Currency Rate'[CurrencyKey], [CurrencyKey],
    'Currency Rate'[DateKey], [OrderDateKey]
)
```

You need both the Order Date and Currency to find the Average Rate for the correct date and currency. OrderDateKey and CurrencyKey are the keys used to look up the Average Rate in the Currency Rate table.

You can use the Exchange Rate to calculate the Sales Amount in local currency with:

```dax
Sales Amount Local Currency =
[Sales Amount] * [Exchange Rate]
```

## Example 2

In this example, the following calculated column defined in the **Sales** table uses the LOOKUPVALUE function to return channel values from the **Sales Order** table.

```dax
CHANNEL =
LOOKUPVALUE (
    'Sales Order'[Channel],
    'Sales Order'[SalesOrderLineKey], [SalesOrderLineKey]
)
```

However, in this case, because a relationship exists between the **Sales Order** and **Sales** tables, it's more efficient to use the [RELATED](./related.md) function.

```dax
CHANNEL =
RELATED ( 'Sales Order'[Channel] )
```

## Related content

- [RELATED function (DAX)](./related.md)
- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
