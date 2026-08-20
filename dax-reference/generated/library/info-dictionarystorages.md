---
name: INFO.DICTIONARYSTORAGES
category: [info]
primaryCategory: info
returns: table
appliesTo: [query]
discouragedInVisualCalculations: false
source: query-languages/dax/info-dictionarystorages-function-dax.md@323524c
sourceDate: 
notes: false
examples: 0
---
# INFO.DICTIONARYSTORAGES

Returns a table with information about each dictionary storage in the semantic model. This function provides metadata about dictionary storage characteristics and compression.

## Syntax

```dax
INFO.DICTIONARYSTORAGES ( [<Restriction name>, <Restriction value>], ... )
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
| --- | --- | --- |
| [ID] | Integer | Unique identifier for the dictionary storage |
| [ColumnStorageID] | Integer | Identifier of the column storage this dictionary belongs to |
| [Type] | Integer | Type of the dictionary storage |
| [DataType] | Integer | Data type stored in the dictionary |
| [DataVersion] | Integer | Version of the data format |
| [BaseId] | Integer | Base identifier for the dictionary |
| [Magnitude] | Integer | Magnitude value for the dictionary |
| [LastId] | Integer | Last identifier used in the dictionary |
| [IsNullable] | Boolean | Whether the dictionary can contain null values |
| [IsUnique] | Boolean | Whether all values in the dictionary are unique |
| [IsOperatingOn32] | Boolean | Whether the dictionary operates on 32-bit values |
| [DictionaryFlags] | Integer | Flags indicating dictionary characteristics |
| [StorageFileID] | Integer | Identifier of the storage file containing the dictionary |
| [Size] | Integer | Size of the dictionary in bytes |

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
	INFO.DICTIONARYSTORAGES()
```

## Example 2 - DAX query with joins

The following DAX query can be run in [DAX query view](https://learn.microsoft.com/en-us/power-bi/transform-model/dax-query-view):

```dax
EVALUATE
	VAR _DictionaryStorages =
		INFO.DICTIONARYSTORAGES()

	VAR _ColumnStorages = 
		SELECTCOLUMNS(
			INFO.COLUMNSTORAGES(),
			"ColumnStorageID", [ID],
			"Column Storage Name", [Name],
			"ColumnID", [ColumnID]
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
			_DictionaryStorages,
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
			"Dictionary Type", [Type],
			"Data Type", [DataType],
			"Is Nullable", [IsNullable],
			"Size", [Size]
		)
	ORDER BY [Table Name], [Column Name]
```
## See also

- [INFO.COLUMNSTORAGES](./info-columnstorages.md)
- [INFO.COLUMNPARTITIONSTORAGES](./info-columnpartitionstorages.md)
- [INFO.SEGMENTSTORAGES](./info-segmentstorages.md)
- [INFO.STORAGEFILES](./info-storagefiles.md)
- [INFO.TABLESTORAGES](./info-tablestorages.md)
