---
name: SAMPLEAXISWITHLOCALMINMAX
category: []
primaryCategory: 
returns: scalar
appliesTo: [measure, column, table, visual-calculation]
discouragedInVisualCalculations: false
source: query-languages/dax/sampleaxiswithlocalminmax-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# SAMPLEAXISWITHLOCALMINMAX

Returns a sample subset from a Table that is obtained by binning the primary X-axis into equal-sized bins and preserving the local min/max for each bin across different series.

## Syntax

```dax
SAMPLEAXISWITHLOCALMINMAX(<Size>, <Table>, <Axis>, <Measure>, [<Measure> [, ...] ], <MinResolution> [, <DynamicSeries> [, <DynamicSeries [, ...] ] ] [, <DynamicSeriesSelectionCriteria] [, <DynamicSeriesSelectionOrder] [, <Max Resolution>] [, <MaxDynamicSeries>] [, <MaxIterations>]) 
```

### Parameters

|Term|Definition|
|--------|--------------|
|`Size`|Number of rows in the sample to return|
|`Table`|Any DAX expression that returns a table of data from where to return a sample subset from.|
|`Axis`|The numerical or datetime column from Table to be binned.|
|`Measure`| Column reference from Table to be sampled. At least one Measure is required, but you can specify multiple.|
|`MinResolution`| Minimum number of selected rows that spans the full non-empty range of X|
|`DynamicSeries`| (Optional) Column to be used as series. You can specify zero, or or multiple.|
|`DynamicSeriesSelectionCriteria`| (Optional) Decides which series values to retain if not all DynamicSeries can be preserved. Valid values are `NONE` or `ALPHABETICAL`|
|`DynamicSeriesSelectionOrder`| (Optional) Decides to use ascending or descending sorting on the criteria identified by DynamicSeriesSelectionCriteria. Valid values are `ASC` or `DESC`.|
|`MaxResolution`| Maximum number of selected rows for a line that spans the full non-empty range of X|
|`MaxDynamicSeries`|Maximum allowed DynamicSeries. If the number of DynamicSeries is higher than MaxDynamicSeries remove DynamicSeries based on DynamicSeriesSelectionCriteria.|
|`MaxIterations`|Maximum number of iterations to try to reach the Size number of rows. |

## Return Value

The sample from Table consisting of Size number of rows.

## Remarks
- If the number of rows in Table are less than the specified Size, then no binning will occur and all rows will be returned.
- The selected bin-sizes will be less than MinResolution
- SAMPLEAXISWITHLOCALMINMAX is used by Power BI to reduce the number of points in a line chart with a continuous (numeric) X-axis.
- This function is not supported for use in DirectQuery mode when used in calculated columns or row-level security (RLS) rules.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query:

```dax
EVALUATE
SAMPLEAXISWITHLOCALMINMAX(
	10,
	SELECTCOLUMNS ( Sales, "x", [Unit Price], "y", [Sales Amount] ),
    [x],
    [y],
	10
	)
```

Returns a 10 row (or less) sample subset of Table that is binned by Unit Price and sampled on Sales Amount.