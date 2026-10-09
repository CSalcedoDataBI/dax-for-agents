---
name: TREATAS
category: [table-manipulation]
primaryCategory: table-manipulation
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/treatas-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# TREATAS

Applies the result of a table expression as filters to columns from an unrelated table. 

## Syntax

```dax
TREATAS(table_expression, <column>[, <column>[, <column>[,…]]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table_expression`|An expression that results in a table.|
|`column`|One or more existing columns. It cannot be an expression. |

## Return value

A table that contains all the rows in column(s) that are also in table_expression.

## Remarks

- The number of columns specified must match the number of columns in the table expression and be in the same order.

- If a value returned in the table expression does not exist in the column, it is ignored. For example, TREATAS({"Red", "Green", "Yellow"}, DimProduct[Color]) sets a filter on column DimProduct[Color] with three values "Red", "Green", and "Yellow". If "Yellow" does not exist in  DimProduct[Color], the effective filter values would be "Red" and "Green".

- Best for use when a relationship does not exist between the tables. If you have multiple relationships between the tables involved, consider using [USERELATIONSHIP](./userelationship.md) instead.

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

In the following example, the model contains two unrelated product tables. If a user applies a filter to DimProduct1[ProductCategory] selecting Bikes, Seats, Tires, the same filter, Bikes, Seats, Tires is applied to DimProduct2[ProductCategory].

```dax
CALCULATE(
    SUM(Sales[Amount]),
    TREATAS(
        VALUES(DimProduct1[ProductCategory]),
        DimProduct2[ProductCategory]
    )
)
```

## Related content

- [INTERSECT](./intersect.md)
- [FILTER](./filter.md)
- [USERELATIONSHIP](./userelationship.md)
