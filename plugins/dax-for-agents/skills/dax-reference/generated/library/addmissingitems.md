---
name: ADDMISSINGITEMS
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/addmissingitems-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ADDMISSINGITEMS

Adds rows with empty values to a table returned by [SUMMARIZECOLUMNS](./summarizecolumns.md).

## Syntax

```dax
ADDMISSINGITEMS ( [<showAll_columnName> [, <showAll_columnName> [, … ] ] ], <table> [, <groupBy_columnName> [, [<filterTable>] [, <groupBy_columnName> [, [<filterTable>] [, … ] ] ] ] ] ] )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`showAll_columnName`| (Optional) A column for which to return items with no data for the measures used. If not specified, all columns are returned.|
|`table`|A SUMMARIZECOLUMNS table.|
|`groupBy_columnName`|(Optional) A column to group by in the supplied table argument.|
|`filterTable`|(Optional) A table expression that defines which rows are returned.|

## Return value

A table with one or more columns.

## Remarks

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## With SUMMARIZECOLUMNS

A table returned by [SUMMARIZECOLUMNS](./summarizecolumns.md) will include only rows with values. By wrapping a [SUMMARIZECOLUMNS](./summarizecolumns.md) expression within an ADDMISSINGITEMS expression, rows containing no values are also returned.

### Example

Without ADDMISSINGITEMS, the following query:

```dax
SUMMARIZECOLUMNS( 
    'Sales'[CustomerId], 
    "Total Qty", SUM ( Sales[TotalQty] )
)
```

Returns,

|CustomerId|TotalQty|
|--------------|------------|
|A|5|
|B|3|
|C|3|
|E|2|

With ADDMISSINGITEMS, the following query:

```dax
EVALUATE
ADDMISSINGITEMS (
    'Sales'[CustomerId],
    SUMMARIZECOLUMNS( 
        'Sales'[CustomerId],
        "Total Qty", SUM ( Sales[TotalQty] )
    ),
    'Sales'[CustomerId]
)
```

Returns,

|CustomerId|TotalQty|
|--------------|------------|
|A|5|
|B|3|
|C|3|
|D| |
|E|2|
|F| |
