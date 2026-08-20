---
name: DETAILROWS
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/detailrows-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DETAILROWS

Evaluates a Detail Rows Expression defined for a measure and returns the data.

## Syntax

```dax
DETAILROWS([Measure])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Measure`|Name of a measure.|

## Return value

A table with the data returned by the Detail Rows Expression. If no Detail Rows Expression is defined, the data for the table containing the measure is returned.
