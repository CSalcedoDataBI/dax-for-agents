---
name: INFO.ALTERNATEOFDEFINITIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-alternateofdefinitions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.ALTERNATEOFDEFINITIONS

Returns a table with information about each alternate of definition in the semantic model. This function provides metadata about alternate definitions for model objects.

## Syntax

```dax
INFO.ALTERNATEOFDEFINITIONS ( [<Restriction name>, <Restriction value>], ... )
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

A table whose columns match the schema rowset for alternate of definitions in the current semantic model.

| Column | Description |
|---|---|
| [ID] | Unique identifier for the alternate of definition object. |
| [ColumnID] | Reference to the column object that has an alternate definition. |
| [BaseColumnID] | Reference to the base column that this alternate definition is derived from. |
| [BaseTableID] | Reference to the base table containing the base column. |
| [Summarization] | The summarization method applied to the alternate definition (e.g., Sum, Count, Average). |

## Remarks

* Can only be run by users with write permission on the semantic model and not when live connected to the semantic model in Power BI Desktop.
* This function can be used in [DAX queries](https://learn.microsoft.com/en-us/dax/dax-queries), and can't be used in calculations.

## Example 1 - DAX query

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	INFO.ALTERNATEOFDEFINITIONS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _AlternateOfDefinitions =
		INFO.ALTERNATEOFDEFINITIONS()

	VAR _Columns = 
		SELECTCOLUMNS(
			INFO.COLUMNS(),
			"ColumnID", [ID],
			"Column Name", [ExplicitName],
			"TableID", [TableID]
		)

	VAR _BaseColumns = 
		SELECTCOLUMNS(
			INFO.COLUMNS(),
			"BaseColumnID", [ID],
			"Base Column Name", [ExplicitName]
		)

	VAR _BaseTables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"BaseTableID", [ID],
			"Base Table Name", [Name]
		)

	VAR _CombinedWithColumns =
		NATURALLEFTOUTERJOIN(
			_AlternateOfDefinitions,
			_Columns
		)

	VAR _CombinedWithBaseColumns =
		NATURALLEFTOUTERJOIN(
			_CombinedWithColumns,
			_BaseColumns
		)

	VAR _CombinedWithBaseTables =
		NATURALLEFTOUTERJOIN(
			_CombinedWithBaseColumns,
			_BaseTables
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedWithBaseTables,
			"Column Name", [Column Name],
			"Base Table Name", [Base Table Name],
			"Base Column Name", [Base Column Name],
			"Summarization", [Summarization]
		)
	ORDER BY [Column Name]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
