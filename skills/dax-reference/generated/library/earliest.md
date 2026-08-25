---
name: EARLIEST
category: [filter]
primaryCategory: filter
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/earliest-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# EARLIEST

Returns the current value of the specified column in an outer evaluation pass of the specified column.

## Syntax

```dax
EARLIEST(<column>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`column`|A reference to a column.|

## Return value

A column with filters removed.

## Remarks

- The EARLIEST function is similar to EARLIER, but lets you specify one additional level of recursion.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The current sample data does not support this scenario.

```dax
= EARLIEST(<column>)
```

## Related content

- [EARLIER function](./earlier.md)
- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)
