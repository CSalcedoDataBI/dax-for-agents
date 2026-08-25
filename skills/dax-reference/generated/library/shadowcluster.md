---
name: SHADOWCLUSTER
category: []
primaryCategory: 
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/shadowcluster-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SHADOWCLUSTER

Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function.
  
## Syntax  
  
```dax
SHADOWCLUSTER(<table expression>)
```
  
### Parameters  
  
|Term|Definition|
|--------|--------------|
|table expression|Any table expression.|
  
## Return value

A table of values.
  
## Remarks

- You use SHADOWCLUSTER within the context GROUPCROSSAPPLY and GROUPCROSSAPPLYTABLE functions, to override the standard behavior of those functions.

- When a table is marked as SHADOWCLUSTER, it is marked internally as a "shadow" table expression so that it is only enabled in an ALLSELECTED context.


## Related content

- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)  
- [GROUPCROSSAPPLY function](./groupcrossapply.md)  
- [GROUPCROSSAPPLYTABLE function](./groupcrossapplytable.md)  
