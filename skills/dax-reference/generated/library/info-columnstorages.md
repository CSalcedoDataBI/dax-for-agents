---
name: INFO.COLUMNSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-columnstorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.COLUMNSTORAGES

Returns a table with information about each column storage in the semantic model. This function provides metadata about how columns are stored and their storage characteristics.

## Syntax

```dax
INFO.COLUMNSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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

| Column | Data type | Description |
| ------ | --------- | ----------- |
| [ID] | Integer | Unique identifier for the column storage |
| [ColumnID] | Integer | Identifier of the column that this storage belongs to |
| [Name] | String | Name of the column storage |
| [StoragePosition] | Integer | Position of the column in storage |
| [DictionaryStorageID] | Integer | Identifier for the dictionary storage |
| [Settings] | String | Storage settings and configuration |
| [ColumnFlags] | Integer | Flags indicating column storage properties |
| [Collation] | String | Collation settings for the column |
| [OrderByColumn] | String | Column used for ordering |
| [Locale] | String | Locale information for the column |
| [BinaryCharacters] | String | Binary character information |
| [Statistics_DistinctStates] | Integer | Number of distinct states in statistics |
| [Statistics_MinDataID] | Integer | Minimum data ID in statistics |
| [Statistics_MaxDataID] | Integer | Maximum data ID in statistics |
| [Statistics_OriginalMinSegmentDataID] | Integer | Original minimum segment data ID |
| [Statistics_RLESortOrder] | Integer | RLE sort order in statistics |
| [Statistics_RowCount] | Integer | Row count in statistics |
| [Statistics_HasNulls] | Boolean | Whether statistics contain nulls |
| [Statistics_RLERuns] | Integer | Number of RLE runs in statistics |
| [Statistics_OthersRLERuns] | Integer | Number of other RLE runs |
| [Statistics_Usage] | Integer | Usage statistics |
| [Statistics_DBType] | Integer | Database type in statistics |
| [Statistics_XMType] | Integer | XML type in statistics |

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
	INFO.COLUMNSTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _ColumnStorages =
		INFO.COLUMNSTORAGES()

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

	VAR _CombinedWithColumns =
		NATURALLEFTOUTERJOIN(
			_ColumnStorages,
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
			"Storage Name", [Name],
			"Storage Position", [StoragePosition],
			"Statistics Row Count", [Statistics_RowCount]
		)
	ORDER BY [Table Name], [Column Name]
```
## See also

- [INFO.COLUMNPARTITIONSTORAGES](./info-columnpartitionstorages.md)
- [INFO.DICTIONARYSTORAGES](./info-dictionarystorages.md)
- [INFO.SEGMENTSTORAGES](./info-segmentstorages.md)
- [INFO.STORAGEFILES](./info-storagefiles.md)
- [INFO.TABLESTORAGES](./info-tablestorages.md)
