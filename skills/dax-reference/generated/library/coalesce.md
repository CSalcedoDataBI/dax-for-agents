---
name: COALESCE
category: [logical]
primaryCategory: logical
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/coalesce-function-dax.md@323524c
sourceDate: 
notes: false
examples: 4
---
# COALESCE

Returns the first expression that does not evaluate to BLANK. If all expressions evaluate to BLANK, BLANK is returned.

## Syntax

```dax
COALESCE(<expression>, <expression>[, <expression>]…)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`expression`|Any DAX expression that returns a scalar expression.|

## Return value

A scalar value coming from one of the expressions or BLANK if all expressions evaluate to BLANK. 

## Remarks

Input expressions may be of different data types.

## Example 1

  The following DAX query:

```dax
EVALUATE { COALESCE(BLANK(), 10, DATE(2008, 3, 3)) }
```

 Returns `10`, which is the first expression that does not evaluate to BLANK.

## Example 2

  The following DAX expression:

```dax
= COALESCE(SUM(FactInternetSales[SalesAmount]), 0)
```

Returns the sum of all values in the SalesAmount column in the FactInternetSales table, or `0`. 
This can be used to convert BLANK values of total sales to `0`.

## Ejemplos ejecutables

**4** consulta(s) medidas contra un modelo que sí está en este repositorio, cada una con el número que devolvió el motor:
[`examples/logical/coalesce.md`](../../examples/logical/coalesce.md).

Se ejecutan y se comparan con `python lab/check_lab.py examples localhost:<puerto>`.
