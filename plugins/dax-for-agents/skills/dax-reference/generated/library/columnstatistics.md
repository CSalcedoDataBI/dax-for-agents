---
name: COLUMNSTATISTICS
category: [information]
primaryCategory: information
returns: table
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: true
source: query-languages/dax/columnstatistics-function-dax.md@323524c
sourceDate: 07/13/2026
notes: false
examples: 0
---
# COLUMNSTATISTICS

Returns a table of statistics for every column in every table in the model.

## Syntax

```dax
COLUMNSTATISTICS ()
```

### Parameters

This function doesn't take any parameters.

## Return value

A table of statistics. Each row of this table represents a different column in the model. Table columns include:

- `Table Name`: The current column’s table.
- `Column Name`: The current column’s name.
- `Min`: The minimum value found within the current column.
- `Max`: The maximum value found within the current column.
- `Cardinality`: The number of distinct values found within the current column.
- `Max Length`: The length of the longest string found within the current column (only applicable for string columns).

## Remarks

- Columns in an error state and columns from query-scope calculated tables don't appear in the result table.

- If you apply a filter from the filter context to `COLUMNSTATISTICS()`, the function returns an error.

- For binary-typed columns, the Min and Max statistics have BLANK values.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

_Examples in this article can be used with the sample Adventure Works DW 2020 Power BI Desktop model. To get the model, see [DAX sample model](https://aka.ms/dax-docs-samples)._

The following DAX query:

```dax
DEFINE
    TABLE FilteredProduct =
        FILTER ( Product, [Color] == "Blue" )
    COLUMN Customer[Location] = [State-Province] & " " & [Country-Region]

EVALUATE
COLUMNSTATISTICS ()
```

Returns a table with statistics for all columns from all tables in the model. The table also includes statistics for the query-scope calculated column, Customer[Location]. However, the table doesn't include the columns from the query-scope calculated table, FilteredProduct.

The following excerpt shows the **Customer** table rows from the result, including the calculated **Location** column:

|Table Name|Column Name|Min|Max|Cardinality|Max Length|
|---|---|---|---|---|---|
|Customer|CustomerKey|-1|29483|18485| |
|Customer|Customer ID|[Not Applicable]|AW00029483|18485|16|
|Customer|Customer|[Not Applicable]|Zoe Watson|18401|26|
|Customer|City|[Not Applicable]|York|270|21|
|Customer|State-Province|[Not Applicable]|Yveline|54|19|
|Customer|Country-Region|[Not Applicable]|United States|7|16|
|Customer|Postal Code|[Not Applicable]|YO15|324|16|
|Customer|Location|[Not Applicable] [Not Applicable]|Yveline France|54|33|

:::image type="content" source="https://learn.microsoft.com/en-us/dax/media/columnstatistics-function-dax/columnstatistics-result-table.png" alt-text="COLUMNSTATISTICS result table":::

## Related content

- [Filter context](https://learn.microsoft.com/en-us/dax/dax-overview#filter-context)
- [CALCULATETABLE function](./calculatetable.md)
