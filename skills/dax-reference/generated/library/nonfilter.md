---
name: NONFILTER
category: []
primaryCategory: 
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/nonfilter-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# NONFILTER

Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function.
  
## Syntax  
  
```dax
NONFILTER(<table expression>)
```
  
### Parameters  
  
|Term|Definition|  
|--------|--------------|  
|table expression|Any table expression.|
  
## Return value

A table of values.  
  
## Remarks

- You use NONFILTER within the context GROUPCROSSAPPLY and GROUPCROSSAPPLYTABLE functions, to override the standard behavior of those functions.

- A NONFILTER makes the table expression permanently hidden from the filter context even if its columns may have lineage. Those columns with lineage act as if they are extension columns.

## Related content

- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)  
- [GROUPCROSSAPPLY function](./groupcrossapply.md)  
- [GROUPCROSSAPPLYTABLE function](./groupcrossapplytable.md)  
