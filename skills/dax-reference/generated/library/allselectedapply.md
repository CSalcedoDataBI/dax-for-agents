---
name: ALLSELECTEDAPPLY
category: []
primaryCategory: 
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/allselectedapply-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ALLSELECTEDAPPLY

Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function.
  
## Syntax  
  
```dax
ALLSELECTEDAPPLY(<table expression>)
```
  
### Parameters  
  
|Term|Definition|
|--------|--------------|
|table expression|Any table expression.|
  
## Return value

A table of values.
  
## Remarks

- You use ALLSELECTEDAPPLY within the context GROUPCROSSAPPLY and GROUPCROSSAPPLYTABLE functions, to override the standard behavior of those functions.

- When a filter is specified as ALLSELECTEDAPPLY, it is initially hidden in the filter context. Upon an ALLSELECTED inside CALCULATE or CALCULATETABLE, this table expression is enabled in fliter context.

## Related content

- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)  
- [GROUPCROSSAPPLY function](./groupcrossapply.md)  
- [GROUPCROSSAPPLYTABLE function](./groupcrossapplytable.md)  
