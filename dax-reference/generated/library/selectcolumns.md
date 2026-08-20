---
name: SELECTCOLUMNS
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/selectcolumns-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SELECTCOLUMNS

Returns a table with selected columns from the table and new columns specified by the DAX expressions.

## Syntax

```dax
SELECTCOLUMNS(<Table>, [<Name>], <Expression>, [<Name>], …) 
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Table`|  Any DAX expression that returns a table. |
|`Name` |  The name given to the column, enclosed in double quotes. |
|`Expression` |Any expression that returns a scalar value like a column reference, integer, or string value.|

## Return value

A table with the same number of rows as the table specified as the first argument. The returned table has one column for each pair of `Name`, `Expression` arguments, and each expression is evaluated in the context of a row from the specified `Table` argument.

## Remarks

SELECTCOLUMNS has the same signature as ADDCOLUMNS, and has the same behavior except that instead of starting with the `Table` specified, SELECTCOLUMNS starts with an empty table before adding columns.

This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

For the following table named **Customer**:

Country  |State  |Count  |Total
---------|---------|---------|---------
IND     |   JK      |    20     |  800
IND     |   MH      |    25     |  1000
IND     |   WB      |    10     |  900
USA     |   CA      |    5     |   500
USA     |   WA      |    10     |  900

```dax
SELECTCOLUMNS(Customer, "Country, State", [Country]&", "&[State])
```

Returns,

|Country, State |
|---------|
|IND, JK     |
|IND, MH     |
|IND, WB     |
|USA, CA    |
|USA, WA    |
