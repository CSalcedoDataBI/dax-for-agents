---
name: DATATABLE
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/datatable-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# DATATABLE

Provides a mechanism for declaring an inline set of data values.

## Syntax

```dax
DATATABLE (ColumnName1, DataType1, ColumnName2, DataType2..., {{Value1, Value2...}, {ValueN, ValueN+1...}...})
```

### Parameters

|Term|Definition|
|--------|--------------|
|`ColumnName`|A column name.|
|`DataType`|An enumeration that includes: BOOLEAN/LOGICAL, CURRENCY/DECIMAL, DATETIME, DOUBLE, INTEGER/INT64, STRING/TEXT.|
|`value`|A single argument using Excel syntax for a one dimensional array constant, nested to provide an array of arrays.  This argument represents the set of data values that will be in the table<br /><br />For example,<br />{ {values in row1}, {values in row2}, {values in row3}, etc. }<br />Where {values in row1} is a comma delimited set of constant expressions, namely a combination of constants, combined with a handful of basic functions including DATE, TIME, and BLANK, as well as a plus operator between DATE and TIME and a unary minus operator so that negative values can be expressed.<br /><br />The following are all valid values: 3, -5, BLANK(), "2009-04-15 02:45:21". Values may not refer to anything outside the immediate expression, and cannot refer to columns, tables, relationships, or anything else.<br /><br />A missing value will be treated identically to BLANK().  For example, the following are the same:   {1,2,BLANK(),4}  {1,2,,4}|

## Return value

A table declaring an inline set of values.

## Remarks

- Unlike DATATABLE, [Table Constructor](https://learn.microsoft.com/en-us/dax/table-constructor) allows any scalar expressions as input values.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

```dax
= DataTable("Name", STRING,
               "Region", STRING
               ,{
                        {" User1","East"},
                        {" User2","East"},
                        {" User3","West"},
                        {" User4","West"},
                        {" User4","East"}
                }
           )
```
