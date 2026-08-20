---
name: INFO.PARTITIONS
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-partitions-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PARTITIONS

Returns a table with information about each partition in the semantic model. This function provides metadata about table partitions and their properties.

## Syntax

```dax
INFO.PARTITIONS ( [<Restriction name>, <Restriction value>], ... )
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

| Column | Data Type | Description |
|--------|-----------|-------------|
| [ID] | Integer | Unique identifier for the partition |
| [TableID] | Integer | ID of the table this partition belongs to |
| [Name] | String | Name of the partition |
| [Description] | String | Description of the partition |
| [DataSourceID] | Integer | ID of the data source for this partition |
| [QueryDefinition] | String | Query definition used to populate the partition |
| [State] | Integer | Current state of the partition |
| [Type] | Integer | Type of partition |
| [PartitionStorageID] | Integer | ID of the partition storage |
| [Mode] | Integer | Processing mode for the partition |
| [DataView] | Integer | Data view setting for the partition |
| [ModifiedTime] | DateTime | Date and time when the partition was last modified |
| [RefreshedTime] | DateTime | Date and time when the partition was last refreshed |
| [SystemFlags] | Integer | System flags for the partition |
| [ErrorMessage] | String | Error message if the partition is in an error state |
| [RetainDataTillForceCalculate] | Boolean | Whether to retain data until force calculate |
| [RangeStart] | String | Start range for incremental refresh, if applicable |
| [RangeEnd] | String | End range for incremental refresh, if applicable |
| [RangeGranularity] | Integer | Granularity for range-based partitioning |
| [RefreshBookmark] | String | Bookmark for incremental refresh operations |
| [QueryGroupID] | Integer | ID of the query group this partition belongs to |
| [ExpressionSourceID] | Integer | ID of the expression source |
| [MAttributes] | String | Additional partition attributes |

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
	INFO.PARTITIONS()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _Partitions =
		INFO.PARTITIONS()

	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TableID", [ID],
			"Table Name", [Name]
		)

	VAR _DataSources = 
		SELECTCOLUMNS(
			INFO.DATASOURCES(),
			"DataSourceID", [ID],
			"Data Source Name", [Name]
		)

	VAR _CombinedWithTables =
		NATURALLEFTOUTERJOIN(
			_Partitions,
			_Tables
		)

	VAR _CombinedWithDataSources =
		NATURALLEFTOUTERJOIN(
			_CombinedWithTables,
			_DataSources
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedWithDataSources,
			"Table Name", [Table Name],
			"Partition Name", [Name],
			"Data Source Name", [Data Source Name],
			"Type", [Type],
			"Refreshed Time", [RefreshedTime]
		)
	ORDER BY [Table Name], [Partition Name]
```
## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.RELATIONSHIPS](./info-relationships.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
