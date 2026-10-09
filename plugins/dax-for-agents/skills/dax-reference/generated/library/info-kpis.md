---
name: INFO.KPIS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-kpis-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.KPIS

Returns a table with information about each KPI in the semantic model. This function provides metadata about Key Performance Indicators defined in the model.

## Syntax

```dax
INFO.KPIS ( [<Restriction name>, <Restriction value>], ... )
```

## Parameters

Parameters are optional for this DAX function. When parameters are used, both must be given. More than one pair of parameters is allowed. The restriction name and value are text and entered in double-quotes.

| Term | Definition |
|---|---|
| Restriction name | Name of the restriction used to filter the results. |
| Restriction value | Value used to filter the results of the restriction. |

## Restrictions

Typically, all columns of the DAX function results can be used as a restriction. Additional restrictions may also be allowed.

## Return value

A table with the following columns:

| Column | Description |
|--------|-------------|
| [ID] | Unique identifier for the KPI |
| [MeasureID] | Identifier of the measure associated with the KPI |
| [Description] | Description of the KPI |
| [TargetDescription] | Description of the KPI target |
| [TargetExpression] | DAX expression defining the KPI target value |
| [TargetFormatString] | Format string for displaying the target value |
| [StatusGraphic] | Graphic used to display the KPI status |
| [StatusDescription] | Description of the KPI status |
| [StatusExpression] | DAX expression defining the KPI status |
| [TrendGraphic] | Graphic used to display the KPI trend |
| [TrendDescription] | Description of the KPI trend |
| [TrendExpression] | DAX expression defining the KPI trend |
| [ModifiedTime] | Timestamp of when the KPI was last modified |

## Remarks

- Typically used in DAX queries to inspect and document model metadata.
- Permissions required depend on the host. Querying full metadata may require model admin permissions.

## Examples (Microsoft — no verificados aquí)

> Estos ejemplos vienen de `query-docs` y están medidos sobre **Adventure Works DW
> 2020**, un modelo que **no está en este repositorio**. Sus cifras no se han ejecutado
> aquí y no hay forma de reproducirlas desde el repo. Se conservan por el contexto que
> aportan, y porque son CC BY 4.0 de Microsoft.

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.KPIS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _KPIs =
		SELECTCOLUMNS(
			INFO.KPIS(),
			"KPIID", [ID],
			"MeasureID", [MeasureID],
			"KPI Description", [Description],
			"TargetExpression", [TargetExpression]
		)
	VAR _Measures = 
		SELECTCOLUMNS(
			INFO.MEASURES(),
			"MeasureID", [ID],
			"Measure Name", [Name]
		)
	VAR _CombinedTable =
		NATURALLEFTOUTERJOIN(
			_KPIs,
			_Measures
		)
	RETURN
		SELECTCOLUMNS(
			_CombinedTable,
			"Measure Name", [Measure Name],
			"KPI Description", [KPI Description],
			"Target Expression", [TargetExpression]
		)
	ORDER BY [Measure Name]
```

## See also

- [INFO.CALCULATIONGROUPS](./info-calculationgroups.md)
- [INFO.CALCULATIONITEMS](./info-calculationitems.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
