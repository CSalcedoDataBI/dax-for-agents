---
name: TABLEOF
category: [information]
primaryCategory: information
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/tableof-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 0
---
# TABLEOF

Returns a reference to the table associated with a specified column, measure, or calendar.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

## Syntax

```dax
TABLEOF ( <myColumnRef> )
TABLEOF ( <measureName> )
TABLEOF ( <myCalendar> )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`reference`|A column, measure, or calendar reference.|

## Return value

A table reference.

## Remarks

- The `TABLEOF` function returns a table reference, not the table data itself.
- When you pass a column name, it returns the table that contains that column.
- When you pass a measure name, it returns the table where that measure is defined.
- When you pass a calendar reference, it returns the table associated with that calendar.
- This function is useful in scenarios where you need to dynamically determine which table a column or measure belongs to.
- `TABLEOF` doesn't resolve columns from row context; it only resolves columns from the current filter context (base table).
- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Example 1 - Using TABLEOF with a column
```dax
EVALUATE
ROW ( "RowCount", COUNTROWS ( TABLEOF ( 'Customer'[Customer ID] ) ) )
```

Returns:

| **RowCount** |
| ------------- |
| 18485 |

## Example 2 - Using TABLEOF with a measure
```dax
DEFINE
    MEASURE Sales[Projected Sales] =
        SUM ( 'Sales'[Sales Amount] ) * 1.06

EVALUATE
ROW (
    "Total Projected Sales", ROUND ( SUMX ( TABLEOF ( [Projected Sales] ), [Projected Sales] ), 2 )
)
```

Returns:

| **Total Projected Sales** |
| ------------- |
| 116397830.65 |

## Example 3 - Using TABLEOF in a user-defined function
```dax
DEFINE
    FUNCTION GetTableRowCount = (
            columnRef : ANYREF
        ) =>
        COUNTROWS ( TABLEOF ( columnRef ) )

EVALUATE
ROW (
    "ResellerCount", GetTableRowCount ( 'Reseller'[Reseller ID] ),
    "CustomerCount", GetTableRowCount ( 'Customer'[Customer ID] )
)
```

Returns:

| **ResellerCount** | **CustomerCount** |
| ------------- | ------------- |
| 702 | 18485 |

## Related content
- [Information functions](https://learn.microsoft.com/en-us/dax/information-functions-dax)
