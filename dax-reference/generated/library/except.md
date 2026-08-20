---
name: EXCEPT
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/except-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# EXCEPT

Returns the rows of the first table in the expression which do not appear in the second table.

## Syntax

```dax
EXCEPT(<table_expression1>, <table_expression2>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Table_expression`|Any DAX expression that returns a table.|

## Return value

A table that contains the rows of one table minus all the rows of another table.

## Remarks

- If a row appears at all in both tables, it and its duplicates are not present in the result set. If a row appears in only table_expression1, it and its duplicates will appear in the result set.

- The column names will match the column names in table_expression1.

- The returned table has lineage based on the columns in table_expression1 , regardless of the lineage of the columns in the second table. For example, if the first column of first table_expression has lineage to the base column C1 in the model, the Except will reduce the rows based on the availability of values in the first column of second table_expression and keep the lineage on base column C1 intact.

- The two tables must have the same number of columns.

- Columns are compared based on positioning, and data comparison with no type coercion.

- The set of rows returned depends on the order of the two expressions.

- The returned table does not include columns from tables related to table_expression1.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

States1

|State|
|---------|
|A|
|B|
|B|
|B|
|C|
|D|
|D|

States2

|State|
|---------|
|B|
|C|
|D|
|D|
|D|
|E|
|E|
|E|

Except(States1, States2)

|State|
|---------|
|A|

Except(States2, States1)

|State|
|---------|
|E|
|E|
|E|
