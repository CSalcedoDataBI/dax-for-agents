---
name: INFO.PARTITIONSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-partitionstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.PARTITIONSTORAGES

Returns a table with information about each partition storage in the semantic model. This function provides metadata about how partitions are stored.

## Syntax

```dax
INFO.PARTITIONSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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
| [ID] | Unique identifier for the partition storage |
| [PartitionID] | Identifier of the partition |
| [Name] | Name of the partition storage |
| [StoragePosition] | Position of the storage within the partition |
| [SegmentMapStorageID] | Identifier linking to segment map storage |
| [DataObjectId] | Identifier of the data object |
| [StorageFolderID] | Identifier of the storage folder |
| [DeltaTableMetadataStorageID] | Identifier linking to delta table metadata storage |

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
	INFO.PARTITIONSTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _PartitionStorages =
		SELECTCOLUMNS(
			INFO.PARTITIONSTORAGES(),
			"PartitionStorageID", [ID],
			"PartitionID", [PartitionID],
			"Storage Name", [Name]
		)
	VAR _Partitions = 
		SELECTCOLUMNS(
			INFO.PARTITIONS(),
			"PartitionID", [ID],
			"Partition Name", [Name],
			"TableID", [TableID]
		)
	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TableID", [ID],
			"Table Name", [Name]
		)
	VAR _CombinedTable1 =
		NATURALLEFTOUTERJOIN(
			_PartitionStorages,
			_Partitions
		)
	VAR _CombinedTable2 =
		NATURALLEFTOUTERJOIN(
			_CombinedTable1,
			_Tables
		)
	RETURN
		SELECTCOLUMNS(
			_CombinedTable2,
			"Table Name", [Table Name],
			"Partition Name", [Partition Name],
			"Storage Name", [Storage Name]
		)
	ORDER BY [Table Name], [Partition Name]
```

## See also

- [INFO.TABLES](./info-tables.md)
- [INFO.COLUMNS](./info-columns.md)
- [INFO.MEASURES](./info-measures.md)
- [INFO functions overview](https://learn.microsoft.com/en-us/dax/info-functions-dax)
