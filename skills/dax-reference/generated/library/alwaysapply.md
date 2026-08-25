---
name: ALWAYSAPPLY
category: []
primaryCategory: 
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/alwaysapply-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# ALWAYSAPPLY

Modifies how filters are applied while evaluating a GROUPCROSSAPPLY or GROUPCROSSAPPLYTABLE function.
  
## Syntax
  
```dax
ALWAYSAPPLY(<table expression>)  
```
  
### Parameters
  
|Term|Definition|
|--------|--------------|
|table expression|Any table expression.|
  
## Return value

A table of values.
  
## Remarks

- You use ALWAYSAPPLY within the context GROUPCROSSAPPLY and GROUPCROSSAPPLYTABLE functions, to override the standard behavior of those functions.
  
- By default, a value filter does not affect measure if it doesn't change filter context. This behavior can be controlled by ALWAYSAPPLY function so that an empty table can still affect measure even if it doesn't change filter context.
  
## Related content

- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)  
- [GROUPCROSSAPPLY function](./groupcrossapply.md)  
- [GROUPCROSSAPPLYTABLE function](./groupcrossapplytable.md)  
