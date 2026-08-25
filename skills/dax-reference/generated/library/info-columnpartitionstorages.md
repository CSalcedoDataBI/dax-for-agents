---
name: INFO.COLUMNPARTITIONSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-columnpartitionstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.COLUMNPARTITIONSTORAGES

Returns a table with information about each column partition storage in the semantic model. This function provides metadata about how column partitions are stored.

## Syntax

```dax
INFO.COLUMNPARTITIONSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

| Column name | Data type | Description |
|-------------|-----------|-------------|
| [ID] | Integer | The unique identifier of the column partition storage |
| [ColumnStorageID] | Integer | The identifier of the column storage this partition belongs to |
| [PartitionStorageID] | Integer | The identifier of the partition storage |
| [DataVersion] | Integer | The version of the data in the partition storage |
| [State] | Integer | The current state of the column partition storage |
| [SegmentStorageID] | Integer | The identifier of the segment storage |
| [StorageFileID] | Integer | The identifier of the storage file |

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
	INFO.COLUMNPARTITIONSTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _ColumnPartitionStorages =
		INFO.COLUMNPARTITIONSTORAGES()

	VAR _ColumnStorages = 
		SELECTCOLUMNS(
			INFO.COLUMNSTORAGES(),
			"ColumnStorageID", [ID],
			"ColumnID", [ColumnID],
			"Storage Name", [Name]
		)

	VAR _Columns = 
		SELECTCOLUMNS(
			INFO.COLUMNS(),
			"ColumnID", [ID],
			"Column Name", [ExplicitName],
			"TableID", [TableID]
		)

	VAR _Tables = 
		SELECTCOLUMNS(
			INFO.TABLES(),
			"TableID", [ID],
			"Table Name", [Name]
		)

	VAR _CombinedWithColumnStorages =
		NATURALLEFTOUTERJOIN(
			_ColumnPartitionStorages,
			_ColumnStorages
		)

	VAR _CombinedWithColumns =
		NATURALLEFTOUTERJOIN(
			_CombinedWithColumnStorages,
			_Columns
		)

	VAR _CombinedWithTables =
		NATURALLEFTOUTERJOIN(
			_CombinedWithColumns,
			_Tables
		)

	RETURN
		SELECTCOLUMNS(
			_CombinedWithTables,
			"Table Name", [Table Name],
			"Column Name", [Column Name],
			"Storage Name", [Storage Name],
			"Data Version", [DataVersion],
			"State", [State]
		)
	ORDER BY [Table Name], [Column Name]
```
## See also

- [INFO.COLUMNSTORAGES](./info-columnstorages.md)
- [INFO.DICTIONARYSTORAGES](./info-dictionarystorages.md)
- [INFO.SEGMENTSTORAGES](./info-segmentstorages.md)
- [INFO.STORAGEFILES](./info-storagefiles.md)
- [INFO.TABLESTORAGES](./info-tablestorages.md)
