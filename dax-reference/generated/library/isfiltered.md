---
name: ISFILTERED
category: [information]
primaryCategory: information
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/isfiltered-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ISFILTERED

Returns `TRUE` when the specified table or column is being filtered directly.

## Syntax

```dax
ISFILTERED(<TableNameOrColumnName>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`TableNameOrColumnName`|The name of an existing table or column. It cannot be an expression.|

## Return value

`TRUE` when `ColumnName` or a column of `TableName` is being filtered directly. Otherwise returns `FALSE`.

## Remarks

- A column or table is said to be filtered directly when a filter is applied to `ColumnName` or any column of `TableName`.

- A column or table is said to be cross-filtered when a filter is applied to `ColumnName`, any column of `TableName`, or to any column of a related table. Therefore, the [ISCROSSFILTERED](./iscrossfiltered.md) function also returns `TRUE` when `ColumnName`, any column of `TableName`, or a column of a related table is filtered.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Related content

- [ISCROSSFILTERED function](./iscrossfiltered.md)
- [FILTERS function](./filters.md)
- [HASONEFILTER function](./hasonefilter.md)
- [HASONEVALUE function](./hasonevalue.md)
