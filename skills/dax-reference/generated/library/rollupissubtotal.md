---
name: ROLLUPISSUBTOTAL
category: [table-manipulation]
primaryCategory: table-manipulation
returns: scalar
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/rollupissubtotal-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ROLLUPISSUBTOTAL

Pairs rollup groups with the column added by [ROLLUPADDISSUBTOTAL](./rollupaddissubtotal.md). This function can only be used within an [ADDMISSINGITEMS](./addmissingitems.md) expression.

## Syntax

```dax
ROLLUPISSUBTOTAL ( [<grandTotalFilter>], <groupBy_columnName>, <isSubtotal_columnName> [, [<groupLevelFilter>] [, <groupBy_columnName>, <isSubtotal_columnName> [, [<groupLevelFilter>] [, … ] ] ] ] )
```

### Parameters

|Term|Definition|
|--------|--------------|
|`grandTotalFilter`|(Optional) Filter to be applied to the grandtotal level.|
|`groupBy_columnName`|Name of an existing column used to create summary groups based on the values found in it. Cannot be an expression.|
|isSubtotal_columnName |Name of an ISSUBTOTAL column. The values of the column are calculated using the ISSUBTOTAL function. |
|`groupLevelFilter`|(Optional) Filter to be applied to the current level.|

## Return value

None

## Remarks

This function can only be used within an [ADDMISSINGITEMS](./addmissingitems.md) expression.
