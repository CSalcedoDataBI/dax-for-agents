---
name: CONVERT
category: [math-and-trig]
primaryCategory: math-and-trig
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/convert-function-dax.md@323524c
sourceDate: 06/29/2026
notes: false
examples: 0
---
# CONVERT

Converts an expression of one data type to another.

## Syntax

```dax
CONVERT(<Expression>, <Datatype>)
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Expression`|Any valid expression.|
|`Datatype`|An enumeration that includes: BOOLEAN/LOGICAL, CURRENCY/DECIMAL, DATETIME, DOUBLE, INTEGER/INT64, STRING/TEXT.|

## Return value

Returns the value of `Expression`, translated to `Datatype`.

## Remarks

- The function returns an error when a value can't be converted to the specified data type.

- DAX calculated columns must be of a single data type. Since MEDIAN and MEDIANX functions over an integer column return mixed data types, either integer or double, the following calculated column expression returns an error: 
    ```dax
    MedianOrderQuantity =
    MEDIAN ( [Order Quantity] )
    ```

- To avoid mixed data types, change the expression to always return the double data type, for example:
    ```dax
    MedianOrderQuantity =
    MEDIANX ( 'Sales', CONVERT ( [Order Quantity], DOUBLE ) )
    ```

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

DAX query

```dax
EVALUATE
{ CONVERT ( DATE ( 1900, 1, 1 ), INTEGER ) }
```

Returns

|[Value]  |
|---------|
|2     |
