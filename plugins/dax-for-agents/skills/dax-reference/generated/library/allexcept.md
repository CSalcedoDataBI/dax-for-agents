---
name: ALLEXCEPT
category: [filter]
primaryCategory: filter
returns: table
appliesTo: [measure, column, table]
discouragedInVisualCalculations: false
source: query-languages/dax/allexcept-function-dax.md@323524c
sourceDate: 
notes: true
examples: 0
---
# ALLEXCEPT

Removes all context filters in the table except filters that have been applied to the specified columns.

## Syntax

```dax
ALLEXCEPT(<table>,<column>[,<column>[,…]])
```

### Parameters

|Term|Definition|
|--------|--------------|
|`table`|The table over which all context filters are removed, except filters on those columns that are specified in subsequent arguments.|
|`column`|The column for which context filters must be preserved.|

The first argument to the ALLEXCEPT function must be a reference to a base table. All subsequent arguments must be references to base columns. You cannot use table expressions or column expressions with the ALLEXCEPT function.

## Return value

A table with all filters removed except for the filters on the specified columns.

## Remarks

- This function is not used by itself, but serves as an intermediate function that can be used to change the set of results over which some other calculation is performed.

- ALL and ALLEXCEPT can be used in different scenarios:

    |Function and usage|Description|
    |----------------------|---------------|
    |ALL(Table)|Removes all filters from the specified table. In effect, ALL(Table) returns all of the values in the table, removing any filters from the context that otherwise might have been applied. This function is useful when you are working with many levels of grouping, and want to create a calculation that creates a ratio of an aggregated value to the total value.|
    |ALL (Column[, Column[, …]])|Removes all filters from the specified columns in the table; all other filters on other columns in the table still apply. All column arguments must come from the same table. The ALL(Column) variant is useful when you want to remove the context filters for one or more specific columns and to keep all other context filters.|
    |ALLEXCEPT(Table, Column1 [,Column2]...)|Removes all context filters in the table except filters that are applied to the specified columns. This is a convenient shortcut for situations in which you want to remove the filters on many, but not all, columns in a table.|

- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following measure formula sums SalesAmount_USD and uses the ALLEXCEPT function to remove any context filters on the DateTime table except if the filter has been applied to the CalendarYear column.

```dax
= CALCULATE(SUM(ResellerSales_USD[SalesAmount_USD]), ALLEXCEPT(DateTime, DateTime[CalendarYear]))
```

Because the formula uses ALLEXCEPT, whenever any column but CalendarYear from the table DateTime is used to slice a visualization, the formula will remove any slicer filters, providing a value equal to the sum of SalesAmount_USD. However, if the column CalendarYear is used to slice the visualization, the results are different. Because CalendarYear is specified as the argument to ALLEXCEPT, when the data is sliced on the year, a filter will be applied on years at the row level

## Related content

- [Filter functions](https://learn.microsoft.com/en-us/dax/filter-functions-dax)
- [ALL function](./all.md)
- [FILTER function](./filter.md)
